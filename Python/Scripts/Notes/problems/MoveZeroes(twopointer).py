from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]):
        reader = 0

        for writer in range(len(nums)):
            if nums[writer] != 0 and nums[reader] == 0:
                # https://www.youtube.com/watch?v=19ulSNSRKyU
                nums[writer], nums[reader] = nums[reader], nums[writer]

            if nums[reader] != 0:
                reader += 1

        return nums


test_list = [0,1,0,3,12]
expected = [1,3,12,0,0]
test = Solution()
result = test.moveZeroes(test_list)

try:
    assert result == expected
except AssertionError:
    print(f"Expected: {expected}")
    print(f"Result: {result}")