# Maze Generation Algorithms

## Binary Tree Algorithm
- For each cell, randomly carve a passage either north or east
- Creates a "perfect maze" with exactly one path between any two points
- Has a bias toward the northeast corner
- Simple and fast implementation

## Sidewinder Algorithm
- Creates horizontal "runs" of connected cells
- Randomly ends runs by connecting one cell northward
- Creates east-west corridors with occasional north passages
- More balanced than Binary Tree

## Aldous-Broder Algorithm
- Performs a random walk, connecting unvisited cells
- Creates unbiased, perfect mazes
- Slower but produces more balanced mazes
- Guarantees uniform distribution of maze types

## Pathfinding: Dijkstra's Algorithm

The C++ implementation includes Dijkstra's algorithm for pathfinding:
- Finding the shortest path between any two cells
- Calculating the "solution" (longest shortest path through the maze)
- Visualizing the path through ASCII display
- Distance calculation from any starting point