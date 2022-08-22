from ctypes import *
import time, platform, enum, os
"""
此python模块将使用于api函数中的c类型封装成原生对应的python类型
This module encapsulates c structures used in the api functions as corresponding python class
"""


class DobotCommunicate(enum.Enum):
    """
    通讯返回值类型
    """
    DobotCommunicate_NoError = 0        #通讯无错误
    DobotCommunicate_Timeout = 1        #通讯超时
    DobotCommunicate_InvalidParams = 2  #通讯无效参数


class DobotRun(enum.Enum):
    """
    运动指令返回值类型
    """
    DobotRun_NoError = 0    #运动无错误
    DobotRun_Alarms = 1     #运动异常报警
    DobotRun_Stop = 2       #运动异常停止


class ControlMode(enum.Enum):
    """
    机械臂使能类型
    """
    DisableControlMode = 0    #下使能
    EnableControlMode = 1     #上使能
    DragControlMode = 2       #拖拽模式


class ArmOrientation(enum.Enum):
    """
    机械臂姿态（四轴机器人）类型
    """
    LeftyArmOrientation = 0    #左手方向
    RightyArmOrientation = 1   #右手方向


class JointTeachMode(enum.Enum):
    """
    关节示教类型
    """
    Joint1 = 0    #关节1
    Joint2 = 1    #关节2
    Joint3 = 2    #关节3
    Joint4 = 3    #关节4
    Joint5 = 4    #关节5
    Joint6 = 5    #关节6


class CoorTeachMode(enum.Enum):
    """
    坐标系示教类型
    """
    x = 0    #笛卡尔坐标系x
    y = 1    #笛卡尔坐标系y
    z = 2    #笛卡尔坐标系z
    Rx = 3   #笛卡尔坐标系Rx
    Ry = 4   #笛卡尔坐标系Ry
    Rz = 5   #笛卡尔坐标系Rz


VersionLength = 25
ROBOT_AXIS = 6


class Version(Structure):
    """
    机械臂版本类型
    """
    _pack_ = 1
    _fields_ = [
        ("verTeach", c_char * VersionLength),    #示教器版本
        ("verControl", c_char * VersionLength),  #控制器版本
        ("verAlgs", c_char * VersionLength),     #算法版本
        ("verSystem", c_char * VersionLength),   #系统版本
    ]


class RunCmd(Structure):
    """
    机械臂运动坐标系参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("x", c_float),    #笛卡尔坐标系x
        ("y", c_float),    #笛卡尔坐标系y
        ("z", c_float),    #笛卡尔坐标系z
        ("Rx", c_float),   #笛卡尔坐标系Rx
        ("Ry", c_float),   #笛卡尔坐标系Ry
        ("Rz", c_float),   #笛卡尔坐标系Rz
        ("tool", c_int),   #工具坐标系索引
        ("user", c_int),   #用户坐标系索引
        ("r", c_int),      #（六轴机器人）姿态参数r
        ("d", c_int),      #（六轴机器人）姿态参数d
        ("n", c_int),      #（六轴机器人）姿态参数n
        ("cfg", c_int),    #（六轴机器人）姿态参数cfg
        ("arm", c_int)     #（四轴机器人）姿态参数arm
    ]


class JointCoordinate(Structure):
    """
    机械臂运动关节参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("j", c_float * ROBOT_AXIS),  # 关节坐标数组
    ]


class CartesianCoordinate(Structure):
    """
    坐标系参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("x", c_float),    #笛卡尔坐标系x
        ("y", c_float),    #笛卡尔坐标系y
        ("z", c_float),    #笛卡尔坐标系z
        ("Rx", c_float),   #笛卡尔坐标系Rx
        ("Ry", c_float),   #笛卡尔坐标系Ry
        ("Rz", c_float),   #笛卡尔坐标系Rz
    ]


class OffsetXYZ(Structure):
    """
    机械臂偏移运动坐标系参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("offsetX", c_float),    #笛卡尔坐标系x方向上偏移
        ("offsetY", c_float),    #笛卡尔坐标系y方向上偏移
        ("offsetZ", c_float),    #笛卡尔坐标系z方向上偏移
    ]


class RDNCoordinate(Structure):
    """
    机械臂姿态（六轴机器人）参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("r", c_int),    #姿态参数r
        ("d", c_int),    #姿态参数d
        ("n", c_int),    #姿态参数n
        ("cfg", c_int),  #姿态参数cfg
    ]


class ForceOrgValue(Structure):
    """
    力矩传感器参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("orgValue", c_float * ROBOT_AXIS),  # 力矩传感器参数数组
    ]


class AlarmsPara(Structure):
    """
    报警信息参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("id", c_int),                #报警id
        ("level", c_int),             #报警层级
        ("description", c_wchar * 256 ),   #报警描述
        ("cause", c_wchar * 256),         #报警原因
        ("solution", c_wchar * 256),      #报警解决方法
    ]


class PayLoad(Structure):
    """
    机械臂负载参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("inertiaX", c_float),    #X惯性
        ("inertiaY", c_float),    #Y惯性
        ("inertiaZ", c_float),    #Z惯性
        ("toolLength", c_float),  #工具长度
        ("loadValue", c_float),   #负载重量
    ]


IoCountSum = 64
AlarmsCountMax = 64
AlarmsTypeMax = 7


class IO(Structure):
    """
    IO信号参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("enable", c_bool),                #IO信号使能
        ("value", c_bool * IoCountSum),    #IO信号数组
    ]


class AI(Structure):
    """
    模拟输入信号参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("mode1", c_int),  #模拟输入信号1
        ("mode2", c_int)   #模拟输入信号2
    ]


class AO(Structure):
    """
    模拟输出信号参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("mode1", c_int),   #模拟输出信号1
        ("value1", c_int),  #模拟输出信号1值
        ("mode2", c_int),   #模拟输出信号2
        ("value2", c_int)   #模拟输出信号2值
    ]


class Alarms(Structure):
    """
    报警信息id数组参数类型
    """
    _pack_ = 1
    _fields_ = [
        ("alarmsID", (c_int * AlarmsCountMax) * AlarmsTypeMax),    #报警信息id数组
    ]


class Exchange(Structure):
    """
    实时数据交互类型
    """
    _pack_ = 1
    _fields_ = [
        ("controlMode", c_bool),                 #实时机械臂使能状态
        ("powerState", c_bool),                  #实时机械臂电源状态（六轴机器人此参数有用，四轴机器人此参数无用）
        ("isCollision", c_bool),                 #实时检测是否碰撞                              
        ("jogMode", c_bool),                     #实时点动模式
        ("isAuto", c_bool),                      #实时手自动模式
        ("toolCoordinate", c_int),               #实时工具坐标系索引
        ("userCoordinate", c_int),               #实时用户坐标系索引
        ("joint", JointCoordinate),              #实时关节数组
        ("coordinate", CartesianCoordinate),     #实时笛卡尔坐标系数组
        ("alarms", Alarms),                      #实时报警信息id数组
        ("rdn", RDNCoordinate),                  #实时姿态（六轴机器人）
        ("arm", c_int),                          #实时姿态（四轴机器人）
        ("ioOut", IO),                           #实时IO信号输出
        ("ioIn", IO),                            #实时IO信号输入
    ]


"""
此部分将dll中提供的api函数封装成python函数 并添加了简易的异常处理功能：如果api函数未成功执行则重复执行到成功为止
This section encapsulate api functions provided by the dll as python function and add a rudimentary exception handling mechanism: 
Keep calling an api function until it execute successfully

此部分中函数参数中的api代表 load() 返回的CDLL实例
The common parameter "api" used by the following functions represent the CDLL instance returned from load() function.
"""


def load():
    if platform.system() == "Windows":
        return CDLL(os.getcwd() + "\Dobot.dll", RTLD_GLOBAL)
    elif platform.system() == "Linux":
        return CDLL("libDobot.so", RTLD_GLOBAL)


def dSleep(ms):
    time.sleep(ms / 1000)


def getTime():
    return [time.time()]


"""设备连接"""


def ConnectDobot(api, ip):
    """
    连接机器人控制器
    :param api:python调用动态库获取的对象
    :param ip:控制器 ip 地址，如192.168.5.1
    :return:通讯返回值结果DobotCommunicate
    """
    ipPara = create_string_buffer(100)
    ipPara.raw = ip.encode('utf-8')
    result = c_int(0)
    result = api.ConnectDobot(ipPara)
    return result

def DisconnectDobot(api):
    """
    断开连接机器人控制器
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    result = api.DisconnectDobot()
    return result


"""设备信息"""


def GetDobotVersion(api):
    """
    获取设备信息，包括示教器版本、算法版本、控制器版本、系统版本等
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate,Version机械臂版本类型
    """
    versionParam = Version()
    result = c_int(0)
    result = api.GetDobotVersion(byref(versionParam))
    return [
        result,
        versionParam.verTeach.decode('utf-8'),
        versionParam.verControl.decode('utf-8'),
        versionParam.verAlgs.decode('utf-8'),
        versionParam.verSystem.decode('utf-8')
    ]


"""速度设置"""


def SetRapidRate(api, value):
    """
    设置全局速度比例，数值范围：1~100
    :param api:python调用动态库获取的对象
    :param value:速度比例
    :return:通讯返回值结果DobotCommunicate
    """
    valuePara = c_int(value)
    result = c_int(0)
    result = api.SetRapidRate(valuePara)
    return result


def GetRapidRate(api):
    """
    获取全局速度比例
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和value速度比例
    """
    value = c_int()
    result = c_int(0)
    result = api.GetRapidRate(byref(value))
    return [result, value.value]


"""示教指令"""


def JointTeachStart(api, jointTeachMode, direction):
    """
    设置关节示教启动
    :param api:python调用动态库获取的对象
    :param jointTeachMode:设置示教关节，JointTeachMode关节示教类型为Joint1~Joint6
    :param direction:正方向为true, 负方向为false
    :return:通讯返回值结果DobotCommunicate
    """
    jointTeachModePara = c_int(jointTeachMode) 
    directionPara = c_bool(direction)
    result = c_int(0)
    result = api.JointTeachStart(jointTeachModePara, directionPara)
    return result


def CoorTeachStart(api, coorTeachMode, direction):
    """
    设置坐标系示教启动
    :param api:python调用动态库获取的对象
    :param coorTeachMode:设置示教坐标系，CoorTeachMode坐标系示教类型为x,y,z,a,b,c
    :param direction:正方向为true, 负方向为false
    :return:通讯返回值结果DobotCommunicate
    """
    coorTeachModePara = c_int(coorTeachMode) 
    directionPara = c_bool(direction)
    result = c_int(0)
    result = api.CoorTeachStart(coorTeachModePara, directionPara)
    return result


def TeachStop(api):
    """
    示教停止。配合关节示教启动，坐标系示教启动使用
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    result = api.TeachStop()
    return result


"""运动指令"""


def MovJ(api, pointList, tool = 0, user = 0, rdnList = [-1, -1, -1, -1], arm = 0, isBlock = False):
    """
    坐标系运动接口(点到点运动方式)
    四轴机器人生效参数: pointList[0],pointList[1],pointList[2],pointList[3],tool,user,arm,isBlock
    四轴时机器人如果为关节型机器人(例：MG400)，不需填姿态arm，如果为SCARA型机器人(例：M1Pro)，需填姿态arm
    六轴机器人生效参数: pointList[0],pointList[1],pointList[2],pointList[3],pointList[4],pointList[5],tool,user,rdnList,isBlock
    :param api:python调用动态库获取的对象
    :param pointList:运动点位list
    :param tool:工具坐标系索引，默认为0
    :param user:用户坐标系索引，默认为0
    :param rdnList:姿态参数list（六轴机器人），默认为[-1,-1,-1,-1]
    :param arm:姿态参数（四轴机器人），默认为0左手姿态
    :param isBlock:是否阻塞。false不阻塞代码运行，直接运行下一条指令；true会阻塞代码运行，运动指令执行完才会运行下一条指令
    :return:isBlock为false时返回：通讯返回值结果DobotCommunicate
            isBlock为true时返回：运动指令返回值结果DobotRun
    """
    runCmdParam = RunCmd()
    runCmdParam.x = c_float(pointList[0])
    runCmdParam.y = c_float(pointList[1])
    runCmdParam.z = c_float(pointList[2])
    runCmdParam.Rx = c_float(pointList[3])
    runCmdParam.Ry = c_float(pointList[4])
    runCmdParam.Rz = c_float(pointList[5])
    runCmdParam.tool = c_int(tool)
    runCmdParam.user = c_int(user)
    runCmdParam.r = c_int(rdnList[0])
    runCmdParam.d = c_int(rdnList[1])
    runCmdParam.n = c_int(rdnList[2])
    runCmdParam.cfg = c_int(rdnList[3])
    runCmdParam.arm = c_int(arm)
    result = c_int(0)
    result = api.MovJ(byref(runCmdParam), isBlock)
    return result


def MovL(api, pointList, tool = 0, user = 0, rdnList = [-1, -1, -1, -1], arm = 0, isBlock = False):
    """
    坐标系运动接口(直线运动方式)
    四轴机器人生效参数: pointList[0],pointList[1],pointList[2],pointList[3],tool,user,arm,isBlock
    四轴时机器人如果为关节型机器人(例：MG400)，不需填姿态arm，如果为SCARA型机器人(例：M1Pro)，需填姿态arm
    六轴机器人生效参数: pointList[0],pointList[1],pointList[2],pointList[3],pointList[4],pointList[5],tool,user,rdnList,isBlock
    :param api:python调用动态库获取的对象
    :param pointList:运动点位list
    :param tool:工具坐标系索引，默认为0
    :param user:用户坐标系索引，默认为0
    :param rdnList:姿态参数list（六轴机器人），默认为[-1,-1,-1,-1]
    :param arm:姿态参数（四轴机器人），默认为0左手姿态
    :param isBlock:是否阻塞。false不阻塞代码运行，直接运行下一条指令；true会阻塞代码运行，运动指令执行完才会运行下一条指令
    :return:isBlock为false时返回：通讯返回值结果DobotCommunicate
            isBlock为true时返回：运动指令返回值结果DobotRun
    """
    runCmdParam = RunCmd()
    runCmdParam.x = c_float(pointList[0])
    runCmdParam.y = c_float(pointList[1])
    runCmdParam.z = c_float(pointList[2])
    runCmdParam.Rx = c_float(pointList[3])
    runCmdParam.Ry = c_float(pointList[4])
    runCmdParam.Rz = c_float(pointList[5])
    runCmdParam.tool = c_int(tool)
    runCmdParam.user = c_int(user)
    runCmdParam.r = c_int(rdnList[0])
    runCmdParam.d = c_int(rdnList[1])
    runCmdParam.n = c_int(rdnList[2])
    runCmdParam.cfg = c_int(rdnList[3])
    runCmdParam.arm = c_int(arm)
    result = c_int(0)
    result = api.MovL(byref(runCmdParam), isBlock)
    return result


def JointMovJ(api, jointCoordinateList, isBlock = False):
    """
    关节运动接口
    :param api:python调用动态库获取的对象
    :param jointCoordinateList:存储JointCoordinate 机械臂运动关节参数类型的list
    :param isBlock:是否阻塞。false不阻塞代码运行，直接运行下一条指令；true会阻塞代码运行，运动指令执行完才会运行下一条指令
    :return:isBlock为false时返回：通讯返回值结果DobotCommunicate
            isBlock为true时返回：运动指令返回值结果DobotRun
    """
    jointCoordinateParam = JointCoordinate()
    sixFloats = c_float * 6
    j = sixFloats(jointCoordinateList[0], jointCoordinateList[1],
                  jointCoordinateList[2], jointCoordinateList[3],
                  jointCoordinateList[4], jointCoordinateList[5])
    jointCoordinateParam.j = j
    result = c_int(0)
    result = api.JointMovJ(byref(jointCoordinateParam), isBlock)
    return result


def RelMovJ(api, offsetX, offsetY, offsetZ, isBlock = False):
    """
    偏移指令接口(点对点运动方式)
    :param api:python调用动态库获取的对象
    :param offsetX:笛卡尔坐标系x方向上的偏移
    :param offsetY:笛卡尔坐标系y方向上的偏移
    :param offsetZ:笛卡尔坐标系z方向上的偏移
    :param isBlock:是否阻塞。false不阻塞代码运行，直接运行下一条指令；true会阻塞代码运行，运动指令执行完才会运行下一条指令
    :return:isBlock为false时返回：通讯返回值结果DobotCommunicate
            isBlock为true时返回：运动指令返回值结果DobotRun
    """
    offsetXYZParam = OffsetXYZ()
    offsetXYZParam.offsetX = c_float(offsetX)
    offsetXYZParam.offsetY = c_float(offsetY)
    offsetXYZParam.offsetZ = c_float(offsetZ)
    result = c_int(0)
    result = api.RelMovJ(byref(offsetXYZParam), isBlock)
    return result


def RelMovL(api, offsetX, offsetY, offsetZ, isBlock = False):
    """
    偏移指令接口(直线运动方式)
    :param api:python调用动态库获取的对象
    :param offsetX:笛卡尔坐标系x方向上的偏移
    :param offsetY:笛卡尔坐标系y方向上的偏移
    :param offsetZ:笛卡尔坐标系z方向上的偏移
    :param isBlock:是否阻塞。false不阻塞代码运行，直接运行下一条指令；true会阻塞代码运行，运动指令执行完才会运行下一条指令
    :return:isBlock为false时返回：通讯返回值结果DobotCommunicate
            isBlock为true时返回：运动指令返回值结果DobotRun
    """
    offsetXYZParam = OffsetXYZ()
    offsetXYZParam.offsetX = c_float(offsetX)
    offsetXYZParam.offsetY = c_float(offsetY)
    offsetXYZParam.offsetZ = c_float(offsetZ)
    result = c_int(0)
    result = api.RelMovL(byref(offsetXYZParam), isBlock)
    return result


"""转换工具"""


def PositiveSolution(api, wDataList, tool, user):
    """
    转换工具正解。将关节坐标转换为笛卡尔坐标。
    :param api:python调用动态库获取的对象
    :param wDataList:存储JointCoordinate 机械臂运动关节参数类型的list
    :param tool:工具坐标系索引
    :param user:用户坐标系索引
    :return:通讯返回值结果DobotCommunicate和CartesianCoordinate机械臂运动坐标系参数类型
    """
    wDataParam = JointCoordinate()
    sixFloats = c_float * 6
    wDataParam.j = sixFloats(wDataList[0], wDataList[1], wDataList[2],
                             wDataList[3], wDataList[4], wDataList[5])
    rDataParam = CartesianCoordinate()
    result = c_int(0)
    result = api.PositiveSolution(byref(wDataParam), c_int(tool), c_int(user), byref(rDataParam))
    return [
        result, 
        rDataParam.x, rDataParam.y, rDataParam.z, rDataParam.Rx, rDataParam.Ry,
        rDataParam.Rz
    ]


def InverseSolution(api, wData1List, wData2List, tool, user):
    """
    转换工具逆解。将笛卡尔坐标转换为关节坐标。
    :param api:python调用动态库获取的对象
    :param wData1List:存储CartesianCoordinate坐标系参数类型的list
    :param wData2List:姿态参数list（六轴机器人），默认为[-1,-1,-1,-1]
    :param tool:工具坐标系索引
    :param user:用户坐标系索引
    :return:通讯返回值结果DobotCommunicate和JointCoordinate机械臂运动关节参数类型
    """
    wData1Param = CartesianCoordinate()
    wData1Param.x = c_float(wData1List[0])
    wData1Param.y = c_float(wData1List[1])
    wData1Param.z = c_float(wData1List[2])
    wData1Param.Rx = c_float(wData1List[3])
    wData1Param.Ry = c_float(wData1List[4])
    wData1Param.Rz = c_float(wData1List[5])
    wData2Param = RDNCoordinate()
    wData2Param.r = c_int(wData2List[0])
    wData2Param.d = c_int(wData1List[1])
    wData2Param.n = c_int(wData2List[2])
    wData2Param.cfg = c_int(wData2List[3])
    rDataParam = JointCoordinate()
    result = c_int(0)
    result = api.InverseSolution(byref(wData1Param), byref(wData2Param), tool, user,
                                byref(rDataParam))
    return [result, 
        rDataParam[0],
        rDataParam[1],
        rDataParam[2],
        rDataParam[3],
        rDataParam[4],
        rDataParam[5]
    ]


"""本体状态设置"""


def GetExchange(api):
    """
    获取控制器数据
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和Exchange实时数据交互类型
    """
    result = c_int(0)
    exchangeObj = Exchange()
    result = api.GetExchange(byref(exchangeObj))
    jointList = [ 
        exchangeObj.joint.j[0],
        exchangeObj.joint.j[1],
        exchangeObj.joint.j[2],
        exchangeObj.joint.j[3],
        exchangeObj.joint.j[4],
        exchangeObj.joint.j[5],
    ]
    coordinateList = [
        exchangeObj.coordinate.x,
        exchangeObj.coordinate.y,
        exchangeObj.coordinate.z,
        exchangeObj.coordinate.Rx,
        exchangeObj.coordinate.Ry,
        exchangeObj.coordinate.Rz,
    ]
    alarmsIdTypeMap = dict()
    for i in range(0, AlarmsTypeMax):
        for j in range(0, AlarmsCountMax):
            if exchangeObj.alarms.alarmsID[i][j] != 0 :
                alarmsIdTypeMap[exchangeObj.alarms.alarmsID[i][j]] = i;
    rdnList =  [
            exchangeObj.rdn.r, 
            exchangeObj.rdn.d, 
            exchangeObj.rdn.n, 
            exchangeObj.rdn.cfg
    ]
    DOMap = dict()
    for i in range(0, 64):
        DOMap[i+1] = exchangeObj.ioOut.value[i]
    DIMap = dict()
    for i in range(0, 64):
        DIMap[i+1] = exchangeObj.ioIn.value[i]
   
    return [
        result,
        exchangeObj.controlMode,
        exchangeObj.powerState,
        exchangeObj.isCollision,
        exchangeObj.jogMode,
        exchangeObj.isAuto,
        exchangeObj.toolCoordinate,
        exchangeObj.userCoordinate,
        jointList,
        coordinateList,
        alarmsIdTypeMap,
        rdnList,
        exchangeObj.arm,
        DOMap,
        DIMap,
    ]    


def SetControlMode(api, controlMode):
    """
    设置机械臂使能
    :param api:python调用动态库获取的对象
    :param controlMode:ControlMode 机械臂使能类型，Disable为下使能，Enable为上使能，Drag为拖拽模式
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    controlModePara = c_int(controlMode)
    result = api.SetControlMode(byref(controlModePara))
    return result


def GetControlMode(api):
    """
    获取机械臂使能
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和ControlMode机械臂使能类型
    """
    result = c_int(0)
    controlMode = c_int(0)
    result = api.GetControlMode(byref(controlMode))
    return [result, controlMode.value]


def SetPowerMode(api, isOn):
    """
    设置机械臂电源状态
    :param api:python调用动态库获取的对象
    :param isOn:上电为true；下电为false
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    isOnPara = c_bool(isOn)
    result = api.SetPowerMode(isOnPara)
    return result


def GetPowerMode(api):
    """
    获取机械臂电源状态（六轴机器人）
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和isOn: 上电为true；下电为false
    """
    result = c_int(0)
    isOn = c_bool(False)
    result = api.GetPowerMode(byref(isOn))
    return [result, isOn.value]


def GetAlarmsParameter(api, id, type, isEn):
    """
    获取报警信息。返回报警id对应的信息，包括报警层级、报警描述、报警原因、报警解决方法
    :param api:python调用动态库获取的对象
    :param id:报警id
    :param type:报警类型，控制器报警为0；伺服关节报警为1~6
    :param isEn:英文为true，中文为false
    :return:通讯返回值结果DobotCommunicate和AlarmsPara报警信息参数类型
    """
    result = c_int(0)
    alarmsParam = AlarmsPara()
    result = api.GetAlarmsParameter(c_int(id), c_int(type), byref(alarmsParam), c_bool(isEn))
    return [
        result,
        alarmsParam.id,
        alarmsParam.level,
        alarmsParam.description,
        alarmsParam.cause,
        alarmsParam.solution
    ]


def ClearAlarms(api):
    """
    清除报警信息
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    result = api.ClearAlarms()
    return result


def EmergencyStop(api):
    """
    急停
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    result = api.EmergencyStop()
    return result


def SetCollisionMode(api, isOn, level):
    """
    设置碰撞开关和等级
    :param api:python调用动态库获取的对象
    :param isOn:碰撞检测开启为true; 碰撞检测关闭为false
    :param level:碰撞等级为1~5
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    isOnPara = c_bool(isOn)
    levelPara = c_int(level)
    result = api.SetCollisionMode(isOnPara, levelPara)
    return result


def GetCollisionMode(api):
    """
    获取碰撞开关和等级
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate
            isOn: 碰撞检测开启为true; 碰撞检测关闭为false
            level: 碰撞等级为1~5
    """
    result = c_int(0)
    isOn = c_bool(False)
    level = c_int(0)
    result = api.GetCollisionMode(byref(isOn), byref(level))
    return [result, isOn.value, level.value]


def ResetCollision(api):
    """
    复位碰撞状态
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    result = api.ResetCollision()
    return result


def GetCartesianCoordinate(api):
    """
    获取笛卡尔坐标
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和CartesianCoordinate机械臂运动坐标系参数类型
    """
    result = c_int(0)
    cartesianCoordinateParam = CartesianCoordinate()
    result = api.GetCartesianCoordinate(byref(cartesianCoordinateParam))
    return [
        result,
        cartesianCoordinateParam.x, cartesianCoordinateParam.y,
        cartesianCoordinateParam.z, cartesianCoordinateParam.Rx,
        cartesianCoordinateParam.Ry, cartesianCoordinateParam.Rz
    ]


def GetJointCoordinate(api):
    """
    获取关节坐标
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和JointCoordinate机械臂运动关节参数类型
    """
    result = c_int(0)
    jointCoordinateParam = JointCoordinate()
    result = api.GetJointCoordinate(byref(jointCoordinateParam))
    return [result, jointCoordinateParam.j]


def GetRdnCoordinate(api):
    """
    获取机器人姿态(六轴机器人)
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和RDNCoordinate机械臂姿态（六轴机器人）参数类型
    """
    result = c_int(0)
    rdnCoordinateParam = RDNCoordinate()
    result = api.GetRdnCoordinate(byref(rdnCoordinateParam))
    return [
        result,
        rdnCoordinateParam.r, rdnCoordinateParam.d, rdnCoordinateParam.n,
        rdnCoordinateParam.cfg
    ]


def GetArmOrientation(api):
    """
    获取机器人姿态(四轴机器人)
    :param api: python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和armOrientation：0为左手方向，1为右手方向
    """
    result = c_int(0)
    armOrientation = c_int(0)
    result = api.GetArmOrientation(byref(armOrientation))
    return [result, armOrientation.value]


def SetTeachTrajectory(api, isOn):
    """
    设置拖动示教状态
    :param api:python调用动态库获取的对象
    :param isOn:启动拖动示教为true; 停止拖动示教为false
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    isOnPara = c_bool(isOn)
    result = api.SetTeachTrajectory(isOnPara)
    return result


def SetPayLoad(api, payLoadList):
    """
    设置负载参数
    :param api:python调用动态库获取的对象
    :param payLoadList:存储PayLoad机械臂负载参数类型的list
    :return:通讯返回值结果DobotCommunicate
    """
    payLoadParam = PayLoad()
    payLoadParam.inertiaX = c_float(payLoadList[0])
    payLoadParam.inertiaY = c_float(payLoadList[1])
    payLoadParam.inertiaZ = c_float(payLoadList[2])
    payLoadParam.toolLength = c_float(payLoadList[3])
    payLoadParam.loadValue = c_float(payLoadList[4])
    result = c_int(0)
    result = api.SetPayLoad(byref(payLoadParam))
    return result


def GetPayLoad(api):
    """
    获取负载参数
    :param api: python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和PayLoad机械臂负载参数类型
    """
    result = c_int(0)
    payLoadParam = PayLoad()
    result = api.GetPayLoad(byref(payLoadParam))
    return [
        result,
        payLoadParam.inertiaX, payLoadParam.inertiaY,
        payLoadParam.inertiaZ, payLoadParam.toolLength,
        payLoadParam.loadValue
    ]


"""用户坐标系"""


def SetCoordinateUserIndex(api, index):
    """
    设置用户坐标系索引
    :param api:python调用动态库获取的对象
    :param index:用户坐标系索引
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    indexPara = c_int(index)
    result = api.SetCoordinateUserIndex(indexPara)
    return result


def GetCoordinateUserIndex(api):
    """
    获取用户坐标系当前索引
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和index: 返回用户坐标系的当前索引
    """
    result = c_int(0)
    index = c_int(0)
    result = api.GetCoordinateUserIndex(byref(index))
    return [result, index.value]


def SetCoordinateUserParams(api, x, y, z, Rx, Ry, Rz, index=1):
    """
    设置用户坐标系索引和参数
    :param api:python调用动态库获取的对象
    :param x:对应坐标系参数x
    :param y:对应坐标系参数y
    :param z:对应坐标系参数z
    :param Rx:对应坐标系参数Rx
    :param Ry:对应坐标系参数Ry
    :param Rz:对应坐标系参数Rz
    :param index:用户坐标系索引，默认为1
    :return:通讯返回值结果DobotCommunicate
    """
    wDataParam = CartesianCoordinate()
    wDataParam.x = c_float(x)
    wDataParam.y = c_float(y)
    wDataParam.z = c_float(z)
    wDataParam.Rx = c_float(Rx)
    wDataParam.Ry = c_float(Ry)
    wDataParam.Rz = c_float(Rz)
    result = c_int(0)
    result = api.SetCoordinateUserParams(byref(wDataParam), c_int(index))
    return result


def GetCoordinateUserParams(api, index = 1):
    """
    根据索引获取用户坐标系参数
    :param api:python调用动态库获取的对象
    :param index:获取的用户坐标系索引，默认为1
    :return:通讯返回值结果DobotCommunicate和 CartesianCoordinate对应参数
    """
    result = c_int(0)
    rDataParam = CartesianCoordinate()
    result = api.GetCoordinateUserParams(byref(rDataParam), index)
    return [
        result,
        rDataParam.x, rDataParam.y, rDataParam.z, rDataParam.Rx, rDataParam.Ry,
        rDataParam.Rz
    ]


def CalibrateCoordinateUser(api, wDataList, index = 1):
    """
    用户坐标系标定
    :param api:python调用动态库获取的对象
    :param wDataList:CartesianCoordinate 类型list，长度为3，即标定需要输入的3个点的笛卡尔坐标
    :param index:设置用户坐标系索引，默认为1
    :return:通讯返回值结果DobotCommunicate和 CartesianCoordinate对应参数，即标定后的笛卡尔坐标系
    """
    wDataParam1 = CartesianCoordinate()
    wDataParam1.x = c_float(wDataList[0][0])
    wDataParam1.y = c_float(wDataList[0][1])
    wDataParam1.z = c_float(wDataList[0][2])
    wDataParam1.Rx = c_float(wDataList[0][3])
    wDataParam1.Ry = c_float(wDataList[0][4])
    wDataParam1.Rz = c_float(wDataList[0][5])
    
    wDataParam2 = CartesianCoordinate()
    wDataParam2.x = c_float(wDataList[1][0])
    wDataParam2.y = c_float(wDataList[1][1])
    wDataParam2.z = c_float(wDataList[1][2])
    wDataParam2.Rx = c_float(wDataList[1][3])
    wDataParam2.Ry = c_float(wDataList[1][4])
    wDataParam2.Rz = c_float(wDataList[1][5])
    
    wDataParam3 = CartesianCoordinate()
    wDataParam3.x = c_float(wDataList[2][0])
    wDataParam3.y = c_float(wDataList[2][1])
    wDataParam3.z = c_float(wDataList[2][2])
    wDataParam3.Rx = c_float(wDataList[2][3])
    wDataParam3.Ry = c_float(wDataList[2][4])
    wDataParam3.Rz = c_float(wDataList[2][5])
    rDataParam = CartesianCoordinate()
    result = c_int(0)
    result = api.CalibrateCoordinateUserToPy(wDataParam1, wDataParam2, wDataParam3, byref(rDataParam), c_int(index))
    return [
        result,
        rDataParam.x, rDataParam.y, rDataParam.z, rDataParam.Rx, rDataParam.Ry,
        rDataParam.Rz
    ]


"""工具坐标系"""


def SetCoordinateToolIndex(api, index):
    """
    设置工具坐标系索引
    :param api: python调用动态库获取的对象
    :param index:工具坐标系索引
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    indexPara = c_int(index)
    result = api.SetCoordinateToolIndex(indexPara)
    return result


def GetCoordinateToolIndex(api):
    """
    获取工具坐标系当前索引
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和index: 返回工具坐标系的当前索引
    """
    result = c_int(0)
    index = c_int(0)
    result = api.GetCoordinateToolIndex(byref(index))
    return [result, index.value]


def SetCoordinateToolParams(api, x, y, z, Rx, Ry, Rz, index = 1):
    """
    设置工具坐标系索引和参数
    :param api:python调用动态库获取的对象
    :param x:对应坐标系参数x
    :param y:对应坐标系参数y
    :param z:对应坐标系参数z
    :param Rx:对应坐标系参数Rx
    :param Ry:对应坐标系参数Ry
    :param Rz:对应坐标系参数Rz
    :param index:工具坐标系索引，默认为1
    :return:通讯返回值结果DobotCommunicate
    """
    wDataParam = CartesianCoordinate()
    wDataParam.x = c_float(x)
    wDataParam.y = c_float(y)
    wDataParam.z = c_float(z)
    wDataParam.Rx = c_float(Rx)
    wDataParam.Ry = c_float(Ry)
    wDataParam.Rz = c_float(Rz)
    result = c_int(0)
    result = api.SetCoordinateToolParams(byref(wDataParam), c_int(index))
    return result


def GetCoordinateToolParams(api, index = 1):
    """
    根据索引获取工具坐标系参数
    :param api:python调用动态库获取的对象
    :param index:获取的工具坐标系索引，默认为1
    :return:通讯返回值结果DobotCommunicate和 CartesianCoordinate对应参数
    """
    result = c_int(0)
    rDataParam = CartesianCoordinate()
    result = api.GetCoordinateToolParams(byref(rDataParam), index)
    return [
        result,
        rDataParam.x, rDataParam.y, rDataParam.z, rDataParam.Rx, rDataParam.Ry,
        rDataParam.Rz
    ]


def CalibrateCoordinateToolPosition(api, wDataList, index = 1):
    """
    工具坐标系位置标定
    :param api:python调用动态库获取的对象
    :param wDataList:CartesianCoordinate 类型list，长度为3，即位置标定需要输入的3个点的笛卡尔坐标
    :param index:设置工具坐标系索引，默认为1
    :return:通讯返回值结果DobotCommunicate和 CartesianCoordinate对应参数，即标定后的笛卡尔坐标系
    """
    wDataParam1 = CartesianCoordinate()
    wDataParam1.x = c_float(wDataList[0][0])
    wDataParam1.y = c_float(wDataList[0][1])
    wDataParam1.z = c_float(wDataList[0][2])
    wDataParam1.Rx = c_float(wDataList[0][3])
    wDataParam1.Ry = c_float(wDataList[0][4])
    wDataParam1.Rz = c_float(wDataList[0][5])
    
    wDataParam2 = CartesianCoordinate()
    wDataParam2.x = c_float(wDataList[1][0])
    wDataParam2.y = c_float(wDataList[1][1])
    wDataParam2.z = c_float(wDataList[1][2])
    wDataParam2.Rx = c_float(wDataList[1][3])
    wDataParam2.Ry = c_float(wDataList[1][4])
    wDataParam2.Rz = c_float(wDataList[1][5])
    
    wDataParam3 = CartesianCoordinate()
    wDataParam3.x = c_float(wDataList[2][0])
    wDataParam3.y = c_float(wDataList[2][1])
    wDataParam3.z = c_float(wDataList[2][2])
    wDataParam3.Rx = c_float(wDataList[2][3])
    wDataParam3.Ry = c_float(wDataList[2][4])
    wDataParam3.Rz = c_float(wDataList[2][5])
    rDataParam = CartesianCoordinate()
    result = c_int(0)
    result = api.CalibrateCoordinateToolPositionToPy(wDataParam1, wDataParam2, wDataParam3, byref(rDataParam), c_int(index))
    return [
        result,
        rDataParam.x, rDataParam.y, rDataParam.z, rDataParam.Rx, rDataParam.Ry,
        rDataParam.Rz
    ]


def CalibrateCoordinateToolPose(api, wDataList, index = 1):
    """
    工具坐标系姿态标定
    :param api:python调用动态库获取的对象
    :param wDataList:CartesianCoordinate 类型list，长度为3，即姿态标定需要输入的3个点的笛卡尔坐标
    :param index:设置工具坐标系索引，默认为1
    :return:通讯返回值结果DobotCommunicate和 CartesianCoordinate对应参数，即标定后的笛卡尔坐标系
    """
    wDataParam1 = CartesianCoordinate()
    wDataParam1.x = c_float(wDataList[0][0])
    wDataParam1.y = c_float(wDataList[0][1])
    wDataParam1.z = c_float(wDataList[0][2])
    wDataParam1.Rx = c_float(wDataList[0][3])
    wDataParam1.Ry = c_float(wDataList[0][4])
    wDataParam1.Rz = c_float(wDataList[0][5])
    
    wDataParam2 = CartesianCoordinate()
    wDataParam2.x = c_float(wDataList[1][0])
    wDataParam2.y = c_float(wDataList[1][1])
    wDataParam2.z = c_float(wDataList[1][2])
    wDataParam2.Rx = c_float(wDataList[1][3])
    wDataParam2.Ry = c_float(wDataList[1][4])
    wDataParam2.Rz = c_float(wDataList[1][5])
    
    wDataParam3 = CartesianCoordinate()
    wDataParam3.x = c_float(wDataList[2][0])
    wDataParam3.y = c_float(wDataList[2][1])
    wDataParam3.z = c_float(wDataList[2][2])
    wDataParam3.Rx = c_float(wDataList[2][3])
    wDataParam3.Ry = c_float(wDataList[2][4])
    wDataParam3.Rz = c_float(wDataList[2][5])
    rDataParam = CartesianCoordinate()
    result = c_int(0)
    result = api.CalibrateCoordinateToolPoseToPy(wDataParam1, wDataParam2, wDataParam3, byref(rDataParam), c_int(index))
    return [
        result,
        rDataParam.x, rDataParam.y, rDataParam.z, rDataParam.Rx, rDataParam.Ry,
        rDataParam.Rz
    ]


"""传感器接口"""


def SetForceSensor(api, isOn):
    """
    设置力矩传感器开关状态
    :param api:python调用动态库获取的对象
    :param isOn:开启力矩传感器为true; 关闭力矩传感器为false
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    isOnPara = c_bool(isOn)
    result = api.SetForceSensor(isOnPara)
    return  result


def GetForceSensor(api):
    """
    获取力矩传感器开关状态
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和isOn: 开启力矩传感器为true; 关闭力矩传感器为false
    """
    result = c_int(0)
    isOn = c_bool(False)
    result = api.GetForceSensor(byref(isOn))
    return [result, isOn.value]


def GetForceOrgParams(api):
    """
    获取力矩传感器原始参数
    :param api: python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和ForceOrgValue力矩传感器参数类型
    """
    result = c_int(0)
    rDataParam = ForceOrgValue()
    result = api.GetForceOrgParams(byref(rDataParam))
    return [result, 
        rDataParam.orgValue[0],
        rDataParam.orgValue[1],
        rDataParam.orgValue[2],
        rDataParam.orgValue[3],
        rDataParam.orgValue[4],
        rDataParam.orgValue[5]
    ]


def SetForceHome(api):
    """
    力矩传感器复位
    :param api: python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    result = api.SetForceHome()
    return result


def SetTorqueParams(api, value):
    """
    设置力矩传感器扭力值
    :param api: python调用动态库获取的对象
    :param value:扭力值
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    valuePara = c_float(value)
    result = api.SetTorqueParams(valuePara)
    return result


def GetTorqueParams(api):
    """
    获取力矩传感器扭力值
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和value:扭力值
    """
    result = c_int(0)
    value = c_float(0)
    result = api.GetTorqueParams(byref(value))
    return [result, value.value]


"""控制器模拟IO接口""" 


def GetAI(api):
    """
    获取模拟信号输入
    :param api: python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和AI控制器模拟量输入参数类型
    """
    result = c_int(0)
    AIParam = AI()
    AIParam.mode1 = c_int(0)
    AIParam.mode2 = c_int(0)
    result = api.GetAI(byref(AIParam))
    return [
        result,
        AIParam.mode1,
        AIParam.mode2
    ]


def SetAO(api, AOList):
    """
    设置模拟信号输出
    :param api:python调用动态库获取的对象
    :param AOList:存储AO模拟输出信号参数类型的list
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    AOParam = AO()
    AOParam.mode1 = AOList[0]
    AOParam.value1 = AOList[1]
    AOParam.mode2 = AOList[2]
    AOParam.value2 = AOList[3]         
    result = api.SetAO(byref(AOParam))
    return result


def GetAO(api):
    """
    获取模拟信号输出
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和AO模拟输出信号参数类型
    """
    result = c_int(0)
    AOParam = AO()
    AOParam.mode1 = c_int(0)
    AOParam.value1 = c_int(0)
    AOParam.mode2 = c_int(0)
    AOParam.value2 = c_int(0)
    result = api.GetAO(byref(AOParam))
    return [
        result,
        AOParam.mode1,
        AOParam.value1,
        AOParam.mode2,
        AOParam.value2
    ]


"""控制器数字IO接口""" 


def SetDO(api, DOMap):
    """
    设置数字信号输出
    :param api:python调用动态库获取的对象
    :param DOMap:存储IO信号参数类型的dict
    :return:通讯返回值结果DobotCommunicate
    """
    result = c_int(0)
    DOParam = IO()
    DOParam.enable = True
    for i in range(0, 64):
        DOParam.value[i] = DOMap[i+1]               
    result = api.SetDO(byref(DOParam))
    return result


def GetDO(api):
    """
    获取数字信号输出
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和IO信号参数类型
    """
    result = c_int(0)
    DOParam = IO()
    result = api.GetDO(byref(DOParam))
    DOMap = dict()
    for i in range(0, 64):
        DOMap[i+1] = DOParam.value[i]
    return [
        result,
        DOMap
    ]


def GetDI(api):
    """
    获取数字信号输入
    :param api:python调用动态库获取的对象
    :return:通讯返回值结果DobotCommunicate和IO信号参数类型
    """
    result = c_int(0)
    DIParam = IO()
    result = api.GetDI(byref(DIParam))
    DIMap = dict()
    for i in range(0, 64):
        DIMap[i+1] = DIParam.value[i]
    return [
        result,
        DIMap
    ]


