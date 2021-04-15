# Connectivity problem.
# https://www.coursera.org/learn/algorithms-part1/lecture/EcF3P/quick-find
# "Find" query - Check if two objects are in the same component.
# "Union" command - Replace components containing two objects with their union.
#
# Quick-find is too slow for huge arrays,
#   where every node points to one common connection, done with one slow for loop.
#   You have to check EVERY element in the list to see if they're connected.
#
# Quick-union is a better, lazy approach, but is also too slow,
#   where each connection is a tree with a common root node, and you only
#   connect roots to each other when joining with union().
#   Trees can get too tall and then it's slow to work through entire branch
#   just to get one value.
#
# Weighted quick-union would be:
#   Modify quick-union to avoid tall trees.
#   Keep track of size of each tree (number of objects/nodes).
#   Balance by linking root of smaller tree to root of larger tree.

class QuickFind:
    def __init__(self, node_count):
        self.node_count = node_count
        self.nodes = [node for node in range(0, node_count)]

    def verify_indexes(self):
        """ Print current index/nodes list (indicating connections)."""
        for index, node in enumerate(self.nodes):
            print(f"{index} connects to {node}")

    def is_connected(self, node_a, node_b):
        """ Check if two nodes are connected. Return True if so."""
        if self.nodes[node_a] == self.nodes[node_b]:
            return True
        return False

    def union(self, node_a, node_b):
        """ Connect the two provided nodes."""
        first_node = self.nodes[node_a]
        second_node = self.nodes[node_b]
        # We want every node to connect to a common point if there are multiple
        # unions, so we for loop over every index that has the first provided node,
        # and change it to the second provided node. That means every node will
        # link that is already linked before. That means this is slow.
        for index, node in enumerate(self.nodes):
            if self.nodes[index] == first_node:
                self.nodes[index] = second_node


class QuickUnion:
    def __init__(self, node_count: int):
        """
        Construct node relationships using indexes as pointers.
        So, nodes must always be integers >= 0.
        Example: index [1] with a value of 1 means node "1" is a root.
        Index [2] with a value of 3 means node 2's parent is node 3.
        """
        self.node_count = node_count
        self.nodes = [node for node in range(0, node_count)]
        self.size = [1 for _ in range(0, node_count)]

    def verify_indexes(self):
        """ Print current index/nodes list (indicating connections)."""
        for index, node in enumerate(self.nodes):
            if index == node:
                print(f"{index} is a root.")
            else:
                print(f"{index} connects to {node}")

        print(self.size)

    def find_root(self, node):
        """
        Return root of given node.
        The root of anything will be when the node and index are the same.
        So to find it, we just keep moving up the node's pointers (indexes).
        """
        while node != self.nodes[node]:
            node = self.nodes[node]
        return node

    def is_connected(self, node_a, node_b) -> bool:
        """Check if two nodes are connected (if they share the same root)."""
        if self.find_root(node_a) == self.find_root(node_b):
            return True
        else:
            return False

    def union(self, a_node, b_node):
        """Connect two nodes by changing root of node_a to point to root of node_b."""
        a_root = self.find_root(a_node)
        b_root = self.find_root(b_node)

        if a_root == b_root:
            return

        # Link root of smaller tree to root of bigger tree and update size.
        if self.size[a_root] < self.size[b_root]:
            self.nodes[a_root] = b_root
            self.size[b_root] += self.size[a_root]
        else:
            self.nodes[b_root] = a_root
            self.size[a_root] += self.size[b_root]


print("Quick-find ----------------")
uf = QuickFind(10)
uf.union(0, 4)
uf.union(4, 6)
uf.verify_indexes()
print(uf.is_connected(0, 6))

print("Quick-union ---------------")
quf = QuickUnion(10)
quf.union(0, 4)
quf.union(4, 6)
quf.verify_indexes()
print(uf.is_connected(0, 6))