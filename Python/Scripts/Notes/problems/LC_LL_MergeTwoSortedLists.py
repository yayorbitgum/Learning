# https://leetcode.com/explore/interview/card/top-interview-questions-easy/93/linked-list/771/
# Merge two sorted linked lists.
# This is a recursive solution but was the one I could understand the best.


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:

        # If one node is empty, then there's nothing to sort so just return the other list.
        # This should be the base case.
        # If both lists are empty then we'll just get an empty list back.
        if l1 is None:
            return l2
        if l2 is None:
            return l1

        # Modifies the lists in place, essentially tossing them back and forth.
        # This way, the next value as we merge them recursively should always be the next lowest value.
        if l1.val < l2.val:
            l1.next = self.mergeTwoLists(l1.next, l2)
            return l1
        else:
            l2.next = self.mergeTwoLists(l2.next, l1)
            return l2