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
    public PlayerBaseState CurrentState{ get; private set; }
    public Rigidbody Rigidbody{ get; private set; }

    // Instantiating concrete states.
    /// <summary>
    /// Idle state for player.
    /// </summary>
    public readonly PlayerIdleState idle = new PlayerIdleState();
    /// <summary>
    /// Jumping state for player.
    /// </summary>
    public readonly PlayerJumpingState jumping = new PlayerJumpingState();
    /// <summary>
    /// Ducking state for player.
    /// </summary>
    public readonly PlayerDuckingState ducking = new PlayerDuckingState();
    /// <summary>
    /// Spinning state for player.
    /// </summary>
    public readonly PlayerSpinningState spinning = new PlayerSpinningState();
    
    // Example variables.
    public float jumpForce;
    public float jumpBoostMultiplier;
    public Transform head;
    public Transform weapon01;
    public Transform weapon02;
    private bool isSquatting;

    public Sprite idleSprite;
    public Sprite duckingSprite;
    public Sprite jumpingSprite;
    public Sprite spinningSprite;
    public float spinMultiplier;

    private SpriteRenderer face;

    /// <summary>
    /// Get references to our object's SpriteRenderer and Rigidbody. SetFacialExpression to idleSprite.
    /// Awake is called when the script instance is being loaded.
    /// </summary>
    private void Awake()
    {
        face = GetComponentInChildren<SpriteRenderer>();
        Rigidbody = GetComponent<Rigidbody>();
        SetFacialExpression(idleSprite);
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
        CurrentState.Update(this);
    }

    /// <summary>
    /// Run the CollisionEnter method for the current concrete state.
    /// </summary>
    /// <param name="other"></param>
    private void OnCollisionEnter(Collision other)
    {
        CurrentState.OnCollisionEnter(this, other);
    }

    /// <summary>
    /// Transition to new player concrete state, and run code in its "EnterState" method.
    /// </summary>
    /// <param name="state">Concrete state to transition to.</param>
    public void TransitionToState(PlayerBaseState state)
    {
        CurrentState = state;
        CurrentState.EnterState(this);
    }

    /// <summary>
    /// Simply sets the facial expression sprite.
    /// </summary>
    /// <param name="newExpression"></param>
    public void SetFacialExpression(Sprite newExpression)
    {
        face.sprite = newExpression;
    }

    // ---------------------------------------------------------------------------------------
    // Still debating whether these methods should be isolated in each State instead.
    /// <summary>
    /// Add upward force to PlayerFSM's Rigidbody. Add additional boost boost optionally.
    /// </summary>
    /// <param name="boost">Extra boost. Defaults to 1 if left blank (1 provides no extra boost).</param>
    public void Jump(float boost = 1f)
    {
        Rigidbody.AddForce(Vector3.up * (jumpForce * boost));
    }

    public void Squat()
    {
        if (isSquatting)
            return;

        isSquatting = true;
        head.Translate(Vector3.down * 0.5f);
    }

    public void SitUp()
    {
        if (isSquatting)
            head.Translate(Vector3.up * 0.5f);

        isSquatting = false;
    }

    public void SpinMove()
    {
        spinMultiplier += 10f;
        Rigidbody.AddForce(Vector3.up * 50);
        Rigidbody.AddTorque(new Vector3(0, spinMultiplier, 0), ForceMode.Impulse);
    }
}
