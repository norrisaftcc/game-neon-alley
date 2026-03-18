"""
Text-based renderer for mazes.

This module provides an ASCII/ANSI text-based visualization for mazes,
suitable for terminal display.
"""

import sys
import os
import platform

from .renderer_base import MazeRendererBase
from .themes import ThemeManager

class TextRenderer(MazeRendererBase):
    """Renders mazes as text/ASCII art with optional ANSI colors."""
    
    def __init__(self, theme_name="default", use_color=True):
        """
        Initialize a text renderer with the specified theme.
        
        Args:
            theme_name: The name of the theme to use
            use_color: Whether to use ANSI color codes
        """
        super().__init__(theme_name)
        self.theme = ThemeManager.get_theme(theme_name)
        
        # Check if we should disable colors
        if platform.system() == "Windows" and "TERM" not in os.environ:
            self.use_color = False
        else:
            self.use_color = use_color and self.theme.use_terminal_colors
    
    def render_maze(self, grid, solution_path=None, show_distances=False, distances=None, **kwargs):
        """
        Render a maze as ASCII text with optional ANSI colors.
        
        Args:
            grid: The maze grid to render
            solution_path: Optional list of cells forming a path through the maze
            show_distances: Whether to show distances in cells
            distances: Optional distances object for showing distance values
            
        Returns:
            A string containing the rendered maze
        """
        # Get entrance and exit cells
        entrance, exit = self.get_entrance_exit(grid)
        
        # Set up color codes if using color
        if self.use_color:
            reset = self.theme.reset_code
            bold = self.theme.bold_code
            entrance_color = self.theme.entrance_code
            exit_color = self.theme.exit_code
            path_color = self.theme.path_code
            distance_color = self.theme.distance_code
        else:
            reset = ""
            bold = ""
            entrance_color = ""
            exit_color = ""
            path_color = ""
            distance_color = ""
        
        # Display the top border
        output = ['+' + '---+' * grid.cols]
        
        for r in range(grid.rows):
            # Display cell contents and eastern boundaries
            row = ['|']
            eastern_boundary = ['+']
            
            for c in range(grid.cols):
                cell = grid.at(r, c)
                
                # Cell contents
                # Special rendering for entrance and exit cells
                if cell.row == entrance.row and cell.col == entrance.col:
                    # Entrance cell (bottom left)
                    if self.is_on_path(r, c, solution_path) and distances:
                        dist = distances.get_distance(cell)
                        if dist < 10:
                            content = f"{entrance_color}{bold} {self.theme.entrance_symbol}{dist}{reset}"
                        else:
                            content = f"{entrance_color}{bold}{self.theme.entrance_symbol}{dist}{reset}"
                    else:
                        content = f"{entrance_color}{bold} {self.theme.entrance_symbol} {reset}"
                elif cell.row == exit.row and cell.col == exit.col:
                    # Exit cell (top right)
                    content = f"{exit_color}{bold} {self.theme.exit_symbol} {reset}"
                elif self.is_on_path(r, c, solution_path):
                    # Path cell always shows distance to exit
                    if distances:
                        dist = distances.get_distance(cell)
                        if dist < 10:
                            content = f"{path_color} {dist} {reset}"
                        else:
                            content = f"{path_color}{dist}{reset} "
                    else:
                        content = f"{path_color} {self.theme.path_symbol} {reset}"
                elif show_distances and distances:
                    # Regular cell with distance
                    dist = distances.get_distance(cell)
                    if dist == sys.maxsize:  # Unreachable cell
                        content = "   "
                    elif dist < 10:
                        content = f"{distance_color} {dist} {reset}"
                    else:
                        content = f"{distance_color}{dist}{reset} "
                else:
                    # Regular empty cell
                    content = "   "
                
                row.append(content)
                
                # Eastern boundary
                if c < grid.cols - 1 and cell.linked(4):  # 4 is EAST
                    row.append(' ')
                else:
                    row.append('|')
                
                # Southern boundary
                if r < grid.rows - 1 and cell.linked(2):  # 2 is SOUTH
                    eastern_boundary.append('   +')
                else:
                    eastern_boundary.append('---+')
            
            output.append(''.join(row))
            output.append(''.join(eastern_boundary))
        
        return '\n'.join(output)
    
    def set_color_mode(self, use_color):
        """
        Set whether to use ANSI color codes.
        
        Args:
            use_color: True to enable colors, False to disable
        """
        if platform.system() == "Windows" and "TERM" not in os.environ:
            self.use_color = False
        else:
            self.use_color = use_color