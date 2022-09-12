using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FollowObject : MonoBehaviour
{
    public GameObject follow;

    // Update is called once per frame
    void Update()
    {
        this.transform.position = follow.transform.position;
    }
}
