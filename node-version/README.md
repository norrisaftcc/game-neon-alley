# NEON ALLEY Node.js Spike

Run the game:

```bash
cd /home/runner/work/game-neon-alley/game-neon-alley/node-version
node game.js
```

Run the built-in tests:

```bash
node --test utils.test.js
```

## What this spike shows

- **No compile step**: run one file with `node game.js`
- **JSON data files**: game content is readable without pipe parsing
- **Async file I/O**: save and load use `fs/promises` with `await`
- **Small codebase**: the game logic lives in `game.js` and `utils.js`
- **Built-in tools only**: no npm packages, no extra setup

## Included features

- Main menu with new run, load run, help, and quit
- Turn-based combat with attack, item, and flee choices
- Inventory items for healing, damage, shields, battery, and escape
- JSON save/load in `saves/savegame.json`
- Data files for enemies, loot, and alley segments

## C++ vs Node.js

| Topic | C++ MVP | Node.js spike |
| --- | --- | --- |
| Start the game | compile, then run | `node game.js` |
| Load data | parse pipe-delimited text | `JSON.parse()` on `.json` files |
| Save game | file streams + manual formatting | `await saveJson(path, state)` |
| Data shape | parallel arrays | objects inside arrays |
| Quick edits | rebuild after changes | restart Node right away |

## Beginner notes

- `game.js` holds the main loop and combat.
- `utils.js` keeps reusable helpers small and easy to read.
- The save file is plain JSON, so students can open it and inspect state.
