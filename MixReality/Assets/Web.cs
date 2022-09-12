using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using UnityEngine.UI;

public class Web : MonoBehaviour
{
    ClientWebSocket ws;
    CancellationToken ct;
    string rec_str;


    public bool moveFinish = true;

    public void Link(string ipAdd)
    {
        moveFinish = true;
        Websocket(ipAdd);
    }

    public async void Websocket(string ipAdd)
    {

        try
        {
            ws = new ClientWebSocket();
            ct = new CancellationToken();
            ipAdd = "ws://" + ipAdd + ":8888";
            Uri url = new Uri(ipAdd);
            await ws.ConnectAsync(url, ct);
            while (true)
            {
                var result = new byte[1024];
                await ws.ReceiveAsync(new ArraySegment<byte>(result), new CancellationToken());
                rec_str = Encoding.UTF8.GetString(result, 0, result.Length);
                Debug.Log("rec: " + rec_str);
                if (rec_str != null)
                {
                    //rbSave = JsonUtility.FromJson<RobotData>(rec_str);
                    moveFinish = true;
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.Message);
        }
    }

    public RobotData rbSave = new RobotData();
    public Vector3 sendPos = new Vector3(0, 0, 0);
    public async void sendMsg()
    {
        moveFinish = false;

        rbSave.eeX = sendPos.x;
        rbSave.eeY = sendPos.y;
        rbSave.eeZ = sendPos.z;
        rbSave.time= DateTime.Now.TimeOfDay.ToString();
        
        string jsonStr = JsonUtility.ToJson(rbSave);
        Debug.Log(jsonStr);

        await ws.SendAsync(new ArraySegment<byte>(Encoding.UTF8.GetBytes(jsonStr)), WebSocketMessageType.Binary, true, ct);
    }

    public void controlGripper()
    {
        moveFinish = true;
        rbSave.gripper = !rbSave.gripper;
    }


    public async void goodbye()
    {
        rbSave.connect = false;
        string jsonStr = JsonUtility.ToJson(rbSave);
        Debug.Log(jsonStr);

        await ws.SendAsync(new ArraySegment<byte>(Encoding.UTF8.GetBytes(jsonStr)), WebSocketMessageType.Binary, true, ct);
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
