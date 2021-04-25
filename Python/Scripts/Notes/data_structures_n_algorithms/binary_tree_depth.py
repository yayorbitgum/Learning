

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: TreeNode) -> int:

        if root is None:
            return 0

        depth_left = self.maxDepth(root.left)
        depth_right = self.maxDepth(root.right)

        if depth_right > depth_left:
            return depth_right + 1
        else:
            return depth_left + 1


F = TreeNode(6, None, None)
E = TreeNode(5, None, None)
D = TreeNode(4, None, None)
C = TreeNode(3, None, F)
B = TreeNode(2, D, E)
A = TreeNode(1, B, C)
F.left = E
F.right = C

test = Solution()
print(test.maxDepth(A))