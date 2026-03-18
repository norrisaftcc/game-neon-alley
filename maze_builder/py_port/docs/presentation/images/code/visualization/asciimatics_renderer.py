"""
Asciimatics-based renderer for mazes.

This module provides an interactive terminal-based visualization for mazes using
the asciimatics library, supporting animations and interactive exploration.
"""

import time
from asciimatics.screen import Screen
from asciimatics.effects import Print
from asciimatics.renderers import ColourImageFile, FigletText
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.event import KeyboardEvent

from .renderer_base import MazeRendererBase
from .themes import ThemeManager

# ANSI color codes by index
# 0: Black, 1: Red, 2: Green, 3: Yellow, 4: Blue, 5: Magenta, 6: Cyan, 7: White
# Add 8 for bright/bold versions

class AsciimaticsRenderer(MazeRendererBase):
    """Renders and animates mazes using asciimatics for terminal-based visualizations."""
    
    # Mapping of direction keys to constants
    KEY_UP = Screen.KEY_UP
    KEY_DOWN = Screen.KEY_DOWN
    KEY_LEFT = Screen.KEY_LEFT
    KEY_RIGHT = Screen.KEY_RIGHT
    KEY_QUIT = ord('q')
    KEY_HELP = ord('h')
    KEY_TOGGLE_SOLUTION = ord('s')
    
    def __init__(self, theme_name="default"):
        """
        Initialize an asciimatics renderer with the specified theme.
        
        Args:
            theme_name: The name of the theme to use
        """
        super().__init__(theme_name)
        self.theme = ThemeManager.get_theme(theme_name)
        self.current_position = None
        self.show_solution = False
        self.goal_position = None
        self.path = None
        self.screen = None
        self.paused = False
        self.help_text = [
            "Movement: Arrow Keys",
            "Toggle Solution: 's'",
            "Help: 'h'",
            "Quit: 'q'"
        ]
    
    def _theme_to_screen_colors(self):
        """
        Convert theme colors to asciimatics screen color constants.
        
        Returns:
            A dictionary of color mappings
        """
        # Convert hex colors to closest ANSI color constants
        # For simplicity we're using basic colors here
        if self.theme_name == "retro":
            return {
                "wall": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
                "path": (Screen.COLOUR_GREEN, 0, Screen.COLOUR_BLACK),
                "entrance": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
                "exit": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
                "player": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_GREEN),
                "help_text": (Screen.COLOUR_GREEN, 0, Screen.COLOUR_BLACK),
                "title": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK)
            }
        elif self.theme_name == "wizardry":
            return {
                "wall": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLACK),
                "path": (Screen.COLOUR_BLUE, 0, Screen.COLOUR_BLACK),
                "entrance": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
                "exit": (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK),
                "player": (Screen.COLOUR_CYAN, Screen.A_BOLD, Screen.COLOUR_BLACK),
                "help_text": (Screen.COLOUR_WHITE, 0, Screen.COLOUR_BLACK),
                "title": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLACK)
            }
        else:  # default theme
            return {
                "wall": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
                "path": (Screen.COLOUR_CYAN, 0, Screen.COLOUR_BLACK),
                "entrance": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLACK),
                "exit": (Screen.COLOUR_RED, Screen.A_BOLD, Screen.COLOUR_BLACK), 
                "player": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE),
                "help_text": (Screen.COLOUR_WHITE, 0, Screen.COLOUR_BLACK),
                "title": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK)
            }
    
    def _draw_maze(self, screen, grid, path=None):
        """
        Draw the maze on the screen.
        
        Args:
            screen: The asciimatics screen to draw on
            grid: The maze grid to render
            path: Optional solution path
        """
        colors = self._theme_to_screen_colors()
        
        # Get entrance and exit
        entrance, exit = self.get_entrance_exit(grid)
        
        # Set default current position if not set yet
        if self.current_position is None:
            self.current_position = (entrance.row, entrance.col)
        
        if self.goal_position is None:
            self.goal_position = (exit.row, exit.col)
        
        # Title
        title_text = self.theme.title_text
        screen.print_at(
            title_text, 
            (screen.width - len(title_text)) // 2, 
            1,
            colour=colors["title"][0],
            attr=colors["title"][1],
            bg=colors["title"][2]
        )
        
        # Calculate position to center the maze
        maze_height = grid.rows * 2 + 1
        maze_width = grid.cols * 4 + 1
        start_y = max(3, (screen.height - maze_height) // 2)
        start_x = max(0, (screen.width - maze_width) // 2)
        
        # Draw top border
        for x in range(grid.cols):
            screen.print_at(
                "+---", 
                start_x + x * 4, 
                start_y,
                colour=colors["wall"][0],
                attr=colors["wall"][1],
                bg=colors["wall"][2]
            )
        screen.print_at(
            "+", 
            start_x + grid.cols * 4, 
            start_y,
            colour=colors["wall"][0],
            attr=colors["wall"][1],
            bg=colors["wall"][2]
        )
        
        # Draw cells and walls
        for r in range(grid.rows):
            # Cell contents and eastern boundaries
            row_chars = ["|"]
            for c in range(grid.cols):
                cell = grid.at(r, c)
                
                # Determine cell content and color
                content = "   "
                color = colors["path"]
                
                # Special cell rendering
                cell_pos = (r, c)
                is_entrance = (cell.row == entrance.row and cell.col == entrance.col)
                is_exit = (cell.row == exit.row and cell.col == exit.col)
                is_player = cell_pos == self.current_position
                is_on_path = self.show_solution and path and self.is_on_path(r, c, path)
                
                if is_player:
                    content = " @ "
                    color = colors["player"]
                elif is_entrance:
                    content = " E "
                    color = colors["entrance"]
                elif is_exit:
                    content = " X "
                    color = colors["exit"]
                elif is_on_path:
                    # For path cells with distance
                    if path:
                        for i, path_cell in enumerate(path):
                            if path_cell.row == r and path_cell.col == c:
                                distance = len(path) - i - 1
                                if distance < 10:
                                    content = f" {distance} "
                                else:
                                    content = f"{distance} "
                                break
                    color = colors["path"]
                
                screen.print_at(
                    content,
                    start_x + c * 4 + 1,
                    start_y + r * 2 + 1,
                    colour=color[0],
                    attr=color[1],
                    bg=color[2]
                )
                
                # Eastern boundary
                if c < grid.cols - 1 and cell.linked(4):  # 4 is EAST
                    east_char = " "
                else:
                    east_char = "|"
                
                screen.print_at(
                    east_char,
                    start_x + c * 4 + 4,
                    start_y + r * 2 + 1,
                    colour=colors["wall"][0],
                    attr=colors["wall"][1],
                    bg=colors["wall"][2]
                )
            
            # Southern boundary
            if r < grid.rows - 1:
                for c in range(grid.cols):
                    cell = grid.at(r, c)
                    if cell.linked(2):  # 2 is SOUTH
                        south_char = "+   "
                    else:
                        south_char = "+---"
                    
                    screen.print_at(
                        south_char,
                        start_x + c * 4,
                        start_y + r * 2 + 2,
                        colour=colors["wall"][0],
                        attr=colors["wall"][1],
                        bg=colors["wall"][2]
                    )
                
                screen.print_at(
                    "+",
                    start_x + grid.cols * 4,
                    start_y + r * 2 + 2,
                    colour=colors["wall"][0],
                    attr=colors["wall"][1],
                    bg=colors["wall"][2]
                )
        
        # Draw bottom border
        for x in range(grid.cols):
            screen.print_at(
                "+---", 
                start_x + x * 4, 
                start_y + grid.rows * 2,
                colour=colors["wall"][0],
                attr=colors["wall"][1],
                bg=colors["wall"][2]
            )
        screen.print_at(
            "+", 
            start_x + grid.cols * 4, 
            start_y + grid.rows * 2,
            colour=colors["wall"][0],
            attr=colors["wall"][1],
            bg=colors["wall"][2]
        )
        
        # Status line
        status = f"Position: {self.current_position[0]},{self.current_position[1]} | "
        if self.current_position == self.goal_position:
            status += "You reached the exit!"
        elif self.show_solution:
            status += "Solution visible"
        else:
            status += "Navigate to the exit (X)"
        
        screen.print_at(
            status,
            (screen.width - len(status)) // 2,
            start_y + maze_height + 1,
            colour=colors["help_text"][0],
            attr=colors["help_text"][1],
            bg=colors["help_text"][2]
        )
        
        # Help text (if paused)
        if self.paused:
            help_y = start_y + maze_height + 3
            for i, line in enumerate(self.help_text):
                screen.print_at(
                    line,
                    (screen.width - len(line)) // 2,
                    help_y + i,
                    colour=colors["help_text"][0],
                    attr=colors["help_text"][1],
                    bg=colors["help_text"][2]
                )
    
    def _process_input(self, event, grid):
        """
        Process keyboard input for interactive maze navigation.
        
        Args:
            event: The keyboard event to process
            grid: The maze grid
            
        Returns:
            True if the application should continue, False to quit
        """
        if not isinstance(event, KeyboardEvent):
            return True
            
        if event.key_code == self.KEY_QUIT:
            return False
        
        if event.key_code == self.KEY_HELP:
            self.paused = not self.paused
            return True
        
        if event.key_code == self.KEY_TOGGLE_SOLUTION:
            self.show_solution = not self.show_solution
            return True
        
        # Move player
        row, col = self.current_position
        new_row, new_col = row, col
        
        if event.key_code == self.KEY_UP and row > 0:
            # Check if there's a path north
            cell = grid.at(row, col)
            if cell.linked(1):  # 1 is NORTH
                new_row = row - 1
        elif event.key_code == self.KEY_DOWN and row < grid.rows - 1:
            # Check if there's a path south
            cell = grid.at(row, col)
            if cell.linked(2):  # 2 is SOUTH
                new_row = row + 1
        elif event.key_code == self.KEY_RIGHT and col < grid.cols - 1:
            # Check if there's a path east
            cell = grid.at(row, col)
            if cell.linked(4):  # 4 is EAST
                new_col = col + 1
        elif event.key_code == self.KEY_LEFT and col > 0:
            # Check if there's a path west
            cell = grid.at(row, col)
            if cell.linked(8):  # 8 is WEST
                new_col = col - 1
        
        self.current_position = (new_row, new_col)
        return True
    
    def _interactive_maze(self, screen, grid, path=None):
        """
        Run the interactive maze application.
        
        Args:
            screen: The asciimatics screen
            grid: The maze grid
            path: Optional solution path
        """
        # Clear the screen
        screen.clear()
        
        # Save the screen for later reference
        self.screen = screen
        
        # Event loop
        while True:
            self._draw_maze(screen, grid, path)
            screen.refresh()
            
            # Get input
            event = screen.get_event()
            if event:
                # Process input
                if not self._process_input(event, grid):
                    raise StopApplication("User quit")
            
            # Short sleep to prevent high CPU usage
            time.sleep(0.05)
    
    def render_maze(self, grid, solution_path=None, interactive=True, **kwargs):
        """
        Render a maze using asciimatics.
        
        Args:
            grid: The maze grid to render
            solution_path: Optional list of cells forming a path through the maze
            interactive: Whether to run in interactive mode or just return a display function
            **kwargs: Additional keyword arguments:
                show_solution: Start with solution visible
                current_position: Initial player position as (row, col)
            
        Returns:
            If interactive is True, runs the interactive app.
            If interactive is False, returns a function that can be passed to asciimatics.
        """
        # Save path for later
        self.path = solution_path
        
        # Set initial state from kwargs
        if 'show_solution' in kwargs:
            self.show_solution = kwargs['show_solution']
        
        if 'current_position' in kwargs:
            self.current_position = kwargs['current_position']
        
        # If running interactively, start the screen and run the app
        if interactive:
            try:
                # Set up entrance as initial position if not set
                if self.current_position is None:
                    entrance, _ = self.get_entrance_exit(grid)
                    self.current_position = (entrance.row, entrance.col)
                
                # Run the interactive app
                Screen.wrapper(lambda screen: self._interactive_maze(screen, grid, solution_path))
                return None
            except ResizeScreenError:
                return self.render_maze(grid, solution_path, interactive, **kwargs)
        else:
            # Return a function that can be used with asciimatics effects
            return lambda screen: self._draw_maze(screen, grid, solution_path)


def demo_maze(theme_name="default"):
    """
    Standalone demo function to showcase the asciimatics renderer.
    
    Args:
        theme_name: The name of the theme to use
    """
    import sys
    import os
    
    # Add the parent directory to the path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from grid import Grid
    from algorithms.binary_tree import BinaryTreeMaze
    from pathfinding.dijkstra import Dijkstra
    
    # Create a grid and apply a maze generation algorithm
    grid = Grid(15, 15)
    BinaryTreeMaze.on(grid)
    
    # Find a path from entrance to exit
    entrance = grid.at(grid.rows - 1, 0)  # Bottom left
    exit = grid.at(0, grid.cols - 1)      # Top right
    solution = Dijkstra.shortest_path(grid, entrance, exit)
    
    # Create a renderer and run the interactive app
    renderer = AsciimaticsRenderer(theme_name=theme_name)
    renderer.render_maze(grid, solution_path=solution, interactive=True)


if __name__ == "__main__":
    # Run the demo if this module is executed directly
    import sys
    theme = "default"
    if len(sys.argv) > 1:
        theme = sys.argv[1]
    demo_maze(theme)