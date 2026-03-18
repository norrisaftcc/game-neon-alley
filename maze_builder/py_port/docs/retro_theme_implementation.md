# Implementing the Retro Terminal Theme

This document explains how the 1980s-style terminal theme was implemented in the MazeBuilder application.

## Overview

The retro terminal theme emulates the look and feel of vintage computer terminals from the 1980s, particularly the phosphor green monochrome displays commonly found on early PCs. This alternate theme complements the default fantasy-themed "Digital Grimoire" interface, offering users a nostalgic experience reminiscent of early computing.

## Key Implementation Details

### 1. Theme Selection and State Management

The theme is managed through Streamlit's session state, initialized at the start of the application:

```python
# Initialize session state
if 'maze' not in st.session_state:
    # Other state variables...
    st.session_state.theme = "wizardry"  # Default theme: wizardry or retro
```

A radio button in the sidebar allows users to toggle between themes:

```python
# Add theme selector in sidebar
with st.sidebar:
    st.title("Settings")
    theme = st.radio(
        "Interface Theme:",
        options=["wizardry", "retro"],
        format_func=lambda x: "Digital Grimoire" if x == "wizardry" else "1980s Terminal",
        index=0 if st.session_state.theme == "wizardry" else 1,
        key="theme_selector"
    )
    st.session_state.theme = theme
```

### 2. CSS Styling Overrides

The retro theme applies CSS overrides using Streamlit's `st.markdown` with `unsafe_allow_html=True`:

```python
# Retro terminal theme
st.markdown("""
<style>
    /* Override Streamlit's default styling for retro theme */
    .main {
        background-color: #000000 !important;
        color: #00FF00 !important;
        font-family: 'Courier New', monospace !important;
    }
    .stApp {
        background-color: #000000 !important;
    }
    h1, h2, h3 {
        color: #00FF00 !important;
        font-family: 'Courier New', monospace !important;
    }
    /* Additional styles... */
</style>
""", unsafe_allow_html=True)
```

### 3. Theme-Conditional UI Elements

Throughout the app, UI elements render differently based on the current theme:

```python
# Theme-specific section header
if st.session_state.theme == "wizardry":
    st.markdown("## ARCANE KNOWLEDGE")
else:
    st.markdown("## TECHNICAL DOCUMENTATION")
```

### 4. Algorithm Descriptions

Each maze generation algorithm has two different descriptions - a fantasy-themed one for the Grimoire theme and a technical, DOS-like one for the retro theme:

```python
if algorithm == "binary_tree":
    if st.session_state.theme == "wizardry":
        st.markdown("""
        **Binary Tree Algorithm**
        
        A simple algorithm that creates mazes with a bias toward the northeast corner...
        """)
    else:
        st.markdown("""
        **BINTREE.SYS - VERSION 2.3**
        
        MEMORY USAGE: LOW
        PROCESSING TIME: FAST
        DIFFICULTY RATING: EASY
        
        FEATURES:
        * OPTIMIZED FOR 8086 PROCESSORS
        * LOW MEMORY FOOTPRINT
        * PREDICTABLE PATTERN GENERATION...
        """)
```

### 5. Maze Rendering

The `render_maze()` function changes the visualization style based on the current theme:

```python
# Set theme-specific colors
if st.session_state.theme == "wizardry":
    # Wizardry theme colors
    bg_color = '#000000'  # Black background 
    wall_color = '#FFFF00'  # Bright yellow walls
    # ...
else:
    # Retro 1980s terminal theme
    bg_color = '#000000'  # Black background
    wall_color = '#00FF00'  # Bright green walls
    # ...
```

For the retro theme:
- Walls are drawn in bright green (#00FF00)
- Solution paths use dashed lines instead of filled rectangles
- Text is displayed in monospace font
- A terminal-style title is used

### 6. ASCII-Style Statistics

The stats display uses ASCII box drawing characters for the retro theme:

```python
# Retro terminal style stats
st.markdown("""
<div class="stats-container" style="font-family: 'Courier New', monospace; padding: 15px;">
<pre>
╔════════════════ SYSTEM STATISTICS ═════════════════╗
║                                                    ║
║  ENTRANCE DIST: 0       CURRENT POS: ({},{})       ║
║  PATH LENGTH: {}          STEPS TO EXIT: {}         ║
║                                                    ║
║  MEMORY: {}K           CPU USAGE: {}%               ║
║  DISK ACCESS: ENABLED   ERROR STATUS: NONE         ║
║                                                    ║
╚════════════════════════════════════════════════════╝
</pre>
</div>
""", unsafe_allow_html=True)
```

### 7. DOS-Style Algorithm Naming

Algorithm selection options use DOS-era 8.3 filename conventions in retro mode:

```python
if st.session_state.theme == "retro":
    algorithm_options = {
        "binary_tree": "BINTREE.SYS - Basic Maze",
        "sidewinder": "SNAKERUN.SYS - Advanced Maze",
        "aldous_broder": "RANDWALK.SYS - Premium Maze"
    }
```

### 8. Custom Error Messages

Even error messages match the theme, showing DOS-like file path errors:

```python
st.markdown("""
<div style="text-align: center; padding: 50px; background-color: #000000; color: #00FF00; border: 1px solid #00FF00;">
    <h2 style="color: #00FF00;">*** MODULE NOT LOADED ***</h2>
    <pre>
ERROR CODE 404: MODULE NOT FOUND
SYSTEM PATH: C:\\MAZEBUILDER\\MODULES\\{}
ACCESS STATUS: DENIED
    </pre>
</div>
""".format(st.session_state.active_tab.upper().replace(" ", "_")), unsafe_allow_html=True)
```

## Technical Challenges

1. **CSS Specificity**: Overriding Streamlit's default styles required using `!important` to ensure theme styles took precedence.

2. **Session State Timing**: The theme state needed to be initialized before any theme-dependent code executed, which required careful organization of the application flow.

3. **Consistent Theme Application**: Ensuring all UI elements respected the current theme required carefully checking theme state throughout the codebase.

4. **Matplotlib Integration**: Custom styling was applied to the matplotlib-generated maze visualization to match the overall theme.

## Future Enhancements

1. **Sound Effects**: Add vintage computer beeps and terminal sounds for the retro theme.

2. **Terminal Animation**: Implement typing animations for text in the retro theme.

3. **Command-Line Interface**: Add a simulated command prompt for the retro theme.

4. **CRT Effect**: Add a subtle CRT screen effect (scan lines, screen curvature) for the retro theme.

5. **Loading Screens**: Add authentic-looking "loading" screens with progress indicators.

---

This implementation demonstrates how modern web applications can incorporate nostalgic design elements while maintaining educational value and usability. The dual-theme approach also showcases Streamlit's flexibility for creating themed interfaces.