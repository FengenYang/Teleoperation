import os
import numpy as np
import cri.dobot.magician.DobotDllType as dobot

np.set_printoptions(precision=2, suppress=True)

def _block(command):
    dobot.SetQueuedCmdStartExec(api)
    retval = command    
    while dobot.GetQueuedCmdCurrentIndex(api)[0] < retval: dobot.dSleep(1)
    dobot.SetQueuedCmdStopExec(api)

# Path to dependent dlls
dll_path = r'C:\Users\nl13426\Repositories\cri\cri\dobot\magician'
# os.environ["PATH"] += os.pathsep + os.pathsep.join([dll_path])

# Load Dll and get the CDLL object
os.chdir(dll_path)
api = dobot.load()

# Connect Dobot
resultConnect = dobot.ConnectDobot(api, "", 115200)[0]
print("\nConnected (0 for NoError; 1 for Error; 2 for Connected)", resultConnect)

print("\nDevice SN: ", dobot.GetDeviceSN(api)[0])
print("Device name: ", dobot.GetDeviceName(api)[0])

_block(dobot.SetPTPCoordinateParams(api, *[100, 200, 100, 200])[0]) #"[xyzVel, xyzAcc, rVel, rAcc]
print("[xyzVel, rVel, xyzAcc, rAcc]:", dobot.GetPTPCoordinateParams(api))

if resultConnect == 0:

    # Home
    dobot.SetHOMECmd(api, temp = 0)
    _block(dobot.SetPTPCmd(api,dobot.PTPMode.PTPMOVLXYZMode, *[200, 0, 100, 0])[0])
    print('joints:', np.array(dobot.GetPose(api)[4:]))

    # MOVL (MovJ) interface
    print('\ntest MOVL')
    for z in [-50, 0]:
        _block(dobot.SetPTPCmd(api, dobot.PTPMode.PTPMOVLXYZMode, *[200, 0, 100 + z, 0])[0])
        print('pose:', np.array(dobot.GetPose(api)[:4]))
        print('joints:', np.array(dobot.GetPose(api)[4:]))

    # MOVLANGLE (MOVJANGLE) interface
    print('\ntest MOVLANGLE')
    for r in [15, -15]:
        _block(dobot.SetPTPCmd(api, dobot.PTPMode.PTPMOVLANGLEMode, *[r, -1.05, 13.77, r])[0])
        print('pose:', np.array(dobot.GetPose(api)[:4]))
        print('joints:', np.array(dobot.GetPose(api)[4:]))

    # MOVLXYZINC (MOVJZYZINC) interface 
    print('\ntest MOVLXYZINC')
    for z in [-50, 50]:
        _block(dobot.SetPTPCmd(api, dobot.PTPMode.PTPMOVLXYZINCMode, *[0, 0, z, -z])[0])
        print('pose:', np.array(dobot.GetPose(api)[:4]))
        print('joints:', np.array(dobot.GetPose(api)[4:]))

    # # Arc Command interface 
    # print('\ntest ARCCmd')
    # _block(dobot.SetARCParams(api, *[100, 100, 100, 100])[0])
    # print('Arc parameters', dobot.GetARCParams(api))
    # _block(dobot.SetARCCommonParams(api, *[1, 1])[0])
    # print('Arc common parameters', dobot.GetARCCommonParams(api))
    # _block(dobot.SetARCCmd(api, [200, 0, 100, 0], [200, 100, 100, 50])[0])
    # print('pose:', np.array(dobot.GetPose(api)[:4]))
    # print('joints:', np.array(dobot.GetPose(api)[4:]))

    # Home
    _block(dobot.SetPTPCmd(api,dobot.PTPMode.PTPMOVLXYZMode, *[200, 0, 100, 0])[0])

#Disconnect Dobot
dobot.ClearAllAlarmsState(api)
dobot.DisconnectDobot(api)
