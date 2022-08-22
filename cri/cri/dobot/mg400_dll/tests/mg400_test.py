import cri.dobot.mg400.DobotSDK as dobot
import os
import numpy as np
np.set_printoptions(precision=2, suppress=True)

#Path to dependent dlls
dll_path = r'C:\Users\nl13426\Repositories\cri\cri\dobot\mg400'
# os.environ["PATH"] += os.pathsep + os.pathsep.join([dll_path]) # don't need in vscode

#Load Dll and get the CDLL object
os.chdir(dll_path) # needed in vscode
api = dobot.load()

#Connect Dobot
resultConnect = dobot.ConnectDobot(api, "192.168.1.6")
dobot.SetControlMode(api, 1) 
dobot.dSleep(1000)

print("\nConnected (0 for NoError; 1 for Error)", resultConnect)
print('Control mode:', dobot.GetControlMode(api)[1]) # doesn't work

print("\nCurrent Version is", dobot.GetDobotVersion(api)[1:])
print("Tool index:", dobot.GetCoordinateToolIndex(api)[1])
print("User index:", dobot.GetCoordinateUserIndex(api)[1])
print("Payload", dobot.GetPayLoad(api)) # Do not try to change payload!!!

dobot.SetRapidRate(api, 100)
print("Current speed percentage is", dobot.GetRapidRate(api)[1])

if resultConnect == 0:

    # Home
    dobot.MovL(api, [300, 0, 0, 0, 0, 0], isBlock = True)
    print('joint', np.array(dobot.GetJointCoordinate(api)[1]))
  
    # MovL (MovJ) interface
    print('\ntest MovL')
    for z in [-100, 100]:
        result = dobot.MovL(api, [300, 0, 0 + z, z, 0, 0], isBlock = True)
        print(result)
        print('pose', np.array(dobot.GetCartesianCoordinate(api)[1:]))
        print('joint', np.array(dobot.GetJointCoordinate(api)[1]))

    # JointMovJ interface - seems broken
    print('\ntest JointMovJ')
    for r in [15, -15]:
        result = dobot.JointMovJ(api, [r, 19, 40, r, 0, 0], isBlock = True)
        print(result)
        print('pose', np.array(dobot.GetCartesianCoordinate(api)[1:]))
        print('joint', np.array(dobot.GetJointCoordinate(api)[1]))

    # RelMovL (RelMovJ) interface - seems broken
    print('\ntest RelMovJ')
    for z in [100, -200]:
        result = dobot.RelMovJ(api, *[0, 0, z], isBlock = True)
        print(result)
        print('pose', np.array(dobot.GetCartesianCoordinate(api)[1:]))
        print('joint', np.array(dobot.GetJointCoordinate(api)[1]))

    # Home
    dobot.MovL(api, [300, 0, 0, 0, 0, 0], isBlock = True)

#Disconnect Dobot
print('\nDisconnecting')
dobot.dSleep(5000)
dobot.ClearAlarms(api)
dobot.SetControlMode(api, 0) 
dobot.DisconnectDobot(api)
