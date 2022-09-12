using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MagicianConfigure : MonoBehaviour
{
    public Web ws=null;
    public Vector3 originPos,originBP,originEE;
    public float posRatio = 0;
    public Vector3 targetOffset;

    // Start is called before the first frame update
    void Start()
    {
        ws=this.GetComponentInChildren<Web>();
        originPos = GameObject.Find("magician").transform.position;
        originBP = GameObject.Find("magician/base_link/link_1/link_2").transform.position;
        originEE = GameObject.Find("REndEffector").transform.position;
        posRatio = 100 / (originEE.y - originBP.y);

        targetOffset = GameObject.Find("TargetObject").transform.position - GameObject.Find("magician").transform.position;
    }

}
