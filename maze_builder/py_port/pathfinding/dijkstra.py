import heapq
import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cell import Cell
from grid import Grid
from pathfinding.distances import Distances

# For debugging
import logging
# Set to ERROR level to suppress debug messages during normal operation
# Change to DEBUG for development/troubleshooting
logging.basicConfig(level=logging.ERROR)

class Dijkstra:
    """
    Implements Dijkstra's algorithm for finding shortest paths through the maze.
    
    Dijkstra's is a greedy algorithm that always expands the node with the
    smallest known distance from the start.
    """
    
    @staticmethod
    def calculate_distances(grid, start):
        """Calculate distances from a starting cell to all other cells."""
        distances = Distances(start)
        
        # Priority queue with (distance, cell_key) pairs
        frontier = [(0, f"{start.row},{start.col}")]
        
        while frontier:
            current_distance, current_key = heapq.heappop(frontier)
            row, col = map(int, current_key.split(','))
            
            if not grid.is_valid(row, col):
                continue
                
            cell = grid.at(row, col)
            cell_distance = distances.get_distance(cell)
            
            # Process each linked neighbor
            for direction in cell.get_links():
                offset_row, offset_col = Grid.DIRECTION_OFFSETS[direction]
                neighbor_row, neighbor_col = row + offset_row, col + offset_col
                
                if not grid.is_valid(neighbor_row, neighbor_col):
                    continue
                    
                neighbor = grid.at(neighbor_row, neighbor_col)
                new_distance = cell_distance + 1
                neighbor_distance = distances.get_distance(neighbor)
                
                if new_distance < neighbor_distance:
                    distances.set_distance(neighbor, new_distance)
                    heapq.heappush(frontier, (new_distance, f"{neighbor_row},{neighbor_col}"))
        
        return distances
    
    @staticmethod
    def shortest_path(grid, start, end):
        """Find the shortest path between two cells."""
        # Calculate distances from start to all cells
        distances = Dijkstra.calculate_distances(grid, start)

        # Debug output
        logging.debug(f"Calculating shortest path from ({start.row},{start.col}) to ({end.row},{end.col})")
        logging.debug(f"End cell distance: {distances.get_distance(end)}")

        # If end is unreachable, return empty path
        if distances.get_distance(end) == sys.maxsize:
            logging.debug("End cell is unreachable")
            return []

        # Reconstruct the path from end to start
        path = []
        current = end
        path.append(current)

        # Walk backward from end to start, always choosing the neighbor
        # with the smallest distance value
        while current != start:
            row = current.row
            col = current.col
            current_distance = distances.get_distance(current)
            logging.debug(f"Current cell: ({row},{col}) with distance {current_distance}")

            next_cell = None
            next_distance = current_distance

            # Check each linked neighbor
            for direction in current.get_links():
                offset_row, offset_col = Grid.DIRECTION_OFFSETS[direction]
                neighbor_row = row + offset_row
                neighbor_col = col + offset_col

                if not grid.is_valid(neighbor_row, neighbor_col):
                    continue

                neighbor = grid.at(neighbor_row, neighbor_col)
                neighbor_distance = distances.get_distance(neighbor)

                logging.debug(f"  Checking neighbor ({neighbor_row},{neighbor_col}) with distance {neighbor_distance}")

                # If this neighbor is closer to the start
                if neighbor_distance < next_distance:
                    next_cell = neighbor
                    next_distance = neighbor_distance
                    logging.debug(f"    Found better path via ({neighbor_row},{neighbor_col})")

            if next_cell is None:
                logging.debug("Error: No path found! Breaking out of loop.")
                break  # Something went wrong

            path.append(next_cell)
            current = next_cell

        # Reverse the path so it goes from start to end
        path.reverse()
        logging.debug(f"Path length: {len(path)}")
        return path
    
    @staticmethod
    def longest_path(grid):
        """Find the longest shortest path (solution) in the maze."""
        # Start from the top-left corner
        start = grid.at(0, 0)
        
        # Find the farthest cell from the start
        distances = Dijkstra.calculate_distances(grid, start)
        farthest = distances.get_max_cell(grid)
        
        # Now find the farthest cell from that cell
        distances = Dijkstra.calculate_distances(grid, farthest)
        end = distances.get_max_cell(grid)
        
        # Return the path between these two maximally distant cells
        return Dijkstra.shortest_path(grid, farthest, end)