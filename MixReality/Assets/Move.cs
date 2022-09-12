using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using RootMotion.FinalIK;

public class Move : MonoBehaviour
{
    private float posRatio=1;
    Vector3 basePoint,eePoint,originPoint;
    // Start is called before the first frame update
    void Start()
    {
        originPoint = GameObject.Find("magician").transform.position;
        basePoint = GameObject.Find("magician/base_link/link_1/link_2").transform.position;
        eePoint = GameObject.Find("REndEffector").transform.position;
        posRatio = 100 / (eePoint.y-basePoint.y);

        //GameObject robot = GameObject.Find("magician");
        //ws = robot.GetComponent<MagicianConfigure>().ws;
        //ws.Link("172.23.22.144");
    }

    OVRInput.Controller leftcontroller = OVRInput.Controller.LTouch;
    OVRInput.Controller rightcontroller = OVRInput.Controller.RTouch;
    public GameObject Robot;
    public GameObject leftGripper;
    public GameObject rightGripper;
    bool isGrabbing = false;
    int lastMode = 99;
    bool testGripper = false;
    // Update is called once per frame
    void Update()
    {
        Web message = GameObject.Find("magician").GetComponentInChildren<Web>();

        
        //use the left controller joystick
        Vector2 thumbstick = OVRInput.Get(OVRInput.Axis2D.PrimaryThumbstick, leftcontroller);
        if (thumbstick.y > 0) { 
            Robot.transform.position += new Vector3(0, 0, 0.01f);   //move forward
            GameObject.Find("MovePosition").transform.position += new Vector3(0, 0, 0.01f);
            GameObject.Find("TargetObject").transform.position += new Vector3(0, 0, 0.01f);
            this.GetComponent<IK>().GetIKSolver().SetIKPosition(GameObject.Find("MovePosition").transform.position);
        }

        if (thumbstick.y < 0) { 
            Robot.transform.position -= new Vector3(0, 0, 0.01f);   //move backward
            GameObject.Find("MovePosition").transform.position -= new Vector3(0, 0, 0.01f);
            GameObject.Find("TargetObject").transform.position -= new Vector3(0, 0, 0.01f);
            this.GetComponent<IK>().GetIKSolver().SetIKPosition(GameObject.Find("MovePosition").transform.position);
        }

        if (thumbstick.x > 0){
            Robot.transform.position += new Vector3(0.01f, 0, 0);   //move right
            GameObject.Find("MovePosition").transform.position += new Vector3(0.01f, 0, 0);
            GameObject.Find("TargetObject").transform.position += new Vector3(0.01f, 0, 0);
            this.GetComponent<IK>().GetIKSolver().SetIKPosition(GameObject.Find("MovePosition").transform.position);
        }
        if (thumbstick.x < 0) { 
            Robot.transform.position -= new Vector3(0.01f, 0, 0);   //move left
            GameObject.Find("MovePosition").transform.position -= new Vector3(0.01f, 0, 0);
            GameObject.Find("TargetObject").transform.position -= new Vector3(0.01f, 0, 0);
            this.GetComponent<IK>().GetIKSolver().SetIKPosition(GameObject.Find("MovePosition").transform.position);
        }
            
        if (OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger, leftcontroller) || testGripper) {
            //control the gripper
            if (isGrabbing) {
                isGrabbing = false;
                leftGripper.transform.Rotate(new Vector3(-15, 0, 0));
                rightGripper.transform.Rotate(new Vector3(15, 0, 0));
                GameObject.Find("TargetObject").transform.position -= new Vector3(0, 99, 0);
            }
            else { 
                isGrabbing = true;
                leftGripper.transform.Rotate(new Vector3(15, 0, 0));
                rightGripper.transform.Rotate(new Vector3(-15, 0, 0));
            }

            message.rbSave.pump = true;
            message.rbSave.move = false;
            message.rbSave.gripper = isGrabbing;
            message.sendMsg();
            message.rbSave.move = true;

            testGripper = false;
        }
        /*if (isGrabbing) {
            GameObject.Find("TargetObject").transform.position = GameObject.Find("Gripper").transform.position;
        }*/


        if (OVRInput.Get(OVRInput.Button.PrimaryHandTrigger, leftcontroller)) {
            message.rbSave.move = false;
            message.rbSave.pump = false;
            message.sendMsg();
            message.rbSave.move = true;
        }

        if (OVRInput.Get(OVRInput.RawButton.Y, leftcontroller)) { 
            Robot.transform.position += new Vector3(0, 0.01f, 0);
            GameObject.Find("MovePosition").transform.position += new Vector3(0, 0.01f, 0);
            GameObject.Find("TargetObject").transform.position += new Vector3(0, 0.01f, 0);
            this.GetComponent<IK>().GetIKSolver().SetIKPosition(GameObject.Find("MovePosition").transform.position);
        }
            
        if (OVRInput.Get(OVRInput.RawButton.X, leftcontroller)) { 
            Robot.transform.position -= new Vector3(0, 0.01f, 0);
            GameObject.Find("MovePosition").transform.position -= new Vector3(0, 0.01f, 0);
            GameObject.Find("TargetObject").transform.position -= new Vector3(0, 0.01f, 0);
            this.GetComponent<IK>().GetIKSolver().SetIKPosition(GameObject.Find("MovePosition").transform.position);
        }

        if (OVRInput.GetDown(OVRInput.RawButton.LThumbstick, leftcontroller))
        {
            GameObject.Find("Input").GetComponent<InputConfigure>().hideshowKeyboard();
        }

        //Control the end effector position with the right hand joystick
        int eeMode = 99;
        if (OVRInput.Get(OVRInput.RawButton.RThumbstickUp, rightcontroller) || righthandPose==2) {
            eeForward();
            eeMode = 2;
            if (lastMode != 2) { 
                message.rbSave.Mode = 2;
                message.sendMsg();
                message.rbSave.Mode = 99;
                lastMode = 2;
            }
        }
        else if (OVRInput.Get(OVRInput.RawButton.RThumbstickDown, rightcontroller) || righthandPose==1) {
            eeBackward();
            eeMode = 1;
            if (lastMode != 1) { 
                message.rbSave.Mode = 1;
                message.sendMsg();
                message.rbSave.Mode = 99;
                lastMode = 1;
            }
        }
        else if (OVRInput.Get(OVRInput.RawButton.RThumbstickRight, rightcontroller) || righthandPose==3) {
            eeRight();
            eeMode = 3;
            if (lastMode != 3) {
                
                message.rbSave.Mode = 3;
                message.sendMsg();
                message.rbSave.Mode = 99;
                lastMode = 3;
            }
        }
        else if (OVRInput.Get(OVRInput.RawButton.RThumbstickLeft, rightcontroller) || righthandPose==4) {
            eeLeft();
            eeMode = 4;
            if (lastMode != 4) {
                
                message.rbSave.Mode = 4;
                message.sendMsg();
                message.rbSave.Mode = 99;
                lastMode = 4;
            }
        }
        else if (OVRInput.Get(OVRInput.Button.PrimaryIndexTrigger, rightcontroller) || righthandPose==5){
            eeUp();
            eeMode = 5;

            if (lastMode != 5)
            {
                message.rbSave.Mode = 5;
                message.sendMsg();
                message.rbSave.Mode = 99;
                lastMode = 5;
            }
        }
        else if (OVRInput.Get(OVRInput.Button.PrimaryHandTrigger, rightcontroller) || righthandPose==6){
            eeDown();
            eeMode = 6;
            if (lastMode != 6)
            {
                message.rbSave.Mode = 6;
                message.sendMsg();
                message.rbSave.Mode = 99;
                lastMode = 6;
            }
        }

        if (eeMode==99 && lastMode!=99) {
            //send the message to stop the real end effector
            message.rbSave.Mode = 0;
            Vector3 nowthePos = GameObject.Find("REndEffector").transform.position;
            message.sendPos = (nowthePos - Robot.GetComponent<MagicianConfigure>().originEE) * Robot.GetComponent<MagicianConfigure>().posRatio;

            message.sendMsg();
            message.rbSave.Mode = 99;
            lastMode = 99;
        }
        
    }


    public void eeForward() {
        this.GetComponent<IK>().GetIKSolver().SetIKPosition(this.GetComponent<IK>().GetIKSolver().GetIKPosition() + new Vector3(0, 0, 0.0015f));
        GameObject.Find("MovePosition").transform.position += new Vector3(0, 0, 0.0015f);
    }
    public void eeBackward() { 
        this.GetComponent<IK>().GetIKSolver().SetIKPosition(this.GetComponent<IK>().GetIKSolver().GetIKPosition() - new Vector3(0, 0, 0.0015f));
        GameObject.Find("MovePosition").transform.position -= new Vector3(0, 0, 0.0015f);
    }
    public void eeLeft() {
        this.GetComponent<IK>().GetIKSolver().SetIKPosition(this.GetComponent<IK>().GetIKSolver().GetIKPosition() - new Vector3(0.0015f, 0, 0));
        GameObject.Find("MovePosition").transform.position -= new Vector3(0.0015f, 0, 0);
    }
    public void eeRight() {
        this.GetComponent<IK>().GetIKSolver().SetIKPosition(this.GetComponent<IK>().GetIKSolver().GetIKPosition() + new Vector3(0.0015f, 0, 0));
        GameObject.Find("MovePosition").transform.position += new Vector3(0.0015f, 0, 0);
    }
    public void eeUp() {
        this.GetComponent<IK>().GetIKSolver().SetIKPosition(this.GetComponent<IK>().GetIKSolver().GetIKPosition() + new Vector3(0, 0.0015f, 0));
        GameObject.Find("MovePosition").transform.position += new Vector3(0, 0.0015f, 0);
    }
    public void eeDown() {
        this.GetComponent<IK>().GetIKSolver().SetIKPosition(this.GetComponent<IK>().GetIKSolver().GetIKPosition() - new Vector3(0, 0.0015f, 0));
        GameObject.Find("MovePosition").transform.position -= new Vector3(0, 0.0015f, 0);
    }

    int lefthandPose = 0; //1 means thumbsup, 2 means thumbsdown
    int righthandPose = 0;
    public void thumbsUp() {
        lefthandPose = 1;
    }
    public void thumbsDown() {
        lefthandPose = 2;
    }

    public void thumbsNo() {
        lefthandPose = 0;
        righthandPose = 0;
    }

    public void poseMoveforward() {
        if (lefthandPose == 1) {
            righthandPose = 2;
        }
            
    }
    public void poseMovebackward()
    {
        if (lefthandPose == 1) {
            righthandPose = 1;
        }
            
    }
    public void poseMoveleft()
    {
        if (lefthandPose == 1) {
            righthandPose = 4;
        }
            
    }
    public void poseMoveright()
    {
        if (lefthandPose == 1) {
            righthandPose = 3;
        }
            
    }
    public void poseMoveUP()
    {
        if (lefthandPose == 1) {
            righthandPose = 5;
        }
            
    }
    public void poseMoverDown()
    {
        if (lefthandPose == 1) {
            righthandPose = 6;
        }
            
    }
    public void poseMoverStop()
    {
        if (lefthandPose == 1) {
            righthandPose = 0;
            return;
        }
            
    }

    public void poseGripper() {
        testGripper = true;
    }
}
