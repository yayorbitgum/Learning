from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        # Must modify in place without making copy of array.
        indices = []
        for index, num in enumerate(nums):
            if num == 0:
                indices.append(index)

        # This way we can pop from nums and append them onto the end
        #   without breaking the for loop.
        # Essentially iterating over the 0s in nums in reverse.
        indices.reverse()
        for index in indices:
            nums.append(nums.pop(index))

        print(nums)


ex1 = [0, 1, 0, 3, 12]
test = Solution()
test.moveZeroes(ex1)