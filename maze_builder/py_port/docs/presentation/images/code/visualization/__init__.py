"""
Visualization module for the MazeBuilder library.

This package provides different rendering options for mazes
and separates visualization logic from the core maze generation code.
"""

from .renderer_base import MazeRendererBase
from .text_renderer import TextRenderer
from .matplotlib_renderer import MatplotlibRenderer
from .themes import ThemeManager, MazeTheme, WizardryTheme, RetroTheme

# Optional import for the asciimatics renderer
# This way the library still works if asciimatics is not installed
try:
    from .asciimatics_renderer import AsciimaticsRenderer
    __has_asciimatics__ = True
except ImportError:
    __has_asciimatics__ = False

__all__ = [
    'MazeRendererBase',
    'TextRenderer',
    'MatplotlibRenderer',
    'ThemeManager',
    'MazeTheme',
    'WizardryTheme',
    'RetroTheme'
]

# Add AsciimaticsRenderer to __all__ if available
if __has_asciimatics__:
    __all__.append('AsciimaticsRenderer')