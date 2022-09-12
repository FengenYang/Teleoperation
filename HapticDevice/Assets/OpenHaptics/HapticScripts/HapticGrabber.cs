using System.Collections;
using System.Collections.Generic;
using UnityEngine.Profiling;
using UnityEngine;
using RootMotion.FinalIK;
//using HapticPlugin;


//! This object can be applied to the stylus of a haptic device. 
//! It allows you to pick up simulated objects and feel the involved physics.
//! Optionally, it can also turn off physics interaction when nothing is being held.
public class HapticGrabber : MonoBehaviour 
{
	public int buttonID = 0;		//!< index of the button assigned to grabbing.  Defaults to the first button
	public bool ButtonActsAsToggle = false;	//!< Toggle button? as opposed to a press-and-hold setup?  Defaults to off.
	public enum PhysicsToggleStyle{ none, onTouch, onGrab };
	public PhysicsToggleStyle physicsToggleStyle = PhysicsToggleStyle.none;   //!< Should the grabber script toggle the physics forces on the stylus? 

	public bool DisableUnityCollisionsWithTouchableObjects = true;

	private  GameObject hapticDevice = null;   //!< Reference to the GameObject representing the Haptic Device
	private bool buttonStatus = false;          //!< Is the button currently pressed?
	private bool buttonStatus2 = false;
	private GameObject touching = null;			//!< Reference to the object currently touched
	private GameObject grabbing = null;			//!< Reference to the object currently grabbed
	private FixedJoint joint = null;            //!< The Unity physics joint created between the stylus and the object being grabbed.

	private WebSocket ws= null;

	public GameObject robotArm;
	private IK ik;
    private void Awake()
    {
        ws = gameObject.AddComponent<WebSocket>();
		ws.Link();
		ik = robotArm.GetComponent<IK>();
		grabCube = false;
	}

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

	float ratio = 1;
	float gripperOffset = 0;
	Vector3 roboteePos;
	//! Automatically called for initialization
	void Start () 
	{
		
		if (hapticDevice == null)
		{

			HapticPlugin[] HPs = (HapticPlugin[])Object.FindObjectsOfType(typeof(HapticPlugin));
			foreach (HapticPlugin HP in HPs)
			{
				if (HP.hapticManipulator == this.gameObject)
				{
					hapticDevice = HP.gameObject;
				}
			}

		}

		if ( physicsToggleStyle != PhysicsToggleStyle.none)
			hapticDevice.GetComponent<HapticPlugin>().PhysicsManipulationEnabled = false;

		if (DisableUnityCollisionsWithTouchableObjects)
			disableUnityCollisions();

		//save the initial state of Robot arm
		Vector3 bp = GameObject.Find("OriginalCoords").transform.position;
		Vector3 rp = GameObject.Find("RobotEnd").transform.position;

		ws.originPos = rp;
		ws.movePos = rp;
		ws.Ratio = 100 / (bp.y - rp.y);
		
		gripperOffset = rp.y - GameObject.Find("EndEffector").transform.position.y;
		roboteePos = GameObject.Find("EndEffector").transform.position;
		ik.GetIKSolver().SetIKPosition(rp);
		hapticDevice.GetComponent<HapticPlugin>().Buttons[0] = 0;
		hapticDevice.GetComponent<HapticPlugin>().Buttons[1] = 0;
	}

	void disableUnityCollisions()
	{
		GameObject[] touchableObjects;
		touchableObjects =  GameObject.FindGameObjectsWithTag("Touchable") as GameObject[];  //FIXME  Does this fail gracefully?

		// Ignore my collider
		Collider myC = gameObject.GetComponent<Collider>();
		if (myC != null)
			foreach (GameObject T in touchableObjects)
			{
				Collider CT = T.GetComponent<Collider>();
				if (CT != null)
					Physics.IgnoreCollision(myC, CT);
			}
		
		// Ignore colliders in children.
		Collider[] colliders = gameObject.GetComponentsInChildren<Collider>();
		foreach (Collider C in colliders)
			foreach (GameObject T in touchableObjects)
			{
				Collider CT = T.GetComponent<Collider>();
				if (CT != null)
					Physics.IgnoreCollision(C, CT);
			}

	}

	public GameObject endeffector;
	public GameObject targetCube;
	private bool grabCube = false;
	Vector3 offset = new Vector3(0, 0, 0);
	Vector3 saveEndPos = new Vector3(0, 0, 0);
	//! Update is called once per frame
	void FixedUpdate () 
	{
		bool newButtonStatus = hapticDevice.GetComponent<HapticPlugin>().Buttons [buttonID] == 1;
		bool oldButtonStatus = buttonStatus;
		buttonStatus = newButtonStatus;

		bool newButtonStatus2 = hapticDevice.GetComponent<HapticPlugin>().Buttons[1] == 1;
		bool oldButtonStatus2 = buttonStatus2;
		buttonStatus2 = newButtonStatus2;

		//change target color
		if (grabCube) {
			targetCube.transform.position = GameObject.Find("EndEffector").transform.position;
		}

		//check the haptic button, control the gripper
		if (oldButtonStatus2 == false && newButtonStatus2 == true) {
			ws.rbSave.move = false;

			ws.rbSave.gripper = !ws.rbSave.gripper;
			ws.sendMsg();
			grabCube = !grabCube;
			ws.rbSave.move = true;
		}

		
		if (oldButtonStatus == false && newButtonStatus == true)
		{/*
			if (ButtonActsAsToggle)
			{
				if (grabbing)
					release();
				else
					grab();
			} else
			{
				grab();
			}*/


			//Move the real robot arm
			Vector3 rp = this.transform.position + new Vector3(0, gripperOffset, 0);
			//GameObject.Find("Target").transform.position = rp;
			ws.movePos = rp;
			ws.sendMsg();

			//set the virtual robot arm position
			roboteePos = this.transform.position;
			
		}

		GameObject.Find("choosePos").transform.position = Vector3.Lerp(GameObject.Find("choosePos").transform.position, roboteePos + new Vector3(0, gripperOffset, 0), 0.02f);
		ik.GetIKSolver().SetIKPosition(GameObject.Find("choosePos").transform.position);
		GameObject.Find("link_6").transform.position = GameObject.Find("RobotEnd").transform.position;

		//move the virtual robot arm to the target position
		GameObject line = GameObject.Find("Connect");
		LineRenderer lr = line.GetComponent<LineRenderer>();
		lr.SetPosition(0, endeffector.transform.position);
		lr.SetPosition(1, roboteePos);


			/*
			if ((lastEEPos - roboteePos).magnitude > 2)
			{
				//Debug.Log("sdfsdfsd");
				
			}
			else
				offset = new Vector3(0, 0, 0);*/

		if (oldButtonStatus == true && newButtonStatus == false)
		{
			if (ButtonActsAsToggle)
			{
				//Do Nothing
			} else
			{
				release();
			}

			/*
			GameObject line = GameObject.Find("Connect");
			LineRenderer lr = line.GetComponent<LineRenderer>();
			lr.SetPosition(0, Vector3.zero);
			lr.SetPosition(1, Vector3.zero);*/

			
		}
		if (oldButtonStatus == true && newButtonStatus == true) {

			/*GameObject ee = GameObject.Find("EndEffector");
			GameObject bp = GameObject.Find("OriginalCoords");
			Debug.Log("Distance");
			Debug.Log(ee.transform.position.x-bp.transform.position.x);
			Debug.Log(ee.transform.position.y - bp.transform.position.y);
			Debug.Log(ee.transform.position.z - bp.transform.position.z);
			Debug.Log("EE position");
			Debug.Log(ee.transform.position.x);
			Debug.Log(ee.transform.position.y);
			Debug.Log(ee.transform.position.z);

			if (ws.moveFinish)
			{
				ws.computePosition();
				ws.sendMsg();
			}


			GameObject line = GameObject.Find("Connect");
			LineRenderer lr = line.GetComponent<LineRenderer>();
			lr.SetPosition(0, endeffector.transform.position);
			lr.SetPosition(1, this.transform.position);

			Vector3 offset = (this.transform.position - ik.GetIKSolver().GetIKPosition()).normalized;
			Vector3 lastEEPos = ik.GetIKSolver().GetIKPosition();
			ik.GetIKSolver().SetIKPosition(offset + lastEEPos);*/
		}

		// Make sure haptics is ON if we're grabbing
		if ( grabbing && physicsToggleStyle != PhysicsToggleStyle.none)
			hapticDevice.GetComponent<HapticPlugin>().PhysicsManipulationEnabled = true;
		if (!grabbing && physicsToggleStyle == PhysicsToggleStyle.onGrab)
			hapticDevice.GetComponent<HapticPlugin>().PhysicsManipulationEnabled = false;

		/*
		if (grabbing)
			hapticDevice.GetComponent<HapticPlugin>().shapesEnabled = false;
		else
			hapticDevice.GetComponent<HapticPlugin>().shapesEnabled = true;
			*/

		if (Input.GetKey(KeyCode.R)) {
			ws.rbSave.Mode = 10;
			ws.sendMsg();
			ws.rbSave.Mode = 99;
		}
		if (Input.GetKey(KeyCode.A)) {
			//close the air pump
			ws.rbSave.move = false;
			ws.rbSave.pump = false;
			ws.sendMsg();
			ws.rbSave.move = true;
			ws.rbSave.pump = true;
		}
		if (Input.GetKey(KeyCode.C)) {
			ws.rbSave.connect = false;
			ws.sendMsg();
		}
	}

    private void OnApplicationQuit()
    {
		ws.goodbye();
    }

    private void hapticTouchEvent( bool isTouch )
	{
		if (physicsToggleStyle == PhysicsToggleStyle.onGrab)
		{
			if (isTouch)
				hapticDevice.GetComponent<HapticPlugin>().PhysicsManipulationEnabled = true;
			else			
				return; // Don't release haptics while we're holding something.
		}
		
		if( physicsToggleStyle == PhysicsToggleStyle.onTouch )
		{
			hapticDevice.GetComponent<HapticPlugin>().PhysicsManipulationEnabled = isTouch;
			GetComponentInParent<Rigidbody>().velocity = Vector3.zero;
			GetComponentInParent<Rigidbody>().angularVelocity = Vector3.zero;

		}
	}

	void OnCollisionEnter(Collision collisionInfo)
	{
		Collider other = collisionInfo.collider;
		//Debug.unityLogger.Log("OnCollisionEnter : " + other.name);
		GameObject that = other.gameObject;
		Rigidbody thatBody = that.GetComponent<Rigidbody>();

		// If this doesn't have a rigidbody, walk up the tree. 
		// It may be PART of a larger physics object.
		while (thatBody == null)
		{
			//Debug.logger.Log("Touching : " + that.name + " Has no body. Finding Parent. ");
			if (that.transform == null || that.transform.parent == null)
				break;
			GameObject parent = that.transform.parent.gameObject;
			if (parent == null)
				break;
			that = parent;
			thatBody = that.GetComponent<Rigidbody>();
		}

		if( collisionInfo.rigidbody != null )
			hapticTouchEvent(true);

		if (thatBody == null)
			return;

		if (thatBody.isKinematic)
			return;
	
		touching = that;
	}
	void OnCollisionExit(Collision collisionInfo)
	{
		Collider other = collisionInfo.collider;
		//Debug.unityLogger.Log("onCollisionrExit : " + other.name);

		if( collisionInfo.rigidbody != null )
			hapticTouchEvent( false );

		if (touching == null)
			return; // Do nothing

		if (other == null ||
		    other.gameObject == null || other.gameObject.transform == null)
			return; // Other has no transform? Then we couldn't have grabbed it.

		if( touching == other.gameObject || other.gameObject.transform.IsChildOf(touching.transform))
		{
			touching = null;
		}
	}
		
	//! Begin grabbing an object. (Like closing a claw.) Normally called when the button is pressed. 
	void grab()
	{
		GameObject touchedObject = touching;
		if (touchedObject == null) // No Unity Collision? 
		{
			// Maybe there's a Haptic Collision
			touchedObject = hapticDevice.GetComponent<HapticPlugin>().touching;
		}

		if (grabbing != null) // Already grabbing
			return;
		if (touchedObject == null) // Nothing to grab
			return;

		// Grabbing a grabber is bad news.
		if (touchedObject.tag =="Gripper")
			return;

		Debug.Log( " Object : " + touchedObject.name + "  Tag : " + touchedObject.tag );

		grabbing = touchedObject;

		//Debug.logger.Log("Grabbing Object : " + grabbing.name);
		Rigidbody body = grabbing.GetComponent<Rigidbody>();

		// If this doesn't have a rigidbody, walk up the tree. 
		// It may be PART of a larger physics object.
		while (body == null)
		{
			//Debug.logger.Log("Grabbing : " + grabbing.name + " Has no body. Finding Parent. ");
			if (grabbing.transform.parent == null)
			{
				grabbing = null;
				return;
			}
			GameObject parent = grabbing.transform.parent.gameObject;
			if (parent == null)
			{
				grabbing = null;
				return;
			}
			grabbing = parent;
			body = grabbing.GetComponent<Rigidbody>();
		}

		joint = (FixedJoint)gameObject.AddComponent(typeof(FixedJoint));
		joint.connectedBody = body;
	}
	//! changes the layer of an object, and every child of that object.
	static void SetLayerRecursively(GameObject go, int layerNumber )
	{
		if( go == null ) return;
		foreach(Transform trans in go.GetComponentsInChildren<Transform>(true))
			trans.gameObject.layer = layerNumber;
	}

	//! Stop grabbing an obhject. (Like opening a claw.) Normally called when the button is released. 
	void release()
	{
		if( grabbing == null ) //Nothing to release
			return;


		Debug.Assert(joint != null);

		joint.connectedBody = null;
		Destroy(joint);



		grabbing = null;

		if (physicsToggleStyle != PhysicsToggleStyle.none)
			hapticDevice.GetComponent<HapticPlugin>().PhysicsManipulationEnabled = false;
			
	}

	//! Returns true if there is a current object. 
	public bool isGrabbing()
	{
		return (grabbing != null);
	}
}
