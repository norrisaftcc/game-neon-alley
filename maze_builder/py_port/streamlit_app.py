import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from grid import Grid
from cell import Cell
from algorithms.binary_tree import BinaryTreeMaze
from algorithms.sidewinder import SidewinderMaze
from algorithms.aldous_broder import AldousBroderMaze
from pathfinding.dijkstra import Dijkstra

# Set page configuration
st.set_page_config(
    page_title="MazeBuilder: The Digital Grimoire",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state first
if 'maze' not in st.session_state:
    st.session_state.maze = Grid(10, 10)
    st.session_state.algorithm = "binary_tree"
    st.session_state.seed = 1234
    st.session_state.show_solution = False
    st.session_state.current_position = (9, 0)  # Entrance at bottom left
    st.session_state.path = []
    st.session_state.active_tab = "Constructor's Workshop"
    st.session_state.theme = "wizardry"  # Default theme: wizardry or retro

# Custom CSS to style the app
st.markdown("""
<style>
    /* General styling */
    .main {
        background-color: #191970;
        color: #FFFFF0;
    }
    .stApp {
        background-color: #191970;
    }
    h1, h2, h3 {
        color: #FFD700;
        font-family: serif;
    }
    
    /* Custom container styling */
    .grimoire-container {
        background-color: #E8DCCA;
        border: 2px solid #9370DB;
        border-radius: 10px;
        padding: 20px;
        color: #4A3C31;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #9370DB;
        color: #FFFFF0;
        border: 2px solid #FFD700;
        border-radius: 5px;
        padding: 10px 24px;
        font-family: serif;
    }
    
    /* Selectbox styling */
    .stSelectbox label, .stSlider label {
        color: #9370DB;
        font-weight: bold;
    }
    
    /* Stats container */
    .stats-container {
        display: flex;
        justify-content: space-around;
        background-color: rgba(232, 220, 202, 0.2);
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
    }
    
    .stat-item {
        text-align: center;
    }
    
    /* Navigation tabs */
    .tab-container {
        display: flex;
        overflow-x: auto;
        margin-bottom: 20px;
    }
    
    .tab {
        padding: 8px 16px;
        margin-right: 8px;
        border: 1px solid #FFD700;
        border-radius: 5px 5px 0 0;
        cursor: pointer;
    }
    
    .tab.active {
        background-color: #9370DB;
        color: #FFFFF0;
        border-bottom: none;
    }
</style>
""", unsafe_allow_html=True)

# Apply theme-specific styling to the entire app
if st.session_state.theme == "retro":
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
        .grimoire-container {
            background-color: #000000 !important;
            border: 1px solid #00FF00 !important;
            color: #00FF00 !important;
            font-family: 'Courier New', monospace !important;
        }
        .stButton>button {
            background-color: #000000 !important;
            color: #00FF00 !important;
            border: 1px solid #00FF00 !important;
            font-family: 'Courier New', monospace !important;
        }
        .stButton>button:hover {
            background-color: #004400 !important;
        }
        .stSelectbox, .stTextInput {
            color: #00FF00 !important;
        }
        .tab {
            border: 1px solid #00FF00 !important;
            color: #00FF00 !important;
        }
        .tab.active {
            background-color: #004400 !important;
            color: #00FF00 !important;
        }
        .stats-container {
            background-color: #001100 !important;
            border: 1px solid #00FF00 !important;
        }
        div.stSelectbox > div[data-baseweb="select"] > div {
            background-color: #000000 !important;
            border-color: #00FF00 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Retro terminal title
    st.markdown("""
    <h1 style='text-align: center; font-family: "Courier New", monospace; color: #00FF00;'>
        MAZEBUILDER v1.0 - TERMINAL MODE
    </h1>
    <div style='text-align: center; font-family: "Courier New", monospace; color: #00FF00;'>
        (C) 1986 CYBERNETIC SYSTEMS INC.
    </div>
    """, unsafe_allow_html=True)
else:
    # Original wizardry theme title
    st.markdown("""
    <h1 style='text-align: center; text-shadow: 2px 2px 4px #000000;'>
        MAZEBUILDER: THE DIGITAL GRIMOIRE
    </h1>
    """, unsafe_allow_html=True)

# Session state should already be initialized at the top of the script
# This section only adds theme selector to the sidebar

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

    if theme == "retro":
        st.markdown("""
        <div style="background-color: #000000; color: #00FF00; padding: 10px; border-radius: 5px; font-family: monospace; margin-top: 20px;">
            <h3 style="color: #00FF00; margin:0;">RETRO MODE ACTIVATED</h3>
            <p>Emulating classic 1980s computer terminal.</p>
            <p>━━━━ SYSTEM INFO ━━━━<br>
            MazeBuilder v1.0<br>
            Memory: 64K<br>
            Graphics: CGA<br>
            </p>
        </div>
        """, unsafe_allow_html=True)

# Create tabs
tabs = ["The Atrium", "Constructor's Workshop", "Explorer's Chart", "Archivist's Tome"]
st.markdown('<div class="tab-container">' + ''.join([f'<div class="tab {"active" if tab == st.session_state.active_tab else ""}" id="{tab}">{tab}</div>' for tab in tabs]) + '</div>', unsafe_allow_html=True)

# Constructor's Workshop (Maze Generation)
if st.session_state.active_tab == "Constructor's Workshop":
    # Create a two-column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Maze display area
        st.markdown('<div style="background-color: rgba(232, 220, 202, 0.1); padding: 20px; border-radius: 10px; border: 2px solid #FFD700;">', unsafe_allow_html=True)
        
        # Function to render the maze using the visualization layer
        def render_maze(grid, solution_path=None):
            # Import the MatplotlibRenderer from our visualization layer
            from visualization.matplotlib_renderer import MatplotlibRenderer

            # Create a renderer with the appropriate theme
            renderer = MatplotlibRenderer(theme_name=st.session_state.theme, figsize=(10, 10))

            # Render the maze
            return renderer.render_maze(
                grid,
                solution_path=solution_path,
                show_distances=st.session_state.show_solution
            )
        
        # Calculate solution if needed
        if st.session_state.show_solution:
            entrance = st.session_state.maze.at(st.session_state.maze.rows - 1, 0)
            exit = st.session_state.maze.at(0, st.session_state.maze.cols - 1)
            st.session_state.path = Dijkstra.shortest_path(st.session_state.maze, entrance, exit)
        
        # Display the maze
        fig = render_maze(st.session_state.maze, st.session_state.path)
        st.pyplot(fig)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons
        col1a, col1b, col1c = st.columns(3)
        with col1a:
            if st.button("📜 Show/Hide Solution"):
                st.session_state.show_solution = not st.session_state.show_solution
                st.rerun()
        
        with col1b:
            if st.button("🏺 Save Design"):
                st.success("Maze design saved to the archives!")
        
        with col1c:
            if st.button("👁️ First Person View"):
                st.info("First person view is coming in a future update!")
    
    with col2:
        # Controls in a styled container
        st.markdown('<div class="grimoire-container">', unsafe_allow_html=True)
        st.markdown("## MAZE GRIMOIRE")
        
        # Algorithm selection
        if st.session_state.theme == "retro":
            algorithm_options = {
                "binary_tree": "BINTREE.SYS - Basic Maze",
                "sidewinder": "SNAKERUN.SYS - Advanced Maze",
                "aldous_broder": "RANDWALK.SYS - Premium Maze"
            }
        else:
            algorithm_options = {
                "binary_tree": "Binary Tree Algorithm",
                "sidewinder": "Sidewinder Algorithm",
                "aldous_broder": "Aldous-Broder Algorithm"
            }
        
        algorithm = st.selectbox(
            "Algorithm:",
            options=list(algorithm_options.keys()),
            format_func=lambda x: algorithm_options[x],
            index=list(algorithm_options.keys()).index(st.session_state.algorithm)
        )
        
        # Dimensions selection with theme-specific labels
        if st.session_state.theme == "retro":
            dimension_labels = {
                "small": "COMPACT (10x10) - 64K",
                "medium": "STANDARD (15x15) - 128K",
                "large": "EXTENDED (20x20) - 256K",
                "custom": "CUSTOM SIZE - EXPERIMENTAL"
            }
        else:
            dimension_labels = {
                "small": "Small Scroll (10x10)",
                "medium": "Medium Tome (15x15)",
                "large": "Large Grimoire (20x20)",
                "custom": "Custom Dimensions..."
            }

        dimensions = st.selectbox(
            "Dimensions:" if st.session_state.theme == "wizardry" else "MEMORY ALLOCATION:",
            options=["small", "medium", "large", "custom"],
            format_func=lambda x: dimension_labels[x],
            index=0
        )
        
        # Handle custom dimensions
        if dimensions == "custom":
            cols = st.columns(2)
            rows = cols[0].number_input("Rows:", min_value=5, max_value=50, value=10)
            cols = cols[1].number_input("Columns:", min_value=5, max_value=50, value=10)
        else:
            size_mapping = {"small": 10, "medium": 15, "large": 20}
            rows = cols = size_mapping[dimensions]
        
        # Seed input with theme-specific label
        seed_label = "Mystical Seed:" if st.session_state.theme == "wizardry" else "RANDOM NUMBER SEED:"
        seed = st.text_input(seed_label, value=str(st.session_state.seed))
        try:
            seed = int(seed)
        except ValueError:
            # Use the hash of the string if it's not a number
            seed = hash(seed)

        # Additional options with theme-specific label
        solution_label = "Show Path with Distances" if st.session_state.theme == "wizardry" else "DISPLAY SOLUTION PATH"
        st.checkbox(solution_label, value=st.session_state.show_solution,
                   on_change=lambda: setattr(st.session_state, 'show_solution', not st.session_state.show_solution))

        # Generate button with theme-specific label
        button_label = "CAST THE SPELL" if st.session_state.theme == "wizardry" else "EXECUTE PROGRAM"
        if st.button(button_label, use_container_width=True):
            # Create the grid
            new_grid = Grid(rows, cols)
            
            # Apply the selected algorithm
            if algorithm == "binary_tree":
                BinaryTreeMaze.on(new_grid)
            elif algorithm == "sidewinder":
                SidewinderMaze.on(new_grid)
            else:  # aldous_broder
                new_grid, _ = AldousBroderMaze.on(new_grid, seed=seed)
            
            # Update session state
            st.session_state.maze = new_grid
            st.session_state.algorithm = algorithm
            st.session_state.seed = seed
            st.session_state.current_position = (rows-1, 0)  # Reset to entrance
            st.session_state.path = []
            
            # Recalculate path if showing solution
            if st.session_state.show_solution:
                entrance = new_grid.at(new_grid.rows - 1, 0)
                exit = new_grid.at(0, new_grid.cols - 1)
                st.session_state.path = Dijkstra.shortest_path(new_grid, entrance, exit)
                
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Algorithm explanation
        st.markdown('<div class="grimoire-container" style="margin-top: 20px;">', unsafe_allow_html=True)

        # Theme-specific section header
        if st.session_state.theme == "wizardry":
            st.markdown("## ARCANE KNOWLEDGE")
        else:
            st.markdown("## TECHNICAL DOCUMENTATION")

        if algorithm == "binary_tree":
            if st.session_state.theme == "wizardry":
                st.markdown("""
                **Binary Tree Algorithm**

                A simple algorithm that creates mazes with a bias toward the northeast corner.
                For each cell, it randomly connects either northward or eastward,
                creating a pattern that resembles a binary tree structure.

                *Characteristics: Fast, biased, distinct diagonal textures*
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
                * PREDICTABLE PATTERN GENERATION
                * COMPATIBLE WITH CGA DISPLAY

                ERROR CODE 0: NORTHEAST BIAS DETECTED - NORMAL OPERATION
                """)
        elif algorithm == "sidewinder":
            if st.session_state.theme == "wizardry":
                st.markdown("""
                **Sidewinder Algorithm**

                Creates east-west passages (runs) that connect northward at random intervals.
                This algorithm maintains a perfect northern passage and creates a more
                varied maze compared to Binary Tree.

                *Characteristics: Balanced, distinct horizontal bias, perfect northern edge*
                """)
            else:
                st.markdown("""
                **SNAKERUN.SYS - VERSION 1.7**

                MEMORY USAGE: MEDIUM
                PROCESSING TIME: MODERATE
                DIFFICULTY RATING: MEDIUM

                FEATURES:
                * REQUIRES 80286 PROCESSOR
                * HORIZONTAL BIAS OPTIMIZATION
                * RUN-LENGTH COMPRESSION
                * TOP ROW PERFECT PATH FEATURE

                WARNING: MAY CAUSE SYSTEM SLOWDOWN ON OLDER HARDWARE
                """)
        else:  # aldous_broder
            if st.session_state.theme == "wizardry":
                st.markdown("""
                **Aldous-Broder Algorithm**

                Uses random walks to create unbiased perfect mazes. The algorithm visits
                cells randomly, only creating passages to unvisited cells, until all
                cells have been visited.

                *Characteristics: Unbiased, slower performance, truly random patterns*
                """)
            else:
                st.markdown("""
                **RANDWALK.SYS - VERSION 0.9 BETA**

                MEMORY USAGE: HIGH
                PROCESSING TIME: SLOW
                DIFFICULTY RATING: HARD

                FEATURES:
                * REQUIRES 80386 PROCESSOR (RECOMMENDED)
                * FLOATING POINT COPROCESSOR SUPPORT
                * ADVANCED RANDOM NUMBER GENERATION
                * UNBIASED PATH DISTRIBUTION

                WARNING: EXTENDED MEMORY REQUIRED (286K MINIMUM)
                CAUTION: MAY CAUSE SYSTEM MEMORY OVERFLOW ON PROLONGED USE
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats bar at the bottom
    if st.session_state.path:
        if st.session_state.theme == "wizardry":
            st.markdown("""
            <div class="stats-container">
                <div class="stat-item">
                    <div>Distance from Entrance</div>
                    <div>0</div>
                </div>
                <div class="stat-item">
                    <div>Path Length</div>
                    <div>{}</div>
                </div>
                <div class="stat-item">
                    <div>Current Position</div>
                    <div>({},{})</div>
                </div>
                <div class="stat-item">
                    <div>Steps to Exit</div>
                    <div>{}</div>
                </div>
            </div>
            """.format(
                len(st.session_state.path),
                st.session_state.current_position[0],
                st.session_state.current_position[1],
                len(st.session_state.path) - 1
            ), unsafe_allow_html=True)
        else:
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
            """.format(
                st.session_state.current_position[0],
                st.session_state.current_position[1],
                len(st.session_state.path),
                len(st.session_state.path) - 1,
                64 if rows <= 10 else 128 if rows <= 15 else 256,
                min(95, 40 + len(st.session_state.path))  # Fake CPU usage
            ), unsafe_allow_html=True)

else:
    # Placeholder for other tabs with theme-specific styling
    if st.session_state.theme == "wizardry":
        st.markdown("""
        <div style="text-align: center; padding: 50px; background-color: rgba(232, 220, 202, 0.1); border-radius: 10px;">
            <h2 style="color: #9370DB;">🧙‍♂️ Coming Soon 🧙‍♂️</h2>
            <p>The ancient texts for this section are still being deciphered.</p>
            <p>Return to the Constructor's Workshop to create mazes in the meantime.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Go to Constructor's Workshop"):
            st.session_state.active_tab = "Constructor's Workshop"
            st.rerun()
    else:
        st.markdown("""
        <div style="text-align: center; padding: 50px; background-color: #000000; color: #00FF00; border: 1px solid #00FF00; border-radius: 5px; font-family: 'Courier New', monospace;">
            <h2 style="color: #00FF00;">*** MODULE NOT LOADED ***</h2>
            <pre>
ERROR CODE 404: MODULE NOT FOUND
SYSTEM PATH: C:\\MAZEBUILDER\\MODULES\\{}
ACCESS STATUS: DENIED
            </pre>
            <p>This module requires additional system resources.</p>
            <p>Return to main program functionality.</p>
        </div>
        """.format(st.session_state.active_tab.upper().replace(" ", "_")), unsafe_allow_html=True)

        if st.button("RETURN TO MAIN PROGRAM"):
            st.session_state.active_tab = "Constructor's Workshop"
            st.rerun()

# Footer with theme-specific styling
if st.session_state.theme == "wizardry":
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; font-size: 0.8em; color: rgba(255, 255, 255, 0.6);">
        Created with the MazeBuilder Python Library • The Digital Grimoire Interface • May 2025
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; margin-top: 30px; font-size: 0.8em; font-family: 'Courier New', monospace; color: #00FF00;">
        MAZEBUILDER v1.0 (C) 1986 CYBERNETIC SYSTEMS INC.
        <br>
        AVAILABLE MEMORY: 640K • DISK SPACE: 10MB • DATE: 01-01-1986
        <br>
        PRESS ANY KEY TO CONTINUE...
    </div>
    """, unsafe_allow_html=True)