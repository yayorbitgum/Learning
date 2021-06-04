// Copyright 2021, Alex Gulikers, 7 Minutes Dead.
// Although these are mostly notes for reference to myself, so you are welcome to pick it apart!


#include "MagneticBalls.h"
#include "Components/PrimitiveComponent.h"

// Sets default values for this component's properties
UMagneticBalls::UMagneticBalls()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	// ...
}


// Called when the game starts
void UMagneticBalls::BeginPlay()
{
	Super::BeginPlay();

	if (!DestinationObject){
		const FString ThisBall = GetOwner()->GetName();
		UE_LOG(LogTemp, Error, TEXT("Magnetic Ball '%s' is missing destination!"), *ThisBall);
	}
	// ...

}


// Called every frame
void UMagneticBalls::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	if (DestinationObject) {
		CurrentPosition = GetOwner()->GetTransform().GetLocation();
		Destination = DestinationObject->GetTransform().GetLocation();

		Distance = GetOwner()->GetDistanceTo(DestinationObject);

		if (Distance >= MaxFollowDistance) {
			GetOwner()->SetActorLocation(FMath::VInterpTo(CurrentPosition, Destination, DeltaTime, MoveSpeed));
		}
	}

	// ...
}
