// Copyright 2021, Alex Gulikers, 7 Minutes Dead.
// Although these are mostly notes for reference to myself, so you are welcome to pick it apart!


#include "OpenDoor.h"
#include "BehaviorTree/BehaviorTreeTypes.h"
#include "GameFramework/Actor.h"
#include "Math/UnrealMathUtility.h"

// -------------------------------------------------------------------------------
// Sets default values for this component's properties.
UOpenDoor::UOpenDoor()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.
	// You can turn these features off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;
	// ...
}

// -------------------------------------------------------------------------------
// Called when the game starts.
void UOpenDoor::BeginPlay()
{
	Super::BeginPlay();
	Elapsed = 0;
	DoorRotation = GetOwner()->GetActorRotation();
	ClosedDoorPos = DoorRotation.Yaw;
	OpenDoorPos = DoorRotation.Yaw + OpenAngle;
	PlayerPawn = GetWorld()->GetFirstPlayerController()->GetPawn();
	// ...

	if (!PressurePlate) {
		FString CheckMe = GetOwner()->GetName();
		UE_LOG(LogTemp, Error, TEXT("Pressure Plate hasn't been set for %s! Check OpenDoor component."), *CheckMe);
		RequestEngineExit("No pressure plate set. See Error message.");
	}
}


// -------------------------------------------------------------------------------
// Called every frame.
void UOpenDoor::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	// ----------------------------------------------------------------
	// If we execute this without PressurePlate object being set in the editor, the engine will crash from null pointer.
	if (PressurePlate->IsOverlappingActor(PlayerPawn)) {
		Elapsed = 0;
		OpenTheDoor(DeltaTime);
	}
	else {
		// Start our door closing timer as soon as the player steps out of the trigger.
		Elapsed += DeltaTime;
		if (Elapsed > DoorOpenTime) {
			CloseTheDoor(DeltaTime);
		}
	}
}

// -------------------------------------------------------------------------------
/// Smoothly open the door towards TargetYawAdjustment.
void UOpenDoor::OpenTheDoor(float DeltaTime)
{
	DoorRotation = GetOwner()->GetActorRotation();
	// FInterpTo gives us a framerate-independent Lerp, by allowing us to pass in DeltaTime too.
	SmoothedTargetRotation.Yaw = FMath::FInterpTo(DoorRotation.Yaw, OpenDoorPos, DeltaTime, OpenRate);
	GetOwner()->SetActorRotation(SmoothedTargetRotation);
}

// -------------------------------------------------------------------------------
/// Smoothly close the door back towards StartingYaw position.
void UOpenDoor::CloseTheDoor(float DeltaTime)
{
	DoorRotation = GetOwner()->GetActorRotation();
	SmoothedTargetRotation.Yaw = FMath::FInterpTo(DoorRotation.Yaw, ClosedDoorPos, DeltaTime, OpenRate);
	GetOwner()->SetActorRotation(SmoothedTargetRotation);
}
