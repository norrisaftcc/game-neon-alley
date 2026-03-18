"""
Step-by-step visualization support for maze generation algorithms.

This module provides classes that wrap the existing maze generation algorithms
to enable step-by-step visualization of the maze generation process.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict, Generator
import random

from grid import Grid
from cell import Cell


@dataclass
class AlgorithmStep:
    """Represents a single step in the maze generation algorithm."""
    current_cell: Cell
    candidate_cells: List[Cell]
    chosen_cell: Optional[Cell]
    connection_made: Optional[Tuple[Cell, Cell]]
    algorithm_specific_data: Dict
    description: str
    step_number: int
    total_steps: int
    

class StepByStepMazeBuilder:
    """Base class for step-by-step maze builders."""
    
    def __init__(self, grid: Grid):
        self.grid = grid
        self.step_count = 0
        self.total_steps = self._calculate_total_steps()
        
    def _calculate_total_steps(self) -> int:
        """Calculate the total number of steps for this algorithm."""
        # Most algorithms visit each cell once
        return self.grid.rows * self.grid.cols
        
    def steps(self) -> Generator[AlgorithmStep, None, None]:
        """Generate steps for the algorithm. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement steps()")
        
    def run_to_completion(self) -> None:
        """Run the algorithm to completion without yielding steps."""
        for step in self.steps():
            pass  # Algorithm is executed in the generator


class StepByStepBinaryTree(StepByStepMazeBuilder):
    """Step-by-step version of the Binary Tree algorithm."""
    
    def steps(self) -> Generator[AlgorithmStep, None, None]:
        """Generate each step of the Binary Tree algorithm."""
        for cell in self.grid.cells():
            self.step_count += 1
            neighbors = []
            
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)
                
            if neighbors:
                chosen = random.choice(neighbors)
                direction = "north" if chosen == cell.north else "east"
                
                yield AlgorithmStep(
                    current_cell=cell,
                    candidate_cells=neighbors,
                    chosen_cell=chosen,
                    connection_made=(cell, chosen),
                    algorithm_specific_data={"direction": direction},
                    description=f"Cell ({cell.row},{cell.col}): Linking {direction}",
                    step_number=self.step_count,
                    total_steps=self.total_steps
                )
                
                cell.link(chosen)
            else:
                yield AlgorithmStep(
                    current_cell=cell,
                    candidate_cells=[],
                    chosen_cell=None,
                    connection_made=None,
                    algorithm_specific_data={},
                    description=f"Cell ({cell.row},{cell.col}): No valid neighbors (corner)",
                    step_number=self.step_count,
                    total_steps=self.total_steps
                )


class StepByStepSidewinder(StepByStepMazeBuilder):
    """Step-by-step version of the Sidewinder algorithm."""
    
    def steps(self) -> Generator[AlgorithmStep, None, None]:
        """Generate each step of the Sidewinder algorithm."""
        for row in range(self.grid.rows):
            run = []
            
            for col in range(self.grid.cols):
                self.step_count += 1
                cell = self.grid.at(row, col)
                run.append(cell)
                
                at_eastern_boundary = (col == self.grid.cols - 1)
                at_northern_boundary = (row == 0)
                
                should_close_run = (at_eastern_boundary or 
                                  (not at_northern_boundary and random.choice([True, False])))
                
                if should_close_run:
                    if not at_northern_boundary:
                        # Pick a random cell from the run to connect north
                        chosen_cell = random.choice(run)
                        if chosen_cell.north:
                            yield AlgorithmStep(
                                current_cell=cell,
                                candidate_cells=run,
                                chosen_cell=chosen_cell,
                                connection_made=(chosen_cell, chosen_cell.north),
                                algorithm_specific_data={
                                    "run": run.copy(),
                                    "closing_run": True,
                                    "run_member": chosen_cell
                                },
                                description=f"Closing run at ({cell.row},{cell.col}), connecting ({chosen_cell.row},{chosen_cell.col}) north",
                                step_number=self.step_count,
                                total_steps=self.total_steps
                            )
                            chosen_cell.link(chosen_cell.north)
                    else:
                        yield AlgorithmStep(
                            current_cell=cell,
                            candidate_cells=[],
                            chosen_cell=None,
                            connection_made=None,
                            algorithm_specific_data={
                                "run": run.copy(),
                                "at_boundary": True
                            },
                            description=f"At northern boundary ({cell.row},{cell.col}), cannot close run",
                            step_number=self.step_count,
                            total_steps=self.total_steps
                        )
                    
                    run.clear()
                else:
                    # Continue the run
                    if cell.east:
                        yield AlgorithmStep(
                            current_cell=cell,
                            candidate_cells=[cell.east],
                            chosen_cell=cell.east,
                            connection_made=(cell, cell.east),
                            algorithm_specific_data={
                                "run": run.copy(),
                                "continuing_run": True
                            },
                            description=f"Continuing run at ({cell.row},{cell.col}), linking east",
                            step_number=self.step_count,
                            total_steps=self.total_steps
                        )
                        cell.link(cell.east)


class StepByStepAldousBroder(StepByStepMazeBuilder):
    """Step-by-step version of the Aldous-Broder algorithm."""
    
    def __init__(self, grid: Grid, start_cell: Optional[Cell] = None):
        super().__init__(grid)
        self.unvisited_count = self.grid.rows * self.grid.cols - 1
        if start_cell is None:
            self.current = self.grid.random_cell()
        else:
            self.current = start_cell
        self.current.visited = True
        
    def _calculate_total_steps(self) -> int:
        """Aldous-Broder doesn't have a fixed number of steps."""
        return -1  # Unknown until completion
        
    def steps(self) -> Generator[AlgorithmStep, None, None]:
        """Generate each step of the Aldous-Broder algorithm."""
        while self.unvisited_count > 0:
            self.step_count += 1
            neighbors = list(self.current.neighbors())
            chosen = random.choice(neighbors)
            
            if not hasattr(chosen, 'visited') or not chosen.visited:
                # This is an unvisited cell
                yield AlgorithmStep(
                    current_cell=self.current,
                    candidate_cells=neighbors,
                    chosen_cell=chosen,
                    connection_made=(self.current, chosen),
                    algorithm_specific_data={
                        "unvisited_count": self.unvisited_count,
                        "linking": True
                    },
                    description=f"At ({self.current.row},{self.current.col}), found unvisited ({chosen.row},{chosen.col}), linking",
                    step_number=self.step_count,
                    total_steps=self.total_steps
                )
                
                self.current.link(chosen)
                chosen.visited = True
                self.unvisited_count -= 1
            else:
                # Already visited, just move
                yield AlgorithmStep(
                    current_cell=self.current,
                    candidate_cells=neighbors,
                    chosen_cell=chosen,
                    connection_made=None,
                    algorithm_specific_data={
                        "unvisited_count": self.unvisited_count,
                        "just_moving": True
                    },
                    description=f"At ({self.current.row},{self.current.col}), moving to visited ({chosen.row},{chosen.col})",
                    step_number=self.step_count,
                    total_steps=self.total_steps
                )
            
            self.current = chosen
        
        # Final step to indicate completion
        yield AlgorithmStep(
            current_cell=self.current,
            candidate_cells=[],
            chosen_cell=None,
            connection_made=None,
            algorithm_specific_data={
                "completed": True,
                "total_iterations": self.step_count
            },
            description=f"Algorithm complete after {self.step_count} steps",
            step_number=self.step_count,
            total_steps=self.step_count
        )