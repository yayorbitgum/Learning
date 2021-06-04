// Copyright 2021, Alex Gulikers, 7 Minutes Dead.
// Although these are mostly notes for reference to myself, so you are welcome to pick it apart!

#include "ItemGrabber.h"
#include "GameFramework/PlayerController.h"
#include "DrawDebugHelpers.h"
// To give myself a heads up that something is an out parameter.
#define OUT


// ----------------------------------------------------------------------
/// Sets default values for this component's properties.
UItemGrabber::UItemGrabber()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	// ...
}


// ----------------------------------------------------------------------
/// Called when the game starts.
void UItemGrabber::BeginPlay()
{
	Super::BeginPlay();
	NotifyLoading();
	Player = GetWorld()->GetFirstPlayerController();
	// GetPhysicsHandle();
	// ...
}


// ----------------------------------------------------------------------
/// Called every frame.
void UItemGrabber::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	// Get player's viewpoint and set it to our PlayerView data structure.
	Player->GetPlayerViewPoint(
		OUT PlayerView.Location,
		OUT PlayerView.Rotation);

	GetGrabbableObject();
	DebugLineStuff();

	// If key is pressed, grab object and move to set short distance in front of player.
	// If key is released, release object.
	// ...
}


// ----------------------------------------------------------------------
/// Do a line trace and see what object we can grab. Update GrabbableHit.
void UItemGrabber::GetGrabbableObject()
{
	// The max length point of the ray cast we want.
	// Player location + rotation * the length of grab.
	LineTraceEnd = PlayerView.Location + PlayerView.Rotation.Vector() * Reach;

	// Define what should be considered a collision for what can be grabbed.
	const FCollisionQueryParams TraceParameters(
		FName(TEXT("")),	// The tag name.
		false,				// Use complex collisions?
		GetOwner()			// Which objects to ignore (make sure the ray hitting ourselves doesn't count).
	);

	// LineTrace (raycast) from player to LineTraceEnd and see what we hit.
	GetWorld()->LineTraceSingleByObjectType(
		OUT GrabbableHit,
		PlayerView.Location,
		LineTraceEnd,
		FCollisionObjectQueryParams(ECC_PhysicsBody),
		TraceParameters
	);
}


void UItemGrabber::GetPhysicsHandle()
{
	// Get the PhysicsHandle component we added to the DefaultPawnBP.
	// UItemGrabber is also attached to DefaultPawnBP, so GetOwner will work for this too.
	// Since FindComponentByClass is a function template, we construct by <type>.
	// This will return the first UPhysicsHandleComponent found in the Owner (DefaultPawnBP).
	PhysicsHandle = GetOwner()->FindComponentByClass<UPhysicsHandleComponent>();

	if (!PhysicsHandle) {
		UE_LOG(LogTemp, Error,
			TEXT("%s has no Physics Handle Component (needed by ItemGrabber)!"),
			*GetOwner()->GetName()
		);
	}
}

// --------------------------------------------------------------------
// Debug helper functions.
// --------------------------------------------------------------------

/// Draw debug line for grabby hands, log grabbable object hit.
void UItemGrabber::DebugLineStuff()
{
	FColor Color;

	DrawDebugLine(
		GetWorld(),				 // InWorld.
		PlayerView.Location,	 // LineStart.
		LineTraceEnd,			 // LineEnd.
		Color.FromHex("00FF15"), // Color.
		false,					 // PersistentLines.
		1,						 // LifeTime.
		0,						 // DepthPriority
		2						 // Thickness.
	);

	// Checking if GrabbableHit has an actor yet,
	// should stop us from referencing a null pointer and crashing.
	if (GrabbableHit.GetActor()) {
		UE_LOG(LogTemp, Warning,
			TEXT("Grabbable object: %s"),
			*GrabbableHit.GetActor()->GetName()
		);
	}
}

/// Notify this component was loaded successfully.
void UItemGrabber::NotifyLoading()
{
	UE_LOG(LogTemp, Warning,
	TEXT("UItemGrabber loaded successfully on %s."),
	*GetOwner()->GetName()
);
}
