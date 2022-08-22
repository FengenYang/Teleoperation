"""Simple test script for SyncRobot and AsyncRobot class using Magician Controller.
Note: Tested in VSCode & spyder
"""

import numpy as np
import pandas as pd

from cri.robot import SyncRobot, AsyncRobot
from cri.controller import MagicianController as Controller

#===================WebSocket=====================
import asyncio
from encodings import utf_8
from hashlib import new
import websockets
import json
import time

import datetime
import matplotlib.pyplot as plt

serverTime=[]
serverX=[]
serverY=[]
serverZ=[]
clientTime=[]
clientX=[]
clientY=[]
clientZ=[]

async def recv_msg(websocket):
    #====init the real robot with the angles from cri====
    #saveJoint=(robot.joint_angles[0],robot.joint_angles[1],90+robot.joint_angles[2],robot.joint_angles[3])
    #initStr='{"eeX":0.0,"eeY":0.0,"eeZ":0.0,"angles":['+ (",".join(str(i) for i in robot.joint_angles)) +'],"connect":true}'
    #print(initStr)
    #initStr=json.loads(initStr)
    #initStr=json.dumps(initStr,ensure_ascii=False)
    #await websocket.send(initStr)
    #===================================================

    while True:
        async for message in websocket:
            if isinstance(message,bytes):
                message=message.decode()
                data=json.loads(message)
                print("recdata")
                print(data)
                
                if data['connect']==False:
                    print("Client disconnect")
                    #draw the server data plot
                    '''
                    plt.figure('Dobot positionX')
                    plt.plot(serverTime,serverX,'bo-')
                    plt.plot(clientTime,clientX,'ro-')
                    plt.xlabel('Time')
                    plt.ylabel('PositionX')
                    plt.gcf().autofmt_xdate()
                    plt.savefig('./XSave.jpg')

                    plt.figure('Dobot positionY')
                    plt.plot(serverTime,serverY,'bo-')
                    plt.plot(clientTime,clientY,'ro-')
                    plt.xlabel('Time')
                    plt.ylabel('PositionY')
                    plt.gcf().autofmt_xdate()
                    plt.savefig('./YSave.jpg')

                    plt.figure('Dobot positionZ')
                    plt.plot(serverTime,serverZ,'bo-')
                    plt.plot(clientTime,clientZ,'ro-')
                    plt.xlabel('Time')
                    plt.ylabel('PositionZ')     
                    plt.gcf().autofmt_xdate()
                    plt.savefig('./ZSave.jpg')
                    '''

                    #write the data into a csv
                    dataframe=pd.DataFrame({'serverTime':serverTime,'serverX':serverX,'serverY':serverY,'serverZ':serverZ,
                                            'clientTime':clientTime,'clientX':clientX,'clientY':clientY,'clientZ':clientZ})
                    dataframe.to_csv("datasave.csv",index=False,sep=',')                        

                    await websocket.close()
                    break
                
                if(not data['move']):
                    if(not data['pump']):
                        robot.close_Pump()
                    elif(data['gripper']):
                        robot.control_gripper(1)                  
                    elif(not data['gripper']):
                        robot.control_gripper(0)
                    continue

                if(data['Mode']==0):
                    #save the position data for results
                    stime=datetime.datetime.now().strftime ( '%H:%M:%S.%f')
                    robot.move_linear_stop()

                    serverTime.append(stime)
                    serverX.append(robot.pose[0])
                    serverY.append(robot.pose[2])
                    serverZ.append(robot.pose[1])
                    
                    cTime=data['time']
                    clientTime.append(cTime)
                    clientX.append(data['eeX'])
                    clientY.append(data['eeY'])
                    clientZ.append(-data['eeZ'])

                    
                elif(data['Mode']==1):
                    if robot.pose[0]<20:
                        robot.move_linear_forward()
                elif(data['Mode']==2):
                    if robot.pose[0]>-40:
                        robot.move_linear_back()
                elif(data['Mode']==3):
                    if robot.pose[1]>-100:
                        robot.move_linear_left()
                elif(data['Mode']==4):
                    if robot.pose[1]<100:
                        robot.move_linear_right()
                elif(data['Mode']==5):
                    if robot.pose[2]<0:
                        robot.move_linear_up()
                elif(data['Mode']==6):
                    if robot.pose[2]>-130:
                        robot.move_linear_down()
                elif(data['Mode']==10):
                    robot.move_linear((0,0,0,0,0,0)) #Reset the robot
                elif(data['Mode']==99):
                    if(data['eeX']>20):
                        data['eeX']=20
                    elif(data['eeX']<-40):
                        data['eeX']=-40

                    if(data['eeY']>0):
                        data['eeY']=0
                    elif(data['eeY']<-130):
                        data['eeY']=-130
                    
                    if(data['eeZ']>100):
                        data['eeZ']=100
                    elif(data['eeZ']<-100):
                        data['eeZ']=-100

                    print("now move:")
                    print((data['eeX'],-data['eeZ'],data['eeY']))

                    stime=datetime.datetime.now().strftime ( '%H:%M:%S.%f')
                    robot.move_linear((data['eeX'],-data['eeZ'],data['eeY'],0,0,0))
                    serverTime.append(stime)
                    serverX.append(robot.pose[0])
                    serverY.append(robot.pose[2])
                    serverZ.append(robot.pose[1])
                    
                    cTime=data['time']
                    clientTime.append(cTime)
                    clientX.append(data['eeX'])
                    clientY.append(data['eeY'])
                    clientZ.append(-data['eeZ'])

                    #new_data=json.dumps(data,ensure_ascii=False)
                    await websocket.send("finish")
                
                
i=0

async def main_logic(websocket,path):
    print("now it's waiting")
    await recv_msg(websocket)
#=================================================

np.set_printoptions(precision=2, suppress=True)
robot=AsyncRobot(SyncRobot(Controller()))

def main():
    
    base_frame = (0, 0, 0, 0, 0, 0)
    work_frame = (200, 0, 100, 0, 0, 0)  # base frame: x->front, y->left, z->up, rz->anticlockwise

    global robot
    robot.tcp = (0, 0, 0, 0, 0, 0 )
    robot.linear_speed = 100
    robot.angular_speed = 100
    robot.coord_frame = work_frame

    robot.move_linear((0,0,0,0,0,0))
    robot.move_linear_speed(50,50,50)

    #robot.move_linear((-40,100,0,0,0,0))
    #robot.move_linear_forward()
    #time.sleep(1)
    #robot.move_linear_left()
    #time.sleep(1)
    #robot.move_linear_stop()

    #robot.control_gripper(0)
    #robot.close_Pump()

    start_server=websockets.serve(main_logic,'192.168.71.198',8888)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    
    return 0
    
    
    with AsyncRobot(SyncRobot(Controller())) as robot:
        # Set TCP, linear speed,  angular speed and coordinate frame
        robot.tcp = (0, 0, 0, 0, 0, 0 )
        robot.linear_speed = 250
        robot.angular_speed = 250
        robot.coord_frame = work_frame
        print('Linear_speed, Angular_speed:', robot.linear_speed, robot.angular_speed)

        # Display robot info
        print("Robot info: {}".format(robot.info))

        # Display initial joint angles
        print("Initial joint angles: {}".format(np.asarray(robot.joint_angles)))

        # Display initial pose in work frame
        print("Initial pose in work frame: {}".format(robot.pose))
        
        # Move to origin of work frame
        print("Moving to origin of work frame ...")
        robot.move_linear((0, 0, 0, 0, 0, 0))
        
        print("Robot joint angles",robot.joint_angles)
        print("Robot pose: {}".format(robot.pose))

        # Increase and decrease all joint angles
        print("Increasing and decreasing all joint angles ...")
        robot.move_joints(robot.joint_angles + (10,)*4)   
        print("Target joint angles after increase: {}".format(robot.target_joint_angles))
        print("Joint angles after increase: {}".format(robot.joint_angles))
        robot.move_joints(robot.joint_angles - (10,)*4)  
        print("Target joint angles after decrease: {}".format(robot.target_joint_angles))
        print("Joint angles after decrease: {}".format(robot.joint_angles))
        
        # Move backward and forward
        print("Moving backward and forward ...")        
        robot.move_linear((-20, 0, 0, 0, 0, 0))
        robot.move_linear((0, 0, 0, 0, 0, 0))
        
        # Move right and left
        print("Moving right and left ...")  
        robot.move_linear((0, -20, 0, 0, 0, 0))
        robot.move_linear((0, 0, 0, 0, 0, 0))
        
        # Move down and up
        print("Moving down and up ...")  
        robot.move_linear((0, 0, -20, 0, 0, 0))
        robot.move_linear((0, 0, 0, 0, 0, 0))

        # Turn clockwise and anticlockwise around work frame z-axis
        print("Turning clockwise and anticlockwise around work frame z-axis ...")        
        robot.move_linear((0, 0, 0, 0, 0, -20))
        robot.move_linear((0, 0, 0, 0, 0, 0))

        # Move to offset pose then tap down and up in sensor frame
        print("Moving to 20 mm/ 10 deg offset in all pose dimensions ...")         
        robot.move_linear((20, 20, 20, 0, 0, 10))
        print("Target pose after offset move: {}".format(robot.target_pose))
        print("Pose after offset move: {}".format(robot.pose))
        print("Tapping down and up ...")
        robot.coord_frame = base_frame
        robot.coord_frame = robot.target_pose
        robot.move_linear((0, 0, -20, 0, 0, 0))
        robot.move_linear((0, 0, 0, 0, 0, 0))
        robot.coord_frame = work_frame
        print("Moving to origin of work frame ...")
        robot.move_linear((0, 0, 0, 0, 0, 0))
        
        # Pause before commencing asynchronous tests
        print("Repeating test sequence for asynchronous moves ...")

        # # Increase and decrease all joint angles (async)
        # print("Increasing and decreasing all joint angles ...")
        # robot.async_move_joints(robot.joint_angles + (5, 5, 5, 5))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()
        # print("Target joint angles after increase: {}".format(robot.target_joint_angles))
        # print("Joint angles after increase: {}".format(robot.joint_angles))
        # robot.async_move_joints(robot.joint_angles - (5, 5, 5, 5))
        # print("Getting on with something else while command completes ...")      
        # robot.async_result()
        # print("Target joint angles after decrease: {}".format(robot.target_joint_angles))
        # print("Joint angles after decrease: {}".format(robot.joint_angles))

        # Move backward and forward (async)
        print("Moving backward and forward (async) ...")  
        robot.async_move_linear((20, 0, 0, 0, 0, 0))
        print("Getting on with something else while command completes ...")
        robot.async_result()
        robot.async_move_linear((0, 0, 0, 0, 0, 0))
        print("Getting on with something else while command completes ...")      
        robot.async_result()
        
        # # Move right and left
        # print("Moving right and left (async) ...")  
        # robot.async_move_linear((0, 20, 0, 0, 0, 0))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()        
        # robot.async_move_linear((0, 0, 0, 0, 0, 0))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()
        
        # # Move down and up (async)
        # print("Moving down and up (async) ...")  
        # robot.async_move_linear((0, 0, 20, 0, 0, 0))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()
        # robot.async_move_linear((0, 0, 0, 0, 0, 0))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()
        
        # # Turn clockwise and anticlockwise around work frame z-axis (async)
        # print("Turning clockwise and anticlockwise around work frame z-axis (async) ...")   
        # robot.async_move_linear((0, 0, 0, 0, 0, 20))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()
        # robot.async_move_linear((0, 0, 0, 0, 0, 0))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()

        # # Move to offset pose then tap down and up in sensor frame (async)
        # print("Moving to 20 mm/deg offset in all pose dimensions (async) ...") 
        # robot.async_move_linear((20, 20, 20, 20, 20, 20))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()
        # print("Target pose after offset move: {}".format(robot.target_pose))
        # print("Pose after offset move: {}".format(robot.pose))
        # print("Tapping down and up (async) ...")
        # robot.coord_frame = base_frame
        # robot.coord_frame = robot.target_pose
        # robot.async_move_linear((0, 0, 20, 0, 0, 0))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()
        # robot.async_move_linear((0, 0, 0, 0, 0, 0))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()
        # robot.coord_frame = work_frame
        # print("Moving to origin of work frame ...")
        # robot.async_move_linear((0, 0, 0, 0, 0, 0))
        # print("Getting on with something else while command completes ...")
        # robot.async_result()

        print("Final target pose in work frame: {}".format(robot.target_pose))
        print("Final pose in work frame: {}".format(robot.pose))


if __name__ == '__main__':
    main()

