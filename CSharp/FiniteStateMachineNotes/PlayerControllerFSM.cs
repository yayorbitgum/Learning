// This is the Context!

/*
 
 Finite State Machine is made up of:

  + Context -----------
      - Maintains an instance of a Concrete State as its current state.
          - currentState
          + SetState()

  + Abstract State ----------
      - The interface that encapsulates behaviors that are common to all Concrete States.
          + Update()

  + Concrete State : (derived from Abstract State) -----------
      - Implements the behaviors specific to whatever state.
          + Update()
 */

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerControllerFSM : MonoBehaviour
{
    /// <summary>
    /// Holds reference to an instance of PlayerBaseState (ie one of the Concrete States like "PlayerJumpingState").
    /// </summary>
    private PlayerBaseState currentState;

    // Instantiating concrete states.
    public readonly PlayerIdleState idle = new PlayerIdleState();
    public readonly PlayerJumpingState jumping = new PlayerJumpingState();
    public readonly PlayerDuckingState ducking = new PlayerDuckingState();
    
    // Example variables.
    public float jumpForce;
    public Transform head;
    public Transform weapon01;
    public Transform weapon02;

    public Sprite idleSprite;
    public Sprite duckingSprite;
    public Sprite jumpingSprite;
    public Sprite spinningSprite;

    private SpriteRenderer face;
    private Rigidbody rbody;

    /// <summary>
    /// Get references to our object's SpriteRenderer and Rigidbody. SetExpression (face) to idleSprite.
    /// Awake is called when the script instance is being loaded.
    /// </summary>
    private void Awake()
    {
        face = GetComponentInChildren<SpriteRenderer>();
        rbody = GetComponent<Rigidbody>();
        SetExpression(idleSprite);
    }

    /// <summary>
    /// Transition player to idle state on Start.
    /// Start is called on the frame when a script is enabled just before any of the Update methods are called the first time.
    /// </summary>
    private void Start()
    {
        TransitionToState(idle);
    }
    
    /// <summary>
    /// Run the update method for the current concrete state. Update is called once per frame.
    /// </summary>
    void Update()
    {
        currentState.Update(this);
    }

    /// <summary>
    /// Run the CollisionEnter method for the current concrete state.
    /// </summary>
    /// <param name="other"></param>
    private void OnCollisionEnter(Collision other)
    {
        currentState.OnCollisionEnter(this);
    }

    /// <summary>
    /// Transition to new player concrete state, and run code in its "EnterState" method.
    /// </summary>
    /// <param name="state">Concrete state to transition to.</param>
    public void TransitionToState(PlayerBaseState state)
    {
        currentState = state;
        currentState.EnterState(this);
    }

    /// <summary>
    /// Simply sets the facial expression sprite.
    /// </summary>
    /// <param name="newExpression"></param>
    public void SetExpression(Sprite newExpression)
    {
        face.sprite = newExpression;
    }
}
