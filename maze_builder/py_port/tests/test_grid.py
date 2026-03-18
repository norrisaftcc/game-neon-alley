import sys
import os
import pytest
from unittest.mock import patch

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grid import Grid
from cell import Cell

class TestGrid:
    def test_init(self):
        """Test Grid initialization."""
        grid = Grid(3, 4)
        assert grid.rows == 3
        assert grid.cols == 4
        
        # Check cells are created correctly
        assert len(grid.cells) == 3
        assert len(grid.cells[0]) == 4
        
        # Check cell coordinates
        for r in range(3):
            for c in range(4):
                cell = grid.at(r, c)
                assert cell.row == r
                assert cell.col == c

    def test_is_valid(self):
        """Test position validation."""
        grid = Grid(5, 5)
        
        # Valid positions
        assert grid.is_valid(0, 0) is True
        assert grid.is_valid(4, 4) is True
        assert grid.is_valid(2, 3) is True
        
        # Invalid positions
        assert grid.is_valid(-1, 0) is False
        assert grid.is_valid(0, -1) is False
        assert grid.is_valid(5, 0) is False
        assert grid.is_valid(0, 5) is False

    def test_at(self):
        """Test cell access."""
        grid = Grid(3, 3)
        
        # Valid access
        cell = grid.at(1, 2)
        assert cell.row == 1
        assert cell.col == 2
        
        # Invalid access should raise exception
        with pytest.raises(IndexError):
            grid.at(3, 3)

    @patch('random.randint')
    def test_random_int(self, mock_randint):
        """Test random number generation."""
        grid = Grid(2, 2)
        
        mock_randint.return_value = 42
        assert grid.random_int(0, 100) == 42
        mock_randint.assert_called_with(0, 100)

    def test_link_cells(self):
        """Test linking cells together."""
        grid = Grid(3, 3)
        
        # Link cell (1,1) to its eastern neighbor
        grid.link_cells(1, 1, Cell.EAST)
        
        # Check both cells are linked
        assert grid.at(1, 1).linked(Cell.EAST) is True
        assert grid.at(1, 2).linked(Cell.WEST) is True
        
        # Link cell (1,1) to its southern neighbor
        grid.link_cells(1, 1, Cell.SOUTH)
        
        # Check both cells are linked
        assert grid.at(1, 1).linked(Cell.SOUTH) is True
        assert grid.at(2, 1).linked(Cell.NORTH) is True
        
        # Try to link beyond grid bounds - should do nothing
        grid.link_cells(2, 2, Cell.EAST)
        grid.link_cells(2, 2, Cell.SOUTH)
        
        # Should still have original links
        assert grid.at(1, 1).linked(Cell.EAST) is True
        assert grid.at(1, 1).linked(Cell.SOUTH) is True

    def test_display(self):
        """Test maze display functionality."""
        # Create a simple 2x2 grid
        grid = Grid(2, 2)

        # No links initially, should see all walls
        output = grid.display()
        assert "+---+---+" in output
        assert "|   |   |" in output

        # Link some cells
        grid.link_cells(0, 0, Cell.EAST)
        grid.link_cells(0, 0, Cell.SOUTH)

        # Get updated display
        output = grid.display()

        # The grid display format looks like:
        # +---+---+
        # |       |
        # +   +---+
        # |   |   |
        # +---+---+

        # Check for specific patterns in the output
        # The first row should have an opening to the east
        assert "|       |" in output

        # There should be a south opening from (0,0)
        assert "+   +" in output