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
    
    def render_maze(self, grid, solution_path=None, show_distances=False, distances=None, step_data=None, **kwargs):
        """
        Render a maze as ASCII text with optional ANSI colors.
        
        Args:
            grid: The maze grid to render
            solution_path: Optional list of cells forming a path through the maze
            show_distances: Whether to show distances in cells
            distances: Optional distances object for showing distance values
            step_data: Optional AlgorithmStep object for step-by-step visualization
            
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
            # Step-specific colors
            current_cell_color = "\033[41m"  # Red background
            candidate_color = "\033[43m"     # Yellow background
            run_color = "\033[44m"           # Blue background
        else:
            reset = ""
            bold = ""
            entrance_color = ""
            exit_color = ""
            path_color = ""
            distance_color = ""
            current_cell_color = ""
            candidate_color = ""
            run_color = ""
        
        # Display the top border
        output = ['+' + '---+' * grid.cols]
        
        for r in range(grid.rows):
            # Display cell contents and eastern boundaries
            row = ['|']
            eastern_boundary = ['+']
            
            for c in range(grid.cols):
                cell = grid.at(r, c)
                
                # Cell contents
                
                # Check if this cell has special significance in the current step
                is_current_cell = False
                is_candidate_cell = False
                is_run_member = False
                cell_color = ""
                
                if step_data:
                    is_current_cell = (step_data.current_cell and 
                                     cell.row == step_data.current_cell.row and 
                                     cell.col == step_data.current_cell.col)
                    
                    is_candidate_cell = any(cand and cell.row == cand.row and cell.col == cand.col 
                                          for cand in step_data.candidate_cells)
                    
                    # Check if cell is part of a Sidewinder run
                    if "run" in step_data.algorithm_specific_data:
                        is_run_member = any(run_cell and cell.row == run_cell.row and cell.col == run_cell.col
                                          for run_cell in step_data.algorithm_specific_data["run"])
                    
                    # Set colors based on priority
                    if is_current_cell:
                        cell_color = current_cell_color
                    elif is_candidate_cell:
                        cell_color = candidate_color
                    elif is_run_member:
                        cell_color = run_color
                
                # Special rendering for entrance and exit cells
                if cell.row == entrance.row and cell.col == entrance.col:
                    # Entrance cell (bottom left)
                    if self.is_on_path(r, c, solution_path) and distances:
                        dist = distances.get_distance(cell)
                        if dist < 10:
                            content = f"{cell_color}{entrance_color}{bold} {self.theme.entrance_symbol}{dist}{reset}"
                        else:
                            content = f"{cell_color}{entrance_color}{bold}{self.theme.entrance_symbol}{dist}{reset}"
                    else:
                        content = f"{cell_color}{entrance_color}{bold} {self.theme.entrance_symbol} {reset}"
                elif cell.row == exit.row and cell.col == exit.col:
                    # Exit cell (top right)
                    content = f"{cell_color}{exit_color}{bold} {self.theme.exit_symbol} {reset}"
                elif is_current_cell or is_candidate_cell or is_run_member:
                    # Step visualization takes precedence
                    symbol = "█" if is_current_cell else ("▒" if is_candidate_cell else "▓")
                    content = f"{cell_color} {symbol} {reset}"
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
    
    def render_step_info(self, step_data):
        """
        Render information about the current step.
        
        Args:
            step_data: AlgorithmStep object containing step information
            
        Returns:
            A string containing step information
        """
        info = []
        
        # Step progress
        if step_data.total_steps > 0:
            info.append(f"Step {step_data.step_number}/{step_data.total_steps}")
        else:
            info.append(f"Step {step_data.step_number}")
        
        # Description
        info.append(step_data.description)
        
        # Algorithm-specific info
        if "unvisited_count" in step_data.algorithm_specific_data:
            count = step_data.algorithm_specific_data["unvisited_count"]
            info.append(f"Unvisited cells: {count}")
        
        # Legend
        if self.use_color:
            info.append("\nLegend:")
            info.append("\033[41m █ \033[0m Current cell")
            info.append("\033[43m ▒ \033[0m Candidate cells")
            info.append("\033[44m ▓ \033[0m Current run (Sidewinder)")
        
        return "\n".join(info)
    
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