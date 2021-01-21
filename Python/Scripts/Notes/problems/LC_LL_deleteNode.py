# https://leetcode.com/explore/interview/card/top-interview-questions-easy/93/linked-list/553/
# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def deleteNode(self, node: ListNode):
        """
        :type node: ListNode
        :rtype: void Do not return anything, modify node in-place instead.
        """

        if node is None:
            # We can't delete the very last node without knowing what the head is.
            # The question accounts for this, but I want to put this here anyway.
            return

        # Duplicate the values of the next node, then skip over the next node.
        # Effectively replacing current node with next node, then making next node
        # the "next next" node.
        current = node
        current.val = current.next.val
        # I love that I can do current.next.next for linked nodes lol.
        third = current.next.next
        current.next = third