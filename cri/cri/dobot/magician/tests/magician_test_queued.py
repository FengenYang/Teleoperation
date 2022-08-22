# directly tests use of api
# based on dobot test code 'ControlDobot'

from cri.dobot.magician import DobotDllType as dobot
import os

#Path to dependent dlls
dll_path = r'C:\Users\nl13426\Repositories\cri\cri\dobot\magician'
# os.environ["PATH"] += os.pathsep + os.pathsep.join([dll_path])

#Load Dll and get the CDLL object
os.chdir(dll_path)
api = dobot.load()

#Connect Dobot
state = dobot.ConnectDobot(api, "", 115200)[0]
print("Connect status:", state)

if state == 0:
    
    #Clear Command Queued
    dobot.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dobot.SetHOMEParams(api, *[200,]*4, isQueued = 1)
    print('Home Parameters',dobot.GetHOMEParams(api))
    dobot.SetPTPJointParams(api, *[100,]*8, isQueued = 1)
    print('PTP Joint Paramters',dobot.GetPTPJointParams(api))
    dobot.SetPTPCommonParams(api, *[100,]*2, isQueued = 1)
    print('PTP Common Parameters',dobot.GetPTPCommonParams(api))
    
    #Async Home
    # dobot.SetHOMECmd(api, temp = 0, isQueued = 1)

    #Queue Motion Instructions
    for offset in [-50, 50, -50, 50, 0]:
        lastIndex = dobot.SetPTPCmd(api, dobot.PTPMode.PTPMOVJXYZMode, 
                        200 + offset, offset, offset, offset, isQueued = 1)[0]

    #Execute Command Queue
    dobot.SetQueuedCmdStartExec(api)
    while lastIndex > dobot.GetQueuedCmdCurrentIndex(api)[0]:
        dobot.dSleep(100)
    dobot.SetQueuedCmdStopExec(api)

#Disconnect Dobot
dobot.DisconnectDobot(api)
