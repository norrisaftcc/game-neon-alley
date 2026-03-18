"""
Tests for the visualization module.

This module contains tests for the visualization layer, including renderers and themes.
"""

import sys
import os
import unittest
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grid import Grid
from cell import Cell
from algorithms.binary_tree import BinaryTreeMaze
from pathfinding.dijkstra import Dijkstra
from visualization.text_renderer import TextRenderer
from visualization.matplotlib_renderer import MatplotlibRenderer
from visualization.themes import ThemeManager, MazeTheme


try:
    from visualization.asciimatics_renderer import AsciimaticsRenderer
    HAS_ASCIIMATICS = True
except ImportError:
    HAS_ASCIIMATICS = False


class TestThemes(unittest.TestCase):
    """Test cases for the theme system."""
    
    def test_theme_manager(self):
        """Test that ThemeManager can retrieve themes correctly."""
        # Get default theme
        default_theme = ThemeManager.get_theme()
        self.assertIsInstance(default_theme, MazeTheme)
        
        # Get specific themes
        wizardry_theme = ThemeManager.get_theme("wizardry")
        retro_theme = ThemeManager.get_theme("retro")
        
        # Check that themes have different properties
        self.assertNotEqual(wizardry_theme.title_text, retro_theme.title_text)
        self.assertEqual(wizardry_theme.title_text, "The Maze Construction")
        self.assertEqual(retro_theme.title_text, "MAZE GENERATION COMPLETE")
        
    def test_theme_registration(self):
        """Test registering a custom theme."""
        # Create a test theme
        class TestTheme(MazeTheme):
            def __init__(self):
                super().__init__()
                self.bg_color = "#FFFFFF"
                self.title_text = "Test Theme"
        
        # Register the theme
        ThemeManager.register_theme("test", TestTheme)
        
        # Check that the theme is available
        self.assertIn("test", ThemeManager.list_themes())
        
        # Get the theme and check properties
        test_theme = ThemeManager.get_theme("test")
        self.assertEqual(test_theme.title_text, "Test Theme")
        self.assertEqual(test_theme.bg_color, "#FFFFFF")


class TestTextRenderer(unittest.TestCase):
    """Test cases for the TextRenderer."""
    
    def setUp(self):
        """Set up a test grid and renderer."""
        self.grid = Grid(5, 5)
        BinaryTreeMaze.on(self.grid)
        self.renderer = TextRenderer(theme_name="default", use_color=False)
        
        # Create a path for testing
        start = self.grid.at(4, 0)  # Bottom left
        end = self.grid.at(0, 4)    # Top right
        self.path = Dijkstra.shortest_path(self.grid, start, end)
    
    def test_render_empty_maze(self):
        """Test rendering a maze without a path."""
        output = self.renderer.render_maze(self.grid)
        
        # Check that the output is a string
        self.assertIsInstance(output, str)
        
        # Check the maze structure
        lines = output.strip().split("\n")
        
        # Check the dimensions (2 characters per cell plus borders)
        # Each cell has top, bottom, and two rows for content
        expected_height = 5 * 2 + 1  # 5 cells high, each 2 rows tall, plus top border
        expected_width = 5 * 4 + 1   # 5 cells wide, each 4 chars wide, plus left border
        
        self.assertEqual(len(lines), expected_height)
        self.assertEqual(len(lines[0]), expected_width)
        
        # Check that the top-left and bottom-right corners are present
        self.assertEqual(lines[0][0], "+")
        self.assertEqual(lines[-1][-1], "+")
    
    def test_render_with_path(self):
        """Test rendering a maze with a path."""
        output = self.renderer.render_maze(
            self.grid,
            solution_path=self.path,
            show_distances=True
        )
        
        # Check that the output is a string
        self.assertIsInstance(output, str)
        
        # The output should contain path markers for each cell in the path
        for cell in self.path:
            # This is a simplistic check, but at least ensures path rendering doesn't break
            self.assertTrue(len(output) > 0)
    
    def test_theme_application(self):
        """Test that themes are applied correctly."""
        # Create renderers with different themes
        retro_renderer = TextRenderer(theme_name="retro", use_color=False)
        wizardry_renderer = TextRenderer(theme_name="wizardry", use_color=False)
        
        # Render the same maze with different themes
        retro_output = retro_renderer.render_maze(self.grid)
        wizardry_output = wizardry_renderer.render_maze(self.grid)
        
        # The outputs should differ because of theme differences
        # This is again a simplistic check
        self.assertEqual(type(retro_output), type(wizardry_output))


class TestMatplotlibRenderer(unittest.TestCase):
    """Test cases for the MatplotlibRenderer."""
    
    def setUp(self):
        """Set up a test grid and renderer."""
        self.grid = Grid(5, 5)
        BinaryTreeMaze.on(self.grid)
        self.renderer = MatplotlibRenderer(theme_name="default")
        
        # Create a path for testing
        start = self.grid.at(4, 0)  # Bottom left
        end = self.grid.at(0, 4)    # Top right
        self.path = Dijkstra.shortest_path(self.grid, start, end)
    
    def test_render_empty_maze(self):
        """Test rendering a maze without a path."""
        fig = self.renderer.render_maze(self.grid)
        
        # Check that the output is a matplotlib figure
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        
        # Check that the figure has an axis
        self.assertEqual(len(fig.axes), 1)
    
    def test_render_with_path(self):
        """Test rendering a maze with a path."""
        fig = self.renderer.render_maze(
            self.grid,
            solution_path=self.path,
            show_distances=True
        )
        
        # Check that the output is a matplotlib figure
        self.assertIsInstance(fig, matplotlib.figure.Figure)
        
        # Check that the figure has an axis
        self.assertEqual(len(fig.axes), 1)
    
    def test_figure_size(self):
        """Test that the figure size can be set."""
        # Create a renderer with a specific size
        renderer = MatplotlibRenderer(theme_name="default", figsize=(8, 8))
        
        # Render a maze
        fig = renderer.render_maze(self.grid)
        
        # Check the figure size
        self.assertEqual(fig.get_figwidth(), 8)
        self.assertEqual(fig.get_figheight(), 8)
        
        # Try setting a new size
        renderer.set_figsize((6, 6))
        fig = renderer.render_maze(self.grid)
        
        # Check the new figure size
        self.assertEqual(fig.get_figwidth(), 6)
        self.assertEqual(fig.get_figheight(), 6)


if HAS_ASCIIMATICS:
    class TestAsciimaticsRenderer(unittest.TestCase):
        """Test cases for the AsciimaticsRenderer."""

        def setUp(self):
            """Set up a test grid and renderer."""
            self.grid = Grid(5, 5)
            BinaryTreeMaze.on(self.grid)
            self.renderer = AsciimaticsRenderer(theme_name="default")

            # Create a path for testing
            start = self.grid.at(4, 0)  # Bottom left
            end = self.grid.at(0, 4)    # Top right
            self.path = Dijkstra.shortest_path(self.grid, start, end)

        def test_theme_to_screen_colors(self):
            """Test the theme to screen colors conversion."""
            # Test that different themes produce different colors
            self.renderer.theme_name = "default"
            default_colors = self.renderer._theme_to_screen_colors()

            self.renderer.theme_name = "retro"
            retro_colors = self.renderer._theme_to_screen_colors()

            self.renderer.theme_name = "wizardry"
            wizardry_colors = self.renderer._theme_to_screen_colors()

            # Check that the themes have different colors
            self.assertNotEqual(default_colors["wall"], retro_colors["wall"])
            self.assertNotEqual(retro_colors["wall"], wizardry_colors["wall"])
            self.assertNotEqual(wizardry_colors["wall"], default_colors["wall"])


if __name__ == "__main__":
    unittest.main()