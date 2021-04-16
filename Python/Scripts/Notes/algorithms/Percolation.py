# https://www.coursera.org/learn/algorithms-part1/programming/Lhp5z/percolation
# https://coursera.cs.princeton.edu/algs4/assignments/percolation/specification.php
# Check to see if a site (n-by-n grid) percolates.

from UnionFind import QuickUnion


class Percolation:
    """Create an n-by-n grid, with all sites initially blocked."""
    def __init__(self, n):
        self.grid = self.create_grid(n)

    def create_grid(self, n):
        """ Create n-by-n grid with default 0 (blocked) values."""
        grid = []
        # Create x, rows.
        values = [0 for _ in range(n)]
        # Create y, columns.
        for _ in range(n):
            grid.append(values)
        return grid

    def show_grid(self):
        for row in self.grid:
            print(row)

    def open_site(self, x, y):
        """Open site at (row, col) if it's not open already. (Change 0 to 1)."""
        ...

    def is_open(self, x, y) -> bool:
        """Check if a site is open."""
        ...

    def is_full(self, x, y) -> bool:
        """Check if the given site is full."""
        ...

    def num_of_open_sites(self) -> int:
        """Return the number of open sites"""
        ...

    def percolates(self):
        """Check if the system percolates."""
        ...


perc = Percolation(10)
perc.show_grid()