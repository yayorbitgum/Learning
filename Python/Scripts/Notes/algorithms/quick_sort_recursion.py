# A simple version of quicksort, with some recursion!
import random


# ------------------------------------------------------------------------------
def quicksort(array: list, side='Initial') -> list:
    """
    Keep splitting "array" into smaller lists until they're sorted.
    "side" is just used for visualization of sorting in console.
    """
    if len(array) < 2:
        # If current array is one thing or less, then it's definitely sorted. (base case)
        return array

    # Seems like it'd be best to split each part in the middle.
    midpoint = len(array) // 2
    # Pop out the pivot so we don't duplicate it as we keep splitting.
    pivot = array.pop(midpoint)
    # Continually split lists into left/right until we reach base case.
    left = [item for item in array if item <= pivot]
    right = [item for item in array if item > pivot]
    # Visualization of splitting/sorting process.
    print(f"⮡ {side}: "
          f"{left if left else '░░░'} "
          f"<--- {pivot} ---> "
          f"{right if right else '░░░'}".center(80))

    # Recursive return.
    return quicksort(left, 'Left') + [pivot] + quicksort(right, 'Right')


# ------------------------------------------------------------------------------
test = random.sample(range(10, 99), 20)
print(f"Sorting this: {test}\n")
print(f"\nSorted: {quicksort(test)} 🚀")
