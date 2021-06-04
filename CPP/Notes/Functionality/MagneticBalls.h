// Copyright 2021, Alex Gulikers, 7 Minutes Dead.
// Although these are mostly notes for reference to myself, so you are welcome to pick it apart!

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "MagneticBalls.generated.h"


UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class ESCAPE_API UMagneticBalls : public UActorComponent
{
	GENERATED_BODY()

public:
	// Sets default values for this component's properties
	UMagneticBalls();

protected:
	// Called when the game starts
	virtual void BeginPlay() override;

public:
	UPROPERTY(EditAnywhere) AActor* DestinationObject;
	UPROPERTY(EditAnywhere) float MoveSpeed = 0.2f;
	UPROPERTY(EditAnywhere) float MaxFollowDistance = 20;
	float Distance;
	FVector Destination;
	FVector CurrentPosition;
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;


};
