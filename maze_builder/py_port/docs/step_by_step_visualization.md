# Step-by-Step Algorithm Visualization Design

## Overview
This feature will allow users to visualize maze generation algorithms step by step, showing how each algorithm makes decisions and builds the maze over time.

## Requirements
1. Show the algorithm's progress cell by cell
2. Highlight the current cell being processed
3. Show candidate cells for the next move
4. Allow users to control the speed of visualization
5. Support all three algorithms: Binary Tree, Sidewinder, and Aldous-Broder
6. Work with existing renderers (text, matplotlib, asciimatics)

## Architecture

### Core Components

1. **StepByStepMazeBuilder Base Class**
   - Wraps existing algorithm classes
   - Yields control after each step
   - Maintains algorithm state between steps
   - Provides visualization data for each step

2. **Step Data Structure**
   ```python
   class AlgorithmStep:
       current_cell: Cell
       candidate_cells: List[Cell]
       chosen_cell: Optional[Cell]
       connection_made: Optional[Tuple[Cell, Cell]]
       algorithm_specific_data: Dict
       description: str
   ```

3. **Visualization State**
   - Current maze state
   - Cells visited so far
   - Current run (for Sidewinder)
   - Algorithm-specific state

### Implementation Strategy

1. **Binary Tree Step-by-Step**
   - Show current cell
   - Highlight north and east neighbors (if available)
   - Show which direction was chosen
   - Show the connection being made

2. **Sidewinder Step-by-Step**
   - Show current run in different color
   - Show decision point: continue run or close run
   - If closing run, show which cell connects north
   - Highlight the entire run when it's closed

3. **Aldous-Broder Step-by-Step**
   - Show current cell as walker
   - Show available neighbors
   - Show chosen direction
   - Different highlight for visited vs unvisited cells
   - Show progress counter

### User Interface

1. **Command Line Options**
   ```bash
   python run_maze.py --algorithm binary --step-by-step --speed 0.5
   python run_maze.py --algorithm sidewinder --step-by-step --interactive
   ```

2. **Interactive Controls**
   - Space: Next step
   - Enter: Play/Pause
   - +/-: Adjust speed
   - R: Reset
   - Q: Quit

3. **Text Renderer**
   - Use different symbols for:
     - Current cell: █
     - Candidates: ▒
     - Visited: ▓
     - Unvisited: ░
   - Show stats: Steps taken, cells visited

4. **Matplotlib Renderer**
   - Animate using matplotlib.animation
   - Color coding:
     - Current cell: bright red
     - Candidates: yellow
     - Current run (Sidewinder): blue
     - Visited: light gray
     - Unvisited: white
   - Show algorithm description text

5. **Asciimatics Renderer**
   - Real-time terminal animation
   - Smooth transitions between steps
   - Status bar with controls

## API Design

```python
# New module: algorithms/step_by_step.py

class StepByStepBinaryTree:
    def __init__(self, grid):
        self.grid = grid
        self.current_position = (0, 0)
        
    def steps(self):
        """Generator that yields each step of the algorithm"""
        for cell in self.grid.cells():
            neighbors = []
            
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)
                
            if neighbors:
                chosen = random.choice(neighbors)
                
                yield AlgorithmStep(
                    current_cell=cell,
                    candidate_cells=neighbors,
                    chosen_cell=chosen,
                    connection_made=(cell, chosen),
                    description=f"Cell ({cell.row},{cell.col}): Linking {chosen.direction_from(cell)}"
                )
                
                cell.link(chosen)

# Usage in renderers:
stepper = StepByStepBinaryTree(grid)
for step in stepper.steps():
    renderer.render_step(grid, step)
    time.sleep(speed)
```

## Testing Strategy

1. Unit tests for step generation
2. Integration tests with renderers
3. Performance tests for large grids
4. Interactive testing scenarios

## Future Enhancements

1. Save/load visualization sessions
2. Export as video/GIF
3. Comparison mode (show multiple algorithms side by side)
4. Educational mode with detailed explanations
5. Custom algorithm support