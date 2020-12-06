# To learn how to figure this out, I had to follow along with this video:
# https://www.youtube.com/watch?v=lKuK69-hMcc
# And just translate the reasoning into python.


def intersect(smaller_list, larger_list):
    intersections = []
    smaller_counts = {}

    if len(smaller_list) > len(larger_list):
        # We'll ensure the first list is always the smallest. Just swap'em!
        return intersect(larger_list, smaller_list)

    for thing in smaller_list:
        # Using a dictionary to keep counts of each element.
        smaller_counts[thing] = smaller_list.count(thing)

    for element in larger_list:
        try:
            if smaller_counts[element] > 0:
                intersections.append(element)
                # If we found a match in this list, we should decrement it from
                # the other list, ie decrement the count from the dictionary
                # we setup to count items from the first list.
                # This ensures counting full intersections and no extra.
                smaller_counts[element] -= 1
        except KeyError:
            # This just means the element checked in larger_list wasn't anywhere
            # in smaller_list, so no key is present for it in the dictionary.
            pass

    return intersections


# Quick test data --------------------------------------------------------------
test_a = ['x', 'y', 'y', 'x', 'x', 'y']
test_b = ['y', 'y', 'z', 'x', 'x']
# Should give two ys and two xs.
test_c = [1, 2, 2, 1]
test_d = [2, 2]
# Should give [2, 2].
test_e = [4, 9, 5]
test_f = [9, 4, 9, 8, 4]
# Should give [4, 9] or [9, 4].
print(intersect(test_a, test_b))
print(intersect(test_c, test_d))
print(intersect(test_e, test_f))