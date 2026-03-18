# MazeBuilder Python Port Tests

This directory contains tests for the Python port of the MazeBuilder application.

## Running Tests

To run all tests:

```bash
cd py_port
pytest
```

To run a specific test file:

```bash
pytest tests/test_cell.py
```

To run with verbose output:

```bash
pytest -v
```

## Test Coverage

The tests cover:

1. **Cell Class** - `test_cell.py`
   - Initialization
   - Linking and unlinking
   - Bit operations
   - Direction mapping

2. **Grid Class** - `test_grid.py`
   - Initialization
   - Cell access
   - Position validation
   - Cell linking
   - Grid display formatting

3. **Maze Generation Algorithms**
   - **Binary Tree Algorithm** - `test_binary_tree.py`
     - Algorithm execution on various grid positions
     - Edge cases (corners, edges)
     - Complete maze generation
   - **Sidewinder Algorithm** - `test_sidewinder.py`
     - Row connectivity
     - Vertical connections
     - Complete maze patterns
   - **Aldous-Broder Algorithm** - `test_aldous_broder.py`
     - Cell visitation completeness
     - Perfect maze validation
     - Maximum iterations limiting

4. **Pathfinding** - `test_dijkstra.py` and `test_distances.py`
   - Distance calculations from given starting points
   - Shortest path finding between any two cells
   - Longest path (maze solution) finding
   - Distance tracking and cell identification

## Key Test Properties

- **Northeast Entrance/Southwest Exit**: Tests are updated to support the standard entrance in the bottom left and exit in the top right.
- **Path Visualization**: Tests verify that paths show the distance from each cell to the exit.

## Testing Strategy

The tests use various techniques:

1. **Unit Testing** - Testing individual components in isolation
2. **Mock Objects** - Mocking random number generation for deterministic tests
3. **Fixtures** - Shared maze configurations (see `conftest.py`)
4. **Edge Cases** - Testing boundary conditions (grid edges, corners)
5. **Path Validation** - Ensuring paths are connected and valid

## Adding New Tests

When adding new maze algorithms or features, follow this pattern:

1. Create a new test file named `test_your_feature.py`
2. Use the existing test structure as a template
3. Test both normal operation and edge cases
4. For randomized algorithms, use mocking to create deterministic tests
5. For pathfinding algorithms, verify connectivity between cells

All tests are now passing and verify proper functionality of the maze generation,
display, and pathfinding capabilities.