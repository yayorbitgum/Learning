// https://gamedev.stackexchange.com/questions/135209/how-to-store-references-to-scene-objects-in-prefabs
// Singletons in Unity:
// https://www.youtube.com/watch?v=CPKAgyp8cno
//
// -------------------------------------
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ReferenceManager : MonoBehaviour
{
    static public ReferenceManager instance;
    // So we can access our player from any prefab script too (such as the spinning roads).
    static public GameObject Player;

    void Awake()
    {
        instance = this;
    }
}
