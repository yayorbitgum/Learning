# Linked List example and notes for reference.
# ------------------------------------------------------------------------------
class Node:
    """ A single node that stores some data,
    then points to the next node in the list."""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """ A linked list of nodes with some methods to manipulate that list."""
    def __init__(self):
        self.head_node = None

    # --------------------------------------------------------------------------
    def print_list(self):
        """Print the data of all linked nodes."""
        current = self.head_node

        while current:
            print(current.data)
            current = current.next

    # --------------------------------------------------------------------------
    def push(self, new_data):
        """Creates a new node with new data at the front of the list.
        O(1) since we always know what the head node is."""
        new_node = Node(new_data)
        # Set old head node as the next for this new one.
        # (since old head_node is gonna be second node in the list now)
        new_node.next = self.head_node
        # And *then* make this new node the new head node.
        self.head_node = new_node

    # --------------------------------------------------------------------------
    def insert_after(self, prev_node, new_data):
        """ Adds a new node after another existing node.
        O(1) since we know what node to insert after."""
        # Make sure previous node exists.
        if prev_node is None:
            print(f"The provided previous node is not in this LinkedList.")
            return

        new_node = Node(new_data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    # --------------------------------------------------------------------------
    def append(self, new_data):
        """ Adds a new node to the end of the linked list.
        O(n) since we have to traverse the whole list from the start.
        This method can also be optimized to work in O(1) by keeping
        an extra pointer to tail of linked list."""
        new_node = Node(new_data)
        # If the linked list is empty, then make the new node the head.
        if self.head_node is None:
            self.head_node = new_node
            return
        # Otherwise we need to traverse the list until we reach the last node.
        last_node = self.head_node
        while last_node.next:
            last_node = last_node.next
        # Now we can add our new node to the end since we found the last node.
        last_node.next = new_node

    # --------------------------------------------------------------------------
    def delete_node(self, target):
        """ Delete the first occurrence of target in the LinkedList."""
        # Grab the head node.
        current = self.head_node
        # If head_node holds the target to be deleted.
        if current.data == target and current is not None:
            self.head_node = current.next
            return
        # Otherwise search for the target to delete, and keep track of
        # the previous node since we need to change prev.next.
        while current is not None:
            if current.data == target:
                break
            prev = current
            current = current.next

        # If target isn't even in the list.
        if current is None:
            print(f"{target} isn't in this list.")
            return

        # Unlink the node from the linked list.
        prev.next = current.next


# ------------------------------------------------------------------------------
llist = LinkedList()
llist.head_node = Node("1: Some stuff.")
second_node = Node("2: Some other data.")
third_node = Node("3: Some more data.")

llist.head_node.next = second_node
second_node.next = third_node

# Testing out methods.
llist.append('4: Smelly end appended data.')
llist.push('5: Save the best for first with a push to the front!')
llist.push('6: Actually, this data is better. Push me to the front after.')
llist.insert_after(llist.head_node.next, '7: Put me after the node that is after the head node please.')
llist.append('8: This data also smells, put this at the end too.')

# Testing out deleting nodes.
llist.delete_node("3: Some more data.")
llist.delete_node('7: Put me after the node that is after the head node please.')
llist.delete_node('9: Mystery data')

llist.print_list()
