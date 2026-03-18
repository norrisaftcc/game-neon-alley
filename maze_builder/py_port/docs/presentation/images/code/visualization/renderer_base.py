"""
Base class for maze renderers.

This module defines the common interface that all rendering implementations
should follow, allowing for consistent visualization across different output formats.
"""

class MazeRendererBase:
    """Base class that defines the common interface for all maze renderers."""
    
    def __init__(self, theme_name=None):
        """
        Initialize the renderer with an optional theme.
        
        Args:
            theme_name: The name of the theme to use for rendering.
                        If None, the default theme will be used.
        """
        self.theme_name = theme_name or "default"
    
    def render_maze(self, grid, solution_path=None, show_distances=False, distances=None, **kwargs):
        """
        Render a maze with optional solution path and distances.
        
        Args:
            grid: The maze grid to render
            solution_path: Optional list of cells forming a path through the maze
            show_distances: Whether to show distances in cells
            distances: Optional distances object for showing distance values
            **kwargs: Additional renderer-specific parameters
            
        Returns:
            The rendered output in a format specific to the renderer implementation
        """
        raise NotImplementedError("Subclasses must implement render_maze")
    
    def get_entrance_exit(self, grid):
        """
        Get the standard entrance and exit cells for the maze.
        
        By convention, the entrance is at the bottom left and the exit is at the top right.
        
        Args:
            grid: The maze grid
            
        Returns:
            A tuple of (entrance_cell, exit_cell)
        """
        entrance = grid.at(grid.rows - 1, 0)  # Bottom left
        exit = grid.at(0, grid.cols - 1)      # Top right
        return entrance, exit
    
    def is_on_path(self, row, col, path):
        """
        Check if a cell is on the solution path.
        
        Args:
            row: Cell row
            col: Cell column
            path: List of cells in the solution path
            
        Returns:
            True if the cell is on the path, False otherwise
        """
        if not path:
            return False
            
        for cell in path:
            if cell.row == row and cell.col == col:
                return True
        return False
    
    def set_theme(self, theme_name):
        """
        Set the theme to use for rendering.
        
        Args:
            theme_name: The name of the theme to use
        """
        self.theme_name = theme_name