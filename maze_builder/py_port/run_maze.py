#!/usr/bin/env python3
"""
Unified command-line script for maze generation and visualization.

This script provides a single entry point for all maze functionality:
- Generate mazes with different algorithms
- Visualize mazes with different renderers
- Launch interactive maze exploration
"""

import sys
import argparse
import random
import time
import os

from grid import Grid
from algorithms.binary_tree import BinaryTreeMaze
from algorithms.sidewinder import SidewinderMaze
from algorithms.aldous_broder import AldousBroderMaze
from algorithms.step_by_step import StepByStepBinaryTree, StepByStepSidewinder, StepByStepAldousBroder
from pathfinding.dijkstra import Dijkstra
from visualization import TextRenderer, MatplotlibRenderer, ThemeManager

# Check if asciimatics is available
try:
    from visualization import AsciimaticsRenderer
    HAS_ASCIIMATICS = True
except ImportError:
    HAS_ASCIIMATICS = False


def main():
    """Main entry point for the unified maze script."""
    # Set up command-line arguments
    parser = argparse.ArgumentParser(description='MazeBuilder - A maze generation and visualization tool',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog='''
Examples:
  %(prog)s --rows 20 --cols 20 --algorithm binary
    Generate a 20x20 maze using binary tree algorithm

  %(prog)s --algorithm sidewinder --renderer matplotlib --save maze.png
    Generate a maze using sidewinder and save as image

  %(prog)s --renderer asciimatics --show-solution
    Interactive maze explorer with solution display

  %(prog)s --theme retro --algorithm aldous-broder 
    Generate a maze with retro theme using Aldous-Broder algorithm

  %(prog)s --algorithm binary --step-by-step --speed 0.1
    Watch Binary Tree algorithm generate a maze step by step

  %(prog)s --algorithm sidewinder --step-by-step --interactive
    Step through Sidewinder algorithm interactively

Algorithms:
  binary        - Simple algorithm creating mazes with northeast bias
  sidewinder    - Creates balanced horizontal runs with north connections
  aldous-broder - Random walk algorithm creating unbiased mazes

Renderers:  
  text         - ASCII text display in terminal
  matplotlib   - Generate static image file
  asciimatics  - Interactive terminal-based explorer (requires asciimatics)

Themes:
  default      - Classic black and white
  retro        - Green terminal style
  wizardry     - Castle-like appearance
  matrix       - Matrix-inspired green theme

For more information about the algorithms, use:
  python run_maze.py --algorithm <name> --explain
''')
    
    # Maze generation parameters
    parser.add_argument('--rows', '-r', type=int, default=12, help='Number of rows in the maze')
    parser.add_argument('--cols', '-c', type=int, default=12, help='Number of columns in the maze')
    parser.add_argument('--algorithm', '-a', choices=['binary', 'sidewinder', 'aldous-broder'],
                        default='binary', help='Maze generation algorithm to use')
    parser.add_argument('--seed', '-s', type=int, help='Random seed for reproducible mazes')
    
    # Visualization parameters
    parser.add_argument('--theme', '-t', choices=ThemeManager.list_themes(),
                        default='default', help='Visual theme to use')
    parser.add_argument('--renderer', '-R', choices=['text', 'matplotlib', 'asciimatics'],
                        default='text', help='Renderer to use for visualization')
    parser.add_argument('--show-solution', action='store_true', help='Show solution path')
    parser.add_argument('--no-distances', dest='show_distances', action='store_false',
                        help='Hide distances on solution path')
    parser.add_argument('--save', '-S', help='Save output to file (for matplotlib renderer)')
    
    # Save/load parameters
    parser.add_argument('--save-maze', help='Save generated maze to JSON file')
    parser.add_argument('--load-maze', help='Load maze from JSON file')
    
    # Help/info parameters
    parser.add_argument('--explain', action='store_true', help='Show explanation of the chosen algorithm')
    
    # Step-by-step parameters
    parser.add_argument('--step-by-step', action='store_true', help='Enable step-by-step visualization')
    parser.add_argument('--speed', type=float, default=0.5, help='Speed of step-by-step animation (seconds per step)')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode for step-by-step (press keys to advance)')
    
    args = parser.parse_args()

    # Check if asciimatics is requested but not available
    if args.renderer == 'asciimatics' and not HAS_ASCIIMATICS:
        print("Error: The asciimatics renderer was requested but not available.")
        print("Please install it with: pip install asciimatics")
        sys.exit(1)

    # Initialize random seed if provided
    if args.seed is not None:
        random.seed(args.seed)

    # Load maze from file or generate new one
    if args.load_maze:
        grid = Grid.load_from_file(args.load_maze)
        print(f"Loaded maze from {args.load_maze}")
    else:
        # Create grid
        grid = Grid(args.rows, args.cols)

        # Apply selected maze generation algorithm and handle explain flag
        if args.step_by_step:
            # Use step-by-step version
            if args.algorithm == 'binary':
                if args.explain:
                    print("\nBinary Tree Algorithm:")
                    print("For each cell, randomly carve a passage either north or east.")
                    print("Creates a perfect maze with exactly one path between any two points.")
                    print("Has a bias toward the northeast corner.\n")
                stepper = StepByStepBinaryTree(grid)
            elif args.algorithm == 'sidewinder':
                if args.explain:
                    print("\nSidewinder Algorithm:")
                    print("Creates horizontal \"runs\" of connected cells.")
                    print("Randomly ends runs by connecting one cell northward.")
                    print("Creates east-west corridors with occasional north passages.\n")
                stepper = StepByStepSidewinder(grid)
            elif args.algorithm == 'aldous-broder':
                if args.explain:
                    print("\nAldous-Broder Algorithm:")
                    print("Performs a random walk, connecting unvisited cells.")
                    print("Creates unbiased, perfect mazes.")
                    print("Slower but produces more balanced mazes.\n")
                stepper = StepByStepAldousBroder(grid)
            
            # Run step-by-step visualization
            import time
            import os
            
            for step in stepper.steps():
                # Clear screen
                os.system('clear' if os.name == 'posix' else 'cls')
                
                # Render maze with current step highlighted
                text_renderer = TextRenderer(theme_name=args.theme, use_color=True)
                maze_display = text_renderer.render_maze(grid, step_data=step)
                step_info = text_renderer.render_step_info(step)
                
                print(maze_display)
                print("\n" + step_info)
                
                if args.interactive:
                    input("\nPress Enter to continue...")
                else:
                    time.sleep(args.speed)
        else:
            # Normal generation
            if args.algorithm == 'binary':
                if args.explain:
                    print("\nBinary Tree Algorithm:")
                    print("For each cell, randomly carve a passage either north or east.")
                    print("Creates a perfect maze with exactly one path between any two points.")
                    print("Has a bias toward the northeast corner.\n")
                BinaryTreeMaze.on(grid)
            elif args.algorithm == 'sidewinder':
                if args.explain:
                    print("\nSidewinder Algorithm:")
                    print("Creates horizontal \"runs\" of connected cells.")
                    print("Randomly ends runs by connecting one cell northward.")
                    print("Creates east-west corridors with occasional north passages.\n")
                SidewinderMaze.on(grid)
            elif args.algorithm == 'aldous-broder':
                if args.explain:
                    print("\nAldous-Broder Algorithm:")
                    print("Performs a random walk, connecting unvisited cells.")
                    print("Creates unbiased, perfect mazes.")
                    print("Slower but produces more balanced mazes.\n")
                grid, _ = AldousBroderMaze.on(grid)
        
        # Save maze to file if requested
        if args.save_maze:
            grid.save_to_file(args.save_maze)
            print(f"Saved maze to {args.save_maze}")

    # Calculate solution path
    entrance = grid.at(grid.rows - 1, 0)  # Bottom left
    exit = grid.at(0, grid.cols - 1)      # Top right
    solution = Dijkstra.shortest_path(grid, entrance, exit)
    distances = Dijkstra.calculate_distances(grid, exit)

    # Render the maze using the selected renderer
    if args.renderer == 'text':
        # Text renderer
        text_renderer = TextRenderer(theme_name=args.theme, use_color=True)
        output = text_renderer.render_maze(
            grid, 
            solution_path=solution if args.show_solution else None, 
            show_distances=args.show_distances,
            distances=distances
        )
        print(output)
        
    elif args.renderer == 'matplotlib':
        # Matplotlib renderer
        matplot_renderer = MatplotlibRenderer(theme_name=args.theme)
        fig = matplot_renderer.render_maze(
            grid, 
            solution_path=solution if args.show_solution else None, 
            show_distances=args.show_distances
        )
        
        filename = args.save if args.save else f"maze_{args.algorithm}_{args.theme}.png"
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Maze saved to {filename}")
        
    elif args.renderer == 'asciimatics':
        # Asciimatics renderer
        print("Launching interactive maze explorer...")
        print("Use arrow keys to navigate, 's' to toggle solution, 'h' for help, 'q' to quit")
        
        asciimatics_renderer = AsciimaticsRenderer(theme_name=args.theme)
        asciimatics_renderer.render_maze(
            grid, 
            solution_path=solution, 
            interactive=True,
            show_solution=args.show_solution,
            current_position=(entrance.row, entrance.col)
        )


if __name__ == "__main__":
    main()