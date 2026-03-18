# Build Instructions

## C# Version (Windows Forms)

```bash
# Build the C# project (requires Visual Studio or MSBuild)
cd SimpleMazeBuilder1
msbuild SimpleMazeBuilder1.sln

# Run the compiled executable
./SimpleMazeBuilder1/bin/Debug/SimpleMazeBuilder1.exe
```

## C++ Version

```bash
# Compile the C++ version
cd cpp_port
g++ -std=c++11 mazebuilder.cpp -o mazebuilder

# Run with default dimensions (10x10)
./mazebuilder

# Run with custom dimensions
./mazebuilder [rows] [columns]
# Example: ./mazebuilder 15 20

# Compile the pathfinding version
g++ -std=c++11 djikstras.cpp -o djikstras

# Run the pathfinding demo
./djikstras
```

## Python Version

```bash
# Install dependencies
cd py_port
pip install -r requirements.txt

# Run the main maze generator
python main.py

# Run interactive mode
python interactive_maze.py

# Run Streamlit UI
streamlit run streamlit_app.py
```