#!/usr/bin/env python3
"""
Interactive maze explorer using the asciimatics renderer.

This script provides a command-line interface to generate and interactively
explore mazes using the asciimatics terminal-based UI.
"""

import sys
import argparse
import random
import logging

# Disable debug messages
logging.basicConfig(level=logging.ERROR)

from grid import Grid
from algorithms.binary_tree import BinaryTreeMaze
from algorithms.sidewinder import SidewinderMaze
from algorithms.aldous_broder import AldousBroderMaze
from pathfinding.dijkstra import Dijkstra
from visualization import ThemeManager

# Check if asciimatics is available
try:
    from visualization import AsciimaticsRenderer
    HAS_ASCIIMATICS = True
except ImportError:
    HAS_ASCIIMATICS = False


def main():
    """Main entry point for the interactive maze explorer."""
    if not HAS_ASCIIMATICS:
        print("Error: The asciimatics library is required for the interactive maze.")
        print("Please install it with: pip install asciimatics")
        sys.exit(1)

    # Set up command-line arguments
    parser = argparse.ArgumentParser(description='Interactive maze explorer')
    parser.add_argument('--rows', '-r', type=int, default=12, help='Number of rows in the maze')
    parser.add_argument('--cols', '-c', type=int, default=12, help='Number of columns in the maze')
    parser.add_argument('--algorithm', '-a', choices=['binary', 'sidewinder', 'aldous-broder'],
                        default='binary', help='Maze generation algorithm to use')
    parser.add_argument('--seed', '-s', type=int, help='Random seed for reproducible mazes')
    parser.add_argument('--theme', '-t', choices=ThemeManager.list_themes(),
                        default='wizardry', help='Visual theme to use')
    parser.add_argument('--show-solution', action='store_true', help='Start with solution visible')
    args = parser.parse_args()

    # Initialize random seed if provided
    if args.seed is not None:
        random.seed(args.seed)

    # Create grid
    grid = Grid(args.rows, args.cols)

    # Apply selected maze generation algorithm
    if args.algorithm == 'binary':
        BinaryTreeMaze.on(grid)
    elif args.algorithm == 'sidewinder':
        SidewinderMaze.on(grid)
    elif args.algorithm == 'aldous-broder':
        grid, _ = AldousBroderMaze.on(grid)

    # Calculate solution path
    entrance = grid.at(grid.rows - 1, 0)  # Bottom left
    exit = grid.at(0, grid.cols - 1)      # Top right
    solution = Dijkstra.shortest_path(grid, entrance, exit)

    # Initialize the renderer and run the interactive UI
    print("Launching interactive maze explorer...")
    print("Use arrow keys to navigate, 's' to toggle solution, 'h' for help, 'q' to quit")
    
    try:
        renderer = AsciimaticsRenderer(theme_name=args.theme)
        renderer.render_maze(
            grid, 
            solution_path=solution, 
            interactive=True,
            show_solution=args.show_solution,
            current_position=(entrance.row, entrance.col)
        )
    except KeyboardInterrupt:
        print("\nExiting interactive maze explorer.")


if __name__ == "__main__":
    main()