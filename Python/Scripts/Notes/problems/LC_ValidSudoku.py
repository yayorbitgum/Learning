# https://leetcode.com/explore/interview/card/top-interview-questions-easy/92/array/769/
# Even though my solution is very verbose, the solution time was quicker than average,
# and memory usage was average it seems, at 14mb.

from typing import List


class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        """ Check if a sudoku board is valid, regardless if fully solved."""

        def validate_length(nums):
            """Ensures no duplicate numbers in array."""
            if len(nums) != len(set(nums)):
                print('Invalid board or solution.')
                print(nums)
                return False
            return True

        # Horizontal verification. ---------------------------------------------
        for row in board:
            filled = [num for num in row if num != '.']
            if not validate_length(filled):
                return False

        # Vertical verification. -----------------------------------------------
        for index in range(len(board)):
            filled = []
            for row in board:
                if row[index] != '.':
                    filled.append(row[index])
            if not validate_length(filled):
                return False

        # 3x3 block verification. ----------------------------------------------
        def blocks_to_rows(arr, start, row_start):
            """
            Take in 3x3 blocks and convert them to a single list to verify.
            arr: The board.
            s: Start index.
            e: End index.
            """
            block = []
            for i in range(start, start+3):
                block.extend([num for num in arr[i][row_start:row_start+3] if num != '.'])
            print(f"Block: {block}")
            return block

        # There has to be a better way..
        block_a = blocks_to_rows(board, 0, 0)
        block_b = blocks_to_rows(board, 0, 3)
        block_c = blocks_to_rows(board, 0, 6)

        block_d = blocks_to_rows(board, 3, 0)
        block_e = blocks_to_rows(board, 3, 3)
        block_f = blocks_to_rows(board, 3, 6)

        block_g = blocks_to_rows(board, 6, 0)
        block_h = blocks_to_rows(board, 6, 3)
        block_i = blocks_to_rows(board, 6, 6)

        blocks = [block_a, block_b, block_c,
                  block_d, block_e, block_f,
                  block_g, block_h, block_i]

        for block in blocks:
            if not validate_length(block):
                return False

        # If all checks passed above, then the sudoku board is valid.
        return True


ex1 = [["5","3",".",".","7",".",".",".","."],
       ["6",".",".","1","9","5",".",".","."],
       [".","9","8",".",".",".",".","6","."],
       ["8",".",".",".","6",".",".",".","3"],
       ["4",".",".","8",".","3",".",".","1"],
       ["7",".",".",".","2",".",".",".","6"],
       [".","6",".",".",".",".","2","8","."],
       [".",".",".","4","1","9",".",".","5"],
       [".",".",".",".","8",".",".","7","9"]]

ex2 = [["8","3",".",".","7",".",".",".","."],
       ["6",".",".","1","9","5",".",".","."],
       [".","9","8",".",".",".",".","6","."],
       ["8",".",".",".","6",".",".",".","3"],
       ["4",".",".","8",".","3",".",".","1"],
       ["7",".",".",".","2",".",".",".","6"],
       [".","6",".",".",".",".","2","8","."],
       [".",".",".","4","1","9",".",".","5"],
       [".",".",".",".","8",".",".","7","9"]]
test = Solution()

test.isValidSudoku(ex1)
test.isValidSudoku(ex2)