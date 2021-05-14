// Concrete State: Spinning.

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerSpinningState : PlayerBaseState
{
    public override void EnterState(PlayerControllerFSM player)
    {
        player.SetFacialExpression(player.spinningSprite);
        player.SpinMove();
    }

    public override void Update(PlayerControllerFSM player)
    {
        if (Input.GetButtonDown("Duck")){
            // Keep hitting duck for boost!
            player.SpinMove();
        }
    }

    public override void OnCollisionEnter(PlayerControllerFSM player, Collision other)
    {
        player.TransitionToState(player.idle);
    }
}
