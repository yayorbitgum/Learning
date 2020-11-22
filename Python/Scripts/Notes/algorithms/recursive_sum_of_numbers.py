# Practicing recursion! Take a look.
from random import randint
import sys


# ------------------------------------------------------------------------------
def add_me_up(nums: list, total=0):
    """Adds up a list of integers recursively!
    Returns the sum of all the numbers in the provided list "nums"."""
    running_total = nums.pop() + total
    if not nums:
        # If the list of nums is empty from all that poppin', we have our answer.
        return running_total

    return add_me_up(nums, running_total)


# ------------------------------------------------------------------------------
def run_tests(amount):
    """
    Runs the add_me_up() function "amount" of times and displays each result.
    """
    count = 0
    for _ in range(amount):
        count += 1
        low = randint(1, 1000)
        high = randint(low+1, low+1000)
        test = [num for num in range(low, high)]
        print(f"Sum of numbers from {low:,} to {high:,} is {add_me_up(test):,}.")

    print(f"{count} tests ran!")


# ------------------------------------------------------------------------------
# For the sake of testing large number ranges that exceed 1000,
# Python's default recursion depth limit,
# I'm going to increase that limit.
sys.setrecursionlimit(2001)
test_amount = randint(1000, 10000)
run_tests(test_amount)