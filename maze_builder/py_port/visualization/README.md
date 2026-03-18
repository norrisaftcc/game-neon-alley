# MazeBuilder Visualization Module

This module provides rendering capabilities for the MazeBuilder library, separating visualization logic from core maze generation algorithms.

## Key Components

- **BaseRenderer**: Abstract base class defining the common interface for renderers
- **TextRenderer**: ASCII/ANSI text-based renderer for terminal output
- **MatplotlibRenderer**: Graphical renderer using matplotlib
- **ThemeManager**: Central registry for theme management
- **Theme classes**: Define styling properties (colors, fonts, etc.)

## Quick Start

### Text Renderer

```python
from visualization.text_renderer import TextRenderer

# Create a text renderer with the "retro" theme
renderer = TextRenderer(theme_name="retro", use_color=True)

# Render a maze with a solution path
output = renderer.render_maze(grid, solution_path=path, show_distances=True)
print(output)
```

### Matplotlib Renderer

```python
from visualization.matplotlib_renderer import MatplotlibRenderer

# Create a matplotlib renderer with the "wizardry" theme
renderer = MatplotlibRenderer(theme_name="wizardry")

# Render a maze with a solution path
fig = renderer.render_maze(grid, solution_path=path, show_distances=True)

# Display in a GUI or save to file
plt.show()
# or
renderer.save_maze(grid, "maze.png", solution_path=path, dpi=300)
```

## Available Themes

- **default**: Basic black and white theme
- **wizardry**: Fantasy-themed style with midnight blue background and golden elements
- **retro**: 1980s computer terminal theme with green phosphor display

## Extending the Module

### Adding a New Theme

```python
from visualization.themes import MazeTheme, ThemeManager

class MyCustomTheme(MazeTheme):
    def __init__(self):
        super().__init__()
        # Override default properties
        self.bg_color = "#123456"
        self.wall_color = "#ABCDEF"
        # ...etc...

# Register the theme
ThemeManager.register_theme("my_theme", MyCustomTheme)
```

### Adding a New Renderer

```python
from visualization.renderer_base import MazeRendererBase

class MyCustomRenderer(MazeRendererBase):
    def __init__(self, theme_name="default"):
        super().__init__(theme_name)
        # Additional initialization
        
    def render_maze(self, grid, solution_path=None, show_distances=False, distances=None, **kwargs):
        # Implementation details
        # ...
        return result
```

## Technical Notes

- Renderers are responsible for handling theme properties appropriately
- All renderers follow the same interface defined by BaseRenderer
- Themes are managed centrally through ThemeManager
- Terminal colors are automatically disabled on platforms that don't support them