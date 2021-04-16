# From reading "Grokking Algorithms" book.

def binary_search(items: list, item):
    """ Uses binary search to find the index of "item".
        Prints current search range each step.
        Returns the index and the number of steps taken."""
    items.sort()
    lowest_index = 0
    highest_index = len(items) - 1
    count = 0

    # Continuously cut our search range in half until we find our match.
    while lowest_index <= highest_index:
        count += 1
        middle = (lowest_index + highest_index) // 2
        guess = items[middle]
        print(f"Between: {lowest_index} and {highest_index}")

        if guess == item:
            return middle, f"{count} steps taken"
        if guess > item:
            highest_index = middle - 1
        else:
            lowest_index = middle + 1


# Making a list of 500 million numbers takes about 20gb of RAM hahaha.
# TODO: Generate large list file / database on drive and stream in sections instead.
test = [num for num in range(0, 500_000)]
print(binary_search(test, 35))

