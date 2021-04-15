# https://leetcode.com/explore/interview/card/top-interview-questions-medium/103/array-and-strings/776/
# So, we essentially need to find three numbers x, y, and z such that
#   they add up to the given value. If we fix one of the numbers say x,
#   we are left with the two-sum problem at hand!
#
# TODO: Have to account for duplicate searches.
#  Takes too long to finish last 3 test cases for leetcode.

from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        if len(nums) < 3:
            return []

        nums.sort()
        # Three pointers.
        px = 0
        py = 1
        pz = 2
        # Three numbers.
        x = nums[px]
        y = nums[py]
        z = nums[pz]
        results = []
        length = len(nums)

        if x + y + z == 0:
            results.append([x, y, z])

        # We'll keep running this loop and finding triplets until all 3 pointers
        # reach the end of nums and none of them can push up any farther.
        while (px, py, pz) != (length - 3, length - 2, length - 1):

            # We found a valid triplet. Make sure we don't already have this combo.
            if x + y + z == 0 and [x, y, z] not in results:
                results.append([x, y, z])

            # If pointer z has reached the end, then we need to move up pointer y
            # and set pointer z just ahead of it.
            if pz == len(nums) - 1:
                py += 1
                pz = py + 1
                try:
                    y = nums[py]
                    z = nums[pz]
                except IndexError:
                    # If pointer y has now reached the end (so pointer z gives error),
                    # we know it's time to move pointer x up, and move the others back down.
                    px += 1
                    py = px + 1
                    pz = py + 1
                    x = nums[px]
                    y = nums[py]
                    z = nums[pz]
            else:
                # If pointer z hasn't reached the end yet, we just keep moving it up.
                pz += 1
                z = nums[pz]

        return results


test_nums = [-1,0,1,2,-1,-4]
test = Solution()
print(test.threeSum(test_nums))