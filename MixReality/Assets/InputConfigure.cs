using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InputConfigure : MonoBehaviour
{
    public void Start()
    {
        this.transform.position -= new Vector3(0, 99, 0);
    }

    bool isShow = false; //Is the keyboard showing or hiding in the scene?

    public void hideshowKeyboard() {
        if (isShow)
        {
            isShow = false;
            this.transform.position -= new Vector3(0, 99, 0);
        }
        else {
            isShow = true;
            Vector3 handPos = GameObject.Find("OVRCameraRig").transform.position;
            this.transform.position = handPos + new Vector3(-0.7f, 0, 0);
        }
    }
}
