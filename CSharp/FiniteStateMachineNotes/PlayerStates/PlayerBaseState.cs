// This is the Abstract State!

/*
 -----------------------
 Declaring methods here says we need to implement these in our classes derived from this class.
 PlayerController_FSM (as player) is acting as the Context for our state machine.
 By passing it as a parameter to these methods, you're providing the concrete implementations
 of State with a reference to this player Context.
 
 A reference isn't required by the FSM pattern, but it is required in our use case.
 But it's just as valid to make methods that take parameters of different types, or
 no parameters at all.
 
*/
using UnityEngine;

// Abstract means it's a blueprint for any classes made using this.
// This can't be directly instantiated, only derived from.
public abstract class PlayerBaseState
{
    public abstract void EnterState(PlayerControllerFSM player);
    public abstract void Update(PlayerControllerFSM player);
    public abstract void OnCollisionEnter(PlayerControllerFSM player);
}