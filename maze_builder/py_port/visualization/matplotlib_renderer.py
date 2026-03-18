"""
Matplotlib-based renderer for mazes.

This module provides graphical visualization for mazes using matplotlib,
suitable for GUI applications and image export.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from .renderer_base import MazeRendererBase
from .themes import ThemeManager

class MatplotlibRenderer(MazeRendererBase):
    """Renders mazes using matplotlib for graphical output."""
    
    def __init__(self, theme_name="default", figsize=(10, 10)):
        """
        Initialize a matplotlib renderer with the specified theme and figure size.
        
        Args:
            theme_name: The name of the theme to use
            figsize: The size of the matplotlib figure as a tuple (width, height)
        """
        super().__init__(theme_name)
        self.theme = ThemeManager.get_theme(theme_name)
        self.figsize = figsize
    
    def render_maze(self, grid, solution_path=None, show_distances=False, distances=None, **kwargs):
        """
        Render a maze using matplotlib.
        
        Args:
            grid: The maze grid to render
            solution_path: Optional list of cells forming a path through the maze
            show_distances: Whether to show distances in cells
            distances: Optional distances object for showing distance values
            **kwargs: Additional keyword arguments:
                figsize: Override the figure size
                dpi: Set the figure DPI
                
        Returns:
            A matplotlib figure containing the rendered maze
        """
        # Get figure size from kwargs or use default
        figsize = kwargs.get('figsize', self.figsize)
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=figsize)
        
        # Get entrance and exit cells
        entrance, exit = self.get_entrance_exit(grid)
        
        # Set background color from theme
        ax.set_facecolor(self.theme.bg_color)
        
        # Calculate cell size (1.0 is a good default scale)
        cell_size = 1.0
        
        # Draw the cells
        for r in range(grid.rows):
            for c in range(grid.cols):
                cell = grid.at(r, c)
                
                # Cell position (y-axis inverted to match grid coordinates)
                x = c * cell_size
                y = (grid.rows - 1 - r) * cell_size
                
                # Check for special cells
                is_entrance = (cell.row == entrance.row and cell.col == entrance.col)
                is_exit = (cell.row == exit.row and cell.col == exit.col)
                is_on_path = self.is_on_path(r, c, solution_path)
                
                # Determine line style based on theme and whether the cell is on the path
                line_style = '--' if is_on_path else self.theme.line_style
                linewidth = self.theme.line_width
                
                # Draw walls where there are no links
                if not cell.linked(1) and r > 0:  # 1 is NORTH
                    ax.plot([x, x + cell_size], [y + cell_size, y + cell_size], 
                           self.theme.wall_color, linewidth=linewidth, linestyle=line_style)
                if not cell.linked(4) and c < grid.cols - 1:  # 4 is EAST
                    ax.plot([x + cell_size, x + cell_size], [y, y + cell_size], 
                           self.theme.wall_color, linewidth=linewidth, linestyle=line_style)
                if not cell.linked(2) and r < grid.rows - 1:  # 2 is SOUTH
                    ax.plot([x, x + cell_size], [y, y], 
                           self.theme.wall_color, linewidth=linewidth, linestyle=line_style)
                if not cell.linked(8) and c > 0:  # 8 is WEST
                    ax.plot([x, x], [y, y + cell_size], 
                           self.theme.wall_color, linewidth=linewidth, linestyle=line_style)
                
                # Process special cells (entrance, exit, path)
                if is_entrance:
                    if self.theme_name == "retro":
                        # For retro theme, just show a character
                        ax.text(x + cell_size/2, y + cell_size/2, self.theme.entrance_symbol, 
                               color=self.theme.entrance_color, fontsize=self.theme.font_size, 
                               ha='center', va='center', fontweight=self.theme.font_weight, 
                               family=self.theme.font_family)
                    else:
                        # For other themes, use a colored rectangle
                        ax.add_patch(plt.Rectangle((x, y), cell_size, cell_size, 
                                                 fill=True, color=self.theme.entrance_color, alpha=0.8))
                        ax.text(x + cell_size/2, y + cell_size/2, self.theme.entrance_symbol, 
                               color=self.theme.path_text_color, fontsize=self.theme.font_size,
                               ha='center', va='center', fontweight=self.theme.font_weight)
                elif is_exit:
                    if self.theme_name == "retro":
                        # For retro theme, just show a character
                        ax.text(x + cell_size/2, y + cell_size/2, self.theme.exit_symbol, 
                               color=self.theme.exit_color, fontsize=self.theme.font_size, 
                               ha='center', va='center', fontweight=self.theme.font_weight, 
                               family=self.theme.font_family)
                    else:
                        # For other themes, use a colored rectangle
                        ax.add_patch(plt.Rectangle((x, y), cell_size, cell_size, 
                                                 fill=True, color=self.theme.exit_color, alpha=0.8))
                        ax.text(x + cell_size/2, y + cell_size/2, self.theme.exit_symbol, 
                               color=self.theme.path_text_color, fontsize=self.theme.font_size,
                               ha='center', va='center', fontweight=self.theme.font_weight)
                elif is_on_path and show_distances:
                    # Calculate distance from the exit for cells on the path
                    if solution_path and distances:
                        distance = 0
                        for i, path_cell in enumerate(solution_path):
                            if path_cell.row == r and path_cell.col == c:
                                distance = len(solution_path) - i - 1
                                break
                        
                        if self.theme_name == "retro":
                            # For retro theme, show distance without background
                            ax.text(x + cell_size/2, y + cell_size/2, str(distance), 
                                   color=self.theme.path_text_color, fontsize=self.theme.font_size, 
                                   ha='center', va='center', fontweight=self.theme.font_weight, 
                                   family=self.theme.font_family)
                        else:
                            # For other themes, use a colored rectangle
                            ax.add_patch(plt.Rectangle((x, y), cell_size, cell_size, 
                                                     fill=True, color=self.theme.path_color, alpha=0.9))
                            ax.text(x + cell_size/2, y + cell_size/2, str(distance), 
                                   color=self.theme.path_text_color, fontsize=self.theme.font_size, 
                                   ha='center', va='center', fontweight=self.theme.font_weight)
        
        # Set limits and remove axes
        ax.set_xlim(0, grid.cols * cell_size)
        ax.set_ylim(0, grid.rows * cell_size)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Set title based on theme
        plt.title(self.theme.title_text, color=self.theme.title_color, 
                 fontsize=16, fontweight='bold', family=self.theme.title_font)
        
        return fig
    
    def set_figsize(self, figsize):
        """
        Set the figure size for the renderer.
        
        Args:
            figsize: A tuple of (width, height) in inches
        """
        self.figsize = figsize
    
    def save_maze(self, grid, filename, solution_path=None, show_distances=False, **kwargs):
        """
        Render a maze and save it to a file.
        
        Args:
            grid: The maze grid to render
            filename: The filename to save the image to
            solution_path: Optional list of cells forming a path through the maze
            show_distances: Whether to show distances in cells
            **kwargs: Additional keyword arguments passed to render_maze and savefig
        """
        fig = self.render_maze(grid, solution_path, show_distances, **kwargs)
        
        # Get DPI from kwargs or use default
        dpi = kwargs.get('dpi', 100)
        
        # Save the figure
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        plt.close(fig)