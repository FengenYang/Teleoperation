using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using RootMotion.FinalIK;

public class GrabObjectConfigure : MonoBehaviour
{
    public GameObject Robot;
    public GameObject Helper;
    // Start is called before the first frame update
    void Start()
    {
        Helper.transform.position -= new Vector3(0, 9999, 0);
        IK ik = Robot.GetComponentInChildren<IK>();
        ik.GetIKSolver().SetIKPosition(this.transform.position);

        eePos = GameObject.Find("REndEffector").transform.position;
    }

    private bool isSelecting = false;
    // Update is called once per frame
    void Update()
    {
        if (isSelecting)
        {
            Helper.transform.position = Robot.transform.position;
            Helper.transform.eulerAngles = Robot.transform.eulerAngles;
            IK ik = Helper.GetComponentInChildren<IK>();
            ik.GetIKSolver().SetIKPosition(this.transform.position);

            GameObject.Find("helper/helper_7").transform.position = GameObject.Find("EndEffector").transform.position;
        }
        else {
            IK ik = Robot.GetComponentInChildren<IK>();
            Vector3 eePos = ik.GetIKSolver().GetIKPosition();
            Vector3 offset = (this.transform.position - eePos);
            if (offset.magnitude > 0.01) {
                
                Vector3 moveto = eePos + 0.01f * offset;
                ik.GetIKSolver().SetIKPosition(moveto);
            }

            //Move the Gripper to the position
            GameObject.Find("link_7").transform.position = GameObject.Find("REndEffector").transform.position;
        }
    }
    private Vector3 eePos;
    
    private IEnumerator Step() {
        float stepProgress = 0f;
        IK ik = Robot.GetComponentInChildren<IK>();
        while (stepProgress<1) {
            stepProgress += Time.deltaTime * 5;

            Vector3 position = Vector3.Lerp(eePos, this.transform.position, stepProgress);
            ik.GetIKSolver().SetIKPosition(position);
            yield return new WaitForSeconds(.1f);
        }
            
    }

    public void Selecttheobject() {
        isSelecting = true;
    }

    public void Unselecttheobject() {
        isSelecting = false;
        Helper.transform.position -= new Vector3(0,9999,0);

        Web ws = GameObject.Find("magician").GetComponent<MagicianConfigure>().ws;
        Vector3 offSet = GameObject.Find("magician").transform.position - GameObject.Find("magician").GetComponent<MagicianConfigure>().originPos;
        Vector3 eePos = GameObject.Find("magician").GetComponent<MagicianConfigure>().originEE + offSet;

        Vector3 movePos = (GameObject.Find("MovePosition").transform.position - eePos) * GameObject.Find("magician").GetComponent<MagicianConfigure>().posRatio;
        ws.sendPos = movePos;
        ws.sendMsg();
    }
}
