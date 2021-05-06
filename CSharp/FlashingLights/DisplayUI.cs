using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DisplayUI : MonoBehaviour
{
    // __init__
    public GameObject target;
    public Text distance_text;
    Vector3 start;
    float traveled = 0f;

    // Start is called before the first frame update.
    void Start()
    {
        start = target.transform.position;
    }

    // Update is called once per frame.
    void Update()
    {
        var current = target.transform.position;

        traveled = Vector3.Distance(start, current);
        distance_text.text = $"Distance from start: {traveled}";
    }
}
