import json
import time
from amulet import load_level

WORLD_PATH = "world/"
OUT_FILE = "data/subterranean_air.json"

x1, y1, z1 = 3709, -320, 5391
x2, y2, z2 = 4319, 320, 5879

dim = load_level(WORLD_PATH)
get_block = dim.get_block

results = {}

width = x2 - x1 + 1
depth = z2 - z1 + 1
total = width * depth
done = 0

start_time = time.time()


def progress(done, total):
    frac = done / total
    bar_len = 30
    filled = int(bar_len * frac)
    bar = "█" * filled + "-" * (bar_len - filled)
    print(f"\r[{bar}] {done}/{total}", end="")


for x in range(x1, x2 + 1):
    for z in range(z1, z2 + 1):

        # ---------------------------
        # 1. find surface height
        # ---------------------------
        surface_y = None

        for y in range(y2, y1 - 1, -1):
            b = get_block(x, y, z, "minecraft:overworld")
            if b and "air" not in b.namespaced_name.lower():
                surface_y = y
                break

        if surface_y is None:
            done += 1
            continue

        # ---------------------------
        # 2. scan below surface only
        # ---------------------------
        in_air = False
        start = None
        air_ranges = []

        for y in range(surface_y - 1, y1 - 1, -1):
            b = get_block(x, y, z, "minecraft:overworld")
            is_air = (b is None or "air" in b.namespaced_name.lower())

            if is_air:
                if not in_air:
                    start = y
                    in_air = True
            else:
                if in_air:
                    air_ranges.append((y + 1, start))
                    in_air = False

        if in_air:
            air_ranges.append((y1, start))

        if air_ranges:
            results[f"{x},{z}"] = {
                "surface_y": surface_y,
                "air": air_ranges
            }

        done += 1
        if done % 10 == 0:
            progress(done, total)

print("\nSaving...")

with open(OUT_FILE, "w") as f:
    json.dump(results, f)

print("DONE")