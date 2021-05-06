/* 
 *  Stick this on each road piece.
 *  While most attributes can be set from prefab view, "Player" will have to be set to instances in the scene
        with good old-fashioned selection lol.

Notes/references/help -------------------------------------------------------------------------------------
Using if statement to do larger interval updates within the Update() method:
    https://answers.unity.com/questions/1220440/how-to-display-call-a-function-every-second.html

Initially I was for looping over each child object under the Road parent like this 
(which is very cool functionality btw):
    https://forum.unity.com/threads/iterating-child-game-objects-in-c.22860/

    foreach (Transform road_piece in transform)
        {
            Do Stuff to road_piece;
        }

But more searching found that it's better to just make a prefab, and apply one script to *all* objects.
    https://answers.unity.com/questions/59840/unity-editor-adding-a-script-to-multiple-game-obje.html

And so here we are.
*/

// Using --------------------------------------------------------------------------------------------------
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// Main script --------------------------------------------------------------------------------------------
public class RandomRoadElevations : MonoBehaviour
{
    // __init__ (thinking in Python terms helps me for now) -----------------------------------------------
    public int randomRotationAmount;
    public float wobbleRate;
    public float smooth = 1f;
    public float noWobbleDistance = 0f;
    private Quaternion targetRotation;
    float elapsed;
    bool ticktok = false;
    public GameObject Player;
    private Quaternion baseRotation;
    public float distance_weight;

    // ----------------------------------------------------------------------------------------------------
    // Start is called before the first frame update.
    void Start()
    {
        targetRotation = transform.rotation;
        baseRotation = transform.rotation;
    }

    // ----------------------------------------------------------------------------------------------------
    // Update is called once per frame.
    void Update()
    {
        // How much time has passed in total.
        elapsed += Time.deltaTime;

        // Say wobbleRate is "0.5". If it's been half a second, we'll make a new random target rotation.
        if (elapsed >= wobbleRate) {
            // Reset elapsed time so we can start counting up again.
            elapsed = 0f;
            // A random value between 0 and 1, times the rotation amount we exposed in the editor.
            // Grabbing z position means we'll get bigger rotations the farther away we are.
            float x_wobble = Random.value * randomRotationAmount * (transform.position.z * 0.1f);
            var left = Vector3.left;
            var right = Vector3.right;

            // Our new target rotation, wobbling this amount, and spinning on x-axis.
            // Each tick wobbles back and forth between left and right direction.
            if (ticktok) {
                targetRotation  *= Quaternion.AngleAxis(x_wobble, left);
                ticktok = false;
            }
            else {
                targetRotation *= Quaternion.AngleAxis(x_wobble, right);
                ticktok = true;
            }
        }

        var distance_to_player = CheckDistance(Player, transform.position);
        // If the player is close, constantly lerp back to normal "baseRotation" position.
        //  Meaning the road should flatten as the player approaches.
        if (distance_to_player < noWobbleDistance) {
            // First we slerp between base and target rotation, so we can make things spin less
            //  and less, closer and closer to 0 (base rotation) as player gets closer.
            var desired_rotation = Quaternion.Slerp(
                baseRotation, 
                targetRotation, 
                distance_to_player * distance_weight);

            // Then we lerp between the two so that the transition into and out of the window
            //  (no wobble distance) is smooth.
            transform.rotation = Quaternion.Lerp(
                transform.rotation,
                desired_rotation,
                smooth * Time.deltaTime * 10f);
        }
        else {
            // Otherwise constantly lerp towards our new random left/right target rotation we get
            //  every x seconds.
            transform.rotation = Quaternion.Lerp(
                transform.rotation, 
                targetRotation, 
                smooth * Time.deltaTime * 10f);
        }
    }

    // Check the distance between player and this object, return result.
    float CheckDistance(GameObject object1, Vector3 position)
    {
        Vector3 pos1 = object1.transform.position;
        Vector3 pos2 = position;
        return Vector3.Distance(pos1, pos2);
    }
}
