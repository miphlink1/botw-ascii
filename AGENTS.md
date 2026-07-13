# Session Context — botw-ascii

## What this project is
2.5D top-down ASCII renderer of BotW's Great Plateau, in Python. Map data extracted from Grazzy's "I Built All Of Breath Of The Wild In Minecraft" world via the Amulet library. I'm 13, learning Git/Python as I go, on Mac. Please do the coding, and if there's any particular architecture or something specific I should know about/might want to know about (like, underhang detection using BFS) please tell me, I'm not so much learning Python as learning how to structure projects.

## Pipeline status
[X] **Phase 1 — datamining**: raw extraction from Minecraft world (raw_scan, symbol map, air detection, underhangs, openings). Complete. Should no longer need the Minecraft world reloaded for normal work.
[:] **Phase 2 — data polishing**: normalization, translation key, symbol remap, opening→entrance grouping. Mostly done — only trees still in progress.
[ ] **Phase 3 — rendering**: rendering the world. includes map data, underhangs, custom overlays, and entities. yay i finally get to touch an if statement
[ ] **Phase 4 — the player**: Player class, HP, stamina, climbing. inventory and attack animation and hitbox. abilities, bow+shield.
[ ] **Phase 5 — other entities**: Enemy behavior, NPCs, wild animals, fish.
[ ] **Phase 6 — shrines and interiors**: redoing Phase 1 for scraping base data from shrines and then hand-authoring details, fixing interior of Shrine of Resurrection, Old Man's Cabin and Temple of Time.
[ ] **Phase 7 — gameplay and content**: preloading cutscenes and adding dialogue, progression and unlocks. UI/HUD, settings, main menu, world+save states.


## Known open problems (in priority order I'm thinking about them)
1. **custommap** — manual overlay fixes on top of `readmap` (e.g. stone path vs. stone wall being visually identical). Have a custom HTML/JS editor tool for this (`tools/map_editor.html`) — canvas-based, find/replace within a drag-selection, green diff highlighting, yellow "show all matches" highlighting, altitude overlay toggle, undo/redo, exports a sparse `custommap.json` overlay (`{"x,z": "char"}`, not a full duplicate grid).
2. **Trees** — currently baked into `surface.json`/`underhangs.json` as if they were solid terrain/roofs. Trees have irregular trunks (curvy, embedded logs) and varied leaf types (Grazzy's flair), so simple "column scan" assumptions don't work. Current plan (no world reload needed):
   - Flag tree-topped columns in `surface.json` via block IDs in `key.json`
   - Real ground under each tree is already sitting in `underhangs.json` as that column's artmap floor (confirmed: underhangs = air-under-roof, correctly captured tree canopies as "roofs" too) — patch it back into `surface.json`, then strip those fake entries out of `underhangs.json`
   - Cluster tree blocks into individual trees via connectivity (trunks) + nearest-trunk-by-distance (leaves), size-filter to fold stray embedded logs into the nearest real trunk
   - Nearest-to-centroid block = trunk/chop-point, rest = leaves → output `trees.json`
   - This becomes a new script, tentatively `patch_tree_columns.py`, fully self-contained (reads existing JSON only, no Amulet)
   - **Not yet started** — flagged as risky/destructive (overwrites real pipeline output), so plan is to do it on a git branch (`tree-patch`) plus a manual `.bak` copy of the 3 files it touches, before running.
3. Naming convention for maps must be fixed - streamline to:
   - heightmap (formerly altmap)
   - blockmap (raw surface map)
   - symbolmap (translated surface map)
   - overlaymap (sparse overlay on translated surface map for small custom edits)

## Git status
- Repo live on GitHub (`miphlink1/botw-ascii`), pushing works via PAT stored in remote URL.
- Comfortable with: init/add/commit/push, branches for risky changes, undo via history.
- Not yet comfortable with: merge conflicts (haven't hit one yet).
- Homebrew not installed yet (no admin rights, dad needs to run installer — hasn't happened yet). Blocks `gh` CLI and `tree` command specifically.

## Environment
- Mac, VSCode with integrated terminal (has a known broken credential-helper socket issue — auth works fine from real Terminal.app or via token-in-URL workaround).
- No Homebrew yet.

## Directory structure (after streamline above completed):
```
scripts/       # pipeline steps, run in sequence
data/          
  raw/         # first-pass extraction output
  runtime/     # polished/normalized output
    keys/
      translation_key.json
    surface/
      heightmap.json
      blockmap.json
      symbolmap.json
      overlaymap.json (will be added after 1.)
    underhangs/
      underhangs_translated.json
      underhangs.json
test/          # test & debug scripts
tools/         # standalone utilities (map_editor.html lives here)
README.md
TODO.txt
.gitignore
AGENTS.md      # this file
```

## Immediate next step
streamline naming convention first and push to Git, then start working on trees

---
*Last updated: [fill in date]*