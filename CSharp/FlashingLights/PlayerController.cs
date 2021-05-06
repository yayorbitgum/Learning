using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerController : MonoBehaviour
{
    public int move_speed = 20;
    public float turn_speed;
    public float horizontal_input;
    public float vertical_input;
    // Start is called before the first frame update.
    void Start()
    {
        // ----
    }

    // Update is called once per frame.
    void Update()
    {
        // Get horizontal axis input every frame.
        horizontal_input = Input.GetAxis("Horizontal");
        vertical_input = Input.GetAxis("Vertical");

        // Get our forward movement and sideways movement, both smoothed out by deltaTime (time between frames).
        var forward_movement = Vector3.forward * Time.deltaTime * move_speed * vertical_input;
        var sideways_movement = Vector3.right * Time.deltaTime * turn_speed * horizontal_input;
        
        // Apply the translation each frame too.
        transform.Translate(forward_movement);
        transform.Translate(sideways_movement);
        transform.Rotate(0, horizontal_input, 0);
    }
}
