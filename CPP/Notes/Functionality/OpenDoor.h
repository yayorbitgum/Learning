// Copyright 2021, Alex Gulikers, 7 Minutes Dead.
// Although these are mostly notes for reference to myself, so you are welcome to pick it apart!
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "Engine/TriggerVolume.h"
#include "Math/Rotator.h"
#include "OpenDoor.generated.h"


UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class ESCAPE_API UOpenDoor : public UActorComponent
{
	GENERATED_BODY()

public:
	// -------------------------------------------------------------------------
	// Sets default values for this component's properties
	UOpenDoor();

protected:
	// -------------------------------------------------------------------------
	// Called when the game starts
	virtual void BeginPlay() override;

public:
	// -------------------------------------------------------------------------
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
	// -------------------------------------------------------------------------
	void OpenTheDoor(float DeltaTime);
	void CloseTheDoor(float DeltaTime);
	float ClosedDoorPos;
	float OpenDoorPos;

	UPROPERTY(EditAnywhere) float OpenAngle = 90;

	FRotator DoorRotation;
	FRotator SmoothedTargetRotation;

	UPROPERTY(EditAnywhere) float OpenRate = 1;
	UPROPERTY(EditAnywhere) float DoorOpenTime = 1;
	UPROPERTY(EditAnywhere) ATriggerVolume* PressurePlate;
	UPROPERTY(EditAnywhere) APawn* PlayerPawn;
	float Elapsed;

};
