#!/usr/bin/env python3
"""
Tests for save/load functionality in the Grid class.
"""

import json
import os
import tempfile
import unittest

from grid import Grid
from algorithms.binary_tree import BinaryTreeMaze
from algorithms.sidewinder import SidewinderMaze


class TestSaveLoad(unittest.TestCase):
    """Test save and load operations for mazes."""
    
    def setUp(self):
        """Set up test cases."""
        self.test_rows = 5
        self.test_cols = 5
        self.temp_file = None
    
    def tearDown(self):
        """Clean up temporary files."""
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_empty_grid_save_load(self):
        """Test saving and loading an empty grid (no links)."""
        # Create an empty grid
        grid = Grid(self.test_rows, self.test_cols)
        
        # Save to temporary file
        self.temp_file = tempfile.mktemp(suffix='.json')
        grid.save_to_file(self.temp_file)
        
        # Load from file
        loaded_grid = Grid.load_from_file(self.temp_file)
        
        # Verify dimensions
        self.assertEqual(loaded_grid.rows, self.test_rows)
        self.assertEqual(loaded_grid.cols, self.test_cols)
        
        # Verify no links exist
        for r in range(self.test_rows):
            for c in range(self.test_cols):
                cell = loaded_grid.at(r, c)
                self.assertEqual(cell.links, 0)
    
    def test_binary_tree_save_load(self):
        """Test saving and loading a maze generated with Binary Tree algorithm."""
        # Create a maze
        grid = Grid(self.test_rows, self.test_cols)
        BinaryTreeMaze.on(grid)
        
        # Save to temporary file
        self.temp_file = tempfile.mktemp(suffix='.json')
        grid.save_to_file(self.temp_file)
        
        # Load from file
        loaded_grid = Grid.load_from_file(self.temp_file)
        
        # Verify dimensions
        self.assertEqual(loaded_grid.rows, self.test_rows)
        self.assertEqual(loaded_grid.cols, self.test_cols)
        
        # Verify all cells have identical links
        for r in range(self.test_rows):
            for c in range(self.test_cols):
                original_cell = grid.at(r, c)
                loaded_cell = loaded_grid.at(r, c)
                self.assertEqual(loaded_cell.links, original_cell.links)
    
    def test_sidewinder_save_load(self):
        """Test saving and loading a maze generated with Sidewinder algorithm."""
        # Create a maze
        grid = Grid(self.test_rows, self.test_cols)
        SidewinderMaze.on(grid)
        
        # Save to temporary file
        self.temp_file = tempfile.mktemp(suffix='.json')
        grid.save_to_file(self.temp_file)
        
        # Load from file
        loaded_grid = Grid.load_from_file(self.temp_file)
        
        # Verify dimensions
        self.assertEqual(loaded_grid.rows, self.test_rows)
        self.assertEqual(loaded_grid.cols, self.test_cols)
        
        # Verify all cells have identical links
        for r in range(self.test_rows):
            for c in range(self.test_cols):
                original_cell = grid.at(r, c)
                loaded_cell = loaded_grid.at(r, c)
                self.assertEqual(loaded_cell.links, original_cell.links)
    
    def test_saved_file_format(self):
        """Test that the saved file has the expected JSON format."""
        # Create a simple grid with one link
        grid = Grid(2, 2)
        from cell import Cell
        grid.link_cells(0, 0, Cell.EAST)
        
        # Save to temporary file
        self.temp_file = tempfile.mktemp(suffix='.json')
        grid.save_to_file(self.temp_file)
        
        # Read and parse the JSON file
        with open(self.temp_file, 'r') as f:
            data = json.load(f)
        
        # Verify structure
        self.assertEqual(data['rows'], 2)
        self.assertEqual(data['cols'], 2)
        self.assertIn('cells', data)
        self.assertEqual(len(data['cells']), 2)
        self.assertEqual(len(data['cells'][0]), 2)
        
        # Verify cell data
        for r in range(2):
            for c in range(2):
                cell_data = data['cells'][r][c]
                self.assertEqual(cell_data['row'], r)
                self.assertEqual(cell_data['col'], c)
                self.assertIn('links', cell_data)
    
    def test_invalid_file_load(self):
        """Test loading from a non-existent file raises appropriate error."""
        with self.assertRaises(FileNotFoundError):
            Grid.load_from_file('/non/existent/file.json')
    
    def test_corrupted_file_load(self):
        """Test loading from a corrupted file raises appropriate error."""
        # Create a temporary file with invalid JSON
        self.temp_file = tempfile.mktemp(suffix='.json')
        with open(self.temp_file, 'w') as f:
            f.write("This is not valid JSON")
        
        with self.assertRaises(json.JSONDecodeError):
            Grid.load_from_file(self.temp_file)
    
    def test_save_load_preserves_maze_structure(self):
        """Test that saving and loading preserves the maze's connectivity."""
        # Create a maze with a specific seed for reproducibility
        import random
        random.seed(42)
        
        grid = Grid(10, 10)
        BinaryTreeMaze.on(grid)
        
        # Count the number of links in the original
        original_link_count = 0
        for r in range(10):
            for c in range(10):
                cell = grid.at(r, c)
                original_link_count += bin(cell.links).count('1')
        
        # Save and load
        self.temp_file = tempfile.mktemp(suffix='.json')
        grid.save_to_file(self.temp_file)
        loaded_grid = Grid.load_from_file(self.temp_file)
        
        # Count the number of links in the loaded grid
        loaded_link_count = 0
        for r in range(10):
            for c in range(10):
                cell = loaded_grid.at(r, c)
                loaded_link_count += bin(cell.links).count('1')
        
        # Verify the same number of links
        self.assertEqual(loaded_link_count, original_link_count)
        
        # Verify the display output is identical
        self.assertEqual(loaded_grid.display(), grid.display())


if __name__ == '__main__':
    unittest.main()