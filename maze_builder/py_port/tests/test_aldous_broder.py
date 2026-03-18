import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.aldous_broder import AldousBroderMaze
from grid import Grid
from cell import Cell

class TestAldousBroderMaze:
    """
    Tests for the Aldous-Broder maze generation algorithm.
    These tests verify that the algorithm creates valid mazes and exhibits
    the expected characteristics of Aldous-Broder mazes.
    """
    
    def test_explain_method(self):
        """Test that the explain method returns a non-empty string."""
        explanation = AldousBroderMaze.explain()
        assert isinstance(explanation, str)
        assert len(explanation) > 0
        assert "ALDOUS-BRODER ALGORITHM" in explanation
    
    def test_all_cells_visited(self):
        """Test that all cells are connected in the maze."""
        grid = Grid(5, 5)

        # Just test that the regular unpatched algorithm creates a connected maze
        AldousBroderMaze.on(grid)
        
        # Verify that each cell has at least one connection
        for r in range(grid.rows):
            for c in range(grid.cols):
                cell = grid.at(r, c)
                assert len(cell.get_links()) > 0, f"Cell at ({r},{c}) has no connections"
    
    def test_creates_perfect_maze(self):
        """Test that the maze has exactly one path between any two cells."""
        grid = Grid(5, 5)

        # Just run the algorithm normally without patching
        AldousBroderMaze.on(grid)
        
        # BFS to check that all cells are connected
        start = grid.at(0, 0)
        visited = set()
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            cell_key = f"{current.row},{current.col}"
            
            if cell_key in visited:
                continue
                
            visited.add(cell_key)
            
            # Add unvisited linked neighbors to the queue
            for direction in current.get_links():
                r, c = current.row, current.col
                dr, dc = Grid.DIRECTION_OFFSETS[direction]
                nr, nc = r + dr, c + dc
                
                if grid.is_valid(nr, nc):
                    queue.append(grid.at(nr, nc))
        
        # Perfect maze should have exactly one path between any two cells
        # This means every cell must be reachable, with no loops
        assert len(visited) == grid.rows * grid.cols
        
        # Count total links - a perfect maze should have exactly (n-1) links
        # where n is the number of cells
        total_links = 0
        for r in range(grid.rows):
            for c in range(grid.cols):
                # Each connection is counted twice (once from each cell)
                # so we'll only count in one direction (e.g., EAST and SOUTH)
                cell = grid.at(r, c)
                if cell.linked(Cell.EAST):
                    total_links += 1
                if cell.linked(Cell.SOUTH):
                    total_links += 1
        
        # Perfect maze has exactly (rows * cols - 1) links
        expected_links = grid.rows * grid.cols - 1
        assert total_links == expected_links, f"Expected {expected_links} links, got {total_links}"
    
    def test_max_iterations_limit(self):
        """Test that the algorithm respects the max_iterations parameter."""
        grid = Grid(10, 10)
        
        # Test with a low max_iterations value
        max_iterations = 20
        _, iterations = AldousBroderMaze.on(grid, max_iterations=max_iterations)
        
        # Check that the algorithm stopped when it hit max_iterations
        assert iterations <= max_iterations
    
    def test_algorithm_connects_cells(self):
        """Test that the algorithm correctly connects cells."""
        grid = Grid(3, 3)

        # Run the algorithm with a small grid
        grid, iterations = AldousBroderMaze.on(grid)

        # Confirm that connections were made
        connection_count = 0
        for r in range(grid.rows):
            for c in range(grid.cols):
                cell = grid.at(r, c)
                connection_count += len(cell.get_links())

        # In a perfect maze with n cells, there are exactly 2*(n-1) connections
        # when counting connections from both sides (each passage is counted twice)
        expected_connections = 2 * (grid.rows * grid.cols - 1)
        assert connection_count == expected_connections