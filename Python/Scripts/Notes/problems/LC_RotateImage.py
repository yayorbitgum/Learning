# https://leetcode.com/explore/interview/card/top-interview-questions-easy/92/array/770/
# My solution ended up working before I expected it to lol.
# As in I guessed what I needed to do and it happened to work.
# Run time was 28ms on LC, so faster than average thankfully.
from typing import List


class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Rotates a 2D matrix 90 degrees in place.
        Essentially need to make horizontal rows vertical, and fill in right to left.
        """
        width = len(matrix[0])
        # This is only gonna work for square arrays..
        count = 0
        row = 0

        while row < width:
            for item in matrix[row]:
                try:
                    # Duplicate each row of pixels and append them to the ends of the rows.
                    matrix[count].append(item)
                    count += 1

                except IndexError:
                    # We reach the end of the row via index error, so we stop
                    # and we get rid of the original values we duplicated.
                    for _ in range(count):
                        matrix[row].pop(0)
                    row += 1
                    count = 0

        # The image is essentially mirrored at this point, so flip it.
        for row in matrix:
            row.reverse()


# Examples / Test input --------------------------------------------------------
example_a = [[1,2,3],           # [7,4,1]
             [4,5,6],           # [8,5,2]
             [7,8,9]]           # [9,6,3]

example_b = [[5,1,9,11],        # [15,13,2,5]
             [2,4,8,10],        # [14,3,4,1]
             [13,3,6,7],        # [12,6,8,9]
             [15,14,12,16]]     # [16,7,10,11

# Testing ----------------------------------------------------------------------
test = Solution()
test.rotate(example_a)
test.rotate(example_b)