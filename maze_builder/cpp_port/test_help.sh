#!/bin/bash
# Test script for C++ mazebuilder --help command

echo "Testing C++ mazebuilder help commands"
echo "===================================="

# Compile the program first
echo "Compiling mazebuilder.cpp..."
g++ -std=c++11 mazebuilder.cpp -o mazebuilder
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi

# Test -h flag
echo -e "\nTesting -h flag:"
./mazebuilder -h > help_output_h.txt 2>&1
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "✓ Exit code is 0"
else
    echo "✗ Exit code is $exit_code"
fi

# Check if help text is present
if grep -q "MazeBuilder - A maze generation tool" help_output_h.txt; then
    echo "✓ Help header found"
else
    echo "✗ Help header not found"
fi

if grep -q "Usage:" help_output_h.txt; then
    echo "✓ Usage section found"
else
    echo "✗ Usage section not found"
fi

if grep -q "Examples:" help_output_h.txt; then
    echo "✓ Examples section found"
else
    echo "✗ Examples section not found"
fi

if grep -q "Algorithm:" help_output_h.txt; then
    echo "✓ Algorithm section found"
else
    echo "✗ Algorithm section not found"
fi

# Test --help flag
echo -e "\nTesting --help flag:"
./mazebuilder --help > help_output_help.txt 2>&1
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "✓ Exit code is 0"
else
    echo "✗ Exit code is $exit_code"
fi

# Check if help text is present
if grep -q "MazeBuilder - A maze generation tool" help_output_help.txt; then
    echo "✓ Help header found"
else
    echo "✗ Help header not found"
fi

# Test that normal usage still works
echo -e "\nTesting normal usage (5x5 maze):"
./mazebuilder 5 5 > maze_output.txt 2>&1
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo "✓ Exit code is 0"
    # Check if maze was generated
    if grep -q "+----" maze_output.txt && grep -q "|" maze_output.txt; then
        echo "✓ Maze output detected"
    else
        echo "✗ No maze output detected"
    fi
else
    echo "✗ Exit code is $exit_code"
fi

# Clean up
rm -f help_output_h.txt help_output_help.txt maze_output.txt

echo -e "\nTest complete!"