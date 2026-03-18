import sys
import os
import random

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cell import Cell

class SidewinderMaze:
    """
    Sidewinder maze generation algorithm implementation.
    
    The Sidewinder algorithm is a simple maze generation algorithm that creates
    perfect mazes with a distinctive diagonal bias. Unlike Binary Tree which has a 
    strong northeast corner bias, Sidewinder creates a northern edge bias but with 
    a more interesting pattern throughout the maze.
    
    Characteristics of Sidewinder mazes:
    - All northern edge cells are connected in an unbroken corridor
    - Tends to create "rivers" (long horizontal passages) in the maze
    - Creates a more "winding" pattern than Binary Tree
    - Has less obvious bias while still being efficient
    - Produces distinctive diagonal patterns in the maze structure
    
    Time complexity: O(n) where n is the number of cells in the grid
    Space complexity: O(w) where w is the width of the grid (for storing the "run")
    """
    
    @staticmethod
    def on(grid):
        """
        Apply the Sidewinder algorithm to a grid to create a maze.
        
        The algorithm works through the grid row by row:
        1. For each row, we build "runs" of cells connected horizontally
        2. For each cell in a run (except the north row), we randomly decide whether to:
           - Carve east and add the cell to the current run, OR
           - Carve north from a randomly chosen cell in the run and end the run
        3. The north row is handled specially - we only carve east connections
        
        Args:
            grid: The Grid object to apply the algorithm to
        """
        # Special case for the northern row - create a single long corridor
        # This is a characteristic feature of the Sidewinder algorithm
        for c in range(grid.cols - 1):
            # Always connect east along the top row
            grid.link_cells(0, c, Cell.EAST)
        
        # Process all remaining rows
        for r in range(1, grid.rows):
            # For each row, we'll create "runs" of connected cells
            run = []
            
            for c in range(grid.cols):
                # Add the current cell to the run
                run.append((r, c))
                
                # Determine if we should close out this run
                at_eastern_boundary = (c == grid.cols - 1)
                should_close_out = at_eastern_boundary or grid.random_int(0, 1) == 0

                if should_close_out:
                    # Choose a random cell from the run to connect northward
                    if run:  # Check if the run is not empty
                        # Select a random cell from the current run
                        # Use the Grid's random_int method for consistency with tests
                        random_index = grid.random_int(0, len(run) - 1)
                        random_cell = run[random_index]
                        random_row, random_col = random_cell

                        # Carve a passage north from the randomly chosen cell
                        grid.link_cells(random_row, random_col, Cell.NORTH)

                    # Reset the run for the next segment
                    run = []
                else:
                    # Connect east and continue the run
                    grid.link_cells(r, c, Cell.EAST)
        
        return grid

    @staticmethod
    def explain():
        """
        Returns a detailed explanation of the Sidewinder algorithm for educational purposes.
        """
        explanation = """
        THE SIDEWINDER ALGORITHM EXPLAINED
        
        The Sidewinder algorithm creates perfect mazes with a distinctive pattern:
        
        1. INITIALIZATION:
           - Start with a grid of cells with no connections
           - Process the grid row by row from top to bottom
        
        2. NORTHERN ROW SPECIAL CASE:
           - For the northernmost row, connect all cells from west to east
           - This creates a single unbroken corridor along the top
        
        3. FOR ALL OTHER ROWS:
           - Start each row with an empty "run" (a sequence of connected cells)
           - For each cell in the row:
              a. Add the current cell to the run
              b. Randomly decide to either:
                 - Carve a passage EAST and continue the run, OR
                 - End the run by carving NORTH from a randomly chosen cell in the run
              c. If at the eastern boundary, always end the run
        
        4. FEATURES AND PATTERNS:
           - Creates "rivers" - long horizontal passages in the maze
           - Forms a diagonal pattern due to the randomized north connections
           - All northern edge cells form one continuous path
           - No dead-end corridors on the northern edge
        
        5. VISUAL SIGNATURE:
           The Sidewinder algorithm creates diagonal patterns due to how the runs are 
           ended by north connections. These north connections often create alignment 
           that produces a subtle diagonal bias in the maze structure.
        
        The name "Sidewinder" comes from the way the algorithm "slithers" through the 
        maze, creating runs of horizontal cells and then "winding" upward at random 
        intervals - reminiscent of a sidewinder snake's movement.
        """
        return explanation