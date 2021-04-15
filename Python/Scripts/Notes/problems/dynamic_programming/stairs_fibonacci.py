# https://leetcode.com/problems/climbing-stairs/
# after 1, each one is the sum of the previous two. How about that.
# stairs: 1, 2, 3, 4, 5,  6,  7,  8,  9, 10
# ways:   1, 2, 3, 5, 8, 13, 21, 34, 55, 89

class Solution:
    def climbStairs(self, n: int):
        answers = [num for num in range(1, n+1)]
        if n in (1, 2, 3):
            return n

        for num in range(3, n):
            try:
                # Just sum the previous two step counts.
                answers[num] = answers[num - 1] + answers[num - 2]
            except IndexError:
                break

        return answers[n-1]


stairs = [num for num in range(1, 11)]
ways = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

cs = Solution()
for stairs, ways in zip(stairs, ways):
    print(f"{stairs} stairs, expected {ways}, got {cs.climbStairs(stairs)}")