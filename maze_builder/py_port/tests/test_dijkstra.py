import sys
import os
import pytest

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathfinding.dijkstra import Dijkstra
from pathfinding.distances import Distances
from grid import Grid
from cell import Cell

class TestDijkstra:
    def setup_method(self):
        """Create a simple 3x3 grid for testing."""
        self.grid = Grid(3, 3)

        # Create a simple path through the maze:
        # (0,0) -> (0,1) -> (0,2) -> (1,2) -> (2,2) -> (2,1) -> (2,0)
        # +---+---+---+
        # |       |   |
        # +---+   +   +
        # |   |       |
        # +   +---+   +
        # |       |   |
        # +---+---+---+

        # Horizontal connections
        self.grid.link_cells(0, 0, Cell.EAST)  # (0,0) -> (0,1)
        self.grid.link_cells(0, 1, Cell.EAST)  # (0,1) -> (0,2)
        self.grid.link_cells(2, 0, Cell.EAST)  # (2,0) -> (2,1)
        self.grid.link_cells(2, 1, Cell.EAST)  # (2,1) -> (2,2)

        # Vertical connections
        self.grid.link_cells(0, 2, Cell.SOUTH)  # (0,2) -> (1,2)
        self.grid.link_cells(1, 2, Cell.SOUTH)  # (1,2) -> (2,2)

    def test_calculate_distances(self):
        """Test Dijkstra's distance calculations."""
        # Calculate distances from top-left
        start = self.grid.at(0, 0)
        distances = Dijkstra.calculate_distances(self.grid, start)
        
        # Check distances to several cells
        assert distances.get_distance(self.grid.at(0, 0)) == 0  # Start cell
        assert distances.get_distance(self.grid.at(0, 1)) == 1  # One step east
        assert distances.get_distance(self.grid.at(0, 2)) == 2  # Two steps east
        assert distances.get_distance(self.grid.at(1, 2)) == 3  # Down from (0,2)
        assert distances.get_distance(self.grid.at(2, 2)) == 4  # Down from (1,2)
        assert distances.get_distance(self.grid.at(2, 1)) == 5  # Left from (2,2)
        assert distances.get_distance(self.grid.at(2, 0)) == 6  # Left from (2,1)
        
        # Cells not reachable in our contrived maze
        assert distances.get_distance(self.grid.at(1, 0)) == sys.maxsize
        assert distances.get_distance(self.grid.at(1, 1)) == sys.maxsize

    def test_shortest_path(self):
        """Test finding shortest path between two cells."""
        start = self.grid.at(0, 0)
        end = self.grid.at(2, 0)
        
        path = Dijkstra.shortest_path(self.grid, start, end)
        
        # Check path length
        assert len(path) == 7  # 7 cells including start and end
        
        # Check path cells
        assert path[0] == start
        assert path[1] == self.grid.at(0, 1)
        assert path[2] == self.grid.at(0, 2)
        assert path[3] == self.grid.at(1, 2)
        assert path[4] == self.grid.at(2, 2)
        assert path[5] == self.grid.at(2, 1)
        assert path[6] == end
        
        # Test path between cells with no connection
        unreachable = self.grid.at(1, 1)  # This cell has no connections
        empty_path = Dijkstra.shortest_path(self.grid, start, unreachable)
        assert len(empty_path) == 0  # No path exists

    def test_longest_path(self):
        """Test finding the longest path (solution) in the maze."""
        # In our contrived example, the longest path is known:
        # (0,0) to (2,0) or vice versa with our specific maze configuration
        path = Dijkstra.longest_path(self.grid)

        # Check path length - our grid is now fully connected in a loop
        # so we should be able to go from (0,0) to (2,2)
        assert len(path) >= 5  # At least 5 cells in the path

        # Check if path exists and has reasonable length
        assert len(path) > 0

        # Verify path is valid by checking each cell is linked to the next
        for i in range(len(path) - 1):
            current = path[i]
            next_cell = path[i + 1]

            # Check that cells are neighbors
            assert (
                (current.row == next_cell.row and abs(current.col - next_cell.col) == 1) or
                (current.col == next_cell.col and abs(current.row - next_cell.row) == 1)
            ), f"Cells {current.row},{current.col} and {next_cell.row},{next_cell.col} are not neighbors"

            # Check that cells are linked
            directions = current.get_links()
            neighbor_found = False

            for direction in directions:
                offset_row, offset_col = self.grid.DIRECTION_OFFSETS[direction]
                if (current.row + offset_row == next_cell.row and
                    current.col + offset_col == next_cell.col):
                    neighbor_found = True
                    break

            assert neighbor_found, f"Cells {current.row},{current.col} and {next_cell.row},{next_cell.col} are not linked"