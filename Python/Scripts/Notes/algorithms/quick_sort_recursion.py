# A simple version of quicksort, with some recursion!
import random


# ------------------------------------------------------------------------------
def quicksort(array: list):
    """ Keep splitting "array" into smaller lists until they're sorted."""

    if len(array) < 2:
        # If this current array is 0 or 1 items then it's definitely
        # as sorted as it can get.
        return array

    # Seems like it'd be best to split each part in the middle.
    midpoint = len(array) // 2
    # Pop out the pivot so we don't duplicate it as we keep splitting.
    pivot = array.pop(midpoint)
    # Continually split lists into left/right for less/more, until they're
    # smaller than 2 items, and thus sorted!
    left = [item for item in array if item <= pivot]
    right = [item for item in array if item > pivot]
    # Visualization of splitting/sorting process.
    print(f"{left} <--- {pivot} ---> {right}".center(80))

    return quicksort(left) + [pivot] + quicksort(right)


# ------------------------------------------------------------------------------
test = random.sample(range(1, 560), 10)
print(f"Sort this! {test}\n".center(80))
print(f"Sorted: {quicksort(test)}".center(80))