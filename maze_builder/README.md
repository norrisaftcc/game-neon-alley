# MazeBuilder
2d Maze Projects

A C# port of "Mazes for Programmers" by Jamis Buck.

# Current Status
Cell and Grid initialization are complete.
Binary Tree, Sidewinder, and Aldous-Broder maze generation algorithms implemented.
Pathfinding with Dijkstra's algorithm added to C++ and Python ports.
Python visualization layer implemented with multiple renderers and themes.
Interactive terminal-based maze exploration added.

# Sprint 2 Completed (May 2025)
We've successfully completed Sprint 2 with the following achievements:
- Improved visualization with a modular architecture
- Created a dedicated visualization layer with multiple renderers
- Implemented interactive terminal-based maze navigation
- Added theme support with "Wizardry" and "Retro Terminal" styles
- Created unified command-line interfaces

# Sprint 3 Priorities (June 2025)
Based on our progress, our priorities for Sprint 3 are:
- Add A* pathfinding algorithm to C++ version
- Improve performance for large mazes
- Enhance the Streamlit UI with interactive maze solving
- Add 3D visualization options
- Expand test coverage for edge cases

# What's New
- **Save/Load Functionality**: Save mazes to JSON files and load them later for display, solving, or interactive exploration
- **Visualization Layer**: The Python port now features a dedicated visualization layer that separates rendering logic from maze algorithms
- **Multiple Renderers**: Support for text-based (terminal), graphical (matplotlib), and interactive terminal (asciimatics) rendering
- **Theme System**: Built-in themes including "Wizardry" and "Retro Terminal" styles
- **Interactive Exploration**: Navigate through mazes with keyboard controls using the asciimatics renderer
- **Streamlit UI**: Interactive web-based interface for maze generation and exploration

# To Do
- Add A* pathfinding to C++ version
- Complete unit test coverage
- Add 3D visualization options
- Performance optimization for large mazes
- Interactive maze solving in the web UI
- Add more themes and customization options
- Extend save/load functionality to include metadata (algorithm used, generation time, etc.)