#ifndef DOBOTTYPES_H
#define DOBOTTYPES_H

#include <string>
#ifdef _MSC_VER
    typedef unsigned char uint8_t;
    typedef signed char int8_t;
    typedef unsigned short uint16_t;
    typedef signed short int16_t;
    typedef unsigned int uint32_t;
    typedef signed int int32_t;
    typedef unsigned  long long uint64_t;
    typedef signed long long int64_t;
#else
    #include <stdint.h>
#endif

#pragma pack(push)
#pragma pack(1)

namespace DobotType
{

    /**
    * @brief 通讯返回值枚举类型    | Communication return value enumeration type
    */
    enum
    {
        DobotCommunicate_NoError,       //通讯无错误    | No communication error
        DobotCommunicate_Timeout,       //通讯超时      | Communication timeout
        DobotCommunicate_InvalidParams  //通讯无效参数   | Invalid communication parameters
    };

    /**
    * @brief 运动指令返回值枚举类型    | Motion instruction return value enumeration type
    */
    enum
    {
        DobotRun_NoError,       //运动无错误    | No motion error
        DobotRun_Alarms,        //运动异常报警   | Motion alarm abnormally
        DobotRun_Stop           //运动异常停止   | Motion stop abnormally
    };

    /**
    * @brief 机械臂使能枚举类型   | Robotic arm enable enumeration type
    */
    enum ControlMode
    {
        Disable,        //下使能    | Disable
        Enable,         //上使能     | Enable
        Drag            //拖拽模式    | Drag mode
    };

    /**
    * @brief 机械臂姿态（四轴机器人）枚举类型    | Robotic arm posture (four-axis robot) enumeration type
    */
    enum ArmOrientation
    {
        Left,       //左手方向    | Left hand direction
        Right       //右手方向    | Right hand direction
    };

    /**
    * @brief 关节示教枚举类型    | Joint teach enumeration type
    */
    enum JointTeachMode
    {
        Joint1,       //关节1    | Joint1
        Joint2,       //关节2    | Joint2
        Joint3,       //关节3    | Joint3
        Joint4,       //关节4    | Joint4
        Joint5,       //关节5    | Joint5
        Joint6        //关节6    | Joint6
    };

    /**
    * @brief 坐标系示教枚举类型    | Cartesian coordinate teach enumeration type
    */
    enum CoorTeachMode
    {
        x,        //笛卡尔坐标系x     | Cartesian coordinate x
        y,        //笛卡尔坐标系y     | Cartesian coordinate y
        z,        //笛卡尔坐标系z     | Cartesian coordinate z
        Rx,        //笛卡尔坐标系Rx   | Cartesian coordinate Rx
        Ry,        //笛卡尔坐标系Ry   | Cartesian coordinate Ry
        Rz         //笛卡尔坐标系Rz   | Cartesian coordinate Rz
    };

    /**
    * @brief 机械臂版本参数类型    | Robotic arm version parameter type
    */
    typedef struct
    {
        char verTeach[25];       //示教器版本    | Teach pendant version
        char verControl[25];     //控制器版本    | Controller version
        char verAlgs[25];        //算法版本      | Algorithm version
        char verSystem[25];      //系统版本      | System version
    } Version;

    /**
    * @brief 机械臂运动坐标系参数类型                         | Robotic arm motion coordinate parameter type
    * 四轴机器人生效参数: x,y,z,Rx,tool,user,arm              | Effective parameters of four-axis robot: x,y,z,Rx,tool,user,arm
    * 四轴时机器人如果为关节型机器人(例：MG400)，不需填姿态arm   | If the robot is an articulated robot (for example: MG400) when the robot is four-axis, it is not necessary to fill in the posture arm.
    * 四轴时机器人如果为SCARA型机器人(例：M1Pro)，需填姿态arm   | If the robot is a SCARA robot (for example: M1Pro) when the robot is four-axis, the posture arm is required.
    * 六轴机器人生效参数: x,y,z,Rx,Ry,Rz,tool,user,r,d,n,cfg    | Effective parameters of six-axis robot: x,y,z,Rx,Ry,Rz,tool,user,r,d,n,cfg
    */
    typedef struct
    {
        float x;        //笛卡尔坐标系x            | Cartesian coordinate x
        float y;        //笛卡尔坐标系y            | Cartesian coordinate y
        float z;        //笛卡尔坐标系z            | Cartesian coordinate z
        float Rx;       //笛卡尔坐标系Rx           | Cartesian coordinate Rx
        float Ry;       //笛卡尔坐标系Ry           | Cartesian coordinate Ry
        float Rz;       //笛卡尔坐标系Rz           | Cartesian coordinate Rz
        int tool;       //工具坐标系索引           | Tool coordinate index
        int user;       //用户坐标系索引           | User coordinate index
        int r;          //六轴机器人姿态参数r       | Pose parameter r (Six-axis robot)
        int d;          //六轴机器人姿态参数d       | Pose parameter d (Six-axis robot)
        int n;          //六轴机器人姿态参数n       | Pose parameter n (Six-axis robot)
        int cfg;        //六轴机器人姿态参数cfg     | Pose parameter cfg (Six-axis robot)
        ArmOrientation arm;      //四轴机器人姿态参数arm     | Pose parameter arm (Four-axis robot)
    } RunCmd;

#define ROBOT_AXIS      6       //机械臂轴数    | Robot axis number

    /**
    * @brief 机械臂运动关节参数类型    | Robotic arm motion joint parameter type
    */
    typedef struct
    {
        float j[ROBOT_AXIS];        //关节坐标数组    | Joint coordinate array
    } JointCoordinate;

    /**
    * @brief 坐标系参数类型    | Coordinate parameter type
    */
    typedef struct
    {
        float x;        //笛卡尔坐标系x    | Cartesian coordinate x
        float y;        //笛卡尔坐标系y    | Cartesian coordinate y
        float z;        //笛卡尔坐标系z    | Cartesian coordinate z
        float Rx;       //笛卡尔坐标系Rx   | Cartesian coordinate Rx
        float Ry;       //笛卡尔坐标系Ry   | Cartesian coordinate Ry
        float Rz;       //笛卡尔坐标系Rz   | Cartesian coordinate Rz
    } CartesianCoordinate;

    /**
    * @brief 机械臂偏移运动坐标系参数类型    | Robotic arm offset motion coordinate system parameter type
    */
    typedef struct
    {
        float offsetX;        //笛卡尔坐标系x方向上偏移    | Offset in the x direction of the Cartesian
        float offsetY;        //笛卡尔坐标系y方向上偏移    | Offset in the x direction of the Cartesian
        float offsetZ;        //笛卡尔坐标系z方向上偏移    | Offset in the x direction of the Cartesian
    } OffsetXYZ;

    /**
    * @brief 机械臂姿态参数类型    | Robotic arm pose parameter type
    */
    typedef struct
    {
        int r;          //姿态参数r      | Pose parameter r
        int d;          //姿态参数d      | Pose parameter d
        int n;          //姿态参数n      | Pose parameter n
        int cfg;        //姿态参数cfg    | Pose parameter cfg
    } RDNCoordinate;

    /**
    * @brief 力矩传感器参数类型    | Torque sensor parameter type
    */
    typedef struct
    {
        float orgValue[ROBOT_AXIS];       //力矩传感器参数数组   | torque sensor parameter array
    } ForceOrgValue;

    /**
    * @brief 报警信息参数类型    | Alarm information parameter type
    */
    typedef struct
    {
        int id;                          //报警id        | Alarm id
        int level;                       //报警层级       | Alarm level
        wchar_t description[256];        //报警描述       | Alarm description
        wchar_t cause[256];              //报警原因       | Alarm cause
        wchar_t solution[256];           //报警解决方法    | Alarm solution
    } AlarmsPara;

    /**
    * @brief 机械臂负载参数类型    | Robotic arm load parameter type
    */
    typedef struct
    {
        float inertiaX;         //X惯性                | X inertia
        float inertiaY;         //Y惯性                | Y inertia
        float inertiaZ;         //Z惯性                | Z inertia
        float toolLength;       //工具长度（单位为mm）   | Tool length
        float loadValue;        //负载重量（单位为kg）   | Load weight
    } Load;

#define AlarmsCountMax 64       //报警id数最大为64，范围0~63    | The maximum number of alarm ID is 64, the range is 0~63
#define AlarmsTypeMax 7         //报警类型最大为6，范围0~6       | The maximum number of alarm type is 7, the range is 0~6

    /**
    * @brief 报警信息id数组参数类型    | Alarm information id array parameter type
    */
    typedef struct
    {
        int alarmsID[AlarmsTypeMax][AlarmsCountMax];        //报警信息id数组    | Alarm information id array
    } Alarms;

#define IoCountSum    64    //IO信号数目    | Number of IO signals

    /**
    * @brief 控制器IO信号参数类型    | IO signal parameter type
    */
    typedef struct
    {
        bool enable;                  //IO信号使能    | IO signal enable
        bool value[IoCountSum];       //IO信号数组    | IO signal array
    } IO;

    /**
    * @brief 模拟输入信号参数类型        | AI signal parameter type
    *  mode1 模拟输入信号1              | mode1 is AI signal index 1
    *  mode2 模拟输入信号2              | mode2 is AI signal index 2
    */
    typedef struct {
        int mode1;
        int mode2;
    } AI;

    /**
    * @brief 模拟输出信号参数类型        | AO signal parameter type
    *  mode  模拟输出信号类型           | AO mode
    *  value 模拟输出数据值             | AO data
    */
    typedef struct {
        struct {
            int mode;
            int value;
        }in1;
        struct {
            int mode;
            int value;
        }in2;
    } AO;

    /**
    * @brief 实时数据交互类型    | Real-time data interaction type
    */
    typedef struct
    {
        bool  controlMode;                  //实时机械臂使能状态                             | Current robot arm enable state
        bool  powerState;                   //实时机械臂电源状态                             | Current robot power enable state
                                            //（六轴机器人此参数有用，四轴机器人此参数无用）      | (This parameter is useful for six-axis robots, but is useless for four-axis robots)
        bool  isCollision;                  //实时检测是否碰撞                               | Current collision check
        bool  jogMode;                      //实时点动模式                                  | Current jog mode
        bool  isAuto;                       //实时手自动模式                                | Current manual automatic mode
        int  toolCoordinate;                //实时工具坐标系索引                             | Current tool coordinate index
        int  userCoordinate;                //实时用户坐标系索引                             | Current user coordinate index
        float joint[ROBOT_AXIS];            //实时关节数组                                  | Current joint array
        float coordinate[ROBOT_AXIS];       //实时笛卡尔坐标系数组                           | Current Cartesian coordinate array
        Alarms alarms;                      //实时报警信息id数组                             | Current alarm information id array
        RDNCoordinate rdn;                  //实时六轴机器人姿态                             | Current pose (Six-axis robot)
        ArmOrientation arm;                 //实时四轴机器人姿态                             | Current pose (Four-axis robot)
        IO ioOut;                           //实时IO信号输出                                | Current IO signal output
        IO ioIn;                            //实时IO信号输入                                | Current IO signal input
    } Exchange;

}

#pragma pack(pop)

/**
* @brief 机器人连接状态的回调函数                | callback function of robot connection status
* @param isConnect: 布尔类型，当前是否连接       | isConnect: Boolean type, whether it is currently connected
* @param arg: 其他可选参数                     | arg: other optional parameters
* @return 无                                  | None
*/
typedef void (*DobotConnectStateCallback) (bool isConnect, void *arg);

/**
* @brief 机器人实时状态的回调函数                           | callback function of the real-time status of the robot
* @param exchange: DobotType::Exchange 实时数据交互类型    | DobotType::Exchange real-time data interaction type
* @param arg: 其他可选参数                                | arg: other optional parameters
* @return 无                                             | None
*/
typedef void (*DobotExchangeCallback) (DobotType::Exchange *exchange, void *arg);



#endif // DOBOTTYPES_H
