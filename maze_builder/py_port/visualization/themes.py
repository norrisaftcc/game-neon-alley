"""
Theme definitions for maze rendering.

This module provides color schemes and styling for different visualization themes,
separating the styling concerns from the rendering logic.
"""

class MazeTheme:
    """Base class for maze themes."""
    
    def __init__(self):
        """Initialize the theme with default values."""
        # Background color
        self.bg_color = "#FFFFFF"
        
        # Wall and path colors
        self.wall_color = "#000000"
        self.path_color = "#0000FF"
        
        # Special location colors
        self.entrance_color = "#00FF00"
        self.exit_color = "#FF0000"
        
        # Text colors
        self.path_text_color = "#FFFFFF"
        self.distance_text_color = "#000000"
        
        # Title styling
        self.title_color = "#000000"
        self.title_font = "sans-serif"
        self.title_text = "Maze"
        
        # Line styling
        self.line_style = "-"
        self.line_width = 2
        
        # Text styling
        self.font_family = "sans-serif"
        self.font_size = 12
        self.font_weight = "normal"
        
        # Special symbols
        self.entrance_symbol = "E"
        self.exit_symbol = "X"
        self.path_symbol = "*"
        
        # Terminal color codes (for text renderers)
        self.use_terminal_colors = True
        self.reset_code = "\033[0m"
        self.bold_code = "\033[1m"
        self.wall_code = "\033[90m"  # Dark gray
        self.path_code = "\033[32m"  # Green
        self.entrance_code = "\033[33m"  # Yellow
        self.exit_code = "\033[31m"  # Red
        self.distance_code = "\033[36m"  # Cyan


class WizardryTheme(MazeTheme):
    """Fantasy-themed style with midnight blue background and golden elements."""
    
    def __init__(self):
        super().__init__()
        # Background color
        self.bg_color = "#000000"  # Black background
        
        # Wall and path colors
        self.wall_color = "#FFFF00"  # Bright yellow walls
        self.path_color = "#00BFFF"  # Deep sky blue
        
        # Special location colors
        self.entrance_color = "#32CD32"  # Lime green
        self.exit_color = "#FF4500"  # Orange-red
        
        # Text colors
        self.path_text_color = "#FFFFFF"  # White text
        self.distance_text_color = "#CCCCCC"  # Light gray
        
        # Title styling
        self.title_color = "gold"
        self.title_font = "serif"
        self.title_text = "The Maze Construction"
        
        # Line styling
        self.line_style = "-"
        self.line_width = 3
        
        # Text styling
        self.font_family = "serif"
        self.font_size = 12
        self.font_weight = "bold"
        
        # Special symbols
        self.entrance_symbol = "E"
        self.exit_symbol = "X"
        self.path_symbol = "*"
        
        # Terminal color codes
        self.use_terminal_colors = True
        self.reset_code = "\033[0m"
        self.bold_code = "\033[1m"
        self.wall_code = "\033[33m"  # Yellow
        self.path_code = "\033[36m"  # Cyan
        self.entrance_code = "\033[32m"  # Green
        self.exit_code = "\033[31m"  # Red
        self.distance_code = "\033[36m"  # Cyan


class RetroTheme(MazeTheme):
    """1980s computer terminal theme with green phosphor display style."""
    
    def __init__(self):
        super().__init__()
        # Background color
        self.bg_color = "#000000"  # Black background
        
        # Wall and path colors
        self.wall_color = "#00FF00"  # Bright green walls
        self.path_color = "#003300"  # Very dark green
        
        # Special location colors
        self.entrance_color = "#00AA00"  # Darker green
        self.exit_color = "#00AA00"  # Darker green
        
        # Text colors
        self.path_text_color = "#00FF00"  # Bright green text
        self.distance_text_color = "#00FF00"  # Bright green text
        
        # Title styling
        self.title_color = "#00FF00"  # Green
        self.title_font = "monospace"
        self.title_text = "MAZE GENERATION COMPLETE"
        
        # Line styling
        self.line_style = "-"  # Changed to solid for better visibility
        self.line_width = 2
        
        # Text styling
        self.font_family = "monospace"
        self.font_size = 14
        self.font_weight = "bold"
        
        # Special symbols
        self.entrance_symbol = "E"
        self.exit_symbol = "X"
        self.path_symbol = "."
        
        # Terminal color codes
        self.use_terminal_colors = True
        self.reset_code = "\033[0m"
        self.bold_code = "\033[1m"
        self.wall_code = "\033[32m"  # Green
        self.path_code = "\033[32m"  # Green
        self.entrance_code = "\033[32m"  # Green
        self.exit_code = "\033[32m"  # Green
        self.distance_code = "\033[32m"  # Green


class ThemeManager:
    """Manages the different themes available for maze rendering."""
    
    # Register available themes here
    _themes = {
        "default": MazeTheme,
        "wizardry": WizardryTheme,
        "retro": RetroTheme
    }
    
    @classmethod
    def get_theme(cls, theme_name="default"):
        """
        Get a theme instance by name.
        
        Args:
            theme_name: The name of the theme to retrieve
            
        Returns:
            An instance of the requested theme
            
        Raises:
            ValueError: If the theme name is not recognized
        """
        if theme_name not in cls._themes:
            raise ValueError(f"Unknown theme: {theme_name}. Available themes: {', '.join(cls._themes.keys())}")
        
        return cls._themes[theme_name]()
    
    @classmethod
    def register_theme(cls, theme_name, theme_class):
        """
        Register a new theme.
        
        Args:
            theme_name: The name to register the theme under
            theme_class: The theme class to register
            
        Raises:
            ValueError: If the theme name is already registered
        """
        if theme_name in cls._themes:
            raise ValueError(f"Theme {theme_name} is already registered")
        
        cls._themes[theme_name] = theme_class
    
    @classmethod
    def list_themes(cls):
        """
        List all available themes.
        
        Returns:
            A list of theme names
        """
        return list(cls._themes.keys())