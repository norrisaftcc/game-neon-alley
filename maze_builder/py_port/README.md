# MazeBuilder Python Port

This is a Python port of the MazeBuilder program, originally written in C# and C++.

## Features

- Generation of "perfect" mazes using multiple algorithms:
  - Binary Tree
  - Sidewinder
  - Aldous-Broder
- Multiple rendering options:
  - ASCII-based console display
  - Matplotlib graphical rendering
  - Interactive terminal navigation with asciimatics
- Multiple visual themes (default, wizardry, retro)
- Pathfinding using Dijkstra's algorithm
- Finding the "solution" (longest shortest path) through the maze
- Save/load mazes to/from JSON files

## Installation

No special installation is required beyond Python 3.6+. The program uses only standard library modules.

## Usage

```bash
# Generate a default maze
python run_maze.py

# Specify maze dimensions and algorithm
python run_maze.py --rows 20 --cols 20 --algorithm binary

# Show the solution path
python run_maze.py --show-solution

# Use a specific theme
python run_maze.py --theme wizardry

# Save a generated maze to JSON
python run_maze.py --rows 15 --cols 15 --save-maze my_maze.json

# Load a previously saved maze
python run_maze.py --load-maze my_maze.json --show-solution

# Interactive navigation (requires asciimatics)
python interactive_maze.py
# Or
python run_maze.py --renderer asciimatics
```

## Project Structure

For the up-to-date authoritative folder map for this repository, see:

- [`/FOLDER_MAP.md`](../../FOLDER_MAP.md)

## Save and Load Functionality

Mazes can be saved to JSON files for later use:

```bash
# Save a maze to file
python run_maze.py --rows 20 --cols 20 --algorithm binary --save-maze my_maze.json

# Load and display a saved maze
python run_maze.py --load-maze my_maze.json

# Load a maze and solve it
python run_maze.py --load-maze my_maze.json --show-solution

# Load a maze in interactive mode
python run_maze.py --load-maze my_maze.json --renderer asciimatics
```

The JSON format preserves the complete maze structure, including all cell connections.

## Future Enhancements

- Additional maze generation algorithms:
  - Hunt-and-Kill
  - Recursive Backtracker
  - Eller's algorithm
- Advanced pathfinding algorithms (A*)
- 3D maze generation and visualization
- Web-based interface improvements
- Performance optimizations for large mazes

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.
```