// Concrete State: Ducking.

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerDuckingState : PlayerBaseState
{
    private float elapsed;
    public override void EnterState(PlayerControllerFSM player)
    {
        player.SetFacialExpression(player.duckingSprite);
        player.Squat();
    }

    public override void Update(PlayerControllerFSM player)
    {
        // Do big jump if we jump from ducking.
        if (Input.GetButtonDown("Jump")){
            player.SitUp();
            player.Jump(player.jumpBoostMultiplier);
            player.TransitionToState(player.jumping);
        }

        if (Input.GetButtonUp("Duck")){
            player.TransitionToState(player.idle);
            player.SitUp();
        }
    }

    public override void OnCollisionEnter(PlayerControllerFSM player, Collision other)
    {
        player.TransitionToState(player.idle);
    }
}
