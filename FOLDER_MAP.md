# game-neon-alley — Authoritative Folder Map

This file is the single source of truth for repository layout.

> Last updated: 2026-08-02

```
/
├── FOLDER_MAP.md
├── README.md
├── NeonAlley_DesignDoc_MVP.md
└── maze_builder/
    ├── README.md
    ├── docs/
    │   ├── ALGORITHMS.md
    │   ├── ARCHITECTURE.md
    │   └── BUILD_INSTRUCTIONS.md
    ├── cpp_port/
    │   ├── README.md
    │   ├── README_old.md
    │   ├── README_pathing.md
    │   ├── mazebuilder.cpp
    │   ├── djikstras.cpp
    │   ├── test_help.sh
    │   └── mazebuilder
    └── py_port/
        ├── README.md
        ├── requirements.txt
        ├── TODO.md
        ├── main.py
        ├── run_maze.py
        ├── interactive_maze.py
        ├── streamlit_app.py
        ├── cell.py
        ├── grid.py
        ├── static_maze_demo.py
        ├── demo_visualization.py
        ├── demo_step_by_step.py
        ├── test_maze.json
        ├── meeting-notes-may9.md
        ├── algorithms/
        │   ├── __init__.py
        │   ├── aldous_broder.py
        │   ├── binary_tree.py
        │   ├── sidewinder.py
        │   └── step_by_step.py
        ├── pathfinding/
        │   ├── __init__.py
        │   ├── dijkstra.py
        │   └── distances.py
        ├── visualization/
        │   ├── README.md
        │   ├── __init__.py
        │   ├── renderer_base.py
        │   ├── text_renderer.py
        │   ├── matplotlib_renderer.py
        │   ├── asciimatics_renderer.py
        │   └── themes.py
        ├── tests/
        │   ├── README.md
        │   ├── conftest.py
        │   ├── test_aldous_broder.py
        │   ├── test_binary_tree.py
        │   ├── test_cell.py
        │   ├── test_cli.py
        │   ├── test_dijkstra.py
        │   ├── test_distances.py
        │   ├── test_grid.py
        │   ├── test_save_load.py
        │   ├── test_sidewinder.py
        │   ├── test_sidewinder_simplified.py
        │   ├── test_step_by_step.py
        │   └── test_visualization.py
        ├── docs/
        │   ├── collaboration.html
        │   ├── refactoring_summary.md
        │   ├── retro_theme_implementation.md
        │   ├── sprint3_planning.md
        │   ├── step_by_step_visualization.md
        │   ├── streamlit_ui_design.md
        │   ├── streamlit_ui_mockup.html
        │   ├── ui_concept_readme.md
        │   ├── visualization_layer.md
        │   └── presentation/
        │       ├── README.md
        │       ├── index.html
        │       └── images/
        └── demo_images/
            ├── binary_tree_default.png
            ├── maze_default.png
            ├── maze_retro.png
            └── maze_wizardry.png
```

Notes:
- `.git/` internals and Python `__pycache__/` folders are intentionally omitted.
