# NEON ALLEY: Design Document (MVP)

**CSC 134 Sample Project — Arrays & File I/O**
**Version**: 0.1 (MVP Scope)
**Status**: Draft

---

## 1. Purpose

Neon Alley is an instructor-built sample project that demonstrates how arrays and file I/O work together in a real program. Students study this code *after* completing the file I/O module and *before* building their own projects. The game is intentionally scoped to feel like a classic BASIC text adventure — short, replayable, and complete — but organized with functions and data files instead of a wall of spaghetti.

### What Students Should Learn From This Code

| Concept | Where It Shows Up |
|---|---|
| Reading structured data from a file into arrays | Loading the alley map, enemy roster, loot table |
| Writing data to a file | Saving/loading a run in progress |
| Parallel arrays | Enemy names, HP, and damage stored in separate aligned arrays |
| Array traversal + search | Looking up an enemy by index, searching inventory |
| Loops driving a game loop | The core alley-crawl loop |
| Functions organizing a large program | Each system (combat, inventory, I/O) is its own function group |
| `cin.ignore()` and mixed input | Menu choices vs. string input for player name |

---

## 2. Game Concept

> *Your surveillance drone threads through the neon-soaked back alleys of the Sprawl. Corporate security bots and street samurai guard every block. Scavenge what you can, fight what you must, and reach the data drop at the end of the alley before your battery dies.*

**Genre**: Linear dungeon crawl (text-based)
**Structure**: The drone moves through a sequence of alley segments. Each segment is an encounter: fight, loot, event, or the final objective.
**Tone**: Light cyberpunk — neon, chrome, rain. PG-rated. Think *Shadowrun* meets *Oregon Trail*.

---

## 3. Core Loop

```
┌─────────────────────────────────────────┐
│            MAIN MENU                    │
│  1. New Run                             │
│  2. Continue Run (load from file)       │
│  3. How to Play                         │
│  4. Quit                                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         ALLEY CRAWL LOOP                │
│  while (not at final segment            │
│         AND drone HP > 0                │
│         AND battery > 0)                │
│  {                                      │
│      Display current segment            │
│      Load encounter for this segment    │
│      Resolve encounter:                 │
│        - ENEMY  → combat loop           │
│        - LOOT   → add to inventory      │
│        - EVENT  → apply effect           │
│        - FINISH → victory check         │
│      Drain battery by 1                 │
│      Advance to next segment            │
│      Offer: Save & quit? (write file)   │
│  }                                      │
└──────────────┬──────────────────────────┘
               │
               ▼
        WIN / LOSE / SAVED
```

**Battery** is the turn timer. The drone has a fixed number of moves (loaded from config). This prevents infinite grinding and gives the game tension without complex resource management.

---

## 4. Data Files

All game data lives in plain-text files. No data is hardcoded in the C++ source except constants like array sizes. This is the pedagogical core: *the game is nothing without its files.*

### 4.1 `enemies.txt` — Enemy Roster

One enemy per line, pipe-delimited. Loaded into parallel arrays at startup.

```
Sentry Bot|30|8|15
Street Samurai|45|12|25
Junkyard Drone|20|5|10
Corp Enforcer|50|15|30
Razorwire Turret|35|10|20
```

**Format**: `name|hp|damage|xp_reward`

**Arrays**:
```cpp
const int MAX_ENEMIES = 10;

string enemyName[MAX_ENEMIES];
int    enemyHP[MAX_ENEMIES];
int    enemyDamage[MAX_ENEMIES];
int    enemyXP[MAX_ENEMIES];

int    enemyCount = 0;  // actual number loaded
```

**Why parallel arrays?** Students haven't learned structs or classes yet. Parallel arrays are the right tool at this point in the course. The code comments should note: *"Later, you'll learn to bundle these into a single `struct Enemy` — for now, the index is the glue."*

### 4.2 `loot.txt` — Loot Table

```
Repair Kit|heal|20
EMP Grenade|damage|25
Shield Booster|shield|15
Battery Cell|battery|3
Smoke Bomb|escape|0
```

**Format**: `name|type|value`

**Arrays**:
```cpp
const int MAX_LOOT = 10;

string lootName[MAX_LOOT];
string lootType[MAX_LOOT];
int    lootValue[MAX_LOOT];

int    lootCount = 0;
```

### 4.3 `alley.txt` — Map / Encounter Sequence

Each line is one alley segment. The first token is the encounter type; the rest is flavor.

```
enemy|0|The alley narrows. Red sensor lights blink ahead.
loot|2|A smashed vending machine sparks in the rain.
enemy|1|A figure drops from a fire escape, blade drawn.
event|battery|2|You find a dead courier drone. Its cells still hold charge.
loot|0|Behind a dumpster: a dented medkit.
enemy|3|Corporate enforcer blocks the intersection.
enemy|4|Razorwire turret activates as you round the corner.
finish|0|The data drop terminal glows at the dead end.
```

**Format**:
- `enemy|index|description` — fight enemy at that index in the roster
- `loot|index|description` — find loot at that index in the loot table
- `event|stat|value|description` — modify a player stat directly
- `finish|0|description` — final objective

**Arrays**:
```cpp
const int MAX_SEGMENTS = 20;

string segType[MAX_SEGMENTS];       // "enemy", "loot", "event", "finish"
int    segIndex[MAX_SEGMENTS];       // index into enemy/loot array, or value
string segExtra[MAX_SEGMENTS];       // extra field (stat name for events)
string segDescription[MAX_SEGMENTS]; // flavor text

int    segmentCount = 0;
```

### 4.4 `savegame.txt` — Player State (Written by Program)

```
NEON_ALLEY_SAVE_V1
Phantom
75
100
12
3
5
Repair Kit
EMP Grenade
Battery Cell
```

**Format** (line-by-line):
```
header tag
player name
current HP
max HP
current battery
current segment index
inventory count
item 1
item 2
...
```

**Why line-by-line?** Matches how students learned `getline()` and `>>` in the file I/O module. The header tag lets the load function validate the file before trusting it.

---

## 5. Player State

```cpp
// --- Player State (global for MVP; refactor target later) ---
string playerName;
int    playerHP;
int    playerMaxHP    = 100;
int    battery;
int    currentSegment = 0;

const int MAX_INVENTORY = 10;
string inventory[MAX_INVENTORY];
int    inventoryCount = 0;
```

**Note on globals**: The MVP uses global state deliberately — students have functions but not yet parameters-with-return-values for complex state. The code should include a comment block:

```
// ============================================================
// DESIGN NOTE: These are global variables. That means any
// function can read or change them. This works for a small
// program, but gets dangerous fast. When we learn about
// passing parameters and returning values, we'll refactor
// this so each function only touches what it needs.
// ============================================================
```

---

## 6. Combat System

Combat is a simple alternating-turns loop. No initiative, no speed stats — just trade hits until one side drops.

```
┌─────────────────────────────────┐
│  ENCOUNTER: [enemy name]        │
│  Enemy HP: ██████░░░░ 30/30     │
│  Your  HP: ████████░░ 75/100    │
│                                 │
│  1. Attack                      │
│  2. Use Item                    │
│  3. Try to Flee                 │
└─────────────┬───────────────────┘
              │
              ▼
     ┌── ATTACK ──────────────────┐
     │ Player deals 10-20 damage  │
     │ (random range)             │
     │ Enemy deals enemyDamage[i] │
     │ ± small random variance    │
     └───────────────────────────┘
```

### Combat Details

- **Player damage**: `10 + rand() % 11` (range 10–20). Fixed for MVP. No weapon stats.
- **Enemy damage**: `enemyDamage[i] + (rand() % 5 - 2)` (base ± 2).
- **Use Item**: Show inventory, pick by number. Repair Kit heals, EMP Grenade deals bonus damage, etc. Item is removed after use (shift array left).
- **Flee**: 40% success. On failure, enemy gets a free hit. Smoke Bomb guarantees escape.
- **Death**: HP ≤ 0 → game over, return to main menu.

---

## 7. Inventory System

A simple string array with a count tracker.

**Add item**:
```
if inventoryCount < MAX_INVENTORY:
    inventory[inventoryCount] = itemName
    inventoryCount++
else:
    "Inventory full! Leave the [item] behind."
```

**Use/remove item**:
```
display numbered list 1..inventoryCount
get choice
apply item effect based on lootType lookup
shift items left to fill the gap
inventoryCount--
```

**Loot type resolution**: When the player uses an item, search `lootName[]` to find the matching index, then read `lootType[]` and `lootValue[]` to determine the effect. This is another array-search teaching moment.

---

## 8. File I/O Operations

### 8.1 Loading Game Data (Startup)

```
loadEnemies("enemies.txt")    → fills enemyName[], enemyHP[], etc.
loadLoot("loot.txt")          → fills lootName[], lootType[], lootValue[]
loadAlley("alley.txt")        → fills segType[], segIndex[], etc.
```

Each loader:
1. Opens an `ifstream`
2. Reads lines with `getline()`
3. Parses pipe-delimited fields (using `find()` and `substr()`, or a helper function)
4. Stores values in the appropriate arrays
5. Increments the count
6. Closes the file
7. Reports how many entries loaded (or an error if file not found)

**Parsing helper** (good candidate for a reusable function):
```cpp
// Splits a pipe-delimited line into tokens
// Students see: one function, used by three loaders
void splitLine(string line, string tokens[], int maxTokens, int &count);
```

### 8.2 Saving a Run

```
saveGame("savegame.txt")
```

1. Open `ofstream`
2. Write header tag
3. Write player stats, one per line (`<<`)
4. Write inventory count, then each item with `endl`
5. Close file
6. Display confirmation

### 8.3 Loading a Saved Run

```
loadGame("savegame.txt") → returns true/false
```

1. Open `ifstream`
2. Read first line; check header tag — if wrong, report error and return false
3. Read player stats with `getline()` and `stoi()` for ints
4. Read inventory items in a loop up to the stored count
5. Close file
6. Display "Run restored" message

---

## 9. Function Map

```
main()
 ├── loadEnemies()
 ├── loadLoot()
 ├── loadAlley()
 ├── showMainMenu()          → returns choice
 ├── newRun()                → sets starting state
 ├── loadGame()              → reads savegame.txt
 ├── showHowToPlay()
 ├── runAlley()              → the core game loop
 │    ├── displaySegment()   → shows flavor text + encounter type
 │    ├── combat()           → fight loop, returns win/lose
 │    │    ├── useItem()     → inventory submenu during combat
 │    │    └── flee()        → escape attempt
 │    ├── findLoot()         → adds item to inventory
 │    ├── applyEvent()       → modifies a stat
 │    └── saveGame()         → writes savegame.txt
 └── showGameOver()          → win or lose message
```

**Target: ~15 functions.** Large enough to show real decomposition, small enough to read in one sitting.

---

## 10. Technical Constraints

| Constraint | Rationale |
|---|---|
| C++ only, no external libraries | Must compile in student environments (Codespaces, MinGW) |
| Arrays only, no vectors | Students haven't reached Week 13 yet |
| No structs or classes | Students haven't reached Week 11 yet |
| Global state for player data | Parameters with return values haven't been fully taught yet |
| `rand()` / `srand()` for randomness | Standard library, no `<random>` header needed |
| `<fstream>`, `<string>`, `<iostream>`, `<cstdlib>`, `<ctime>` only | Minimal include footprint |
| Max array sizes as named constants | Reinforces `const` usage from Week 2 |
| Pipe-delimited text files | More readable than CSV for game data; teaches parsing |
| Runs in a standard terminal | No ANSI escapes required (but could be added as a bonus) |

---

## 11. Staged Build Plan

The sample code should be presentable in stages for instructor demos.

| Stage | What's Added | Concepts Highlighted |
|---|---|---|
| **Stage 1**: Skeleton | `main()`, main menu, quit. Empty function stubs. | Program structure, function prototypes |
| **Stage 2**: Data loading | `loadEnemies()` reads `enemies.txt`, prints roster. | `ifstream`, `getline`, parsing into arrays |
| **Stage 3**: Alley traversal | Load `alley.txt`, walk through segments displaying text. No combat. | Array of encounter data, game loop |
| **Stage 4**: Combat | Add the fight loop. Enemies use loaded stats. | Parallel array lookup by index, `rand()` |
| **Stage 5**: Loot & inventory | Load `loot.txt`, pick up items, use them in combat. | Array search, insert/remove operations |
| **Stage 6**: Save/load | Write and read `savegame.txt`. | `ofstream`, file format design, validation |
| **Stage 7**: Polish | HP bars, battery warnings, win/lose screens. | `string` manipulation, output formatting |

Each stage compiles and runs. Students can fork at any stage and extend.

---

## 12. Sample Output

```
╔══════════════════════════════════════╗
║          N E O N   A L L E Y        ║
║       Drone Runner v1.0 (MVP)       ║
╠══════════════════════════════════════╣
║  1. New Run                         ║
║  2. Continue Run                    ║
║  3. How to Play                     ║
║  4. Quit                            ║
╚══════════════════════════════════════╝
> 1

Enter drone callsign: Phantom

=== SEGMENT 1 of 8 ===
Battery: [||||||||||] 12    HP: [████████░░] 75/100
The alley narrows. Red sensor lights blink ahead.

  !! HOSTILE CONTACT: Sentry Bot (HP: 30) !!

  1. Attack
  2. Use Item (2 items)
  3. Try to Flee
> 1

  You fire: 16 damage! Sentry Bot HP: 14
  Sentry Bot strikes: 9 damage! Your HP: 66

  1. Attack
  2. Use Item (2 items)
  3. Try to Flee
> 1

  You fire: 13 damage! Sentry Bot HP: 1
  Sentry Bot strikes: 7 damage! Your HP: 59

  1. Attack
  2. Use Item (2 items)
  3. Try to Flee
> 1

  You fire: 18 damage! Sentry Bot DESTROYED.
  +15 XP

  Continue deeper? (s = save & quit, enter = continue)
>
```

---

## 13. Extension Ideas (Post-MVP)

These are *not* in scope for the MVP but document where the project could go, especially as a student fork or a later OOP refactoring exercise:

- **Difficulty levels**: Scale enemy HP/damage by a multiplier loaded from a config file
- **Multiple alleys**: Different `alley_*.txt` files for replayability
- **ANSI terminal graphics**: Color-coded HP bars, neon box-drawing characters
- **High score file**: Append best run stats to `highscores.txt` (demonstrates append mode)
- **Struct refactoring** (Week 11+): Bundle parallel arrays into `struct Enemy`, `struct LootItem`
- **Class refactoring** (Week 12+): `Player` class with methods, `GameEngine` class
- **Vector migration** (Week 13+): Replace fixed arrays with `vector<>`

---

## 14. File Manifest (Deliverables)

```
neon-alley/
├── README.md              ← How to compile and run
├── main.cpp               ← All game code (single file for MVP)
├── data/
│   ├── enemies.txt        ← Enemy roster
│   ├── loot.txt           ← Loot table
│   └── alley.txt          ← Map / encounter sequence
└── savegame.txt           ← Created at runtime (gitignored)
```

Single-file `main.cpp` is deliberate: students can read top-to-bottom without navigating headers. Multi-file refactoring is a future exercise.

---

## 15. Open Questions

1. **Should the alley be randomized or fixed?** Fixed is simpler to debug and demo. Random selection from a pool would demonstrate `rand() % count` with arrays but adds complexity. **Leaning fixed for MVP.**

2. **XP system — does it do anything?** In the MVP, XP is tracked and displayed but doesn't affect gameplay. It's there so students see "accumulate a value across encounters" as a pattern. Could gate a bonus message at the end.

3. **String parsing approach**: `find('|')` + `substr()` vs. `stringstream` with custom delimiter? `find/substr` is more transparent at this level. `stringstream` could be shown as an alternative in comments.

4. **ANSI color**: Include it in MVP or leave it as an extension? Box-drawing characters (╔═╗ etc.) work everywhere. ANSI color codes don't. **Leaning: box-drawing yes, ANSI color as documented extension only.**
