# MazeBuilder: The Digital Grimoire UI Concept

This directory contains design documents and implementation files for the UI concept for the MazeBuilder application, featuring both a fantasy "Digital Grimoire" theme and a retro "1980s Terminal" theme.

## Concept Overview

The UI concept draws inspiration from classic dungeon crawler RPGs, particularly Wizardry I and Wizardry VI, as well as vintage computing interfaces from the 1980s, blending:

- The wireframe minimalism of Wizardry I (1981)
- The more colorful and structured UI of Wizardry VI (1990)
- The phosphor green-on-black aesthetic of early computer terminals
- Modern web-based interactivity through Streamlit

## Interface Themes

### 1. Digital Grimoire Theme (Default)

This interface is themed as an ancient book of magic spells that has been digitized:
- Deep midnight blue backgrounds reminiscent of the night sky
- Parchment-colored panels for controls and information
- Arcane purple and magical amber accents
- Ornate typography for headers
- Bright yellow maze walls against a black background
- Educational algorithm names presented with fantasy-themed descriptions

### 2. 1980s Terminal Theme (Retro Mode)

This alternative interface emulates vintage computer terminals:
- Black backgrounds with bright green phosphor text
- Monospace fonts throughout the interface
- ASCII-style borders and decorations
- DOS-style file naming conventions (8.3 format)
- Dashed-line walls when displaying the solution path
- Technical-sounding descriptions with references to memory requirements and processors

## Files in this Directory

- **streamlit_ui_design.md**: Comprehensive design document detailing the overall vision, UI components, layout, and interaction patterns.
- **streamlit_ui_mockup.html**: Visual mockup of the intended UI that can be viewed in a web browser.
- **ui_concept_readme.md**: This file, providing an overview of the concept.

## UI Highlights

### Common Features Across Themes

- Bottom-left entrance and top-right exit in all mazes
- Three maze generation algorithms with educational descriptions
- Path visualization with distance numbers from entrance to exit
- Multiple maze sizes with appropriate naming conventions
- Consistent layout with sections for controls and visualization
- Debug statistics showing solution details

### Theme-Specific Features

#### Digital Grimoire Theme:
- Colorful interface with magic-inspired terminology
- Algorithms with fantasy-styled descriptions
- Magical-looking entrance and exit markers
- Solution path in vibrant blue with white numbers

#### 1980s Terminal Theme:
- Monochrome green interface with technical terminology
- Algorithms labeled as system programs (.SYS files)
- ASCII-style display elements
- "Old computer" terminology (K memory, MHz processors)
- Retro-style system information display

## Implementation

A working implementation is provided in `/py_port/streamlit_app.py`, which includes:

1. Both UI themes with a selector in the sidebar
2. Algorithm selection with appropriate naming for each theme
3. Maze generation and visualization with theme-specific styling
4. Pathfinding with distance display
5. Stats display styled according to the selected theme

## Running the Streamlit App

To run the implementation:

```bash
cd py_port
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Theme Switching

The theme can be changed using the radio button in the sidebar:
- "Digital Grimoire" - The fantasy-themed interface
- "1980s Terminal" - The retro computer terminal interface

## Next Steps

Future development of the UI concept could include:

1. Implementing the remaining sections (Atrium, Explorer's Chart, Archivist's Tome)
2. Adding a first-person view of the maze with theme-appropriate styling
3. Implementing sound effects and optional background music
4. Creating a 3D view option for more immersive exploration
5. Adding theme-specific interactions (spellcasting or command-line inputs)

## Design Inspiration

The design draws from:
- The minimalist wireframe aesthetics of early Wizardry I (1981)
- The more structured, colorful interface of Wizardry VI (1990)
- Early IBM PC and Commodore 64 terminal displays with green monochrome monitors
- Early MS-DOS command-line interfaces and applications

---

*MazeBuilder: The Digital Grimoire & Terminal Edition - May 2025*