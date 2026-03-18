import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.sidewinder import SidewinderMaze
from grid import Grid
from cell import Cell

def test_simplified():
    """A simplified test to debug the issue."""
    grid = Grid(5, 5)
    
    # Make a more predictable grid.random_int
    # Use a lambda to alternate rather than a fixed sequence
    # This ensures we don't run out of values
    call_count = [0]  # Use a list to store state (mutable)

    def alternate_values(min_val, max_val):
        call_count[0] += 1
        # For the "should close run" decision, alternate between 0 and 1
        if min_val == 0 and max_val == 1:
            return call_count[0] % 2
        # For picking a cell in the run, always pick the first cell
        return 0

    grid.random_int = MagicMock(side_effect=alternate_values)
    
    SidewinderMaze.on(grid)
    
    # Verify that some cells have east links (from horizontal runs)
    east_links = 0
    for r in range(grid.rows):
        for c in range(grid.cols - 1):
            if grid.at(r, c).linked(Cell.EAST):
                east_links += 1
    
    assert east_links > 0, "Should have some east links"
    
    # Verify that all cells in the top row are linked east (except the last one)
    for c in range(grid.cols - 1):
        assert grid.at(0, c).linked(Cell.EAST), f"Top row cell (0,{c}) should link east"