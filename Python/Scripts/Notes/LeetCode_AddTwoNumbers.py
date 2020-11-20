# https://leetcode.com/problems/add-two-numbers/
# I have no idea how to create a linked list out of this "ListNode" class.
# I don't understand this problem yet.


class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):

    def __init__(self):
        self.node_list = []

    # --------------------------------------------------------------------------
    def addTwoNumbers(self, node_a, node_b):
        """Takes in two reversed linked lists, adds them together, outputs list."""
        list_a = self.unpack_nodes(node_a)
        # Reset self.node_list so list_a and _b aren't duplicated and identical.
        # This is dumb but works for now.
        self.node_list = []
        list_b = self.unpack_nodes(node_b)

        # The problem wants us to reverse the numbers then add them together.
        list_a.reverse()
        list_b.reverse()

        # I need to describe this to myself because I have a hard time reading what I came up with here.
        # Unpacking the list of numbers to strings, joining them together, then converting to integer.
        number1 = int(''.join([str(number) for number in list_a]))
        number2 = int(''.join([str(number) for number in list_b]))
        # Adding the two full numbers together, convert to string, split digits out
        # to a list with a list comprehension as we convert each digit to int.
        result = [int(digit) for digit in (str(number1 + number2))]
        result.reverse()

        return self.pack_nodes(result)

    # --------------------------------------------------------------------------
    def unpack_nodes(self, node):
        """ Unpacks this problem's ListNode class recursively into a list."""
        if node is not None:
            self.node_list.append(node.val)
            self.unpack_nodes(node.next)

        return self.node_list

    # --------------------------------------------------------------------------
    def pack_nodes(self, list_input):
        # TODO!
        pass