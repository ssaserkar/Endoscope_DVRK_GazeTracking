using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Globalization;
using UnityEngine.UI;


namespace Tobii.Gaming.Examples.GazePointData
{
    public class MainCamera : MonoBehaviour {

#if UNITY_EDITOR

    public double x;
    public double y;
    public GameObject GazePoint;
    public ToggleGroup toggleGroup;


    public float lookSpeedH = 2f;
    public float lookSpeedV = 2f;
    public float zoomSpeed = 2f;
    public float dragSpeed = 6f;

    

    private float yaw = 0f;
    private float pitch = 0f;
    private float roll = 0f;
    // Start is called before the first frame update
    void Start()
    {

        toggleGroup = GetComponent<ToggleGroup>();
        Toggle[] toggles = GetComponentsInChildren<Toggle>();
        MainCamera MC =GetComponent<MainCamera>();
        // Debug.Log(MC.Transform);
        // MC.
    }

    // Update is called once per frame
    void Update()
    {
        // if (Input.GetMouseButton(1))
        // {
        //     yaw += lookSpeedH * Input.GetAxis("Mouse X");
        //     pitch -= lookSpeedV * Input.GetAxis("Mouse Y");

        //     transform.eulerAngles = new Vector3(pitch, yaw, 0f);
        // }

        // //drag camera around with Middle Mouse
        // if (Input.GetMouseButton(2))
        // {
        //     transform.Translate(-Input.GetAxisRaw("Mouse X") * UnityEngine.Time.deltaTime * dragSpeed, -Input.GetAxisRaw("Mouse Y") * UnityEngine.Time.deltaTime * dragSpeed, 0);
        // }

            //Zoom in and out with Mouse Wheel

            
        // foreach (char c in Input.inputString)
        // {
           
                if (Input.GetKey(KeyCode.A)) 
                {
                    
                    print("Going into Gaze based automation mode!!");
                    GazePoint gazePoint = TobiiAPI.GetGazePoint();
                    if (gazePoint.IsValid)
                    {
                        Vector2 gazePosition = gazePoint.Screen;

                        Vector2 roundedSampleInput =
                            new Vector2(Mathf.RoundToInt(gazePosition.x), Mathf.RoundToInt(gazePosition.y));
                        x = roundedSampleInput.x;
                        y = roundedSampleInput.y;
                        if(x < 775)
                        {
                            //move camera left
                            yaw -= (float).08;
                            // pitch += (float).1; 
                            transform.eulerAngles = new Vector3(pitch, yaw, 0f);
                        }
                        else if(x > 775)
                        {
                            //move camera right
                            yaw += (float).08;
                            // pitch -= (float).1;
                            transform.eulerAngles = new Vector3(pitch, yaw, 0f);
                        }
                        if (y > 425)
                        {
                            //move camera up
                            //yaw += (float).1;
                            pitch -= (float).08;
                            //roll -= (float).1;
                            transform.eulerAngles = new Vector3(pitch, yaw, 0f);
                        }
                        else if(y < 425)
                        {
                            //move camera down
                            pitch += (float).08;
                            //roll -= (float).1;
                            transform.eulerAngles = new Vector3(pitch, yaw, 0f);
                        }
                    }
                }
                else
                if (Input.GetKey(KeyCode.B)) 
                {
                    print("Going into mouse based automation mode!!");

                    if (Input.GetMouseButton(1))
                    {
                        yaw += lookSpeedH * Input.GetAxis("Mouse X");
                        pitch -= lookSpeedV * Input.GetAxis("Mouse Y");

                        transform.eulerAngles = new Vector3(pitch, yaw, 0f);
                    }

                    //drag camera around with Middle Mouse
                    if (Input.GetMouseButton(2))
                    {
                        transform.Translate(-Input.GetAxisRaw("Mouse X") * UnityEngine.Time.deltaTime * dragSpeed, -Input.GetAxisRaw("Mouse Y") * UnityEngine.Time.deltaTime * dragSpeed, 0);
                    }

                    //Zoom in and out with Mouse Wheel
                    transform.Translate(0, 0, Input.GetAxis("Mouse ScrollWheel") * zoomSpeed, Space.Self);

           
                }
                else
                if (Input.GetKey(KeyCode.C))
                {
                    print("Going into keyboard based automation mode!!");
                    if (Input.GetKeyUp(KeyCode.LeftArrow))
                    {
                        print("left arrow key is held down");
                        yaw -= (float)3;
                        // pitch += (float).1; 
                        transform.eulerAngles = new Vector3(pitch, yaw, 0f);
                    }

                    if (Input.GetKeyUp(KeyCode.RightArrow))
                    {
                        print("down arrow key is held down");
                        yaw += (float)3;
                        // pitch -= (float).1;
                        transform.eulerAngles = new Vector3(pitch, yaw, 0f);
                    }
                    if (Input.GetKeyUp(KeyCode.UpArrow))
                    {
                        print("up arrow key is held down");
                        pitch -= (float)3;
                        //roll -= (float).1;
                        transform.eulerAngles = new Vector3(pitch, yaw, 0f);

                    }
                    if (Input.GetKeyUp(KeyCode.DownArrow))
                    {
                        print("down arrow key is held down");
                        pitch += (float)3;
                        //roll -= (float).1;
                        transform.eulerAngles = new Vector3(pitch, yaw, 0f);

                    }
                    
                }
                    

			
    
    // }
    }
#endif
 }
    
}