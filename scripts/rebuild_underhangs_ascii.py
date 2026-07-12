import json
import time
from collections import deque, defaultdict
from amulet import load_level

WORLD_PATH = "world/"
OUT_FILE = "data/underhangs.json"

KEY_FILE = "data/key.json"

x1, y1, z1 = 3709, -320, 5391
x2, y2, z2 = 4319, 320, 5879

dim = load_level(WORLD_PATH)
get_block = dim.get_block

# -------------------------
# LOAD KEY
# -------------------------
with open(KEY_FILE, "r") as f:
    key = json.load(f)

FALLBACK = "!"

def get_symbol(block_name):
    return key.get(block_name, FALLBACK)

# -------------------------
# PROGRESS BAR
# -------------------------
def progress(current, total, start, label=""):
    frac = current / total
    width = 30
    filled = int(width * frac)
    bar = "█" * filled + "-" * (width - filled)
    elapsed = time.time() - start
    eta = int(elapsed / frac - elapsed) if frac > 0 else 0
    print(f"\r{label} [{bar}] {current}/{total} ETA:{eta}s", end="")

# -------------------------
# 1. FIND SUBTERRANEAN AIR
# -------------------------
print("Scanning subterranean air...")

air = set()
start = time.time()

total_cols = (x2 - x1 + 1) * (z2 - z1 + 1)
done = 0

for x in range(x1, x2 + 1):
    for z in range(z1, z2 + 1):

        surface_y = None
        for y in range(y2, y1 - 1, -1):
            b = get_block(x, y, z, "minecraft:overworld")
            if b and "air" not in b.namespaced_name.lower():
                surface_y = y
                break

        if surface_y is None:
            done += 1
            continue

        in_air = False
        start_y = None

        for y in range(surface_y - 1, y1 - 1, -1):
            b = get_block(x, y, z, "minecraft:overworld")
            is_air = (b is None or "air" in b.namespaced_name.lower())

            if is_air:
                if not in_air:
                    start_y = y
                    in_air = True
            else:
                if in_air:
                    for yy in range(y + 1, start_y + 1):
                        air.add((x, yy, z))
                    in_air = False

        if in_air:
            for yy in range(y1, start_y + 1):
                air.add((x, yy, z))

        done += 1
        if done % 500 == 0:
            progress(done, total_cols, start, "Air scan")

print("\nAir scan complete.")
print(f"Air voxels: {len(air):,}")

# -------------------------
# 2. FLOODFILL POCKETS
# -------------------------
print("Grouping pockets...")

dirs = [(1,0,0),(-1,0,0),(0,0,1),(0,0,-1),(0,1,0),(0,-1,0)]
air_set = set(air)
visited = set()
pockets = []

def flood(start_voxel):
    q = deque([start_voxel])
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

start = time.time()

for i, v in enumerate(air):
    if v not in visited:
        pockets.append(flood(v))
    if i % 10000 == 0:
        progress(i, len(air), start, "Floodfill")

print("\nFloodfill complete.")
print(f"Pockets: {len(pockets)}")

# -------------------------
# 3. PROJECT EACH POCKET
# -------------------------
print("Building underhang maps...")

output = []
start = time.time()

for pid, pocket in enumerate(pockets):

    # bounding box
    xs = [p[0] for p in pocket]
    zs = [p[2] for p in pocket]

    x_min, x_max = min(xs), max(xs)
    z_min, z_max = min(zs), max(zs)

    # group columns ONCE (huge speedup)
    columns = defaultdict(list)
    for x, y, z in pocket:
        columns[(x, z)].append(y)

    artmap = []
    altmap = []

    for z in range(z_min, z_max + 1):
        art_row = []
        alt_row = []

        for x in range(x_min, x_max + 1):

            if (x, z) not in columns:
                art_row.append("?")
                alt_row.append("-1")
                continue

            ys = columns[(x, z)]
            lowest_air = min(ys)
            floor_y = lowest_air - 1

            b = get_block(x, floor_y, z, "minecraft:overworld")
            name = b.namespaced_name.lower() if b else "none"

            symbol = get_symbol(name)

            art_row.append(symbol)
            alt_row.append(str(floor_y))

        artmap.append("".join(art_row))
        altmap.append(",".join(alt_row))

    output.append({
        "x": x_min,
        "z": z_min,
        "artmap": artmap,
        "altmap": altmap
    })

    if pid % 10 == 0:
        progress(pid, len(pockets), start, "Projecting")

print("\nProjection complete.")

# -------------------------
# 4. SAVE
# -------------------------
print("Saving...")

with open(OUT_FILE, "w") as f:
    json.dump(output, f)

print("DONE")