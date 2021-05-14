// Concrete State: Jumping.

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerJumpingState : PlayerBaseState
{
    public override void EnterState(PlayerControllerFSM player)
    {
        // Apply jump force when we enter this state.
        player.Jump();
        player.SetFacialExpression(player.jumpingSprite);
    }

    public override void Update(PlayerControllerFSM player)
    {
        // Hitting duck/C while midair will do a spin move SPIN MOVE.
        if (Input.GetButtonDown("Duck")){
            player.TransitionToState(player.spinning);
        }
    }

    public override void OnCollisionEnter(PlayerControllerFSM player, Collision other)
    {
        player.TransitionToState(player.idle);
    }
}
