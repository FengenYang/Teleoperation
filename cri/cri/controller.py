# -*- coding: utf-8 -*-
"""Robot controller interface/implementations provide a common, low-level
interface to various robot arms.
"""

import warnings
from abc import ABC, abstractmethod

import numpy as np

from cri.transforms import quat2axangle, axangle2quat, quat2mat, mat2quat, \
    mat2euler, quat2euler, euler2quat, transform, inv_transform
from cri.abb.abb_client import ABBClient
from cri.ur.rtde_client import RTDEClient
from cri.dobot.magician_client import MagicianClient
# from cri.dobot.mg400_dll_client import Mg400Client
from cri.dobot.mg400_client import Mg400Client

try:
    import pyfranka
except ImportError:
    # warnings.warn("Failed to import pyfranka library: pyfranka controller not available")
    pass


class RobotController(ABC):
    """Robot controller class provides a common interface to various robot arms.
    
    Poses and coordinate frames are specified using 3D Cartesian positions
    and quaternion rotations.  This makes it easy to perform coordinate
    transformations using quaternion operations.    
    """
    def __repr__(self):      
        return "{} ({})".format(self.__class__.__name__, self.info)

    def __str__(self):
        return self.__repr__()

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
 
    @property       
    @abstractmethod
    def info(self):
        """Returns a unique robot identifier string.
        """
        pass

    @property    
    @abstractmethod
    def tcp(self):
        """Returns the tool center point (TCP) of the robot.
        
        The TCP is specified in the output flange frame, which is located at
        the intersection of the tool flange center axis and the flange face,
        with the z-axis aligned with the tool flange center axis.
        
        tool = (x, y, z, qw, qx, qy, qz)
        x, y, z specify a Cartesian position (mm)
        qw, qx, qy, qz specify a quaternion rotation
        """
        pass

    @tcp.setter
    @abstractmethod
    def tcp(self, tcp):
        """Sets the tool center point (TCP) of the robot.
        
        The TCP is specified in the output flange frame, which is located at
        the intersection of the tool flange center axis and the flange face,
        with the z-axis aligned with the tool flange center axis.
        
        tcp = (x, y, z, qw, qx, qy, qz)
        x, y, z specify a Cartesian position (mm)
        qw, qx, qy, qz specify a quaternion rotation
        """
        pass

    @property
    @abstractmethod
    def linear_speed(self):
        """Returns the linear speed of the robot TCP (mm/s).
        """
        pass

    @linear_speed.setter
    @abstractmethod
    def linear_speed(self, speed):
        """Sets the linear speed of the robot TCP (mm/s).
        """
        pass

    @property
    @abstractmethod
    def angular_speed(self):
        """Returns the joint speed of the robot TCP (deg/s).
        """
        pass

    @angular_speed.setter    
    @abstractmethod
    def angular_speed(self, speed):
        """Sets the joint speed of the robot TCP (deg/s).
        """
        pass

    @property    
    @abstractmethod
    def blend_radius(self):
        """Returns the robot blend radius (mm).
        """
        pass

    @blend_radius.setter    
    @abstractmethod
    def blend_radius(self, blend_radius):
        """Sets the robot blend radius (mm).
        """
        pass

    @property
    @abstractmethod
    def joint_angles(self):
        """Returns the current joint angles.
        
        joint angles = (j0, j1, j2, j3, j4, j5, [j6])
        j0, j1, j2, j3, j4, j5, [j6] are numbered from base to end effector and are
        measured in degrees
        """
        pass

    @property
    @abstractmethod
    def commanded_joint_angles(self):
        """Returns the commanded joint angles.

        joint angles = (j0, j1, j2, j3, j4, j5, [j6])
        j0, j1, j2, j3, j4, j5, [j6] are numbered from base to end effector and are
        measured in degrees
        """
        pass

    @property    
    @abstractmethod
    def pose(self):
        """Returns the current TCP pose in the reference coordinate frame.
        
        pose = (x, y, z, qw, qx, qy, qz)
        x, y, z specify a Cartesian position (mm)
        qw, qx, qy, qz specify a quaternion rotation
        """
        pass

    @property
    @abstractmethod
    def commanded_pose(self):
        """Returns the commanded TCP pose in the reference coordinate frame.

        pose = (x, y, z, qw, qx, qy, qz)
        x, y, z specify a Cartesian position (mm)
        qw, qx, qy, qz specify a quaternion rotation
        """
        pass

    @property
    @abstractmethod
    def elbow(self):
        """Returns the current elbow angle.
        """
        pass

    @property
    @abstractmethod
    def commanded_elbow(self):
        """Returns the commanded elbow angle.
        """
        pass

    @abstractmethod
    def move_joints(self, joint_angles):
        """Executes an immediate move to the specified joint angles.
        
        joint_angles = (j0, j1, j2, j3, j4, j5)
        j0, j1, j2, j3, j4, j5 are numbered from base to end effector and are
        measured in degrees
        """
        pass

    @abstractmethod
    def move_linear(self, pose, elbow):
        """Executes a linear/cartesian move from the current base frame pose to
        the specified pose.
        
        pose = (x, y, z, qw, qx, qy, qz)
        x, y, z specify a Cartesian position (mm)
        qw, qx, qy, qz specify a quaternion rotation
        elbow = target elbow angle for 7-DOF robot arm (optional)
        """
        pass

    @abstractmethod
    def move_circular(self, via_pose, end_pose, elbow):
        """Executes a movement in a circular path from the current base frame
        pose, through via_pose, to end_pose.
        
        via_pose, end_pose = (x, y, z, qw, qx, qy, qz)
        x, y, z specify a Cartesian position (mm)
        qw, qx, qy, qz specify a quaternion rotation
        elbow = target elbow angle for 7-DOF robot arm (optional)
        """
        pass

    @abstractmethod        
    def close(self):
        """Releases any resources held by the controller (e.g., sockets).
        """
        pass

   
class ABBController(RobotController):
    """ABB controller class implements common interface robot arms.
    
    Currently implemented using an adapted version of the Python 2 client
    example in OpenABB project (https://github.com/robotics/open_abb), which
    has been modified to run under Python 3.
    
    Poses and coordinate frames are specified using 3D Cartesian positions
    and a quaternion rotations.  This format makes it easy to perform
    coordinate transformations.
    """
    def __init__(self, ip='127.0.0.1', port=5000):
        self._ip = ip
        self._port = port
        self._client = ABBClient(ip, port)
        try:
            self.tcp = (0, 0, 0, 1, 0, 0, 0)    # base frame (quaternion)
            self.linear_speed = 20              # mm/s
            self.angular_speed = 20             # deg/s
            self.blend_radius = 0               # mm

            self._commanded_joint_angles = None
            self._commanded_pose = None
        except:
            self._client.close()
            raise

    @property
    def info(self):
        """Returns a unique robot identifier string.
        """
        return "ip: {}, port: {}, info: {}".format(
                self._ip,
                self._port,
                self._client.get_info(),
                )

    @property    
    def tcp(self):
        """Returns the tool center point (TCP) of the robot.
        """
        return self._tcp

    @tcp.setter    
    def tcp(self, tcp):
        """Sets the tool center point (TCP) of the robot.
        """
        self._client.set_tcp(tcp)
        self._tcp = tcp

    @property
    def linear_speed(self):
        """Returns the linear speed of the robot TCP (mm/s).
        """
        return self._linear_speed

    @linear_speed.setter
    def linear_speed(self, speed):
        """Sets the linear speed of the robot TCP (mm/s).
        """
        try:
            self._angular_speed
        except AttributeError:
            self._client.set_speed(linear_speed=speed,
                                   angular_speed=20)
        else:
            self._client.set_speed(linear_speed=speed,
                                   angular_speed=self._angular_speed)
        self._linear_speed = speed

    @property
    def angular_speed(self):
        """Returns the angular speed of the robot TCP (deg/s).
        """
        return self._angular_speed

    @angular_speed.setter
    def angular_speed(self, speed):
        """Sets the angular speed of the robot TCP (deg/s).
        """
        try:
            self._linear_speed
        except AttributeError:
            self._client.set_speed(linear_speed=20,
                                   angular_speed=speed)
        else:
            self._client.set_speed(linear_speed=self._linear_speed,
                                   angular_speed=speed)
        self._angular_speed = speed

    @property
    def blend_radius(self):
        """Returns the robot blend radius (mm).
        """
        return self._blend_radius

    @blend_radius.setter
    def blend_radius(self, blend_radius):
        """Sets the robot blend radius (mm).
        """
        if blend_radius == 0:
            self._client.set_zone(point_motion=True,
                                  manual_zone=(blend_radius,)*3)
        else:
            self._client.set_zone(point_motion=False,
                                  manual_zone=(blend_radius,)*3)
        self._blend_radius = blend_radius

    @property
    def joint_angles(self):
        """Returns the current joint angles.
        """
        return self._client.get_joint_angles()

    @property
    def commanded_joint_angles(self):
        """ Returns the commanded joint angles.
        """
        return self._commanded_joint_angles

    @property
    def pose(self):
        """Returns the current TCP pose.
        """
        return self._client.get_pose()

    @property
    def commanded_pose(self):
        """Returns the commanded TCP pose.
        """
        return self._commanded_pose

    @property
    def elbow(self):
        """Returns the current elbow angle.
        """
        warnings.warn("elbow property not implemented in ABB controller")
        return None
    @property
    def commanded_elbow(self):
        """Returns the commanded elbow angle.
        """
        warnings.warn("elbow property not implemented in ABB controller")
        return None

    def move_joints(self, joint_angles):
        """Executes an immediate move to the specified joint angles.
        """
        joint_angles = np.array(joint_angles)
        self._commanded_joint_angles = joint_angles
        self._client.move_joints(joint_angles)

    def move_linear(self, pose, elbow=None):
        """Executes a linear/cartesian move from the current base frame pose to
        the specified pose.
        """
        if elbow is not None:
            warnings.warn("elbow property not implemented in ABB controller")
        self._commanded_pose = pose
        self._client.move_linear(pose)

    def move_circular(self, via_pose, end_pose, elbow=None):
        """Executes a movement in a circular path from the current base frame
        pose, through via_pose, to end_pose.
        """
        if elbow is not None:
            warnings.warn("elbow property not implemented in ABB controller")
        self._commanded_pose = end_pose
        self._client.move_circular(via_pose, end_pose)

    def close(self):
        """Releases any resources held by the controller (e.g., sockets).
        """
        self._client.close()


class RTDEController(RobotController):
    """UR RTDE controller class implements common interface to robot arms.
    
    Poses and coordinate frames are specified using 3D Cartesian positions
    and quaternion rotations.  This format makes it easy to perform
    coordinate transformations.
    """
    def __init__(self, ip='192.168.125.1'):
        self._ip = ip
        self._client = RTDEClient(ip)        
        try:   
            self.tcp = (0, 0, 0, 1, 0, 0, 0)    # base frame (quaternion)
            self.linear_accel = 500             # mm/s/s
            self.linear_speed = 20              # mm/s
            self.angular_accel = 50             # deg/s/s
            self.angular_speed = 20             # deg/s
            self.blend_radius = 0               # mm
        except:
            self._client.close()
            raise

    @property    
    def info(self):
        """Returns a unique robot identifier string.
        """
        return "ip: {}, info: {}".format(self._ip, self._client.get_info())

    @property    
    def tcp(self):
        """Returns the tool center point (TCP) of the robot.
        """
        return self._tcp

    @tcp.setter    
    def tcp(self, tcp):
        """Sets the tool center point (TCP) of the robot.
        """
        self._client.set_tcp(quat2axangle(tcp))
        self._tcp = tcp

    @property
    def linear_accel(self):
        """Returns the linear acceleration of the robot TCP (mm/s/s).
        """
        return self._linear_accel
    
    @linear_accel.setter    
    def linear_accel(self, accel):
        """Sets the linear acceleration of the robot TCP (mm/s/s).
        """
        self._client.set_linear_accel(accel)
        self._linear_accel = accel

    @property   
    def linear_speed(self):
        """Returns the linear speed of the robot TCP (mm/s).
        """
        return self._linear_speed

    @linear_speed.setter    
    def linear_speed(self, speed):
        """Sets the linear speed of the robot TCP (mm/s).
        """
        self._client.set_linear_speed(speed)
        self._linear_speed = speed

    @property
    def angular_accel(self):
        """Returns the angular acceleration of the robot TCP (deg/s/s).
        """
        return self._angular_accel

    @angular_accel.setter
    def angular_accel(self, accel):
        """Sets the angular acceleration of the robot TCP (deg/s/s).
        """
        self._client.set_angular_accel(accel)
        self._angular_accel = accel

    @property
    def angular_speed(self):
        """Returns the angular speed of the robot TCP (deg/s).
        """
        return self._angular_speed

    @angular_speed.setter
    def angular_speed(self, speed):
        """Sets the angular speed of the robot TCP (deg/s).
        """
        self._client.set_angular_speed(speed)
        self._angular_speed = speed

    @property
    def blend_radius(self):
        """Returns the robot blend radius (mm).
        """
        return self._blend_radius

    @blend_radius.setter    
    def blend_radius(self, blend_radius):
        """Sets the robot blend radius (mm).
        """
        self._client.set_blend_radius(blend_radius)
        self._blend_radius = blend_radius

    @property
    def joint_angles(self):
        """Returns the current joint angles.
        """
        return self._client.get_joint_angles()

    @property
    def commanded_joint_angles(self):
        """Returns the commanded joint angles.
        """
        return self._client.get_target_joint_angles()

    @property
    def pose(self):
        """Returns the current base frame pose.
        """
        return axangle2quat(self._client.get_pose())

    @property
    def commanded_pose(self):
        """Returns the commanded base frame pose.
        """
        return axangle2quat(self._client.get_target_pose())

    @property
    def elbow(self):
        """Returns the current elbow angle.
        """
        warnings.warn("elbow property not implemented in RTDE controller")
        return None

    @property
    def commanded_elbow(self):
        """Returns the commanded elbow angle.
        """
        warnings.warn("elbow property not implemented in RTDE controller")
        return None

    def move_joints(self, joint_angles):
        """Executes an immediate move to the specified joint angles.
        """
        self._client.move_joints(joint_angles)

    def move_linear(self, pose, elbow=None):
        """Executes a linear/cartesian move from the current base frame pose to
        the specified pose.
        """
        if elbow is not None:
            warnings.warn("elbow property not implemented in RTDE controller")
        self._client.move_linear(quat2axangle(pose))

    def move_circular(self, via_pose, end_pose, elbow=None):
        """Executes a movement in a circular path from the current base frame
        pose, through via_pose, to end_pose.
        """
        if elbow is not None:
            warnings.warn("elbow property not implemented in RTDE controller")
        self._client.move_circular(quat2axangle(via_pose),
                                   quat2axangle(end_pose))
      
    def close(self):
        """Releases any resources held by the controller (e.g., sockets).
        """
        return self._client.close()


class PyfrankaController(RobotController):
    """Pyfranka controller class implements common interface to robot arms.

    Poses and coordinate frames are specified using 3D Cartesian positions
    and quaternion rotations.  This format makes it easy to perform
    coordinate transformations.
    """

    def __init__(self, ip='172.16.0.2'):
        self._ip = ip
        self._client = pyfranka.Robot(ip)
        self._client.recover_from_errors()
        self._client.set_default_behavior()

        self.set_units('millimeters', 'degrees')
        self.tcp = (0, 0, 0, 0, 1, 0, 0)    # Re-align TCP with base frame

        self.rel_velocity = 0.1
        self.rel_accel = 0.1
        self.rel_jerk = 0.1

    @property
    def info(self):
        """Returns a unique robot identifier string.
        """
        return "ip: {}, server version: {}".format(self._ip, self._client.server_version())

    @property
    def tcp(self):
        """Returns the tool center point (TCP) of the robot.
        """
        return self._tcp

    @tcp.setter
    def tcp(self, tcp):
        """Sets the tool center point (TCP) of the robot.
        """
        self._tcp = np.array(tcp, dtype=np.float64).ravel()
        self._client.ee_frame = (self._tcp[:3] * self._scale_linear, self._tcp[3:])
        self._client.stiffness_frame = (self._tcp[:3] * self._scale_linear, self._tcp[3:])

    @property
    def max_trans_velocity(self):
        """Returns the maximum translational velocity of the robot TCP (mm/s).
        """
        return self._client.max_trans_velocity / self._scale_linear

    @property
    def max_rot_velocity(self):
        """Returns the maximum rotational velocity of the robot TCP (deg/s).
        """
        return self._client.max_rot_velocity / self._scale_angle

    @property
    def max_joint_velocity(self):
        """Returns the maximum joint velocity of the robot (deg/s).
        """
        return self._client.max_joint_velocity / self._scale_angle

    @property
    def max_trans_accel(self):
        """Returns the maximum translational acceleration of the robot TCP (mm/s/s).
        """
        return self._client.max_trans_accel / self._scale_linear

    @property
    def max_rot_accel(self):
        """Returns the maximum rotational acceleration of the robot TCP (deg/s/s).
        """
        return self._client.max_rot_accel / self._scale_angle

    @property
    def max_joint_accel(self):
        """Returns the maximum joint acceleration of the robot (deg/s/s).
        """
        return self._client.max_joint_accel / self._scale_angle

    @property
    def max_trans_jerk(self):
        """Returns the maximum translational jerk of the robot TCP (mm/s/s/s).
        """
        return self._client.max_trans_jerk / self._scale_linear

    @property
    def max_rot_jerk(self):
        """Returns the maximum rotational jerk of the robot TCP (deg/s/s/s).
        """
        return self._client.max_rot_jerk / self._scale_angle

    @property
    def max_joint_jerk(self):
        """Returns the maximum joint jerk of the robot TCP (deg/s/s/s).
        """
        return self._client.max_joint_jerk / self._scale_linear

    @property
    def rel_velocity(self):
        """Returns the relative velocity of the robot
        """
        return self._rel_velocity

    @rel_velocity.setter
    def rel_velocity(self, rel_velocity):
        """Sets the velocity to rel_velocity % of the maximum (0 < rel_velocity <= 1)
        """
        self._rel_velocity = rel_velocity
        self._client.rel_velocity = rel_velocity

    @property
    def rel_accel(self):
        """Returns the relative acceleration of the robot
        """
        return self._rel_accel

    @rel_accel.setter
    def rel_accel(self, rel_accel):
        """Sets the acceleraton to rel_accel % of the maximum (0 < rel_accel <= 1)
        """
        self._rel_accel = rel_accel
        self._client.rel_accel = rel_accel

    @property
    def rel_jerk(self):
        """Returns the relative jerk of the robot
        """
        return self._rel_jerk

    @rel_jerk.setter
    def rel_jerk(self, rel_jerk):
        """Sets the jerk to rel_jerk % of the maximum (0 < rel_jerk <= 1)
        """
        self._rel_jerk = rel_jerk
        self._client.rel_jerk = rel_jerk

    @property
    def linear_accel(self):
        """Returns the linear acceleration of the robot TCP (mm/s/s).
        """
        warnings.warn("linear_accel property not implemented in pyfranka")
        return None

    @linear_accel.setter
    def linear_accel(self, accel):
        """Sets the linear acceleration of the robot TCP (mm/s/s).
        """
        warnings.warn("linear_accel property not implemented in pyfranka")

    @property
    def linear_speed(self):
        """Returns the linear speed of the robot TCP (mm/s).
        """
        warnings.warn("linear_speed property not implemented in pyfranka")
        return None

    @linear_speed.setter
    def linear_speed(self, speed):
        """Sets the linear speed of the robot TCP (mm/s).
        """
        warnings.warn("linear_speed property not implemented in pyfranka")

    @property
    def angular_accel(self):
        """Returns the angular acceleration of the robot TCP (deg/s/s).
        """
        warnings.warn("angular_accel property not implemented in pyfranka")
        return None

    @angular_accel.setter
    def angular_accel(self, accel):
        """Sets the angular acceleration of the robot TCP (deg/s/s).
        """
        self._client.set_angular_accel(accel)
        warnings.warn("angular_accel property not implemented in pyfranka")

    @property
    def angular_speed(self):
        """Returns the angular speed of the robot TCP (deg/s).
        """
        warnings.warn("angular_speed property not implemented in pyfranka")
        return None

    @angular_speed.setter
    def angular_speed(self, speed):
        """Sets the angular speed of the robot TCP (deg/s).
        """
        warnings.warn("angular_speed property not implemented in pyfranka")

    @property
    def blend_radius(self):
        """Returns the robot blend radius (mm).
        """
        warnings.warn("blend_radius property not implemented in pyfranka")
        return None

    @blend_radius.setter
    def blend_radius(self, blend_radius):
        """Sets the robot blend radius (mm).
        """
        warnings.warn("blend_radius property not implemented in pyfranka")

    def set_units(self, linear, angular):
        """Sets linear and angular units.
        """
        units_l = {'millimeters' : 0.001,
                   'meters' : 1.0,
                   'inches' : 0.0254,
                   }
        units_a = {'degrees' : 0.0174533,
                   'radians' : 1.0,
                   }
        self._scale_linear = units_l[linear]
        self._scale_angle  = units_a[angular]

    @property
    def joint_angles(self):
        """Returns the current joint angles.
        """
        joint_angles = self._client.current_joints
        joint_angles /= self._scale_angle
        return joint_angles

    def desired_joint_angles(self):
        """Returns the desired joint angles.
        """
        joint_angles = self._client.desired_joints
        joint_angles /= self._scale_angle
        return joint_angles

    def commanded_joint_angles(self):
        """Returns the commanded joint angles.
        """
        joint_angles = self._client.commanded_joints
        joint_angles /= self._scale_angle
        return joint_angles

    @property
    def pose(self):
        """Returns the current base frame pose.
        """
        pose = np.concatenate(self._client.current_pose)
        pose[:3] /= self._scale_linear
        return pose

    @property
    def desired_pose(self):
        """Returns the desired base frame pose.
        """
        pose = np.concatenate(self._client.desired_pose)
        pose[:3] /= self._scale_linear
        return pose

    @property
    def commanded_pose(self):
        """Returns the commanded base frame pose.
        """
        pose = np.concatenate(self._client.commanded_pose)
        pose[:3] /= self._scale_linear
        return pose

    @property
    def elbow(self):
        """Returns the current elbow angle.
        """
        elbow = self._client.current_elbow
        elbow[0] /= self._scale_angle
        return elbow[0]

    @property
    def desired_elbow(self):
        """Returns the desired elbow angle.
        """
        elbow = self._client.desired_elbow
        elbow[0] /= self._scale_angle
        return elbow[0]

    @property
    def commanded_elbow(self):
        """Returns the commanded elbow angle.
        """
        elbow = self._client.commanded_elbow
        elbow[0] /= self._scale_angle
        return elbow[0]

    def move_joints(self, joint_angles):
        """Executes an immediate move to the specified joint angles.
        """
        joint_angles = np.array(joint_angles, dtype=np.float64).ravel()
        joint_angles *= self._scale_angle

        self._client.move_joints(joint_angles)

    def move_linear(self, pose, elbow=None):
        """Executes a linear/cartesian move from the current base frame pose to
        the specified pose, using the optional target elbow angle.
        """
        pose = np.array(pose, dtype=np.float64).ravel()
        pose[:3] *= self._scale_linear

        if elbow is None:
            self._client.move_linear((pose[:3], pose[3:]))
        else:
            elbow *= self._scale_angle
            target_elbow = self._client.current_elbow
            target_elbow[0] = elbow
            self._client.move_linear((pose[:3], pose[3:]), target_elbow)

    def move_circular(self, via_pose, end_pose, elbow=None):
        """Executes a movement in a circular path from the current base frame
        pose, through via_pose, to end_pose.
        """
        raise NotImplementedError

    def set_collision_behavior(self,
                               lower_torque_thresholds_accel,
                               upper_torque_thresholds_accel,
                               lower_torque_thresholds_nominal,
                               upper_torque_thresholds_nominal,
                               lower_force_thresholds_accel,
                               upper_force_thresholds_accel,
                               lower_force_thresholds_nominal,
                               upper_force_thresholds_nominal):
        self._client.set_collision_behavior(lower_torque_thresholds_accel,
            upper_torque_thresholds_accel,
            lower_torque_thresholds_nominal,
            upper_torque_thresholds_nominal,
            lower_force_thresholds_accel,
            upper_force_thresholds_accel,
            lower_force_thresholds_nominal,
            upper_force_thresholds_nominal)

    def set_joint_impedance(self, impedance):
        """Sets the joint impedances.
        """
        impedance = np.array(impedance, dtype=np.float64).ravel()
        self._client.set_joint_impedance(impedance)

    def set_cartesian_impedance(self, impedance):
        """Sets the cartesian impedances.
        """
        impedance = np.array(impedance, dtype=np.float64).ravel()
        self._client.set_cartesian_impedance(impedance)

    def recover_from_errors(self):
        """Recover from errors and reset Franka controller.
        """
        self._client.recover_from_errors()

    def close(self):
        """Recover from errors and reset Franka controller.
        """
        self._client.recover_from_errors()


class Mg400Controller(RobotController):
    """Dobot MG400 controller class implements common interface robot arms.   
    
    Poses and coordinate frames are specified using 3D Cartesian positions
    and quaternion rotations.  This format makes it easy to perform
    coordinate transformations.
    """

    def __init__(self, ip="192.168.1.6"):
        self._ip = ip
        self._client = Mg400Client(ip)
        try:
            self.tcp = (0, 0, 0, 1, 0, 0, 0)     # base frame (quaternion)
            self.linear_speed = 10               # mm/s

            self._commanded_joint_angles = None
            self._commanded_pose = None
        except:
            self._client.close()
            raise

    @property
    def info(self):
        """Returns a unique robot identifier string.
        """
        return "ip: {}, {}".format(
                self._ip,
                self._client.get_info(),
                )

    @property
    def tcp(self):
        """Returns the tool center point (TCP) of the robot.
        """
        return self._tcp

    @tcp.setter
    def tcp(self, tcp):
        """Sets the tool center point (TCP) of the robot.
        """
        self._client.set_tcp(tcp)
        self._tcp = tcp

    @property
    def linear_speed(self):
        """Returns the linear speed of the robot TCP (% of max).
        """
        return self._client.get_speed()[0]

    @linear_speed.setter
    def linear_speed(self, speed):
        """Sets the linear speed of the robot TCP (% of max).
        """
        try:
            self._angular_speed
        except AttributeError:
            self._client.set_speed(linear_speed=speed, 
                                   angular_speed=10)
        else:
            self._client.set_speed(linear_speed=speed, 
                                   angular_speed=self._angular_speed)
        self._linear_speed = speed

    @property
    def angular_speed(self, speed):
        """Returns the angular speed of the robot TCP (% of max).
        """
        return self._client.get_speed()[1]

    @angular_speed.setter
    def angular_speed(self, speed):
        """Sets the angular speed of the robot TCP (% of max).
        """
        try:
            self._linear_speed
        except AttributeError:
            self._client.set_speed(linear_speed=10,
                                   angular_speed=speed)
        else:
            self._client.set_speed(linear_speed=self._linear_speed,
                                   angular_speed=speed)
        self._angular_speed = speed


    @property
    def blend_radius(self):
        """Returns the robot blend radius (mm).
        """
        warnings.warn("blend_radius property not implemented in Dobot MG400 Controller")
        pass
    
    @blend_radius.setter
    def blend_radius(self, blend_radius):
        """Sets the robot blend radius (mm).
        """
        warnings.warn("blend_radius property not implemented in Dobot MG400 Controller")
        pass

    @property
    def joint_angles(self):
        """Returns the current joint angles.
        """
        return self._client.get_joint_angles()

    @property
    def commanded_joint_angles(self):
        """ Returns the commanded joint angles.
        """
        return self._commanded_joint_angles

    @property
    def pose(self):
        """Returns the current TCP pose.
        """
        return self._client.get_pose()

    @property
    def commanded_pose(self):
        """Returns the commanded TCP pose.
        """
        return self._commanded_pose

    @property
    def elbow(self):
        """Returns the current elbow angle.
        """
        warnings.warn("elbow property not implemented in Dobot MG400 Controller")
        return None

    def commanded_elbow(self):
        """Returns the commanded elbow angle.
        """
        warnings.warn("elbow property not implemented in Dobot MG400 controller")
        return None

    def move_joints(self, joint_angles):
        """Executes an immediate move to the specified joint angles.
        """
        self._commanded_joint_angles = joint_angles
        self._client.move_joints(joint_angles)
        pass

    def move_linear(self, pose, elbow=None):
        """Executes linear/Cartesian move from base frame pose to specified pose.
        """
        if elbow is not None:
            warnings.warn("elbow property not implemented in Dobot MG400 Controller")
        self._commanded_pose = pose
        self._client.move_linear(pose)

    def move_circular(self, via_pose, end_pose, elbow=None):
        """Executes a movement in a circular path from the current base frame
        pose, through via_pose, to end_pose.
        """
        if elbow is not None:
            warnings.warn("elbow property not implemented in Dobot MG400 Controller")
        self._client.move_circular(via_pose, end_pose)
    
    def close(self):
        """Releases any resources held by the controller (e.g., sockets).
        """
        self._client.close()


class MagicianController(RobotController):
    """Dobot Magician controller class implements common interface robot arms.   
    
    Poses and coordinate frames are specified using 3D Cartesian positions
    and quaternion rotations.  This format makes it easy to perform
    coordinate transformations.
    """

    def __init__(self, port=""):
        self._port = port
        self._client = MagicianClient(port)
        try:
            self.tcp = (0, 0, 0, 1, 0, 0, 0)     # base frame (quaternion)
            self.linear_speed = 100              # mm/s
            self.angular_speed = 100             # deg/s

            self._commanded_joint_angles = None
            self._commanded_pose = None
        except:
            self._client.close()
            raise

    @property
    def info(self):
        """Returns a unique robot identifier string.
        """
        return "port: {}, {}".format(
                self._port,
                self._client.get_info(),
                )

    @property    
    def tcp(self):
        """Returns the tool center point (TCP) of the robot.
        """
        return self._tcp

    @tcp.setter    
    def tcp(self, tcp):
        """Sets the tool center point (TCP) of the robot.
        """
        self._client.set_tcp(tcp)
        self._tcp = tcp

    @property
    def linear_speed(self):
        """Returns the linear speed of the robot TCP (mm/s).
        """
        return self._client.get_speed()[0]

    @linear_speed.setter
    def linear_speed(self, speed):
        """Sets the linear speed of the robot TCP (mm/s).
        """
        try:
            self._angular_speed
        except AttributeError:
            self._client.set_speed(linear_speed=speed, 
                                   angular_speed=100)
        else:
            self._client.set_speed(linear_speed=speed, 
                                   angular_speed=self._angular_speed)
        self._linear_speed = speed

    @property
    def angular_speed(self):
        """Returns the angular speed of the robot TCP (deg/s).
        """
        return self._client.get_speed()[1]
    
    @angular_speed.setter
    def angular_speed(self, speed):
        """Sets the angular speed of the robot TCP (deg/s).
        """
        try:
            self._linear_speed
        except AttributeError:
            self._client.set_speed(linear_speed=100, 
                                   angular_speed=speed)
        else:
            self._client.set_speed(linear_speed=self._linear_speed, 
                                   angular_speed=speed)
        self._angular_speed = speed

    @property
    def blend_radius(self):
        """Returns the robot blend radius (mm).
        """
        warnings.warn("blend_radius property not implemented in Dobot Magician Controller")
        pass
    
    @blend_radius.setter
    def blend_radius(self, blend_radius):
        """Sets the robot blend radius (mm).
        """
        warnings.warn("blend_radius property not implemented in Dobot Magician Controller")
        pass

    @property
    def joint_angles(self):
        """Returns the robot joint angles.
        """
        return self._client.get_joint_angles()

    @property
    def commanded_joint_angles(self):
        """ Returns the commanded joint angles.
        """
        return self._commanded_joint_angles

    @property
    def pose(self):
        """Returns the TCP pose in the reference coordinate frame.
        """
        return self._client.get_pose()

    @property
    def commanded_pose(self):
        """Returns the commanded TCP pose.
        """
        return self._commanded_pose

    @property
    def elbow(self):
        """Returns the current elbow angle.
        """
        warnings.warn("elbow property not implemented in Dobot Magician Controller")
        return None

    def commanded_elbow(self):
        """Returns the commanded elbow angle.
        """
        warnings.warn("elbow property not implemented in Dobot Magician controller")
        return None

    def move_joints(self, joint_angles):
        """Executes an immediate move to the specified joint angles.
        """
        self._commanded_joint_angles = joint_angles
        self._client.move_joints(joint_angles)

    def move_linear(self, pose, elbow=None):
        """Executes linear/Cartesian move from base frame pose to specified pose.
        """
        if elbow is not None:
            warnings.warn("elbow property not implemented in Dobot Magician Controller")
        self._commanded_pose = pose
        self._client.move_linear(pose)

    def move_linear_step(self,pose,elbow=None):
        if elbow is not None:
            warnings.warn("elbow property not implemented in Dobot Magician Controller")
        self._client.move_linear_step(pose)

    def move_linear_stop(self):
        self._client.move_linear_stop()
    def move_linear_forward(self):
        self._client.move_linear_forward()
    def move_linear_back(self):
        self._client.move_linear_back()
    def move_linear_left(self):
        self._client.move_linear_left()
    def move_linear_right(self):
        self._client.move_linear_right()
    def move_linear_up(self):
        self._client.move_linear_up()
    def move_linear_down(self):
        self._client.move_linear_down()
    def move_linear_speed(self,x,y,z):
        self._client.move_linear_speed(x,y,z)

    def move_circular(self, via_pose, end_pose, elbow=None):
        """Executes a movement in a circular path from the current base frame
        pose, through via_pose, to end_pose.
        """
        if elbow is not None:
            warnings.warn("elbow property not implemented in Dobot Magician Controller")
        warnings.warn("move_circular method not implemented in Dobot Magician Controller")
        pass
    
    def control_gripper(self,gripper):
        self._client.control_gripper(gripper)

    def control_pump(self,pump):
        self._client.control_pump(pump)

    def close(self):
        """Releases any resources held by the controller (e.g., sockets).
        """
        self._client.close()
        

class DummyController(RobotController):
    """Dummy controller class does nothing for testing purposes
    """

    def __init__(self, ip='127.0.0.1', port=5000):
        return None

    @property
    def info(self):
        """Returns a unique robot identifier string.
        """
        return "Dummy controller: does nothing"

    @property    
    def tcp(self):
        """Returns the tool center point (TCP) of the robot.
        """
        return None

    @tcp.setter    
    def tcp(self, tcp):
        """Sets the tool center point (TCP) of the robot.
        """
        pass

    @property
    def linear_speed(self):
        """Returns the linear speed of the robot TCP (mm/s).
        """
        return None

    @linear_speed.setter
    def linear_speed(self, speed):
        """Sets the linear speed of the robot TCP (mm/s).
        """
        pass

    @property
    def angular_speed(self):
        """Returns the angular speed of the robot TCP (deg/s).
        """
        return None

    @angular_speed.setter
    def angular_speed(self, speed):
        """Sets the angular speed of the robot TCP (deg/s).
        """
        pass

    @property
    def blend_radius(self):
        """Returns the robot blend radius (mm).
        """
        pass
    
    @blend_radius.setter
    def blend_radius(self, blend_radius):
        """Sets the robot blend radius (mm).
        """
        pass

    @property
    def joint_angles(self):
        """Returns the robot joint angles.
        """
        return [0,0,0,0,0,0]

    @property
    def commanded_joint_angles(self):
        """ Returns the commanded joint angles.
        """
        return [0,0,0,0,0,0]
        
    @property
    def pose(self):
        """Returns the TCP pose in the reference coordinate frame.
        """
        return [0,0,0,0,0,0,1]

    @property
    def commanded_pose(self):
        """Returns the commanded TCP pose.
        """
        return [0,0,0,0,0,0,1]

    @property
    def elbow(self):
        """Returns the current elbow angle.
        """
        return None

    def commanded_elbow(self):
        """Returns the commanded elbow angle.
        """
        return None

    def move_joints(self, joint_angles):
        """Executes an immediate move to the specified joint angles.
        """
        pass

    def move_linear(self, pose, elbow=None):
        """Executes linear/Cartesian move from base frame pose to specified pose.
        """
        pass

    def move_circular(self, via_pose, end_pose, elbow=None):
        """Executes a movement in a circular path from the current base frame
        pose, through via_pose, to end_pose.
        """
        pass
    
    def close(self):
        """Releases any resources held by the controller (e.g., sockets).
        """
        pass