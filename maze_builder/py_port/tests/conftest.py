import sys
import os
import pytest

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# This file is used by pytest for shared fixtures and configuration
# Currently it just ensures the module paths are set up correctly

@pytest.fixture
def sample_3x3_grid():
    """Create a 3x3 grid with a specific path pattern for testing."""
    from grid import Grid
    from cell import Cell
    
    grid = Grid(3, 3)
    
    # Create a simple path through the maze:
    # (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) -> (2,1) -> (2,0)
    
    # Horizontal connections
    grid.link_cells(0, 0, Cell.EAST)  # (0,0) -> (0,1)
    grid.link_cells(0, 1, Cell.EAST)  # (0,1) -> (0,2)
    grid.link_cells(2, 0, Cell.EAST)  # (2,0) -> (2,1)
    
    # Vertical connections
    grid.link_cells(0, 2, Cell.SOUTH)  # (0,2) -> (1,2)
    grid.link_cells(1, 2, Cell.SOUTH)  # (1,2) -> (2,2)
    grid.link_cells(2, 1, Cell.WEST)   # (2,1) -> (2,0)
    
    return grid