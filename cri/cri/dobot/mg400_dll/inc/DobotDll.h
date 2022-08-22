#ifndef DOBOTINDDLL_H
#define DOBOTINDDLL_H

#include "dobotdll_global.h"
#include "DobotTypes.h"

/**************************************** 设备连接 Robot Connection ***************************************/
/**
* @brief 连接机器人控制器                                | Connect the robot controller
* @param ip: 控制器ip地址                                | ip: controller IP address
* @return DobotCommunicate_NoError: 无错误               | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                 | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数        | DobotCommunicate_InvalidParams: Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int ConnectDobot(const char* ip);

/**
* @brief 断开连接机器人控制器                             | Disconnect the robot controller
* @param 无                                             | None
* @return DobotCommunicate_NoError: 无错误               | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                 | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数        | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int DisconnectDobot(void);

/***************************************** 设备信息 Device Information ***************************************/
/**
* @brief 获取设备信息                                    | Get robot version information
* @param version: DobotType::Version 类型地址指针         | version: DobotType::Version pointer
* @return DobotCommunicate_NoError: 无错误                | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                  | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数         | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetDobotVersion(DobotType::Version* version);

/******************************************  速度设置 Speed setting**************************************/
/**
* @brief 设置全局速度比例                                 | Set the global speed ratio
* @param value: 速度比例，数值范围：1~100                  | value: speed ratio, the value range: 1~100
* @return DobotCommunicate_NoError: 无错误               | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                 | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数        | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetRapidRate(int value);

/**
* @brief 获取全局速度比例                                  | Get the global speed ratio
* @param value: 速度比例，数值范围：1~100                   | value: speed ratio, the value range: 1~100
* @return DobotCommunicate_NoError: 无错误                 | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                   | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数          | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetRapidRate(int* value);

/***************************************** 示教指令 Teaching instruction **************************************/
/**
* @brief 设置关节示教启动                                                                    | Set joint teach status
* @param mode: 设置示教关节，DobotType::JointTeachMode 关节示教枚举类型为 Joint1~Joint6         | mode: set the teaching joint,DobotType::JointTeachMode enumeration type can choose Joint1~Joint6
* @param direction: 正方向为true, 负方向为false                                               | direction : the positive direction use true, the negative direction use false
* @return DobotCommunicate_NoError: 无错误                                                   | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                                     | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                                            | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int JointTeachStart(DobotType::JointTeachMode mode, bool direction);

/**
* @brief 设置坐标系示教启动                                                                    | Set coordinate system teach status
* @param mode: 设置示教坐标系，DobotType::CoorTeachMode 坐标系示教枚举类型为 x,y,z,Rx,Ry,Rz       | mode: set the teaching coordinate system,DobotType::CoorTeachMode enumeration type can choose x,y,z,Rx,Ry,Rz
* @param direction: 正方向为true, 负方向为false                                                | direction : the positive direction use true, the negative direction use false
* @return DobotCommunicate_NoError: 无错误                                                    | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                                      | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                                             | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int CoorTeachStart(DobotType::CoorTeachMode mode, bool direction);

/**
* @brief 示教停止                                            | Teach stop
* @param 无                                                  | None
* @return DobotCommunicate_NoError: 无错误                    | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                      | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数             | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int TeachStop();

/*********************************** 运动指令 Motion instructions **************************************/
/**
* @brief 坐标系运动接口(点到点运动方式)                                       | Coordinate system motion ( point-to-point motion mode )
* @param runCmd: DobotType::RunCmd 类型地址指针                             | runCmd: DobotType:: RunCmd pointer
* @param isBlock: 是否阻塞。false不阻塞代码运行，直接运行下一条指令；            | isBlock: Whether it is blocked. If isBlock is false, the code will not be blocked, and the next instruction will be run directly;
*                 true会阻塞代码运行，运动指令执行完才会运行下一条指令           | if isBlock is true, the code will be blocked, and the next instruction will be run after the motion instruction is executed
* @return isBlock为false时返回：                                            | when isBlock is false return:
*         DobotCommunicate_NoError: 无错误                                  | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                    | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                           | DobotCommunicate_InvalidParams:Invalid parameters
*         isBlock为true时返回：                                              | when isBlock is true return:
*         DobotRun_NoError: 无错误                                           | DobotRun_NoError : No error
*         DobotRun_Alarms: 异常报警                                          | DobotRun_Alarms : Alarm abnormally
*         DobotRun_Stop: 主动停止                                            | DobotRun_Stop : Stop abnormally
*/
extern "C" DOBOTDLLSHARED_EXPORT int MovJ(DobotType::RunCmd* runCmd, bool isBlock = false);

/**
* @brief 坐标系运动接口(直线运动方式)                                           | Coordinate system motion ( line motion mode )
* @param runCmd: DobotType::RunCmd 类型地址指针                               | runCmd: DobotType:: RunCmd pointer
* @param isBlock: 是否阻塞。false不阻塞代码运行，直接运行下一条指令；              | isBlock: Whether it is blocked. If isBlock is false, the code will not be blocked, and the next instruction will be run directly;
*                 true会阻塞代码运行，运动指令执行完才会运行下一条指令             | if isBlock is true, the code will be blocked, and the next instruction will be run after the motion instruction is executed
* @return isBlock为false时返回：                                              | when isBlock is false return:
*         DobotCommunicate_NoError: 无错误                                   | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                     | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                            | DobotCommunicate_InvalidParams:Invalid parameters
*         isBlock为true时返回：                                               | when isBlock is true return:
*         DobotRun_NoError: 无错误                                            | DobotRun_NoError : No error
*         DobotRun_Alarms: 异常报警                                           | DobotRun_Alarms : Alarm abnormally
*         DobotRun_Stop: 主动停止                                             | DobotRun_Stop : Stop abnormally
*/
extern "C" DOBOTDLLSHARED_EXPORT int MovL(DobotType::RunCmd* runCmd, bool isBlock = false);

/**
* @brief 关节运动接口                                                         | Joint motion
* @param jointCoordinate: DobotType::JointCoordinate 类型地址指针             | jointCoordinate: DobotType::JointCoordinate pointer
* @param isBlock: 是否阻塞。false不阻塞代码运行，直接运行下一条指令；              | isBlock: Whether it is blocked. If isBlock is false, the code will not be blocked, and the next instruction will be run directly;
*                 true会阻塞代码运行，运动指令执行完才会运行下一条指令             | if isBlock is true, the code will be blocked, and the next instruction will be run after the motion instruction is executed
* @return isBlock为false时返回：                                              | when isBlock is false return:
*         DobotCommunicate_NoError: 无错误                                    | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                      | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                             | DobotCommunicate_InvalidParams:Invalid parameters
*         isBlock为true时返回：                                                | when isBlock is true return:
*         DobotRun_NoError: 无错误                                             | DobotRun_NoError : No error
*         DobotRun_Alarms: 异常报警                                            | DobotRun_Alarms : Alarm abnormally
*         DobotRun_Stop: 主动停止                                              | DobotRun_Stop : Stop abnormally
*/
extern "C" DOBOTDLLSHARED_EXPORT int JointMovJ(DobotType::JointCoordinate* jointCoordinate, bool isBlock = false);

/**
* @brief 偏移指令接口(点对点运动方式)                                        | Offset motion( point-to-point motion mode)
* @param offsetXYZ: DobotType::OffsetXYZ 类型地址指针                      | offsetXYZ: DobotType::OffsetXYZ pointer
* @param isBlock: 是否阻塞。false不阻塞代码运行，直接运行下一条指令；           | isBlock: Whether it is blocked. If isBlock is false, the code will not be blocked, and the next instruction will be run directly;
*                 true会阻塞代码运行，运动指令执行完才会运行下一条指令          | if isBlock is true, the code will be blocked, and the next instruction will be run after the motion instruction is executed
* @return isBlock为false时返回：                                           | when isBlock is false return:
*         DobotCommunicate_NoError: 无错误                                 | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                   | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                          | DobotCommunicate_InvalidParams:Invalid parameters
*         isBlock为true时返回：                                             | when isBlock is true return:
*         DobotRun_NoError: 无错误                                          | DobotRun_NoError : No error
*         DobotRun_Alarms: 异常报警                                         | DobotRun_Alarms : Alarm abnormally
*         DobotRun_Stop: 主动停止                                           | DobotRun_Stop : Stop abnormally
*/
extern "C" DOBOTDLLSHARED_EXPORT int RelMovJ(DobotType::OffsetXYZ* offsetXYZ, bool isBlock = false);

/**
* @brief 偏移指令接口(直线运动方式)                                          | Offset motion( line motion mode)
* @param offsetXYZ: DobotType::OffsetXYZ 类型地址指针                       | offsetXYZ: DobotType::OffsetXYZ pointer
* @param isBlock: 是否阻塞。false不阻塞代码运行，直接运行下一条指令；            | isBlock: Whether it is blocked. If isBlock is false, the code will not be blocked, and the next instruction will be run directly;
*                 true会阻塞代码运行，运动指令执行完才会运行下一条指令           | if isBlock is true, the code will be blocked, and the next instruction will be run after the motion instruction is executed
* @return isBlock为false时返回：                                            | when isBlock is false return:
*         DobotCommunicate_NoError: 无错误                                  | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                    | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                           | DobotCommunicate_InvalidParams:Invalid parameters
*         isBlock为true时返回：                                              | when isBlock is true return:
*         DobotRun_NoError: 无错误                                           | DobotRun_NoError : No error
*         DobotRun_Alarms: 异常报警                                          | DobotRun_Alarms : Alarm abnormally
*         DobotRun_Stop: 主动停止                                            | DobotRun_Stop : Stop abnormally
*/
extern "C" DOBOTDLLSHARED_EXPORT int RelMovL(DobotType::OffsetXYZ* offsetXYZ, bool isBlock = false);

/**************************** 转换工具 Conversion tool ***********************************/
/**
* @brief 转换工具正解。将关节坐标转换为笛卡尔坐标。                             | Conversion tool positive solution. Convert joint coordinate to Cartesian coordinate
* @param wData: DobotType::JointCoordinate 类型地址指针                     | wData: DobotType::JointCoordinate pointer
* @param tool: 工具坐标系索引                                                | tool: Tool coordinate system index
* @param user: 用户坐标系索引                                                | user: User coordinate system index
* @param rData: DobotType::CartesianCoordinate 类型地址指针                  | rData: DobotType::CartesianCoordinate pointer
* @return DobotCommunicate_NoError: 无错误                                  | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                    | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                           | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int PositiveSolution(DobotType::JointCoordinate* wData, int tool, int user, DobotType::CartesianCoordinate* rData);

/**
* @brief 转换工具逆解。将笛卡尔坐标转换为关节坐标。                               | Conversion tool inverse solution. Convert Cartesian coordinate to joint coordinate
* @param wData1: DobotType::CartesianCoordinate 类型地址指针                  | wData1: DobotType::CartesianCoordinate pointer
* @param wData2: DobotType::RDNCoordinate 类型地址指针                        | wData2: DobotType::RDNCoordinate pointer
* @param tool: 工具坐标系索引                                                  | tool: Tool coordinate system index
* @param user: 用户坐标系索引                                                  | user: User coordinate system index
* @param rData: DobotType::JointCoordinate 类型地址指针                        | rData: DobotType::JointCoordinate pointer
* @return DobotCommunicate_NoError: 无错误                                    | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                      | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                             | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int InverseSolution(DobotType::CartesianCoordinate* wData1, DobotType::RDNCoordinate* wData2, int tool, int user, DobotType::JointCoordinate* rData);

/***************************** 机械臂状态设置与获取 Robot status set and get **********************************/
/**
* @brief   提供机械臂数据的获取接口                                  | Get the robot's data
* @param   exchange : 机械臂数据交互类型                            | Robot data interaction types
* @return  DobotCommunicate_NoError: 无错误                       | DobotCommunicate_NoError: No error
*          DobotCommunicate_Timeout: 超时                         | DobotCommunicate_Timeout: Timeout
*          DobotCommunicate_InvalidParams: 无效参数                | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetExchange(DobotType::Exchange* exchange);

/**
* @brief 设置机械臂使能                                            | Set the robotic arm enable status
* @param controlMode: DobotType::ControlMode 枚举类型地址指针       | controlMode: DobotType::ControlMode pointer
* @return DobotCommunicate_NoError: 无错误                        | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                          | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                 | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetControlMode(DobotType::ControlMode* controlMode);

/**
* @brief 获取机械臂使能                                            | Get the robotic arm enable status
* @param controlMode: DobotType::ControlMode 枚举类型地址指针       | controlMode: DobotType::ControlMode pointer
* @return DobotCommunicate_NoError: 无错误                        | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                          | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                 | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetControlMode(DobotType::ControlMode* controlMode);

/**
* @brief 设置机械臂电源状态（六轴机器人）                            | Set robotic arm power state (Six-axis robot)
* @param isOn: 上电为true；下电为false                             | isOn: power on is true , power off is false
* @return DobotCommunicate_NoError: 无错误                        | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                          | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                 | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetPowerMode(bool isOn);

/**
* @brief 获取机械臂电源状态（六轴机器人）                            | Get robotic arm power state (Six-axis robot)
* @param isOn: 上电为true；下电为false                            | isOn: power on is true , power off is false
* @return DobotCommunicate_NoError: 无错误                       | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                         | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetPowerMode(bool* isOn);

/**
* @brief 获取报警信息                                            | Get alarm information
* @param id: 报警id                                             | id: Alarm id
* @param type: 报警类型，控制器报警为 0；伺服关节报警为 1~6          | type: Alarm type, controller alarm type is 0; servo joint alarm type is 1~6
* @param alarmsPara: DobotType::AlarmsPara 类型地址指针          | alarmsPara: DobotType::AlarmsPara pointer
* @param isEn: 英文为true，中文为false                            | isEn: English is true, Chinese is false
* @return DobotCommunicate_NoError: 无错误                       | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                         | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetAlarmsParameter(int id, int type, DobotType::AlarmsPara* alarmsPara, bool isEn);

/**
* @brief 清除报警信息                                           | Clear alarm information
* @param 无                                                    | None
* @return DobotCommunicate_NoError: 无错误                     | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                       | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数              | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int ClearAlarms(void);

/**
* @brief 急停                                                  | Emergency stop
* @param 无                                                    | None
* @return DobotCommunicate_NoError: 无错误                      | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                        | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数               | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int EmergencyStop(void);

/**
* @brief 设置碰撞开关和等级                                      | Set collision status and level
* @param isOn: 碰撞检测开启为true; 碰撞检测关闭为false             | isOn: The collision detection is turned on as true; the collision detection is turned off as false
* @param level: 碰撞等级为1~5                                    | level: The collision level range is 1~5
* @return DobotCommunicate_NoError: 无错误                     | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                       | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数              | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetCollisionMode(bool isOn, int level);

/**
* @brief 获取碰撞开关和等级                                      | Get collision status and level
* @param isOn: 碰撞检测开启为true; 碰撞检测关闭为false             | isOn: The collision detection is turned on as true; the collision detection is turned off as false
* @param level: 碰撞等级为1~5                                   | level: The collision level range is 1~5
* @return DobotCommunicate_NoError: 无错误                      | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                        | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数               | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetCollisionMode(bool* isOn, int* level);

/**
* @brief 复位碰撞状态                                            | Reset  the collision status
* @return DobotCommunicate_NoError: 无错误                      | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                        | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数               | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int ResetCollision();

/**
* @brief 获取笛卡尔坐标                                                            | Get cartesian coordinate
* @param cartesianCoordinate: DobotType::CartesianCoordinate 类型地址指针          | cartesianCoordinate: DobotType::CartesianCoordinate pointer
* @return DobotCommunicate_NoError: 无错误                                         | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                           | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                                  | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetCartesianCoordinate(DobotType::CartesianCoordinate* cartesianCoordinate);

/**
* @brief 获取关节坐标                                                             | Get joint coordinate
* @param jointCoordinate: DobotType::JointCoordinate 类型地址指针                  | jointCoordinate: DobotType::JointCoordinate pointer
* @return DobotCommunicate_NoError: 无错误                                        | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                          | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                                 | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetJointCoordinate(DobotType::JointCoordinate* jointCoordinate);

/**
* @brief 获取六轴机器人姿态                                                       | Get robot pose(six axis)
* @param rdnCoordinate: DobotType::RDNCoordinate 类型地址指针                     | rdnCoordinate: DobotType::RDNCoordinate pointer
* @return DobotCommunicate_NoError: 无错误                                      | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                        | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                               | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetRdnCoordinate(DobotType::RDNCoordinate* rdnCoordinate);

/**
* @brief 获取四轴机器人姿态                                                       | Get robot pose(four axis)
* @param armOrientation: DobotType::ArmOrientation 枚举类型地址指针               | armOrientation: DobotType::ArmOrientation pointer
* @return DobotCommunicate_NoError: 无错误                                      | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                        | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                               | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetArmOrientation(DobotType::ArmOrientation* armOrientation);

/**
* @brief 设置拖动示教状态                                             | Set drag teaching status
* @param isOn: 启动拖动示教为true; 停止拖动示教为false                  | isOn: start drag teaching is true, stop drag teaching is false
* @return DobotCommunicate_NoError: 无错误                           | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                             | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                    | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetTeachTrajectory(bool isOn);

/**
* @brief 设置负载参数                                                | Set load parameters
* @param load: DobotType::Load 类型地址指针                          | load: DobotType::Load pointer
* @return DobotCommunicate_NoError: 无错误                          | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                            | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                   | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetPayLoad(DobotType::Load* load);

/**
* @brief 获取负载参数                                                | Get load parameters
* @param load: DobotType::Load 类型地址指针                          | load: DobotType::Load pointer
* @return DobotCommunicate_NoError: 无错误                          | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                            | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                   | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetPayLoad(DobotType::Load* load);

/*********************************** 用户坐标系 User coordinate system **************************************/
/**
* @brief 设置用户坐标系索引                                           | Set user coordinate system index
* @param index: 用户坐标系索引                                        | index: User coordinate system index
* @return DobotCommunicate_NoError: 无错误                          | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                            | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                   | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetCoordinateUserIndex(int index);

/**
* @brief 获取用户坐标系当前索引                                        | Get user coordinate system index
* @param index: 返回用户坐标系的当前索引                                | index: Return user coordinate system current index
* @return DobotCommunicate_NoError: 无错误                           | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                             | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                    | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetCoordinateUserIndex(int* index);

/**
* @brief 设置用户坐标系索引和参数                                      | Set user coordinate system index and parameters
* @param wData: DobotType::CartesianCoordinate 类型地址指针           | wData: DobotType::CartesianCoordinate pointer
* @param index: 用户坐标系索引，默认为1                                | index: User coordinate system index, the default is 1.
* @return DobotCommunicate_NoError: 无错误                          | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                            | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                   | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetCoordinateUserParams(DobotType::CartesianCoordinate* wData, int index = 1);

/**
* @brief 根据索引获取用户坐标系参数                                     | Get user coordinate system parameters according to index
* @param rData: DobotType::CartesianCoordinate 类型地址指针           | rData: DobotType::CartesianCoordinate pointer
* @param index: 获取的用户坐标系索引，默认为1                            | index: The index of user coordinate system is obtained, which is initialized to 1
* @return DobotCommunicate_NoError: 无错误                           | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                             | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                    | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetCoordinateUserParams(DobotType::CartesianCoordinate* rData, int index = 1);

/**
* @brief 用户坐标系标定                                                                             | User coordinate system calibration
* @param wData[3]: DobotType::CartesianCoordinate 类型数组，长度为3，即标定需要输入的3个点的笛卡尔坐标    | wData[3]: DobotType::CartesianCoordinate array, the length is 3, which is to calibrate the cartesian coordinate of the 3 points that need to be input
* @param rData: DobotType::CartesianCoordinate 类型地址指针，标定后的笛卡尔坐标系                       | rData: DobotType::CartesianCoordinate pointer, cartesian coordinate system after calibration
* @param index: 设置用户坐标系索引，默认为1                                                            | index: Set the user coordinate system index after calibration, the default is 1
* @return DobotCommunicate_NoError: 无错误                                                          | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                                            | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                                                   | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int CalibrateCoordinateUser(DobotType::CartesianCoordinate wData[3], DobotType::CartesianCoordinate* rData, int index = 1);

/************************************ 工具坐标系 Tool coordinate system **************************************/
/**
* @brief 设置工具坐标系索引                                           | Set tool coordinate system index
* @param index: 工具坐标系索引                                        | index: Tool coordinate system index
* @return DobotCommunicate_NoError: 无错误                           | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                             | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                    | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetCoordinateToolIndex(int index);

/**
* @brief 获取工具坐标系当前索引                                        | Get tool coordinate system current index
* @param index: 返回工具坐标系的当前索引                                | index:Return the current index of the tool coordinate system
* @return DobotCommunicate_NoError: 无错误                            | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                              | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                     | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetCoordinateToolIndex(int* index);

/**
* @brief 设置工具坐标系索引和参数                                      | Set tool coordinate system index and parameters
* @param wData: DobotType::CartesianCoordinate 类型地址指针           | wData: DobotType::CartesianCoordinate pointer
* @param index: 工具坐标系索引，默认为1                                | index:Tool coordinate system index, the default is 1.
* @return DobotCommunicate_NoError: 无错误                           | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                             | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                    | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetCoordinateToolParams(DobotType::CartesianCoordinate* wData, int index = 1);

/**
* @brief 根据索引获取工具坐标系参数                                     | Get tool coordinate system parameters according to the index
* @param rData: DobotType::CartesianCoordinate 类型地址指针           | rData: DobotType::CartesianCoordinate pointer
* @param index: 获取的工具坐标系索引，默认为1                            | index:The index of tool coordinate system is obtained, which is initialized to 1.
* @return DobotCommunicate_NoError: 无错误                            | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                              | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                     | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetCoordinateToolParams(DobotType::CartesianCoordinate* rData, int index = 1);

/**
* @brief 工具坐标系位置标定                                                                              | Tool coordinate system position calibration
* @param wData[3]: DobotType::CartesianCoordinate 类型数组，长度为3，即位置标定需要输入的3个点的笛卡尔坐标    | wData[3]: DobotType::CartesianCoordinate array, the length is 3, which is to calibrate the cartesian coordinate of the 3 points that need to be input for position calibration.
* @param rData: DobotType::CartesianCoordinate 类型地址指针，标定后的笛卡尔坐标系                           | rData: DobotType::CartesianCoordinate pointer, cartesian coordinate system after position calibration.
* @param index: 设置工具坐标系索引，默认为1                                                                | index: Set the tool coordinate system index after position calibration, the default is 1.
* @return DobotCommunicate_NoError: 无错误                                                              | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                                                | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                                                       | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int CalibrateCoordinateToolPosition(DobotType::CartesianCoordinate wData[3], DobotType::CartesianCoordinate* rData, int index = 1);

/**
* @brief 工具坐标系姿态标定                                                                              | Tool coordinate system pose calibration
* @param wData[3]: DobotType::CartesianCoordinate 类型数组，长度为3，即姿态标定需要输入的3个点的笛卡尔坐标    | wData[3]: DobotType::CartesianCoordinate array, the length is 3, which is to calibrate the cartesian coordinate of the 3 points that need to be input for pose calibration.
* @param rData: DobotType::CartesianCoordinate 类型地址指针，标定后的笛卡尔坐标系                           | rData: DobotType::CartesianCoordinate pointer, cartesian coordinate system after pose calibration.
* @param index: 设置工具坐标系索引，默认为1                                                                | index: Set the tool coordinate system index after pose calibration, the default is 1.
* @return DobotCommunicate_NoError: 无错误                                                              | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                                                | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                                                       | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int CalibrateCoordinateToolPose(DobotType::CartesianCoordinate wData[3], DobotType::CartesianCoordinate* rData, int index = 1);

/**********************************************结构体数组toPythonSDK***********************************/
extern "C" DOBOTDLLSHARED_EXPORT int CalibrateCoordinateUserToPy(DobotType::CartesianCoordinate wData1, DobotType::CartesianCoordinate wData2, DobotType::CartesianCoordinate wData3, DobotType::CartesianCoordinate* rData, int index = 1);
extern "C" DOBOTDLLSHARED_EXPORT int CalibrateCoordinateToolPositionToPy(DobotType::CartesianCoordinate wData1, DobotType::CartesianCoordinate wData2, DobotType::CartesianCoordinate wData3, DobotType::CartesianCoordinate* rData, int index = 1);
extern "C" DOBOTDLLSHARED_EXPORT int CalibrateCoordinateToolPoseToPy(DobotType::CartesianCoordinate wData1, DobotType::CartesianCoordinate wData2, DobotType::CartesianCoordinate wData3, DobotType::CartesianCoordinate* rData, int index = 1);

/********************** 本体状态实时回调 Real-time callback of robot body status ***********************************/
/**
* @brief 注册机器人连接状态的回调函数                                      | Register the callback function of the robot connection status
* @param ptr: DobotConnectStateCallback 机器人连接状态的回调函数           | ptr: DobotConnectStateCallback robot connection state callback function
* @param arg: 其他可选参数                                                | arg: other optional parameters
* @return DobotCommunicate_NoError: 无错误                               | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                 | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                        | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int ConnectStateCallback(DobotConnectStateCallback ptr, void*  arg);

/**
* @brief 注册机器人实时状态的回调函数                                      | Register the callback function of the robot real-time status
* @param ptr: DobotExchangeCallback 机器人实时状态的回调函数               | ptr: DobotExchangeCallback robot real-time status callback function
* @param arg: 其他可选参数                                                | arg: other optional parameters
* @return DobotCommunicate_NoError: 无错误                               | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                 | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                        | DobotCommunicate_InvalidParams:Invalid parametersn
*/
extern "C" DOBOTDLLSHARED_EXPORT int ExchangeCallback(DobotExchangeCallback ptr, void*  arg);

/************************************ 力矩传感器接口 Torque sensor interface ***********************************/
/**
* @brief 设置力矩传感器开关状态                                             | Set torque sensor status
* @param isOn: 开启力矩传感器为true; 关闭力矩传感器为false                    | isOn: Turning on the torque sensor is true, turning off the torque sensor is false.
* @return DobotCommunicate_NoError: 无错误                                | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                  | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                         | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetForceSensor(bool isOn);

/**
* @brief 获取力矩传感器开关状态                                              | Get torque sensor status
* @param isOn: 开启力矩传感器为true; 关闭力矩传感器为false                     | isOn: Turning on the torque sensor returns true, turning off the torque sensor returns false
* @return DobotCommunicate_NoError: 无错误                                 | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                   | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                          | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetForceSensor(bool* isOn);

/**
* @brief 获取力矩传感器原始参数                                                  | Get torque sensor original parameters
* @param rData: DobotType::ForceOrgValue 类型地址指针，返回力矩传感器参数类型      | rData: return DobotType::ForceOrgValue pointer
* @return DobotCommunicate_NoError: 无错误                                     | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                                       | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数                              | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetForceOrgParams(DobotType::ForceOrgValue* rData);

/**
* @brief 力矩传感器复位                                     | Reset torque sensor
* @param 无                                                | None
* @return DobotCommunicate_NoError: 无错误                  | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                    | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数           | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetForceHome(void);

/**
* @brief 设置力矩传感器扭力值                                | Set the torque value of the torque sensor
* @param value: 扭力值                                      | value: Torque value
* @return DobotCommunicate_NoError: 无错误                  | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                    | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数           | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int SetTorqueParams(float value);

/**
* @brief 获取力矩传感器扭力值                                | Get the torque value of the torque sensor
* @param value: 扭力值                                     | value: Torque value
* @return DobotCommunicate_NoError: 无错误                 | DobotCommunicate_NoError: No error
*         DobotCommunicate_Timeout: 超时                   | DobotCommunicate_Timeout: Timeout
*         DobotCommunicate_InvalidParams: 无效参数          | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT int GetTorqueParams(float* value);

/************** DI/DO & AI/AO 接口 Digital Input/Output and Analog Input/Output interface *********************/
/**
* @brief   获取控制器的模拟输入信号AI                            | Get the analog input signal AI of the controller
* @param   AI: 模拟输入信号参数类型                             | AI: analog input signal type
* @return  DobotCommunicate_NoError: 无错误                   | DobotCommunicate_NoError: No error
*          DobotCommunicate_Timeout: 超时                     | DobotCommunicate_Timeout: Timeout
*          DobotCommunicate_InvalidParams: 无效参数            | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT  int GetAI(DobotType::AI* AI);

/**
* @brief   获取控制器的模拟输出信号AO                            | Get the analog output signal AO of the controller
* @param   AO: 模拟输出信号参数类型                             | AO: analog output signal type
* @return  DobotCommunicate_NoError: 无错误                   | DobotCommunicate_NoError: No error
*          DobotCommunicate_Timeout: 超时                     | DobotCommunicate_Timeout: Timeout
*          DobotCommunicate_InvalidParams: 无效参数            | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT  int GetAO(DobotType::AO* AO);


/**
* @brief   设置控制器的模拟输出信号AO                            | Set the analog output signal AO of the controller
* @param   AO: 模拟输出信号参数类型                             | AO: analog output signal type
* @return  DobotCommunicate_NoError: 无错误                   | DobotCommunicate_NoError: No error
*          DobotCommunicate_Timeout: 超时                     | DobotCommunicate_Timeout: Timeout
*          DobotCommunicate_InvalidParams: 无效参数            | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT  int SetAO(DobotType::AO* AO);

/**
* @brief   获取控制器的数字输入信号DI                            | Get the digital input signal DI of the controller
* @param   DI: 控制器IO信号参数类型                             | DI: IO signal parameter type
* @return  DobotCommunicate_NoError: 无错误                   | DobotCommunicate_NoError: No error
*          DobotCommunicate_Timeout: 超时                     | DobotCommunicate_Timeout: Timeout
*          DobotCommunicate_InvalidParams: 无效参数            | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT  int GetDI(DobotType::IO* DI);

/**
* @brief   获取控制器的数字输出信号DO                            | Get the digital output signal DO of the controller
* @param   DO: 控制器IO信号参数类型                             | DO: IO signal parameter type
* @return  DobotCommunicate_NoError: 无错误                   | DobotCommunicate_NoError: No error
*          DobotCommunicate_Timeout: 超时                     | DobotCommunicate_Timeout: Timeout
*          DobotCommunicate_InvalidParams: 无效参数            | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT  int GetDO(DobotType::IO* DO);

/**
* @brief   设置控制器的数字输出信号DO                            | Set the digital output signal DO of the controller
* @param   DO: 控制器IO信号参数类型                             | DO: IO signal parameter type
* @return  DobotCommunicate_NoError: 无错误                   | DobotCommunicate_NoError: No error
*          DobotCommunicate_Timeout: 超时                     | DobotCommunicate_Timeout: Timeout
*          DobotCommunicate_InvalidParams: 无效参数            | DobotCommunicate_InvalidParams:Invalid parameters
*/
extern "C" DOBOTDLLSHARED_EXPORT  int SetDO(DobotType::IO* DO);


#endif // DOBOTINDDLL_H
