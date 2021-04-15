# Count and say problem.
# https://leetcode.com/explore/featured/card/top-interview-questions-easy/127/strings/886/
# 33 222 5 1
# two 3s, three 2s, one 5, one 1
# 2 3s, 3 2s, 1 5, 1 1
# result = 23321511
#
# "Make an iterator that returns consecutive keys and groups from the iterable."
# https://docs.python.org/3.4/library/itertools.html#itertools.groupby
from itertools import groupby


class Solution:
    def countAndSay(self, n: int) -> str:
        result = '1'

        for _ in range(n - 1):
            accumulate = ''

            for digit, group in groupby(result):
                count = len(list(group))
                accumulate += f"{count}{digit}"

            result = accumulate

        return result


test = Solution()
print(test.countAndSay(10))