import sys
import os
import pytest

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cell import Cell

class TestCell:
    def test_init(self):
        """Test Cell initialization."""
        cell = Cell(1, 2)
        assert cell.row == 1
        assert cell.col == 2
        assert cell.links == 0  # No links initially

    def test_link_unlink(self):
        """Test linking and unlinking cells."""
        cell = Cell(1, 1)
        
        # Link north
        cell.link(Cell.NORTH)
        assert cell.linked(Cell.NORTH) is True
        assert cell.linked(Cell.SOUTH) is False
        assert cell.linked(Cell.EAST) is False
        assert cell.linked(Cell.WEST) is False
        
        # Link east
        cell.link(Cell.EAST)
        assert cell.linked(Cell.NORTH) is True
        assert cell.linked(Cell.EAST) is True
        
        # Unlink north
        cell.unlink(Cell.NORTH)
        assert cell.linked(Cell.NORTH) is False
        assert cell.linked(Cell.EAST) is True

    def test_get_links(self):
        """Test getting all linked directions."""
        cell = Cell(1, 1)
        
        # No links initially
        assert cell.get_links() == []
        
        # Add some links
        cell.link(Cell.NORTH)
        cell.link(Cell.WEST)
        
        links = cell.get_links()
        assert len(links) == 2
        assert Cell.NORTH in links
        assert Cell.WEST in links
        assert Cell.SOUTH not in links
        assert Cell.EAST not in links

    def test_bit_operations(self):
        """Test that bit operations work as expected."""
        cell = Cell(0, 0)
        
        # Link all directions
        cell.link(Cell.NORTH)  # 1
        cell.link(Cell.SOUTH)  # 2
        cell.link(Cell.EAST)   # 4
        cell.link(Cell.WEST)   # 8
        
        # links should be 15 (1+2+4+8)
        assert cell.links == 15
        
        # Unlink east
        cell.unlink(Cell.EAST)
        assert cell.links == 11  # 15 - 4
        
        # Test individual directions
        assert cell.linked(Cell.NORTH) is True
        assert cell.linked(Cell.SOUTH) is True
        assert cell.linked(Cell.EAST) is False
        assert cell.linked(Cell.WEST) is True

    def test_opposites(self):
        """Test that direction opposites are correct."""
        assert Cell.OPPOSITES[Cell.NORTH] == Cell.SOUTH
        assert Cell.OPPOSITES[Cell.SOUTH] == Cell.NORTH
        assert Cell.OPPOSITES[Cell.EAST] == Cell.WEST
        assert Cell.OPPOSITES[Cell.WEST] == Cell.EAST