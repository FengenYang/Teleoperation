"""Python client interface for Dobot MG400 using sockets
Firmware version 1.5.5.0
Calibration: password admin
"""

import numpy as np

from cri.dobot.mg400.dobot_api import dobot_api_dashboard, dobot_api_feedback, MyType
from cri.transforms import euler2quat, quat2euler, inv_transform 


class Mg400Client:
    """Python client interface for Dobot MG400
    """

    class CommandFailed(RuntimeError):
        pass

    class InvalidZone(ValueError):
        pass

    def __init__(self, ip="192.168.1.6"):
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
        self._dashboard = dobot_api_dashboard(ip, 29999)
        self._feedback = dobot_api_feedback(ip, 30003)  

        self._dashboard.ClearError()
        self._dashboard.EnableRobot()
        self._dashboard.User(0)
        self._dashboard.Tool(0)

    def get_info(self):
        """Returns a unique robot identifier string.
        """
        pass

    def move_joints(self, joint_angles):
        """Executes an immediate move to the specified joint angles.

        joint_angles = (j0, j1, j2, rz, 0, 0)
        j0, j1, j2, rz are numbered from base to end effector and are
        measured in degrees (default)
        """       
        joint_angles = np.array(joint_angles, dtype=np.float32).ravel()
        joint_angles *= self._scale_angle 
        self._feedback.JointMovJ(*joint_angles, 0, 0)
        self._dashboard.Sync()

    def move_linear(self, pose):
        """Executes a linear/cartesian move from the current base frame pose to
        the specified pose.

        pose = (x, y, z, 0, 0, rz)
        x, y, z specify a Euclidean position (default mm)
        """
        pose = inv_transform(self._tcp, pose) # explicit tcp
        pose = quat2euler(pose, 'sxyz')[[0, 1, 2, 5]]
        pose[:3] *= self._scale_linear
        self._feedback.MovL(*pose, 0, 0)
        self._dashboard.Sync()
    
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
        pass # not implemented

    def set_speed(self, linear_speed, angular_speed):
        """Sets the linear speed (default % of maximum)
        """
        linear_speed *= self._scale_linear
        angular_speed *= self._scale_angle
        if linear_speed < 1 or linear_speed > 100: 
            raise Exception("Linear speed value outside range of 1-100%")
        if angular_speed < 1 or linear_speed > 100: 
            raise Exception("Angular speed value outside range of 1-100%")
        self._dashboard.SpeedL(round(linear_speed))
        self._dashboard.SpeedJ(round(angular_speed))
        self._dashboard.Sync()

    def get_speed(self):
        """Gets the linear speed (default % of maximum)
        """
        info = self._feedback.socket_feedback.recv(1440)
        self._dashboard.Sync()
        info = np.frombuffer(info, dtype=MyType)
        linear_speed = info['speed scaling'] / self._scale_linear 
        return linear_speed, None

    def get_joint_angles(self):
        """returns the robot joint angles.

        joint_angles = (j0, j1, j2, rz, 0, 0)
        j0, j1, j2, rz are numbered from base to end effector and are
        measured in degrees (default)
        """
        info = self._feedback.socket_feedback.recv(1440)
        self._dashboard.Sync()
        info = np.frombuffer(info, dtype=MyType)
        joint_angles = info['q_actual'][0]
        joint_angles = joint_angles[:4] / self._scale_angle
        return joint_angles

    def get_pose(self):
        """retvalsurns the TCP pose in the reference coordinate frame.

        pose = (x, y, z, rz, 0, 0)
        x, y, z specify a Euclidean position (default mm)
        rz rotation of end effector
        """
        info = self._feedback.socket_feedback.recv(1440)
        self._dashboard.Sync()
        info = np.frombuffer(info, dtype=MyType)
        pose = info['tool_vector_actual'][0]
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
        via_pose = np.array(via_pose, dtype=np.float32).ravel()[[0, 1, 2, 5]]
        via_pose[:3] *= self._scale_linear
        end_pose = np.array(end_pose, dtype=np.float32).ravel()[[0, 1, 2, 5]]
        end_pose[:3] *= self._scale_linear   
        pose = self.get_pose()[[0, 1, 2, 5]]
        self._feedback.MovL(*pose, 0, 0)
        self._feedback.Circle(1, *via_pose, 0, 0, *end_pose, 0, 0)
        # self._feedback.Arc(*via_pose, 0, 0, *end_pose, 0, 0) # doesn't work
        self._dashboard.Sync()

    def close(self):
        """Releases any resources held by the controller (e.g., sockets). And disconnects from Dobot magician
        """
        self._dashboard.Sync()
        self._dashboard.ClearError()
        self._dashboard.DisableRobot()
        self._dashboard.close()
        self._feedback.close()
        print("Disconnecting Dobot...")
