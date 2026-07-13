# The Legend of Zelda: Breath of the Wild in ASCII

An attempt to recreate BotW's Great Plateau as a 2.5D, top-down ASCII renderer in Python — inspired by the presentation of classic Pokémon games.

## Status

🚧 **Work in progress.** MVP scope: the Great Plateau only.

## Why a 2.5D Great Plateau (and not full 3D)?

A perfect, full 3D ASCII representation of the entire game is likely infeasible due to memory and performance constraints (and raycasting is out of scope for now). The MVP is scoped down to a 2.5D top-down view of just the Great Plateau to keep things achievable.

## Data Source

Instead of hand-authoring the map data, this project extracts it from Grazzy's [*I Built All Of Breath Of The Wild in Minecraft*](https://grazzy.sae.sh/) world, using the [Amulet](https://www.amuletmc.com/) library to read the world data directly.

## Data Pipeline

### 1. Surface data

The first layer extracted is the surface: the highest non-air block for each `[x, z]` column within the bounds of the Great Plateau. 

**Note** Surface data has been streamlined to match underhangs.json, so there is a surface_art.txt and surface_raw.json.

### 2. Underhangs (caves, overhangs, interiors)

Surface data alone only produces a flattened plateau — anything under a roof effectively doesn't exist. That means the Temple of Time would render as a plain rock formation, and the Shrine of Resurrection wouldn't appear at all.

Underhangs solve this, but they're structural rather than per-block: they're rendered together as a group, or not at all. Extracted as:

- **`underhangs.json`** — the most complex data file. Each underhang is treated as its own separate map (though rendered together with others). Underhangs are pre-grouped into **caves**: clusters of subterranean air blocks that touch each other and get rendered as a single unit. Each underhang stores:
  - **artmap** — the block IDs of every block below the lowest block in an air column (in an `[x, z]` position) that doesn't touch the ground
  - **altmap** — the altitude (y level) of each of the artmap's tiles, indexed identically
  - **readmap** — the artmap gone through a translation layer of `key.json` to make the characters more readable. 
  - **custommap** — additional miniscule changes custommised by me. Overlayed over readmap.


### 3. Rendering underhangs

A naive rule like:

```
if abs(player_y - underhang_average_y) <= 35:
    render_underhang()
```

...doesn't hold up. The intended approach instead:

1. Calculate the position of each cave's opening(s) and their median y level.
2. Use line-of-sight (LOS) to check whether an opening is visible to the player.
3. If an opening is visible **and** the player is below the median y level of the overhang above that opening, render the underhang.

This requires a separate pass to calculate opening positions ahead of time.

## Tech Stack

- Python
- [Amulet](https://www.amuletmc.com/) for Minecraft world data extraction

## Installation

_TBD_

## Usage

_TBD_

## Roadmap
See [TODO.txt](./TODO.txt) for the detailed task breakdown.
- [ ] Datamining P
- [ ] Underhang/cave extraction script
- [ ] Cave opening detection + LOS rendering
- [ ] Top-down ASCII renderer
- [ ] _(more TBD)_

## Contributing

_TBD_

## License

_TBD_# botw-ascii
