using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using UnityEngine.UI;

public class WebSocket : MonoBehaviour
{
    ClientWebSocket ws;
    CancellationToken ct;
    string rec_str;
    GameObject robot = null;
    ArticulationBody[] articulationChain =null;

    public bool moveFinish = true;
    // Start is called before the first frame update
    void Start()
    {
    }

    public void Link() {
        moveFinish = true;
        robot = GameObject.FindGameObjectWithTag("robot");
        articulationChain = robot.GetComponentsInChildren<ArticulationBody>();
        Websocket();
    }

    float yDis = 0;
    public String ipadd="172.23.22.144";
    public async void Websocket() {
        /*GameObject finalJoint = GameObject.Find("EndEffector");
        GameObject gripper = GameObject.Find("finalPoint");
        yDis = finalJoint.transform.position.y - gripper.transform.position.y;*/

        try
        {
            ws = new ClientWebSocket();
            ct = new CancellationToken();

            String urlstr = "ws://" + ipadd + ":8888";
            Debug.Log(urlstr);
            Uri url = new Uri(urlstr);
            await ws.ConnectAsync(url, ct);
            while (true) {
                var result = new byte[1024];
                await ws.ReceiveAsync(new ArraySegment<byte>(result), new CancellationToken());
                rec_str = Encoding.UTF8.GetString(result, 0, result.Length);
                Debug.Log("rec: "+rec_str);
                if (rec_str != null) {
                    //rbSave = JsonUtility.FromJson<RobotData>(rec_str);

                    /*for (int i = 0; i < 4; i++)
                    {
                        ArticulationDrive drive = articulationChain[i + 1].xDrive;
                        drive.target = rbSave.angles[i];
                        articulationChain[i + 1].xDrive = drive;
                    }*/
                    moveFinish = true;
                }
            }
        }
        catch (Exception ex) {
            Console.WriteLine(ex.Message);
        }
    }

    public RobotData rbSave=new RobotData();
    public Vector3 movePos=new Vector3(0,0,0);
    public Vector3 originPos = new Vector3(0, 0, 0);
    public float Ratio = 1;
    public async void sendMsg() {
        moveFinish = false;

        rbSave.eeX = -(movePos.x-originPos.x)*Ratio;
        rbSave.eeY = -(movePos.y-originPos.y)*Ratio;
        rbSave.eeZ = (movePos.z-originPos.z)*Ratio;
        rbSave.time = DateTime.Now.TimeOfDay.ToString();

        string jsonStr = JsonUtility.ToJson(rbSave);
        Debug.Log(jsonStr);

        await ws.SendAsync(new ArraySegment<byte>(Encoding.UTF8.GetBytes(jsonStr)),WebSocketMessageType.Binary,true,ct);
    }

    public void controlGripper() {
        moveFinish = true;
        rbSave.gripper = !rbSave.gripper;
    }


    public async void goodbye() {
        rbSave.connect = false;
        string jsonStr = JsonUtility.ToJson(rbSave);
        Debug.Log(jsonStr);

        await ws.SendAsync(new ArraySegment<byte>(Encoding.UTF8.GetBytes(jsonStr)), WebSocketMessageType.Binary, true, ct);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}

[Serializable]
public class RobotData
{
    public float eeX;
    public float eeY;
    public float eeZ;
    public int Mode = 99;

    public float[] angles = new float[4] { 0.0f, 0.0f, 0.0f, 0.0f };
    public bool connect = true;

    public bool move = true;
    public bool gripper = false;
    public bool pump = true;
    public string time = "";
}
