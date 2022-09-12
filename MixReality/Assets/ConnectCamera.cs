using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System;
using System.Net.WebSockets;
using System.Text;
using System.Threading;


public class ConnectCamera : MonoBehaviour
{
    ClientWebSocket ws;
    CancellationToken ct;
    string rec_str;
    Texture2D t2d;


    public async void Websocket(string ipAdd) {
        try
        {
            ws = new ClientWebSocket();
            ct = new CancellationToken();
            
            ipAdd = "ws://" + ipAdd + ":8889";
            Uri url = new Uri(ipAdd);
            await ws.ConnectAsync(url, ct);
            sendMsg();
            while (true)
            {
                var result = new byte[1000000];
                await ws.ReceiveAsync(new ArraySegment<byte>(result), new CancellationToken());
                rec_str = Convert.ToBase64String(result);
                //rec_str = Encoding.Unicode.GetString(result, 0, result.Length);

                if (rec_str != null)
                {
                    Debug.Log(rec_str);
                    //do something...
                    t2d.LoadImage(Convert.FromBase64String(rec_str));
                    
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex.Message);
        }
    }

    public async void sendMsg() {
        string send = "begin";
        await ws.SendAsync(new ArraySegment<byte>(Encoding.UTF8.GetBytes(send)), WebSocketMessageType.Binary, true, ct);
    }

    // Start is called before the first frame update
    void Start()
    {
        t2d = new Texture2D(10, 10);
        Websocket("10.251.70.4");
    }

    // Update is called once per frame
    void Update()
    {
        GameObject.Find("showImg").GetComponent<Renderer>().material.mainTexture = t2d;
    }
}
