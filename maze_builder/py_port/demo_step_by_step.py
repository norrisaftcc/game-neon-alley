#!/usr/bin/env python3
"""
Demo script for the step-by-step visualization feature.
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from grid import Grid
from algorithms.step_by_step import StepByStepBinaryTree, StepByStepSidewinder
from visualization import TextRenderer
import time

def demo_binary_tree():
    """Demo the Binary Tree algorithm step by step."""
    print("Binary Tree Algorithm - Step by Step Demo")
    print("=" * 40)
    
    # Create a small grid for the demo
    grid = Grid(5, 5)
    stepper = StepByStepBinaryTree(grid)
    renderer = TextRenderer(use_color=True)
    
    for step in stepper.steps():
        os.system('clear' if os.name == 'posix' else 'cls')
        
        maze_display = renderer.render_maze(grid, step_data=step)
        step_info = renderer.render_step_info(step)
        
        print(maze_display)
        print("\n" + step_info)
        
        input("\nPress Enter to continue...")

def demo_sidewinder():
    """Demo the Sidewinder algorithm step by step."""
    print("Sidewinder Algorithm - Step by Step Demo")
    print("=" * 40)
    
    # Create a small grid for the demo
    grid = Grid(5, 5)
    stepper = StepByStepSidewinder(grid)
    renderer = TextRenderer(use_color=True)
    
    for step in stepper.steps():
        os.system('clear' if os.name == 'posix' else 'cls')
        
        maze_display = renderer.render_maze(grid, step_data=step)
        step_info = renderer.render_step_info(step)
        
        print(maze_display)
        print("\n" + step_info)
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("Step-by-Step Visualization Demo")
    print("1. Binary Tree Algorithm")
    print("2. Sidewinder Algorithm")
    
    choice = input("\nSelect demo (1 or 2): ")
    
    if choice == "1":
        demo_binary_tree()
    elif choice == "2":
        demo_sidewinder()
    else:
        print("Invalid choice. Please run again and select 1 or 2.")