// Concrete State: Idle.

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerIdleState : PlayerBaseState
{
    // -----------------------------------------------------------------
    // Upon entering the idle state..
    public override void EnterState(PlayerControllerFSM player)
    {
        player.spinMultiplier = 1;
        player.SetFacialExpression(player.idleSprite);
    }

    // -----------------------------------------------------------------
    public override void Update(PlayerControllerFSM player)
    {
        if (Input.GetButtonDown("Jump")){
            player.TransitionToState(player.jumping);
        }

        if (Input.GetButton("Duck")){
            player.SetFacialExpression(player.duckingSprite);
            player.TransitionToState(player.ducking);
        }
    }

    // -----------------------------------------------------------------
    public override void OnCollisionEnter(PlayerControllerFSM player, Collision other)
    {
        
    }
}
