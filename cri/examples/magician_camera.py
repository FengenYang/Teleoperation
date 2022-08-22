import time
import multiprocessing as mp
import numpy as np
import asyncio
import websockets
import cv2
import base64

frame=None

def websocket_process():
    async def main_logic(websocket,path):
        print("link")
        await recv_msg(websocket)

    start_server=websockets.serve(main_logic,'10.251.70.4',8889)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


async def recv_msg(websocket):
    recv_text=await websocket.recv()
    recv_text=recv_text.decode()
    if recv_text=='begin':
        i=0
        while True:
            _,frame=cap.read()
            _,encode_data=cv2.imencode('.jpg',frame,[int(cv2.IMWRITE_JPEG_QUALITY),80])
            
            frame=np.array(encode_data).tobytes()
            
            encode_str=base64.b64encode(frame).decode()
            if(i==0):
                with open('data.txt','w') as f:
                    f.write(str(encode_data))
                i+=1

                try:
                    await websocket.send(encode_str)
                    time.sleep(0.07)
                except Exception as e:
                    print(e)
                    return True

def image_put(q,id):
    cap=cv2.VideoCapture(id)
    cap.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
    cap.set(3,1280)
    cap.set(4,720)
    while True:
        ret,frame=cap.read()
        if ret:
            frame=cv2.resize(frame,None,fx=0.7,fy=0.7)
            q.put(frame)
            q.get() if q.qsize()>1 else time.sleep(0.01)

def image_get(q,img_dict):
    while True:
        frame=q.get()
        if isinstance(frame,np.ndarray):
            img_dict['img']=frame


def run_single_camera(id):
    mp.set_start_method(method='spawn')
    queue=mp.Queue(maxsize=3)
    m=mp.Manager()
    img_dict=m.dict()
    Processes=[mp.Process(target=image_put,args=(queue,id)),
             mp.Process(target=image_get,args=(queue,img_dict)),
             mp.Process(target=websocket_process,args=(img_dict,))]
    
    [process.start() for process in Processes]
    [process.join() for process in Processes]

def run():
    run_single_camera(3)

if __name__=='__main__':
    #run()
    
    cap=cv2.VideoCapture(3,cv2.CAP_DSHOW)
    cap.set(3,1280)
    cap.set(4,720)
    print("camera is ready")
    websocket_process()
    
    '''
    while True:
        ret,frame=cap.read()
        frame=cv2.flip(frame,1)
        cv2.imshow('frame',frame)
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()'''