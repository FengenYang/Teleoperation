using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TypingArea : MonoBehaviour
{
    public GameObject leftHand;
    public GameObject rightHand;
    public GameObject leftTypeHand;
    public GameObject rightTypeHand;

    public GameObject leftControl;
    public GameObject rightControl;
    public GameObject leftTypeControl;
    public GameObject rightTypeControl;

    private void OnTriggerEnter(Collider other)
    {
        GameObject hand = other.GetComponentInParent<OVRGrabber>().gameObject;
        if (hand == null) return;
        if (hand == leftHand)
        {
            leftTypeHand.SetActive(true);
        }
        else if (hand == rightHand) {
            rightTypeHand.SetActive(true);
        }
        else if (hand == leftControl)
        {
            leftTypeControl.SetActive(true);
        }
        else if (hand == rightControl)
        {
            rightTypeControl.SetActive(true);
        }
    }

    private void OnTriggerExit(Collider other)
    {
        GameObject hand = other.GetComponentInParent<OVRGrabber>().gameObject;
        if (hand == null) return;
        if (hand == leftHand)
        {
            leftTypeHand.SetActive(false);
        }
        else if (hand == rightHand) {
            rightTypeHand.SetActive(false);
        }
        else if (hand == leftControl)
        {
            leftTypeControl.SetActive(false);
        }
        else if (hand == rightControl)
        {
            rightTypeControl.SetActive(false);
        }
    }
}
