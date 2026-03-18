# MazeBuilder Architecture

## Core Components

### Cell Class
- Fundamental building block representing a single maze cell
- Tracks position (row, column)
- Manages connections to neighboring cells (north, south, east, west) 
- Uses bit manipulation in C++ for efficient storage of connections

### Grid Class
- Contains and manages a 2D collection of cells
- Provides methods for displaying the maze
- Handles cell neighbor configuration
- Offers utility methods for the maze algorithms

### MazeBuilder Classes
- Abstract base class `MazeBuilder` with derived algorithm implementations
- Each algorithm provides a different method for maze generation:
  - `BinaryTreeMazeBuilder`: Simple algorithm with NE bias
  - `SidewinderMazeBuilder`: Balanced east passages with occasional north links
  - `AldousBroderMazeBuilder`: Unbiased random walk algorithm

### Pathfinding (C++ version)
- `Distances` class: Maps cells to their distances from a starting point
- `Dijkstra` class: Implements pathfinding algorithm
- Can calculate the "solution path" (longest shortest path through the maze)

## Language-Specific Implementations

### C# 
- Windows Forms UI implementation
- Original port from Ruby
- Visual display of maze with cell distances

### C++
- Console-based ASCII display
- Performance-focused implementation
- Enhanced with pathfinding algorithms
- Bit manipulation for connection storage

### Python
- Multiple visualization options (matplotlib, ASCII, asciimatics)
- Step-by-step algorithm visualization
- Streamlit web UI
- Save/load functionality