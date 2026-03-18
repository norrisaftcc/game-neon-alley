import sys
import os
import pytest
import subprocess

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCLI:
    def test_run_maze_help_short_flag(self):
        """Test the -h flag displays help."""
        result = subprocess.run([sys.executable, "run_maze.py", "-h"], 
                                capture_output=True, text=True, 
                                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        assert result.returncode == 0
        assert "MazeBuilder - A maze generation and visualization tool" in result.stdout
        assert "Examples:" in result.stdout
        assert "Algorithms:" in result.stdout
        assert "Renderers:" in result.stdout
        assert "Themes:" in result.stdout
        
    def test_run_maze_help_long_flag(self):
        """Test the --help flag displays help."""
        result = subprocess.run([sys.executable, "run_maze.py", "--help"], 
                                capture_output=True, text=True,
                                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        assert result.returncode == 0
        assert "MazeBuilder - A maze generation and visualization tool" in result.stdout
        assert "Examples:" in result.stdout
        assert "Algorithms:" in result.stdout
        assert "Renderers:" in result.stdout
        assert "Themes:" in result.stdout
        
    def test_run_maze_explain_binary_tree(self):
        """Test the --explain flag with binary tree algorithm."""
        result = subprocess.run([sys.executable, "run_maze.py", "--algorithm", "binary", "--explain"], 
                                capture_output=True, text=True,
                                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        assert result.returncode == 0
        assert "Binary Tree Algorithm:" in result.stdout
        assert "For each cell, randomly carve a passage either north or east." in result.stdout
        
    def test_run_maze_explain_sidewinder(self):
        """Test the --explain flag with sidewinder algorithm."""
        result = subprocess.run([sys.executable, "run_maze.py", "--algorithm", "sidewinder", "--explain"], 
                                capture_output=True, text=True,
                                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        assert result.returncode == 0
        assert "Sidewinder Algorithm:" in result.stdout
        assert "Creates horizontal \"runs\" of connected cells." in result.stdout
        
    def test_run_maze_explain_aldous_broder(self):
        """Test the --explain flag with aldous-broder algorithm."""
        result = subprocess.run([sys.executable, "run_maze.py", "--algorithm", "aldous-broder", "--explain"], 
                                capture_output=True, text=True,
                                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        assert result.returncode == 0
        assert "Aldous-Broder Algorithm:" in result.stdout
        assert "Performs a random walk, connecting unvisited cells." in result.stdout
        
    def test_main_py_help_short_flag(self):
        """Test the -h flag displays help for main.py."""
        result = subprocess.run([sys.executable, "main.py", "-h"], 
                                capture_output=True, text=True, 
                                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        assert result.returncode == 0
        assert "Generate and display mazes" in result.stdout
        assert "--explain" in result.stdout
        
    def test_main_py_help_long_flag(self):
        """Test the --help flag displays help for main.py."""
        result = subprocess.run([sys.executable, "main.py", "--help"], 
                                capture_output=True, text=True,
                                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        assert result.returncode == 0
        assert "Generate and display mazes" in result.stdout
        assert "--explain" in result.stdout