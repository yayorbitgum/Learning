# https://leetcode.com/problems/range-sum-of-bst/
# Range Sum of BST.
# I had to reference this to solve it:
# https://www.tutorialspoint.com/python_data_structure/python_tree_traversal_algorithms.htm

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rangeSumBST(self, root: TreeNode, low: int, high: int) -> int:

        # ----------------------------------------------------------------------
        def gather_values(node: TreeNode):
            """Recursively grab all vals in a tree and add them to a list,
            if they're equal to or between low and high (solution to LC problem).
            Returns a list."""
            values = []

            if node:
                # First we'll grab the root value if there is one, then search left, then right.
                if low <= node.val <= high:
                    values.append(node.val)
                # Note to self: Here we don't need to pass in values recursively,
                # since it's being returned and added recursively.
                # Also note to self, we're essentially adding "values" + returned "values" here.
                values += gather_values(node.left)
                values += gather_values(node.right)

            return values

        # ----------------------------------------------------------------------
        result = 0
        for val in gather_values(root):
            result += val
        return result
