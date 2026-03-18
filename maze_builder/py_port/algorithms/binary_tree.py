import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cell import Cell

class BinaryTreeMaze:
    """
    Binary Tree maze generation algorithm.

    For each cell in the grid, this algorithm randomly carves a passage either
    north or east. If the cell is on the north edge, it always carves east.
    If the cell is on the east edge, it always carves north. If the cell is in
    the northeast corner, it doesn't carve any passages.

    This creates a "perfect maze" (one with exactly one path between any two
    cells) with a bias toward the northeast corner.

    Characteristics of Binary Tree mazes:
    - Distinctive bias toward the northeast corner
    - Northern and eastern edges are always perfectly straight corridors
    - Easy to implement with minimal code
    - Always produces perfect mazes (exactly one path between any two cells)
    - Creates a visually distinctive pattern with diagonal paths

    Time complexity: O(n) where n is the number of cells in the grid
    Space complexity: O(1) - requires no additional storage
    """
    
    @staticmethod
    def on(grid):
        """
        Apply the Binary Tree algorithm to a grid to create a maze.

        The algorithm works by visiting each cell in the grid and randomly
        choosing to carve a passage either north or east (when possible):
        1. If the cell is on the northern edge, we can only carve east
        2. If the cell is on the eastern edge, we can only carve north
        3. If the cell is in the northeast corner, we can't carve any passages
        4. For all other cells, randomly choose between north and east

        Args:
            grid: The Grid object to apply the algorithm to
        """
        for r in range(grid.rows):
            for c in range(grid.cols):
                neighbors = []

                # Consider linking north
                if r > 0:
                    neighbors.append(Cell.NORTH)

                # Consider linking east
                if c < grid.cols - 1:
                    neighbors.append(Cell.EAST)

                # If we have neighbors to link, choose one at random
                if neighbors:
                    direction = neighbors[grid.random_int(0, len(neighbors) - 1)]
                    grid.link_cells(r, c, direction)

        return grid

    @staticmethod
    def explain():
        """
        Returns a detailed explanation of the Binary Tree algorithm for educational purposes.
        """
        explanation = """
        THE BINARY TREE ALGORITHM EXPLAINED

        The Binary Tree algorithm is one of the simplest maze generation algorithms:

        1. INITIALIZATION:
           - Start with a grid of cells with no connections
           - Process each cell in the grid (typically row by row)

        2. FOR EACH CELL:
           - If the cell has a northern neighbor, add NORTH to possible directions
           - If the cell has an eastern neighbor, add EAST to possible directions
           - Randomly choose one of the available directions
           - Create a passage in the chosen direction

        3. EDGE CASES:
           - Northern edge cells can only connect EAST
           - Eastern edge cells can only connect NORTH
           - Northeast corner cell has no connections

        4. FEATURES AND PATTERNS:
           - Creates perfect mazes (exactly one path between any two points)
           - Strong bias toward the northeast corner
           - Northern and eastern edges are always straight corridors
           - Recognizable diagonal texture from southwest to northeast

        5. WHY "BINARY TREE"?
           The name comes from viewing the maze as a binary tree structure:
           - Each cell connects to at most two other cells (north and east)
           - The northeast corner is effectively the "root" of the tree
           - If you follow connections from any cell, you'll always reach the root

        The Binary Tree algorithm is notable for its simplicity and efficiency,
        but the strong bias makes it less suitable for puzzles requiring more
        complexity and less predictable solutions.
        """
        return explanation