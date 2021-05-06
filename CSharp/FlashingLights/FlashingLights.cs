using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FlashingLights : MonoBehaviour
{
    // __init__
    Light lit;
    float elapsed;
    public float flashRateInSec = 1f;

    public float red_min = 0.3f;
    public float green_min;
    public float blue_min;
    public float alpha_min;

    public float red_max = 0.8f;
    public float green_max;
    public float blue_max;
    public float alpha_max;
    Color newColor;

    // Start is called before the first frame update
    void Start()
    {
        lit = GetComponent<Light>();
    }

    // Update is called once per frame
    void Update()
    {
        // How much time has passed in total.
        elapsed += Time.deltaTime;

        if (elapsed >= flashRateInSec)
        {
            elapsed = 0f;
            var red = Random.Range(red_min, red_max);
            var green = Random.Range(green_min, green_max);
            var blue = Random.Range(blue_min, blue_max);
            var alpha = Random.Range(alpha_min, alpha_max);

            newColor = new Color(red, green, blue, alpha);
        }

        lit.color = Color.Lerp(lit.color, newColor, Time.deltaTime * 10);
        
    }
}
