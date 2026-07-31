# PR Draft — `claude/build-mvp-aVV4X` → `main`

Staged here because this session's GitHub access is blocked at the org level
("GitHub access is not enabled for this session — an org admin must connect
the Claude GitHub App"). Paste directly into `gh pr create --title "..."
--body "..."`, or copy into the GitHub web UI at:

https://github.com/norrisaftcc/game-neon-alley/pull/new/claude/build-mvp-aVV4X

Once opened, run the `pr-review-team` skill (`.claude/skills/pr-review-team/`)
to get the product-owner / scrum-leader / junior-dev x2 pass before handing
off to a human reviewer.

---

## Title

```
Neon Alley MVP: playable drone-crawl game + simulated PR review team
```

## Body

```markdown
## Summary

Implements the MVP described in `NeonAlley_DesignDoc_MVP.md` — a
single-file, text-based cyberpunk dungeon crawl built for CSC 134
(Arrays & File I/O), plus repo infrastructure for an internal review
pass before external/human PR review.

**Game (`main.cpp`, ~15 functions, all 7 staged-build-plan stages):**
- Pipe-delimited data loading (`enemies.txt`, `loot.txt`, `alley.txt`) into
  parallel arrays via a shared `splitLine()` helper
- Core alley-crawl loop: battery-timer-gated traversal through 8 segments
- Turn-based combat (attack / use item / flee) with random damage ranges
  matching the design doc's numbers
- Inventory: add/use/remove with array-shift-left on removal, loot-type
  lookup by name
- Save/load to `savegame.txt` with header-tag validation
- Main menu, how-to-play, HP/battery display, win/lose/battery-dead end
  states

**Data files (`data/`):** 5 enemies, 5 loot items, 8 alley segments — matches
the design doc's sample data exactly.

**Review infrastructure (`.claude/`):**
- `agents/product-owner.md` — spec/scope match against the design doc
- `agents/scrum-leader.md` — build/run/testability/process-readiness gate;
  explicitly never self-approves or merges
- `agents/junior-dev.md` — line-level review, meant to be spawned twice
  with different focus areas (combat/inventory vs. file I/O/save-load)
- `skills/pr-review-team/SKILL.md` — orchestrates the above into
  draft-PR → parallel review → synthesize → hold-for-external-review

## Constraints honored (per design doc §10)

C++ only, no external libraries, arrays only (no vectors/structs/classes),
global player state, `rand()`/`srand()`, minimal `<fstream>` / `<string>` /
`<iostream>` / `<cstdlib>` / `<ctime>` includes.

## Test plan

- [x] `g++ -o neon_alley main.cpp -std=c++11` compiles clean, no warnings
- [x] Manual playthrough: main menu → new run → combat (attack/item/flee) →
      loot pickup → event → save & quit → continue run → reach finish segment
- [x] Battery depletion and HP-zero end states both verified
- [ ] Human review (this PR is the handoff point)

## Not in this PR

Everything under "Extension Ideas" in the design doc (§13) — difficulty
levels, multiple alleys, ANSI color, struct/class refactor, vector
migration — is intentionally deferred.
```
