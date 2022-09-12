using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using RootMotion.FinalIK;

public class Move : MonoBehaviour
{
    public Vector3 position
    {
        get
        {
            return ik.GetIKSolver().GetIKPosition();
        }
        set
        {
            ik.GetIKSolver().SetIKPosition(value);
        }
    }

    private IK ik;
    private void Awake()
    {
        ik = GetComponent<IK>();
    }

    // Start is called before the first frame update
    void Start()
    {
        var points = ik.GetIKSolver().GetPoints();
        position = points[points.Length - 1].transform.position;
    }

    // Update is called once per frame
    void Update()
    {
        GameObject endeff = GameObject.Find("Endeffector");
        Vector3 start = endeff.transform.position;
        GameObject choose = GameObject.Find("Sphere");
        Vector3 end = choose.transform.position;
        //position = end;

        GameObject line = GameObject.Find("connect");
        LineRenderer lr = line.GetComponent<LineRenderer>();
        lr.SetPosition(0,ik.GetIKSolver().GetIKPosition());
        lr.SetPosition(1, end);

    }
}
