```thanks Claude - 4/30/2025```

# MazeBuilder C++ Implementation

This is a C++ port of the MazeBuilder program, implementing a simple maze generator using the Binary Tree algorithm. The implementation focuses on three main components:

1. The `Cell` class, which represents a single cell in the maze
2. The `Grid` class, which manages the overall maze structure
3. The `BinaryTreeMaze` class, which implements the Binary Tree maze generation algorithm

## Binary Tree Algorithm

The Binary Tree algorithm is one of the simplest maze generation algorithms. For each cell in the grid, it randomly decides to connect either northward or eastward, with a bias toward the northeast corner of the maze.

The algorithm works as follows:
- For each cell in the grid, identify available neighbors (north and east)
- Randomly choose one of these neighbors to connect to
- If no neighbors are available (e.g., at the north and east edges), don't create any connections

This simple approach guarantees a perfect maze (one with exactly one path between any two cells) but creates a strong bias toward the northeast corner.

## How to Compile and Run

Compile the program with any C++ compiler:

```
g++ -std=c++11 maze_builder.cpp -o maze_builder
```

Run the program with optional parameters for rows and columns:

```
./maze_builder [rows] [columns]
```

If no parameters are provided, the program will create a 10x10 maze by default.

## Example Output

The program displays the maze using ASCII characters, with `+` for corners, `|` for vertical walls, and `---` for horizontal walls. Open passages are represented by spaces:

```
+---+---+---+---+---+
|                   |
+   +   +   +   +---+
|                   |
+   +   +   +   +---+
|                   |
+   +   +   +   +---+
|                   |
+   +   +   +   +---+
|                   |
+---+---+---+---+---+
```

In this visualization, each cell is represented by a 3x1 space, and walls are removed to indicate passages between cells.

## Code Structure

- **Cell Class**: Manages the state of a single cell, tracking its position and connections
- **Grid Class**: Manages the entire maze grid, provides methods for accessing cells and displaying the maze
- **BinaryTreeMaze Class**: Implements the Binary Tree algorithm to generate the maze pattern

## Future Improvements

Potential enhancements to consider:
- Implement additional maze generation algorithms
- Add maze solving capabilities
- Create graphical output options
- Implement maze metrics and analysis
- Support for maze entrance and exit points

## Running the Program

The code should compile with any standard C++ compiler that supports C++11 or later:

```
g++ -std=c++11 maze_builder.cpp -o maze_builder
```

You can then run it with optional parameters for rows and columns:

```
./maze_builder [rows] [columns]
```

