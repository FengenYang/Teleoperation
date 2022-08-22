"""Python client interface for Dobot MG400 using dll api

Notes
VSCode - To find DobotDll dependencies chdir to [dll_path]
        (Including [dll_path] in PATH does not work)
Spyder - Neither option works
"""

import os
import numpy as np

from cri.dobot.mg400_dll import DobotSDK as dobot
from cri.transforms import euler2quat, quat2euler, inv_transform

dll_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mg400_dll')


class Mg400Client:
    """Python client interface for Dobot Magician
    """

    class CommandFailed(RuntimeError):
        pass

    class InvalidZone(ValueError):
        pass

    def __init__(self, ip="192.168.1.6"):
        self._delay = .08

        self.set_units('millimeters', 'degrees')     
        self.connect(ip)

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__, self.get_info())

    def __str__(self):
        return self.__repr__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()        
        
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

    def connect(self, ip):
        """Connects to Dobot MG400.
        """
        os.chdir(dll_path) 
        try:
            self.api = dobot.load()
        except:
            raise Exception("Dobot Dll dependencies not loaded (try VSCode)")

        state = dobot.ConnectDobot(self.api, ip)
        if (state == 0):
            print("Client connected to Dobot MG400...")
        else:
            raise Exception("Connection to Dobot MG400 failed")
    
        dobot.ClearAlarms(self.api)   
        dobot.dSleep(1000)     
        dobot.SetControlMode(self.api, 1) 

    def get_info(self):
        """Returns a unique robot identifier string.
        """
        info = "Version: {}".format(
                dobot.GetDobotVersion(self.api)[1:]
                )
        return info

    def move_joints(self, joint_angles):
        """Executes an immediate move to the specified joint angles.

        joint_angles = (j0, j1, j2, rz, 0, 0)
        j0, j1, j2, rz are numbered from base to end effector and are
        measured in degrees (default)
        """       
        joint_angles = np.array(joint_angles, dtype=np.float32).ravel()
        joint_angles *= self._scale_angle 
        print("Warning: move_joints not implemented")
        # dobot.MovJ(self.api, [*joint_angles, 0, 0], isBlock=True) # not implemented yet
    
    def move_linear(self, pose):
        """Executes a linear/cartesian move from the current base frame pose to
        the specified pose.

        pose = (x, y, z, 0, 0, rz)
        x, y, z specify a Euclidean position (default mm)
        """
        pose = inv_transform(self._tcp, pose) # explicit tcp
        pose = quat2euler(pose, 'sxyz')[[0, 1, 2, 5]]
        pose[:3] *= self._scale_linear
        dobot.MovL(self.api, [*pose, 0, 0], isBlock=True)
    
    def set_tcp(self, tcp):
        """Sets the tool center point (TCP) of the robot.

        The TCP is specified in the output flange frame.
.
        tcp = (x, y, z, 0, 0, rz)
        x, y, z specify a Euclidean position (default mm)
        """
        self._tcp = tcp
        tcp = quat2euler(tcp, 'sxyz')[[0, 1, 2, 5]]
        tcp[:3] *= self._scale_linear
        dobot.SetCoordinateToolParams(self.api, *tcp, 0, 0, index=1) # doesn't work

    def set_speed(self, linear_speed, angular_speed):
        """Sets the linear speed (default % of maximum)
        """
        linear_speed *= self._scale_linear
        if linear_speed < 1 or linear_speed > 100: 
            raise Exception("Speed value outside range of 1-100%")
        dobot.SetRapidRate(self.api, round(linear_speed))
        print("Warning: angular_speed not implemented")

    def get_speed(self):
        """Gets the linear speed (default % of maximum)
        """
        linear_speed = dobot.GetRapidRate(self.api)[1]
        linear_speed /= self._scale_linear
        return linear_speed, None

    def get_joint_angles(self):
        """returns the robot joint angles.

        joint_angles = (j0, j1, j2, rz, 0, 0)
        j0, j1, j2, rz are numbered from base to end effector and are
        measured in degrees (default)
        """
        retvals = dobot.GetJointCoordinate(self.api)[1]  
        joint_angles = np.array(retvals[:4], dtype=np.float64)
        joint_angles /= self._scale_angle
        return joint_angles

    def get_pose(self):
        """retvalsurns the TCP pose in the reference coordinate frame.

        pose = (x, y, z, rz, 0, 0)
        x, y, z specify a Euclidean position (default mm)
        rz rotation of end effector
        """
        retvals = dobot.GetCartesianCoordinate(self.api)[1:]      
        pose = np.array([*retvals[:3], 0, 0, retvals[3]], dtype=np.float64) 
        pose = euler2quat(pose, 'sxyz')
        pose[:3] /= self._scale_linear      
        return pose

    def move_circular(self, via_pose, end_pose):
        """Executes a movement in a circular path from the current base frame
        pose, through via_pose, to end_pose.
        
        via_pose, end_pose = (x, y, z, qw, qx, qy, qz)
        x, y, z specify a Cartesian position (default mm)
        qw, qx, qy, qz specify a quaternion rotation
        """        
        print('Warning: move_circular not implemented')   

    def close(self):
        """Releases any resources held by the controller (e.g., sockets). And disconnects from Dobot magician
        """
        dobot.dSleep(5000)
        dobot.ClearAlarms(self.api)
        dobot.SetControlMode(self.api, 0) 
        dobot.DisconnectDobot(self.api) 
        print("Disconnecting Dobot...")
