import sys

class Distances:
    """
    Tracks distances from a starting cell to other cells in the maze.
    Acts like a specialized dictionary mapping cells to their distances.
    """
    
    def __init__(self, start):
        """Initialize with a starting cell that has distance 0."""
        self.cells = {}  # Dictionary mapping cell keys to distances
        self.root = start
        self.cells[self._key(start.row, start.col)] = 0
    
    def _key(self, row, col):
        """Create a string key from row and column coordinates."""
        return f"{row},{col}"
    
    def get_distance(self, cell):
        """Get the distance to the given cell (returns max int if not found)."""
        key = self._key(cell.row, cell.col)
        return self.cells.get(key, sys.maxsize)
    
    def set_distance(self, cell, distance):
        """Set the distance for the given cell."""
        key = self._key(cell.row, cell.col)
        self.cells[key] = distance
    
    def get_max_cell(self, grid):
        """Get the cell with the maximum distance (farthest from root)."""
        max_distance = 0
        max_cell = self.root
        
        for key, distance in self.cells.items():
            if distance > max_distance:
                row, col = map(int, key.split(','))
                if grid.is_valid(row, col):
                    max_cell = grid.at(row, col)
                    max_distance = distance
        
        return max_cell