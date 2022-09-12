using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using RootMotion.FinalIK;

public class Keyboard : MonoBehaviour
{
    public TMP_InputField inputField;
    public GameObject normalButtons;
    public GameObject capsButtons;
    private bool caps;

    // Start is called before the first frame update
    void Start()
    {
        caps = false;
    }

    public void InsertChar(string c) {
        inputField.text += c;
    }

    public void DeleteChar() {
        if (inputField.text.Length > 0) {
            inputField.text = inputField.text.Substring(0, inputField.text.Length - 1);
        }
    }

    public void LinkRobot() {
        GameObject robot = GameObject.Find("magician");
        Web ws = robot.GetComponent<MagicianConfigure>().ws;

        ws.Link(inputField.text);
    }

    public void RobotRest() {
        MagicianConfigure obj = GameObject.Find("magician").GetComponent<MagicianConfigure>();
        GameObject.Find("magician").transform.position = obj.originPos;
        GameObject.Find("MovePosition").transform.position = obj.originEE;
        GameObject.Find("magician/base_link").GetComponent<IK>().GetIKSolver().SetIKPosition(obj.originEE);

        obj.ws.rbSave.Mode = 10;
        obj.ws.sendMsg();
        obj.ws.rbSave.Mode = 99;
    }

    public void InsertSpace() {
        inputField.text += " ";
    }

    public void CapsPressed() {
        if (!caps)
        {
            normalButtons.SetActive(false);
            capsButtons.SetActive(true);
            caps = true;
        }
        else {
            capsButtons.SetActive(false);
            normalButtons.SetActive(true);
            caps = false;
        }
    }

    public void Disconnect() {
        GameObject.Find("magician").GetComponent<MagicianConfigure>().ws.rbSave.connect = false;
        GameObject.Find("magician").GetComponent<MagicianConfigure>().ws.sendMsg();
    }
}
