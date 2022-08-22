"""Python client interface for Dobot Magician.

Version control
v0.0 -> fork from John Lloyd
v0.1 -> Client interface from Ben Money-Coomes
v0.2 -> Client integrated into cri by Nathan Lepora

Notes
VSCode/Spyder - To find DobotDll dependencies chdir to [dll_path]
                Alternative to include [dll_path] in PATH (not used)
"""

from cri.dobot.magician import DobotDllType as dobot
from cri.transforms import euler2quat, quat2euler 

import numpy as np
import os

dll_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'magician')
# os.environ["PATH"] += os.pathsep + os.pathsep.join([dll_path])


class MagicianClient:
    """Python client interface for Dobot Magician
    """

    class CommandFailed(RuntimeError):
        pass

    class InvalidZone(ValueError):
        pass

    def __init__(self, port=""):
        self._delay = 1
        self.set_units('millimeters', 'degrees')     
        self.connect(port)

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__, self.get_info())

    def __str__(self):
        return self.__repr__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()   

    def _block(self, command):
        """ Changes command into blocking command
        """
        dobot.SetQueuedCmdStartExec(self.api)
        retval = command    
        while dobot.GetQueuedCmdCurrentIndex(self.api)[0] < retval:
            dobot.dSleep(self._delay)
        dobot.SetQueuedCmdStopExec(self.api)     
        
    def set_units(self, linear, angular):
        """Sets linear and angular units.
        """
        units_l = {'millimeters' : 1.0,
               'meters' : 1000.0,
               'inches' : 25.4,
               }
        units_a = {'degrees' : 1.0,
               'radians' : 57.2957795,
               }
        self._scale_linear = units_l[linear]
        self._scale_angle  = units_a[angular]

    def connect(self, port):
        """Connects to Dobot Magician.
        """
        os.chdir(dll_path)
        try:
            self.api = dobot.load()
        except:
            raise Exception("Dobot Dll dependencies not loaded (try VSCode or Spyder)")
            
        state = dobot.ConnectDobot(self.api, port, baudrate=115200)[0] 
        if (state == 0):
            print("Client connected to Dobot Magician...")
        else:
            raise Exception("Connection to Dobot Magician failed")
    
    def get_info(self):
        """Returns a unique robot identifier string.
        """
        info = "SN: {}, Name: {}".format(
                dobot.GetDeviceSN(self.api)[0],
                dobot.GetDeviceName(self.api)[0]
                )
        return info

    def move_joints(self, joint_angles):
        """Executes an immediate move to the specified joint angles.

        joint_angles = (j0, j1, j2, rz)
        j0, j1, j2, rz are numbered from base to end effector and are
        measured in degrees (default)
        """
        joint_angles = np.array(joint_angles, dtype=np.float32).ravel()
        joint_angles *= self._scale_angle
        self._block(dobot.SetPTPCmd(self.api, 
                dobot.PTPMode.PTPMOVLANGLEMode, *joint_angles, isQueued=1)[0])
    
    def move_linear(self, pose):
        """Executes a linear/cartesian move from the current base frame pose to
        the specified pose.

        pose = (x, y, z, qw, qx, qy, qz)
        x, y, z specify a Euclidean position (default mm)
        qw, qx, qy, qz specify a quaternion rotation
        """
        pose = quat2euler(pose, 'sxyz')[[0,1,2,5]]
        self._block(dobot.SetPTPCmd(self.api, 
                dobot.PTPMode.PTPMOVLXYZMode, *pose, isQueued=1)[0])
    
    def move_linear_step(self,pose):
        self._block(dobot.SetPTPCmd(self.api, 
                dobot.PTPMode.PTPMOVLXYZINCMode, *pose, isQueued=1)[0])

    #using JOG mode
    def move_linear_stop(self):
        self._block(dobot.SetJOGCmd(self.api,0,0,isQueued=1)[0])
    def move_linear_forward(self):
        self._block(dobot.SetJOGCmd(self.api,0,1,isQueued=1)[0])
    def move_linear_back(self):
        self._block(dobot.SetJOGCmd(self.api,0,2,isQueued=1)[0])
    def move_linear_left(self):
        self._block(dobot.SetJOGCmd(self.api,0,3,isQueued=1)[0])
    def move_linear_right(self):
        self._block(dobot.SetJOGCmd(self.api,0,4,isQueued=1)[0])
    def move_linear_up(self):
        self._block(dobot.SetJOGCmd(self.api,0,5,isQueued=1)[0])
    def move_linear_down(self):
        self._block(dobot.SetJOGCmd(self.api,0,6,isQueued=1)[0]) 
    def move_linear_speed(self,x,y,z):
        self._block(dobot.SetJOGCoordinateParams(self.api,x,2*x,y,2*y,z,2*z,0.5,1,isQueued=1)[0])

    #using CP mode
    def move_cont(self,x,y,z,i):
        self._block(dobot.SetCPCmd(self.api,0,x,y,z,10,i,isQueued=1)[0])

    def control_gripper(self,gripper):
        #self._block(dobot.SetEndEffectorSuctionCup(self.api,True,gripper,isQueued=1)[0])
        self._block(dobot.SetEndEffectorGripper(self.api,True,gripper,isQueued=1)[0])

    def control_pump(self,pump):
        self._block(dobot.SetEndEffectorSuctionCup(self.api,pump,0,isQueued=1)[0])

    def set_tcp(self, tcp):
        """Sets the tool center point (TCP) of the robot.

        The TCP is specified in the output flange frame, which is located according
        to the dobot magician user manual.
.
        tcp = [x, y, z]
        x, y, z specify a Cartesian position (default mm)
        """
        tcp = quat2euler(tcp, 'sxyz')[[0,1,2]]
        self._block(dobot.SetEndEffectorParams(self.api, *tcp, isQueued=0)[0])

    def set_speed(self, linear_speed, angular_speed):
        """Sets the linear and angular speed (default mm/s deg/s)
        Sets components [linear_speed,linear_accel,angular_speed,angular_accel]
        Sets the accelerations to 2X speeds (defaults mm/s^2, deg/s^2)
        """
        linear_speed *= self._scale_linear
        angular_speed *= self._scale_angle

        if linear_speed < 1 or angular_speed < 1 or linear_speed > 500 or angular_speed > 500: 
            raise Exception("Speed value outside limits of 1-500 mm/s, deg/s")

        linear_accel, angular_accel = (2*linear_speed, 2*angular_speed)  # (mm/s^2,deg/s^2) defaults
        params = (linear_speed, linear_accel, angular_speed, angular_accel)  # (mm/s,deg/s)
        self._block(dobot.SetPTPCoordinateParams(self.api, *params, isQueued=0)[0])

    def get_speed(self):
        """Gets the linear and angular speed (default mm/s deg/s)
        Returns first two components of [linear_speed,angular_speed,linear_accel,angular_accel]
        """
        linear_speed, angular_speed = dobot.GetPTPCoordinateParams(self.api)[:2]
        linear_speed /= self._scale_linear
        angular_speed /= self._scale_angle
        return linear_speed, angular_speed

    def get_joint_angles(self):
        """retvalsurns the robot joint angles.

        joint_angles = (j0, j1, j2, rz)
        j0, j1, j2, rz are numbered from base to end effector and are
        measured in degrees (default)
        """
        retvals = dobot.GetPose(self.api)  # (x,y,z,rz, j1,j2,j3,j4)
        joint_angles = np.array(retvals[4:], dtype=np.float64)
        joint_angles /= self._scale_angle
        return joint_angles

    def get_pose(self):
        """retvalsurns the TCP pose in the reference coordinate frame.

        pose = (x, y, z, qw, qx, qy, qz)
        x, y, z specify a Euclidean position (default mm)
        qw, qx, qy, qz specify a quaternion rotation
        """
        retvals = dobot.GetPose(self.api)  # (x,y,z,rz, j1,j2,j3,j4)      
        pose = np.array([*retvals[:3], 0, 0, retvals[3]], dtype=np.float64) # rx=ry=0 rz=j4 for 4dof robot
        pose = euler2quat(pose, 'sxyz')
        pose[:3] /= self._scale_linear      
        return pose

    def close(self):
        """Releases any resources held by the controller (e.g., sockets). And disconnects from Dobot magician
        """
        dobot.ClearAllAlarmsState(self.api)
        dobot.DisconnectDobot(self.api) 
        print("Disconnecting Dobot...")
