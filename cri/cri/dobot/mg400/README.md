# 先读我

## 1. 运行 Demo 需以下步骤
1. 电脑可用网线连接控制器的网口，然后设置固定 IP，与控制器 IP 在同一网段下。也可无线连接控制器。

   - 四轴机器人（如MG400等）     有线连接时连接LAN1：ip为192.168.1.6 , 有线连接时连接LAN2：ip为192.168.2.6,  无线连接：ip为192.168.9.1
   - 六轴机器人（如CR系列等）    有线连接：ip为192.168.5.1 , 无线连接：ip为192.168.1.6
  
2. 尝试 ping 通控制器 IP，确保在同一网段下。

## 2. 文件说明
1. demo.py: 程序运行入口。  
   
2. dobot_api.py：根据机器人TCP/IP远程控制方案（https://github.com/Dobot-Arm/TCP-IP-Protocol）自行修改。

## 3. 运行Demo
方法一: 需要检测搜索到动态库，需在**VsCode**中打开整个目录，再直接运行 demo.py。  

方法二: 需要检测搜索到动态库，需在**PyCharm**中打开整个目录，再直接运行 demo.py。

## 4. 测试环境
- language: Python 3.7 64-bit
- os: Windows 10 64-bit

## 5.控制器版本
可以使用TCP/IP协议的控制器版本如下：  

- MG400： 1.5.4.0 及以上
- CR： 3.5.1.9 及以上


---


# Readme

## 1. The following steps are required to run Demo
1. The computer can be connected to the network port of the controller with a network cable, and then set a fixed IP, which is in the same network segment as the controller IP. The controller can also be connected wirelessly.

    - Four-axis robots (such as MG400, etc.) When wired connection is connected to LAN1: ip is 192.168.1.6, when wired connection is connected to LAN2: ip is 192.168.2.6, wireless connection: ip is 192.168.9.1 .
    - Six-axis robot (such as CR series, etc.) Wired connection: ip is 192.168.5.1 ,Wireless connection: ip is 192.168.1.6 .

2. Try to ping the controller IP to make sure it is in the same network segment.


## 2. File description
1. demo.py: The entry point of the program.  
   
2. dobot_api.py: According to the robot TCP/IP remote control scheme (https://github.com/Dobot-Arm/TCP-IP-Protocol), modify it by yourself.

## 3. Run Demo
Method 1: If you need to detect and search the dynamic library, you need to open the entire directory in **VsCode**, and then run demo.py directly.  

Method 2: To detect and search the dynamic library, you need to open the entire directory in **PyCharm**, and then run demo.py directly.

## 4. Test environment
- language: Python 3.7 64-bit
- os: Windows 10 64-bit

## 5. Controller version
The controller versions that can use the TCP/IP protocol are as follows:

- MG400: 1.5.4.0 and above
- CR: 3.5.1.9 and above