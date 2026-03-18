import sys
import os
import pytest

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grid import Grid
from algorithms.step_by_step import (
    AlgorithmStep, 
    StepByStepBinaryTree, 
    StepByStepSidewinder, 
    StepByStepAldousBroder
)


class TestStepByStepVisualization:
    def test_algorithm_step_dataclass(self):
        """Test the AlgorithmStep dataclass."""
        from cell import Cell
        
        cell = Cell(0, 0)
        step = AlgorithmStep(
            current_cell=cell,
            candidate_cells=[],
            chosen_cell=None,
            connection_made=None,
            algorithm_specific_data={},
            description="Test step",
            step_number=1,
            total_steps=10
        )
        
        assert step.current_cell == cell
        assert step.candidate_cells == []
        assert step.description == "Test step"
        assert step.step_number == 1
        assert step.total_steps == 10
    
    def test_step_by_step_binary_tree(self):
        """Test step-by-step Binary Tree algorithm."""
        grid = Grid(3, 3)
        stepper = StepByStepBinaryTree(grid)
        
        # Collect all steps
        steps = list(stepper.steps())
        
        # Should have one step per cell
        assert len(steps) == 9
        
        # Check first step
        first_step = steps[0]
        assert first_step.current_cell == grid.at(0, 0)
        assert first_step.step_number == 1
        assert first_step.total_steps == 9
        
        # Verify maze is complete
        # In a 3x3 grid, a complete maze should have at least 8 connections
        connection_count = 0
        for row in range(grid.rows):
            for col in range(grid.cols):
                cell = grid.at(row, col)
                connection_count += len(cell.get_links())
        
        # Each connection is counted from both sides
        assert connection_count >= 16  # 8 connections * 2
    
    def test_step_by_step_sidewinder(self):
        """Test step-by-step Sidewinder algorithm."""
        grid = Grid(3, 3)
        stepper = StepByStepSidewinder(grid)
        
        # Collect all steps
        steps = list(stepper.steps())
        
        # Should have one step per cell
        assert len(steps) == 9
        
        # Check for run-specific data
        has_run_data = False
        for step in steps:
            if "run" in step.algorithm_specific_data:
                has_run_data = True
                break
        
        assert has_run_data, "Sidewinder should have run data in some steps"
    
    def test_step_by_step_aldous_broder(self):
        """Test step-by-step Aldous-Broder algorithm."""
        grid = Grid(3, 3)
        stepper = StepByStepAldousBroder(grid)
        
        # Collect all steps (limit to prevent infinite loop in case of bug)
        steps = []
        step_count = 0
        max_steps = 1000
        
        for step in stepper.steps():
            steps.append(step)
            step_count += 1
            if step_count > max_steps:
                break
        
        # Should have multiple steps (more than cells due to random walk)
        assert len(steps) > 9
        
        # Last step should indicate completion
        last_step = steps[-1]
        assert "completed" in last_step.algorithm_specific_data
        assert last_step.algorithm_specific_data["completed"] == True
        
        # Check for unvisited count tracking
        has_unvisited_data = False
        for step in steps:
            if "unvisited_count" in step.algorithm_specific_data:
                has_unvisited_data = True
                break
        
        assert has_unvisited_data, "Aldous-Broder should track unvisited count"
    
    def test_run_to_completion(self):
        """Test running algorithm to completion without yielding steps."""
        grid = Grid(5, 5)
        stepper = StepByStepBinaryTree(grid)
        
        # Run to completion
        stepper.run_to_completion()
        
        # Verify maze is complete
        connection_count = 0
        for row in range(grid.rows):
            for col in range(grid.cols):
                cell = grid.at(row, col)
                connection_count += len(cell.get_links())
        
        # Each connection is counted from both sides
        # A 5x5 maze should have 24 connections (25 cells - 1)
        assert connection_count >= 48  # 24 connections * 2