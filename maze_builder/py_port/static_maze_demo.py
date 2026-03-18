#!/usr/bin/env python3
"""
Static maze demo using our visualization layer.

This script demonstrates the different renderer options available
in the visualization layer by generating and displaying a maze
with each renderer.
"""

import random
import argparse

from grid import Grid
from algorithms.binary_tree import BinaryTreeMaze
from algorithms.sidewinder import SidewinderMaze
from algorithms.aldous_broder import AldousBroderMaze
from pathfinding.dijkstra import Dijkstra
from visualization import TextRenderer, MatplotlibRenderer, ThemeManager

# Check if asciimatics is available
try:
    from visualization import AsciimaticsRenderer
    HAS_ASCIIMATICS = True
except ImportError:
    HAS_ASCIIMATICS = False


def main():
    """Main entry point for the demo script."""
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description='Maze visualization demo')
    parser.add_argument('--rows', '-r', type=int, default=12, help='Number of rows in the maze')
    parser.add_argument('--cols', '-c', type=int, default=12, help='Number of columns in the maze')
    parser.add_argument('--algorithm', '-a', choices=['binary', 'sidewinder', 'aldous-broder'],
                        default='binary', help='Maze generation algorithm to use')
    parser.add_argument('--seed', '-s', type=int, help='Random seed for reproducible mazes')
    parser.add_argument('--theme', '-t', choices=ThemeManager.list_themes(),
                        default='default', help='Visual theme to use')
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
    distances = Dijkstra.calculate_distances(grid, exit)

    # Display using text renderer
    print("\n=== Text Renderer (theme: {}) ===\n".format(args.theme))
    text_renderer = TextRenderer(theme_name=args.theme, use_color=True)
    text_output = text_renderer.render_maze(
        grid, 
        solution_path=solution, 
        show_distances=True,
        distances=distances
    )
    print(text_output)
    print()

    # Display using matplotlib renderer (save to file)
    print("=== Matplotlib Renderer (theme: {}) ===".format(args.theme))
    matplot_renderer = MatplotlibRenderer(theme_name=args.theme)
    fig = matplot_renderer.render_maze(
        grid, 
        solution_path=solution, 
        show_distances=True
    )
    filename = f"maze_{args.algorithm}_{args.theme}.png"
    fig.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved to {filename}")
    print()

    # Information about the asciimatics renderer
    print("=== Asciimatics Renderer ===")
    if HAS_ASCIIMATICS:
        print("Asciimatics is available. To run the interactive maze explorer:")
        print("  python interactive_maze.py --rows {} --cols {} --algorithm {} --theme {}".format(
            args.rows, args.cols, args.algorithm, args.theme))
    else:
        print("Asciimatics is not installed. To install:")
        print("  pip install asciimatics")
        print("Then run the interactive maze explorer:")
        print("  python interactive_maze.py")
    print()


if __name__ == "__main__":
    main()