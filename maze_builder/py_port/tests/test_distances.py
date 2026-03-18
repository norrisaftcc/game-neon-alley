import sys
import os
import pytest

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathfinding.distances import Distances
from grid import Grid
from cell import Cell

class TestDistances:
    def setup_method(self):
        """Create a simple 3x3 grid for testing."""
        self.grid = Grid(3, 3)
        
        # Create a simple path through the maze:
        # (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) -> (2,1) -> (2,0)
        
        # Horizontal connections
        self.grid.link_cells(0, 0, Cell.EAST)  # (0,0) -> (0,1)
        self.grid.link_cells(0, 1, Cell.EAST)  # (0,1) -> (0,2)
        self.grid.link_cells(2, 0, Cell.EAST)  # (2,0) -> (2,1)
        
        # Vertical connections
        self.grid.link_cells(0, 2, Cell.SOUTH)  # (0,2) -> (1,2)
        self.grid.link_cells(1, 2, Cell.SOUTH)  # (1,2) -> (2,2)
        self.grid.link_cells(2, 1, Cell.WEST)   # (2,1) -> (2,0)

    def test_init(self):
        """Test Distances initialization."""
        start = self.grid.at(0, 0)
        distances = Distances(start)
        
        # Root cell should have distance 0
        assert distances.get_distance(start) == 0
        assert distances.root == start
        
        # Other cells should not have distances set yet
        assert distances.get_distance(self.grid.at(0, 1)) == sys.maxsize

    def test_set_get_distance(self):
        """Test setting and getting distances."""
        start = self.grid.at(0, 0)
        distances = Distances(start)
        
        # Set some distances
        distances.set_distance(self.grid.at(0, 1), 1)
        distances.set_distance(self.grid.at(0, 2), 2)
        distances.set_distance(self.grid.at(1, 2), 3)
        
        # Get those distances back
        assert distances.get_distance(self.grid.at(0, 1)) == 1
        assert distances.get_distance(self.grid.at(0, 2)) == 2
        assert distances.get_distance(self.grid.at(1, 2)) == 3
        
        # Unset distances should return max int
        assert distances.get_distance(self.grid.at(1, 0)) == sys.maxsize
        
        # Update a distance
        distances.set_distance(self.grid.at(0, 1), 10)
        assert distances.get_distance(self.grid.at(0, 1)) == 10

    def test_get_max_cell(self):
        """Test finding the cell with maximum distance."""
        start = self.grid.at(0, 0)
        distances = Distances(start)
        
        # Set distances to multiple cells
        distances.set_distance(self.grid.at(0, 1), 1)
        distances.set_distance(self.grid.at(0, 2), 2)
        distances.set_distance(self.grid.at(1, 2), 3)
        distances.set_distance(self.grid.at(2, 2), 4)
        distances.set_distance(self.grid.at(2, 1), 5)
        distances.set_distance(self.grid.at(2, 0), 6)
        
        # Find max cell
        max_cell = distances.get_max_cell(self.grid)
        
        # Should be (2,0) with distance 6
        assert max_cell == self.grid.at(2, 0)
        
        # If we update the max value to a different cell
        distances.set_distance(self.grid.at(1, 2), 10)
        max_cell = distances.get_max_cell(self.grid)
        
        # Should now be (1,2)
        assert max_cell == self.grid.at(1, 2)

    def test_key_generation(self):
        """Test the key generation for cells."""
        start = self.grid.at(0, 0)
        distances = Distances(start)
        
        # We can't directly test _key since it's private, but we can 
        # test its effect through the public API
        
        # Set and get distance for a cell
        cell = self.grid.at(2, 1)
        distances.set_distance(cell, 42)
        assert distances.get_distance(cell) == 42
        
        # Create a new cell with the same coordinates
        # This tests that the key is based on coordinates, not object identity
        same_coords = Cell(2, 1)
        assert distances.get_distance(same_coords) == 42