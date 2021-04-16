# https://www.coursera.org/learn/algorithms-part1/programming/Lhp5z/percolation
# https://coursera.cs.princeton.edu/algs4/assignments/percolation/specification.php
# Check to see if a site (n-by-n grid) percolates.

from typing import List
from UnionFind import QuickUnion
import random


# ------------------------------------------------------------------------------
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
            grid.append(values[:])
        return grid

    def show_grid(self):
        for row in self.grid:
            print(row)

    def open_site(self, x, y):
        """Open site at coordinates if not open already."""
        if self.grid[y][x] != 1:
            self.grid[y][x] = 1
        else:
            print(f"[{x},{y}] is already open.")

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


# ------------------------------------------------------------------------------
def random_list(low, high, length) -> List:
    """Generate a list of random numbers."""
    results = []
    for _ in range(length):
        n = random.randint(low, high)
        results.append(n)

    return results


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    size = 10
    fill = 30
    perc = Percolation(size)

    random_x_coords = random_list(0, size-1, fill)
    random_y_coords = random_list(0, size-1, fill)
    for xx, yy in zip(random_x_coords, random_y_coords):
        perc.open_site(xx, yy)

    perc.show_grid()