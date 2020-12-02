# https://leetcode.com/explore/featured/card/top-interview-questions-easy/92/array/727/
from typing import List

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        # All for the sake of modifying in place:
        # Pop in loop will skip some, so we call this function recursively
        # if length != Python's set. This is so dumb and slow but it was accepted hahah.
        no_dupes = set(nums)
        if len(no_dupes) != len(nums):
            for i, num in enumerate(nums):
                if nums.count(num) > 1:
                    nums.pop(i)
            self.removeDuplicates(nums)

        return len(nums)