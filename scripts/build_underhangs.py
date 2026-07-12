import json
import time
from collections import deque, defaultdict
from amulet import load_level

WORLD_PATH = "world/"
OUT_FILE = "data/underhangs.json"
BLOCK_STATS_FILE = "data/block_stats_underhangs.json"

x1, y1, z1 = 3709, -320, 5391
x2, y2, z2 = 4319, 320, 5879

dim = load_level(WORLD_PATH)
get_block = dim.get_block

# -------------------------
# 1. FIND SUBTERRANEAN AIR
# -------------------------
print("Scanning subterranean air...")

air = set()

for x in range(x1, x2 + 1):
    for z in range(z1, z2 + 1):

        # surface
        surface_y = None
        for y in range(y2, y1 - 1, -1):
            b = get_block(x, y, z, "minecraft:overworld")
            if b and "air" not in b.namespaced_name.lower():
                surface_y = y
                break

        if surface_y is None:
            continue

        in_air = False
        start = None

        for y in range(surface_y - 1, y1 - 1, -1):
            b = get_block(x, y, z, "minecraft:overworld")
            is_air = (b is None or "air" in b.namespaced_name.lower())

            if is_air:
                if not in_air:
                    start = y
                    in_air = True
            else:
                if in_air:
                    for yy in range(y + 1, start + 1):
                        air.add((x, yy, z))
                    in_air = False

        if in_air:
            for yy in range(y1, start + 1):
                air.add((x, yy, z))

print(f"Air voxels: {len(air):,}")

# -------------------------
# 2. FLOODFILL POCKETS
# -------------------------
print("Grouping pockets...")

dirs = [(1,0,0),(-1,0,0),(0,0,1),(0,0,-1),(0,1,0),(0,-1,0)]
air_set = set(air)
visited = set()
pockets = []

def flood(start):
    q = deque([start])
    group = []

    while q:
        v = q.popleft()
        if v in visited:
            continue
        visited.add(v)
        group.append(v)

        x,y,z = v
        for dx,dy,dz in dirs:
            nv = (x+dx, y+dy, z+dz)
            if nv in air_set and nv not in visited:
                q.append(nv)

    return group

for v in air:
    if v not in visited:
        pockets.append(flood(v))

print(f"Pockets: {len(pockets)}")

# -------------------------
# 3. PROJECT EACH POCKET
# -------------------------
print("Building underhang maps...")

output = []
block_stats = defaultdict(int)

for pid, pocket in enumerate(pockets):

    xs = [p[0] for p in pocket]
    zs = [p[2] for p in pocket]

    x_min, x_max = min(xs), max(xs)
    z_min, z_max = min(zs), max(zs)

    # map all pocket positions for fast lookup
    pocket_set = {(x, y, z) for x, y, z in pocket}

    artmap = []
    altmap = []

    for z in range(z_min, z_max + 1):
        art_row = []
        alt_row = []

        for x in range(x_min, x_max + 1):

            # collect all air voxels in this column
            column = [p for p in pocket if p[0] == x and p[2] == z]

            if not column:
                art_row.append("?")
                alt_row.append("-1")
                continue

            lowest_air = min(p[1] for p in column)
            floor_y = lowest_air - 1

            b = get_block(x, floor_y, z, "minecraft:overworld")
            name = b.namespaced_name.lower() if b else "none"

            block_stats[name] += 1

            art_row.append(name[0])  # TEMP symbol (tileset later)
            alt_row.append(str(floor_y))

        artmap.append("".join(art_row))
        altmap.append(",".join(alt_row))

    output.append({
        "x": x_min,
        "z": z_min,
        "artmap": artmap,
        "altmap": altmap
    })

# -------------------------
# 4. SAVE
# -------------------------
print("Saving...")

with open(OUT_FILE, "w") as f:
    json.dump(output, f)

with open(BLOCK_STATS_FILE, "w") as f:
    json.dump(block_stats, f)

print("DONE")