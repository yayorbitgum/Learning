# Away from the top of my monitor ye text


# ////////////////////////////////////////////////////////
# ////////////////////////
# /////////// Overall Challenges for While loops and input
# http://introtopython.org/while_input.html#Gaussian-Addition
#
# Gaussian Addition
#
#
# - Write a program that passes a list of numbers to a function.
# - The function should use a while loop to keep popping the first and 
#       last numbers from the list and calculate the sum of those two numbers.
# - The function should print out the current numbers that are being added, 
#       and print their partial sum.
# - The function should keep track of how many partial sums there are.
# - The function should then print out how many partial sums there were.
# - The function should perform Gauss' multiplication, and report the final 
#       answer.
# - Prove that your function works, by passing in the range 1-100, 
#       and verifying that you get 5050.
# - Your function should work for any set of consecutive numbers, as long as 
#       that set has an even length.
# - Bonus: Modify your function so that it works for any set of consecutive 
#       numbers, whether that set has an even or odd length.

GaussianList = list(range(1, 302))
CountedList = []


def gaussian_calculation(gausslist):
    partial_sum_count = 0
    running_count = 0

    while len(gausslist) > 0:
        first_number = gausslist.pop(0)
        # This will stop second pop from happening for end of odd numbered range.
        # IE: we just popped the last item above and now the list is empty.
        if len(gausslist) > 0:
            last_number = gausslist.pop(-1)

        partial_sum = first_number + last_number
        CountedList.append(partial_sum)
        partial_sum_count = partial_sum_count + 1

        print(f"Adding together {first_number} and {last_number}. Result: {partial_sum} ")
        print(f"There are currently {partial_sum_count} partial sums. ")

    if len(gausslist) == 0:
        while len(CountedList) > 0:
            add_me = CountedList.pop(0)
            # Adjust the running count back down. If it's not zero, we know we missed pairs
            running_count = running_count + add_me
            partial_sum_count = partial_sum_count - 1

    if len(CountedList) == 0:
        print(f"The final running count is {running_count}")

        if partial_sum_count == 0:
            print("No partial sums remaining. Gottem all!")


gaussian_calculation(GaussianList)
