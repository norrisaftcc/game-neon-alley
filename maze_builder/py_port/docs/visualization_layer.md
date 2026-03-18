# Visualization Layer

The MazeBuilder project now includes a dedicated visualization layer that separates rendering logic from the core maze generation and UI code. This architectural improvement provides several benefits:

1. **Separation of concerns**: Visualization logic is decoupled from application logic
2. **Code reuse**: Multiple interfaces can use the same rendering code
3. **Theme support**: Styling is centralized and abstracted
4. **Extensibility**: New renderers and themes can be easily added

## Architecture

The visualization layer consists of the following components:

### Base Classes

- `MazeRendererBase`: Abstract base class that defines the common interface for all renderers
- `MazeTheme`: Base class for theme definitions that specify colors, fonts, and other styling options

### Renderers

- `TextRenderer`: ASCII/ANSI text-based renderer for terminal output
- `MatplotlibRenderer`: Graphical renderer using matplotlib for GUI applications
- `AsciimaticsRenderer`: Interactive terminal-based renderer using asciimatics for keyboard navigation through the maze

### Themes

- `WizardryTheme`: Fantasy-themed styling with dark background and gold/blue elements
- `RetroTheme`: 1980s computer terminal theme with green phosphor display style
- `ThemeManager`: Central registry for theme management

## Usage Examples

### Text Renderer (Terminal)

```python
from visualization.text_renderer import TextRenderer

# Create a text renderer with a specific theme
renderer = TextRenderer(theme_name="retro", use_color=True)

# Render a maze
output = renderer.render_maze(
    grid,                  # The maze grid
    solution_path=path,    # Optional solution path
    show_distances=True    # Whether to show distances
)

# Print to terminal
print(output)
```

### Matplotlib Renderer (GUI)

```python
from visualization.matplotlib_renderer import MatplotlibRenderer

# Create a matplotlib renderer with a specific theme
renderer = MatplotlibRenderer(theme_name="wizardry", figsize=(10, 10))

# Render a maze
fig = renderer.render_maze(
    grid,                 # The maze grid
    solution_path=path,   # Optional solution path
    show_distances=True   # Whether to show distances
)

# Display in a GUI (e.g., Streamlit)
st.pyplot(fig)

# Or save to file
renderer.save_maze(grid, "maze.png", solution_path=path, dpi=300)
```

### Asciimatics Renderer (Interactive Terminal)

```python
from visualization import AsciimaticsRenderer

# Create an asciimatics renderer with a specific theme
renderer = AsciimaticsRenderer(theme_name="retro")

# Launch the interactive maze explorer
# This will take over the terminal with a full-screen UI
renderer.render_maze(
    grid,                          # The maze grid
    solution_path=path,            # Optional solution path
    interactive=True,              # Run in interactive mode
    show_solution=False,           # Start with solution hidden
    current_position=(start_row, start_col)  # Initial player position
)

# Use arrow keys to navigate, 's' to toggle solution visibility,
# 'h' for help, and 'q' to quit
```

## Creating Custom Themes

To create a custom theme, subclass `MazeTheme` and override the properties:

```python
from visualization.themes import MazeTheme, ThemeManager

class CyberpunkTheme(MazeTheme):
    def __init__(self):
        super().__init__()
        # Set theme-specific properties
        self.bg_color = "#000000"
        self.wall_color = "#FF00FF"  # Neon pink walls
        self.path_color = "#00FFFF"  # Cyan path
        self.title_text = "CYBERMAZE v1.0"
        # ...etc...

# Register the theme
ThemeManager.register_theme("cyberpunk", CyberpunkTheme)
```

## Creating Custom Renderers

To create a custom renderer, subclass `MazeRendererBase` and implement the `render_maze` method:

```python
from visualization.renderer_base import MazeRendererBase
from visualization.themes import ThemeManager

class SVGRenderer(MazeRendererBase):
    def __init__(self, theme_name="default"):
        super().__init__(theme_name)
        self.theme = ThemeManager.get_theme(theme_name)
    
    def render_maze(self, grid, solution_path=None, show_distances=False, distances=None, **kwargs):
        # Implementation details for rendering as SVG
        # ...
        return svg_string
```

## Future Enhancements

Potential future enhancements to the visualization layer:

1. Real-time 3D renderer using a game engine
2. PDF/vector graphics renderer for high-quality prints
3. Interactive web-based renderer using JavaScript libraries
4. Animation support for step-by-step maze generation
5. Accessibility features (e.g., screen reader support)