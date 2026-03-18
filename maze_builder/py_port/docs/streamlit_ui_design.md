# MazeBuilder Streamlit UI Design Document

## Overview

This document outlines the design vision for a Streamlit-based user interface for the MazeBuilder application, drawing inspiration from classic dungeon crawler RPGs, particularly Wizardry I and Wizardry VI. The UI aims to blend nostalgic elements with modern functionality to create an engaging, intuitive experience for maze generation and exploration.

## Design Vision

### Aesthetic Direction: "Digital Grimoire"

The UI will adopt a "Digital Grimoire" aesthetic that combines:

- The wireframe minimalism of early Wizardry I (1981)
- The richer color palette and structured UI of Wizardry VI (1990)
- Modern accessibility and responsiveness through Streamlit

The interface will feel like interacting with an ancient spellbook that has been digitized, with parchment textures, ornate borders, and a design that frames the maze as a magical artifact being studied and manipulated.

## Color Palette

Primary palette inspired by Wizardry's evolution from 4-color to 16-color graphics:

- **Background:** Deep midnight blue (#191970) - representing the depths of the dungeon
- **Primary UI Elements:** Aged parchment (#E8DCCA) - for text areas and control panels
- **Accent 1:** Arcane purple (#9370DB) - for headers and important UI elements
- **Accent 2:** Magic amber (#FFD700) - for highlights and call-to-action elements
- **Text:** Ivory (#FFFFF0) on dark backgrounds, Dark brown (#4A3C31) on light backgrounds

## Typography

- **Headers:** "Luminari" or "Dragon Hunter" - ornate, fantasy-styled font
- **Body Text:** "IBM Plex Mono" - clear, readable, with a hint of retro computer terminals
- **Maze Numbers:** "Press Start 2P" - distinct pixel font for distance numbers within the maze

## Layout Structure

The interface will be organized into distinct "pages" of the digital grimoire:

### 1. The Atrium (Home Page)

```
+-------------------------------------------------+
|          MAZEBUILDER: THE DIGITAL GRIMOIRE      |
+-------------------------------------------------+
|                                                 |
|  +-------------------------------------------+  |
|  |                                           |  |
|  |           [Animated Maze Preview]         |  |
|  |                                           |  |
|  +-------------------------------------------+  |
|                                                 |
|  [Enter the Archives]  [Begin New Construction] |
|                                                 |
|  [About the Ancient Art of Maze Construction]   |
|                                                 |
+-------------------------------------------------+
```

### 2. The Constructor's Workshop (Maze Generation Page)

```
+-------------------------------------------------+
|  THE CONSTRUCTOR'S WORKSHOP     [Return Home]   |
+-------------------------------------------------+
|                                 |               |
|  +-------------------------+    |  +---------+  |
|  |                         |    |  | MAZE    |  |
|  |       MAZE PREVIEW      |    |  | GRIMOIRE|  |
|  |                         |    |  |         |  |
|  |                         |    |  | Algo:   |  |
|  |                         |    |  | [Select]|  |
|  |                         |    |  |         |  |
|  |                         |    |  | Size:   |  |
|  |                         |    |  | [Adjust]|  |
|  |                         |    |  |         |  |
|  |                         |    |  | Seed:   |  |
|  |                         |    |  | [Input] |  |
|  +-------------------------+    |  |         |  |
|                                 |  | [CAST]  |  |
|  [Show Solution] [Save Design]  |  +---------+  |
|                                 |               |
+-------------------------------------------------+
```

### 3. The Explorer's Chart (Maze Exploration Page)

```
+-------------------------------------------------+
|  THE EXPLORER'S CHART          [Return Home]    |
+-------------------------------------------------+
|                                                 |
|  +-------------------------------------------+  |
|  |                                           |  |
|  |                                           |  |
|  |               MAZE VIEW                   |  |
|  |       (with pathfinding solution)         |  |
|  |                                           |  |
|  |                                           |  |
|  +-------------------------------------------+  |
|                                                 |
|  [First Person View]          [Statistics]      |
|                                                 |
|  Distance from Entrance: 0    Path Length: 34   |
|  Current Position: (0,0)      Steps to Exit: 33 |
|                                                 |
|  [Previous Step]   [Auto-Solve]   [Next Step]   |
|                                                 |
+-------------------------------------------------+
```

### 4. The Archivist's Tome (Saved Mazes Page)

```
+-------------------------------------------------+
|  THE ARCHIVIST'S TOME          [Return Home]    |
+-------------------------------------------------+
|                                                 |
|  +-------------------+  +-------------------+   |
|  | [Thumbnail]       |  | [Thumbnail]       |   |
|  | Binary Tree Maze  |  | Sidewinder Maze   |   |
|  | 10x10 - May 2025  |  | 15x15 - May 2025  |   |
|  +-------------------+  +-------------------+   |
|                                                 |
|  +-------------------+  +-------------------+   |
|  | [Thumbnail]       |  | [Thumbnail]       |   |
|  | Aldous-Broder     |  | Custom Design     |   |
|  | 20x20 - May 2025  |  | 12x12 - May 2025  |   |
|  +-------------------+  +-------------------+   |
|                                                 |
|  [Import Design]         [Export Collection]    |
|                                                 |
+-------------------------------------------------+
```

## UI Elements & Styling

### Navigation

- **Spellbook Tabs:** Major sections represented as enchanted bookmarks
- **Scroll Navigation:** Custom scroll bars styled as ancient scroll rollers
- **Breadcrumb Trail:** Glowing runes showing navigation path

### Maze Display

- **2D Top-Down View:** Primary view showing full maze with:
  - Entrance styled as a glowing portal
  - Exit styled as a treasure chest or ancient artifact
  - Path shown with glowing runes/symbols
  - Distance numbers styled as magical numerals

- **Optional First-Person View:** Toggle to see the maze from a Wizardry-style first-person perspective
  - Wireframe walls (Wizardry I style) or solid walls with texture (Wizardry VI style)
  - Limited visibility to enhance exploration feeling
  - Turn-based movement with animated transitions

### Controls

- **Arcane Dials:** Sliders styled as magical measurement tools
- **Spell Selector:** Dropdown menus styled as spell selection parchments
- **Invocation Buttons:** Primary action buttons styled as magical seals
- **Magical Input Fields:** Text inputs with glowing borders and runic decorations

## Interactive Features

### Maze Generation Controls

1. **Algorithm Selection:**
   - Binary Tree (styled as "The Northeasterly Wind")
   - Sidewinder (styled as "The Serpent's Path")
   - Aldous-Broder (styled as "The Wanderer's Weave")

2. **Dimension Controls:**
   - Size slider with visual feedback
   - Presets (small scroll, medium tome, large grimoire)

3. **Randomization:**
   - "Mystical Seed" input for reproducible results
   - "Chaotic Chance" button for true randomness

### Pathfinding Visualization

1. **Solution Controls:**
   - "Reveal the Path" toggle
   - Step-by-step navigation with "Forward Scry" and "Backward Scry" buttons
   - "Auto-Journey" for animated path traversal

2. **Stats Display:**
   - Path length displayed as "Arcane Distance"
   - Path difficulty rated with magical terminology
   - Current position shown on a miniature map

### Maze Interaction

1. **View Modes:**
   - Bird's Eye View (full maze)
   - Explorer's View (first-person)
   - Architect's View (with grid lines and coordinates)

2. **Maze Manipulation:**
   - "Seal Design" to save current maze
   - "Summon Design" to load saved maze
   - "Enchant Walls" to modify existing maze manually

## Animation & Transitions

- **Page Transitions:** Pages turn like a magical book
- **Maze Generation:** Animated construction showing the algorithm's progression
- **Solution Pathfinding:** Glowing trail that progresses through the maze
- **First-Person Movement:** Smooth transitions between cells with slight camera bob

## Responsive Design

The UI will adapt to different screen sizes while maintaining the "Digital Grimoire" aesthetic:

- **Desktop:** Full layout as described above
- **Tablet:** Condensed controls with expandable sections
- **Mobile:** Vertical scrolling layout with maze view prioritized

## Technical Implementation Notes

### Streamlit Components

1. **Custom CSS:**
   ```python
   st.markdown("""
   <style>
   .main {
       background-color: #191970;
       color: #FFFFF0;
       font-family: 'IBM Plex Mono', monospace;
   }
   .stButton>button {
       background-color: #9370DB;
       color: #FFFFF0;
       border: 2px solid #FFD700;
       border-radius: 5px;
       padding: 10px 24px;
       font-family: 'Luminari', fantasy;
   }
   </style>
   """, unsafe_allow_html=True)
   ```

2. **Custom Header:**
   ```python
   st.markdown("""
   <h1 style='text-align: center; 
              font-family: "Luminari", fantasy; 
              color: #FFD700;
              text-shadow: 2px 2px 4px #000000;'>
   MazeBuilder: The Digital Grimoire
   </h1>
   """, unsafe_allow_html=True)
   ```

3. **Maze Rendering:**
   ```python
   # Using matplotlib for maze rendering with custom styling
   import matplotlib.pyplot as plt
   
   fig, ax = plt.subplots(figsize=(10, 10))
   # Maze rendering code...
   ax.set_facecolor('#191970')  # Dark blue background
   # Customize lines, text, etc.
   st.pyplot(fig)
   ```

### Session State Management

```python
# Initialize session state for maze parameters
if 'maze' not in st.session_state:
    st.session_state.maze = grid.Grid(10, 10)  # Default 10x10 grid
    st.session_state.algorithm = "binary_tree"
    st.session_state.show_solution = False
    st.session_state.current_position = (0, 0)  # Start at entrance
```

## Accessibility Considerations

- **Color Blindness:** Ensure path and walls have sufficient contrast
- **Screen Readers:** Add appropriate alt text for all visual elements
- **Keyboard Navigation:** Ensure all features accessible via keyboard
- **Text Scaling:** Support for browser text scaling without breaking layout

## Future Enhancements

- **Sound Effects:** Ambient dungeon sounds, footsteps for movement
- **Background Music:** Toggleable fantasy soundtrack
- **3D View Option:** Using Three.js for a more immersive experience
- **Maze Challenges:** Timed exploration, fog of war, monster encounters
- **Multi-Level Mazes:** Connected levels with stairs and portals

## Conclusion

The MazeBuilder Streamlit UI will transform what could be a simple utility application into an engaging, themed experience that makes maze generation and exploration feel like practicing an arcane art. By combining the nostalgic aesthetics of classic Wizardry games with modern web technologies, we create an interface that is both functional and immersive.

This design preserves the core functionality of the MazeBuilder application while wrapping it in a thematic layer that enhances user engagement and enjoyment. The "Digital Grimoire" concept provides a strong, consistent design language that can be extended as new features are added to the application.