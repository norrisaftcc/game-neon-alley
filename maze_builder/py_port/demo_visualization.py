#!/usr/bin/env python3
"""
Demo script for the visualization layer.

This script demonstrates the capabilities of the visualization layer
by generating mazes with different algorithms and rendering them with different
renderers and themes.
"""

import os
import sys
import argparse
import random

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from grid import Grid
from algorithms.binary_tree import BinaryTreeMaze
from algorithms.sidewinder import SidewinderMaze
from algorithms.aldous_broder import AldousBroderMaze
from pathfinding.dijkstra import Dijkstra
from visualization.text_renderer import TextRenderer
from visualization.matplotlib_renderer import MatplotlibRenderer
from visualization.themes import ThemeManager


def demo_text_rendering():
    """Demonstrate text-based rendering with different themes."""
    print("*** TEXT RENDERING DEMO ***")
    print()
    
    # Create a small grid for demonstration
    grid = Grid(10, 10)
    
    # Apply Sidewinder algorithm (more balanced than Binary Tree)
    SidewinderMaze.on(grid)
    
    # Find a path from bottom-left to top-right
    entrance = grid.at(grid.rows - 1, 0)  # Bottom left
    exit = grid.at(0, grid.cols - 1)      # Top right
    solution = Dijkstra.shortest_path(grid, entrance, exit)
    distances = Dijkstra.calculate_distances(grid, exit)
    
    # Render with different themes
    for theme_name in ThemeManager.list_themes():
        print(f"\n=== {theme_name.upper()} THEME ===\n")
        
        # Create a text renderer with the theme
        renderer = TextRenderer(theme_name=theme_name, use_color=True)
        
        # Render the maze with the solution path
        output = renderer.render_maze(
            grid,
            solution_path=solution,
            show_distances=True,
            distances=distances
        )
        
        print(output)
        print()


def demo_matplotlib_rendering(save_images=False):
    """Demonstrate matplotlib rendering with different themes and algorithms."""
    print("*** MATPLOTLIB RENDERING DEMO ***")
    print()

    # Import matplotlib for closing figures
    import matplotlib.pyplot as plt

    # Create directory for saved images if needed
    if save_images and not os.path.exists("demo_images"):
        os.makedirs("demo_images")

    # Dictionary mapping algorithm names to functions
    algorithms = {
        "binary_tree": BinaryTreeMaze.on,
        "sidewinder": SidewinderMaze.on,
        "aldous_broder": lambda g: AldousBroderMaze.on(g)[0]  # Discard iteration count
    }

    # We'll just use binary_tree for a quick demo
    grid = Grid(10, 10)
    random.seed(12345)  # Use consistent seed for reproducibility
    BinaryTreeMaze.on(grid)

    # Find a path from bottom-left to top-right
    entrance = grid.at(grid.rows - 1, 0)  # Bottom left
    exit = grid.at(0, grid.cols - 1)      # Top right
    solution = Dijkstra.shortest_path(grid, entrance, exit)

    # Render with each theme
    for theme_name in ThemeManager.list_themes():
        print(f"Rendering maze with {theme_name} theme...")

        # Create a matplotlib renderer with the theme
        renderer = MatplotlibRenderer(theme_name=theme_name)

        # Render the maze with the solution path
        fig = renderer.render_maze(
            grid,
            solution_path=solution,
            show_distances=True
        )

        # Save the image if requested
        if save_images:
            filename = f"demo_images/maze_{theme_name}.png"
            fig.savefig(filename, dpi=150, bbox_inches='tight')
            print(f"  Saved to {filename}")

        # Close the figure to free memory
        plt.close(fig)


def main():
    """Main entry point for the demo."""
    parser = argparse.ArgumentParser(description='Demonstration of the visualization layer')
    parser.add_argument('--text', action='store_true', help='Run text rendering demo')
    parser.add_argument('--graphical', action='store_true', help='Run matplotlib rendering demo')
    parser.add_argument('--save', action='store_true', help='Save generated images to demo_images directory')
    args = parser.parse_args()
    
    # If no specific demos are requested, run both
    if not args.text and not args.graphical:
        args.text = True
        args.graphical = True
    
    # Run requested demos
    if args.text:
        demo_text_rendering()
    
    if args.graphical:
        import matplotlib.pyplot as plt
        demo_matplotlib_rendering(save_images=args.save)
    
    print("\nDemo complete!")
    

if __name__ == "__main__":
    main()