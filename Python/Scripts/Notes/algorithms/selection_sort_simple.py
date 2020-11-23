# This is a simple selection sort.
import random


# ------------------------------------------------------------------------------
def find_smallest(stuff):
    """Returns the index of the smallest item in the input list."""
    smallest_item = stuff[0]
    smallest_index = 0

    for index in range(1, len(stuff)):
        if stuff[index] < smallest_item:
            smallest_item = stuff[index]
            smallest_index = index
    return smallest_index


# ------------------------------------------------------------------------------
def selection_sort(stuff):
    sorted_stuff = []

    for _ in range(len(stuff)):
        smallest_index = find_smallest(stuff)
        sorted_stuff.append(stuff.pop(smallest_index))
    return sorted_stuff


# ------------------------------------------------------------------------------
test = random.sample(range(1, 11), 10)
print(test)
print(selection_sort(test))