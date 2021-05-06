using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// This is the camera! This script goes on the camera object.
public class FollowPlayer : MonoBehaviour
{
    // This exposes "player" variable (that is a GameObject type) to the Unity UI.
    // Then we can just drag and drop the actual object in the editor onto this variable to give it a reference.
    public GameObject cityBus;
    public Vector3 cameraOffset;
    private Vector3 velocity = Vector3.zero;
    public float camRotationSmoothingAmount = 0.1F;

    // Start is called before the first frame update.
    void Start()
    {
        transform.rotation = cityBus.transform.rotation;
    }

    // Update is called once per frame
    void Update()
    {
        var cam_r = transform.rotation;
        var bus_r = cityBus.transform.rotation;
        // The camera position will be set to the bus' current position + an offset.
        transform.position = cityBus.transform.position + cameraOffset;
        // Follow rotation too.
        // transform.rotation = Quaternion.Slerp(cam_r, bus_r, camRotationSmoothingAmount);
    }
}
