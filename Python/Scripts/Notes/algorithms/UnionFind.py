# Connectivity problem.
# https://www.coursera.org/learn/algorithms-part1/lecture/EcF3P/quick-find
# "Find" query - Check if two objects are in the same component.
# "Union" command - Replace components containing two objects with their union.

class UnionFind:
    def __init__(self, node_count):
        self.node_count = node_count
        self.nodes = [node for node in range(0, node_count)]

    def verify_indexes(self):
        """ Print current index/nodes list (indicating connections)."""
        for index, node in enumerate(self.nodes):
            print(f"{index} connects to {node}")

    def is_connected(self, first, second):
        """ Check if two nodes are connected. Return True if so."""
        if self.nodes[first] == self.nodes[second]:
            return True
        return False

    def union(self, first, second):
        """ Connect the two provided nodes."""
        first_node = self.nodes[first]
        second_node = self.nodes[second]
        # We want every node to connect to a common point if there are multiple
        # unions, so we for loop over every index that has the first provided node,
        # and change it to the second provided node. That means every node will
        # link that is already linked before.
        for index, node in enumerate(self.nodes):
            if self.nodes[index] == first_node:
                self.nodes[index] = second_node


uf = UnionFind(10)
uf.union(0, 4)
uf.union(4, 6)
uf.verify_indexes()
print(uf.is_connected(0, 6))