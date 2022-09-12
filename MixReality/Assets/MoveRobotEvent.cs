using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using RootMotion.FinalIK;

public class MoveRobotEvent : MonoBehaviour
{
    public GameObject Robot;
    public GameObject TargetPos;

    bool judge = false;
    // Update is called once per frame
    void Update()
    {
        
    }

    public void Selecttherobot() {
        judge = true;
    }

    public void Unselecttherobot() {
        //this.transform.eulerAngles = new Vector3(0,this.transform.eulerAngles.y,0);
        this.transform.eulerAngles = new Vector3(0, 0, 0);
        GameObject.Find("TargetObject").transform.position = GameObject.Find("magician").transform.position + GameObject.Find("magician").GetComponent<MagicianConfigure>().targetOffset;
        judge = false;
    }
}
