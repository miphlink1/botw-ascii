import json, string
from collections import Counter
from amulet import load_level

WORLD_PATH = "world/"
OUT_SURFACE = "data/surface.json"
OUT_HEIGHT = "data/heightmap.json"
OUT_COUNTS = "data/block_counts_raw.json"

x1, y1, z1 = 3709, -320, 5391
x2, y2, z2 = 4319, 320, 5879

dim = load_level(WORLD_PATH)

block_counts = Counter()
surface = []
heightmap = []

def get_block(x,y,z):
    return dim.get_block(x,y,z,"minecraft:overworld").namespaced_name.lower()

for z in range(z1, z2+1):
    row, hrow = [], []
    for x in range(x1, x2+1):

        top_y = None
        top_block = None

        for y in range(y2, y1-1, -1):
            b = get_block(x,y,z)
            if not b or "air" in b:
                continue
            top_y = y
            top_block = b
            break

        if top_block is None:
            raise SystemExit(f"No block at {x},{z}")

        block_counts[top_block] += 1
        row.append(top_block)
        hrow.append(str(top_y))

    surface.append(row)
    heightmap.append(hrow)

with open(OUT_SURFACE, "w") as f:
    json.dump(surface, f)

with open(OUT_HEIGHT, "w") as f:
    json.dump(heightmap, f)

with open(OUT_COUNTS, "w") as f:
    json.dump(block_counts, f)

print("RAW SCAN COMPLETE")