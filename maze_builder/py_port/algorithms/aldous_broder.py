import sys
import os
import random

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cell import Cell

class AldousBroderMaze:
    """
    Aldous-Broder maze generation algorithm implementation.
    
    The Aldous-Broder algorithm is a maze generation algorithm based on random walks.
    Unlike Binary Tree and Sidewinder which have directional biases, Aldous-Broder
    creates completely unbiased mazes. It works by performing a random walk through
    the grid, connecting cells that have not been visited yet.
    
    Characteristics of Aldous-Broder mazes:
    - No directional bias (truly random)
    - Creates perfect mazes (exactly one path between any two cells)
    - Can generate any possible perfect maze with equal probability
    - Tends to create longer, more winding passages than directed algorithms
    - Visually more balanced appearance from all directions
    - No "rivers" or long straight passages
    
    The algorithm is named after mathematicians David Aldous and Andrei Broder, who
    independently proved that random walks can be used to generate spanning trees
    with uniform probability.
    
    Time complexity: O(n²) in the average case, but can be as bad as O(n³) in worst case
    Space complexity: O(n) where n is the number of cells in the grid
    """
    
    @staticmethod
    def on(grid, max_iterations=None, seed=None):
        """
        Apply the Aldous-Broder algorithm to a grid to create a maze.

        The algorithm works through random walks:
        1. Start at a random cell in the grid
        2. Choose a random neighboring cell
        3. If the neighbor has not been visited yet:
           - Connect the current cell to the neighbor
           - Mark the neighbor as visited
        4. Move to the neighbor and repeat until all cells are visited

        Args:
            grid: The Grid object to apply the algorithm to
            max_iterations: Optional maximum number of steps to perform
                            (useful for visualization or limiting computation)
            seed: Optional random seed for reproducible maze generation

        Returns:
            The modified grid and the number of iterations performed
        """
        # Set the random seed if provided
        if seed is not None:
            random.seed(seed)
        # Initialize variables to track progress
        cell_count = grid.rows * grid.cols
        visited_count = 0
        iterations = 0
        visited = set()
        
        # Start at a random cell
        current_row = grid.random_int(0, grid.rows - 1)
        current_col = grid.random_int(0, grid.cols - 1)
        current_cell = grid.at(current_row, current_col)
        
        # Mark the first cell as visited
        visited.add((current_row, current_col))
        visited_count += 1
        
        # Continue until all cells are visited or max iterations reached
        while visited_count < cell_count and (max_iterations is None or iterations < max_iterations):
            # Find all valid neighboring cells (regardless of whether they've been visited)
            neighbors = []
            
            # Check each direction
            for direction in [Cell.NORTH, Cell.EAST, Cell.SOUTH, Cell.WEST]:
                offset_row, offset_col = grid.DIRECTION_OFFSETS[direction]
                neighbor_row = current_row + offset_row
                neighbor_col = current_col + offset_col
                
                if grid.is_valid(neighbor_row, neighbor_col):
                    neighbors.append((neighbor_row, neighbor_col, direction))
            
            # Choose a random neighboring cell
            if neighbors:
                iterations += 1
                next_row, next_col, direction = neighbors[grid.random_int(0, len(neighbors) - 1)]
                
                # If the chosen neighbor has not been visited
                if (next_row, next_col) not in visited:
                    # Connect current cell to the neighbor
                    grid.link_cells(current_row, current_col, direction)
                    
                    # Mark the neighbor as visited
                    visited.add((next_row, next_col))
                    visited_count += 1
                
                # Move to the chosen neighbor
                current_row, current_col = next_row, next_col
                current_cell = grid.at(current_row, current_col)
            else:
                # No neighbors (should never happen in a fully connected grid)
                break
        
        return grid, iterations
    
    @staticmethod
    def explain():
        """
        Returns a detailed explanation of the Aldous-Broder algorithm for educational purposes.
        """
        explanation = """
        THE ALDOUS-BRODER ALGORITHM EXPLAINED
        
        The Aldous-Broder algorithm is a maze generation method based on random walks.
        It creates truly unbiased perfect mazes.
        
        1. INITIALIZATION:
           - Start with a grid of cells with no connections
           - Choose a random starting cell and mark it as visited
        
        2. RANDOM WALK PROCESS:
           - From the current cell, choose a random neighbor (regardless of visit status)
           - If the chosen neighbor has NOT been visited before:
             * Create a passage between the current cell and the neighbor
             * Mark the neighbor as visited
           - Move to the chosen neighbor (whether or not it was previously visited)
           - Repeat until all cells have been visited
        
        3. FEATURES AND PATTERNS:
           - Creates perfect mazes (exactly one path between any two points)
           - No directional bias - any possible maze can be generated with equal probability
           - No "rivers" or long straight passages characteristic of directed algorithms
           - Visually more balanced and random appearance
        
        4. PERFORMANCE CHARACTERISTICS:
           - Much slower than directed algorithms like Binary Tree or Sidewinder
           - Average case time complexity is O(n²) where n is the number of cells
           - Worst case can be O(n³) due to the random walk nature
           - Can take a very long time for large mazes
        
        5. MATHEMATICAL BACKGROUND:
           - Based on the mathematical concept of generating spanning trees via random walks
           - Named after David Aldous and Andrei Broder, who independently discovered
             that random walks create uniform spanning trees
           - A "uniform spanning tree" is any possible spanning tree with equal probability
        
        The Aldous-Broder algorithm's main advantage is its lack of bias - it can generate
        any possible perfect maze with equal probability, unlike algorithms that have
        inherent directional biases. The tradeoff is significantly longer generation time,
        especially for large mazes.
        """
        return explanation