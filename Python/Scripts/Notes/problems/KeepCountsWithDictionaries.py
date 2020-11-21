# For my reference, things learned from this problem:
# https://www.codewars.com/kata/554ca54ffa7d91b236000023
#
# Needed a way to keep a running count for each item in a list that
# passed through, because the order of the items could not be changed.
# So I'd have to know how many times "4" has appeared, as we're iterating through
# the list, for example, to know when to not include further occurrences of "4".

def delete_nth(order: list, max_e):
    # Using dictionary to make running counts so we can maintain order.
    seen = {}
    filtered = []

    for current in order:
        if current in seen:
            # Only way I could think to iterate up.
            count = seen[current]
            count += 1
            seen[current] = count
        else:
            # Now we have a counter for each individual number!
            seen[current] = 1

        # Make sure our current number's counter hasn't gone past our max.
        if seen[current] <= max_e:
            filtered.append(current)

    return filtered


test = [4, 6, 10, 4, 4, 5]
print(delete_nth(test, 2))