using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class showCamera : MonoBehaviour
{
    string deviceName;
    WebCamTexture webCam;
    // Start is called before the first frame update
    void Start()
    {
        WebCamDevice[] devices = WebCamTexture.devices;
        deviceName = devices[2].name;
        webCam = new WebCamTexture(deviceName, 1920, 1080, 30);
        this.GetComponent<RawImage>().texture = webCam;
        webCam.Play();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
