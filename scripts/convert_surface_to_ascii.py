import json
import time

SURFACE_FILE = "data/surface.json"
KEY_FILE = "data/key.json"
OUT_FILE = "data/surface_ascii.txt"

FALLBACK = "!"

# -------------------------
# LOAD FILES
# -------------------------
with open(SURFACE_FILE, "r") as f:
    surface = json.load(f)

with open(KEY_FILE, "r") as f:
    key = json.load(f)

# -------------------------
# PROGRESS BAR
# -------------------------
def progress(current, total, start):
    frac = current / total
    width = 30
    filled = int(width * frac)
    bar = "█" * filled + "-" * (width - filled)
    elapsed = time.time() - start
    eta = int(elapsed / frac - elapsed) if frac > 0 else 0
    print(f"\r[{bar}] {current}/{total} ETA:{eta}s", end="")

# -------------------------
# CONVERT
# -------------------------
print("Converting surface map to ASCII...")

ascii_map = []
start = time.time()

total_rows = len(surface)

for i, row in enumerate(surface):

    ascii_row = []

    for block in row:
        symbol = key.get(block, FALLBACK)
        ascii_row.append(symbol)

    ascii_map.append("".join(ascii_row))

    if i % 50 == 0:
        progress(i, total_rows, start)

print("\nConversion complete.")

# -------------------------
# SAVE
# -------------------------
print("Saving...")

with open(OUT_FILE, "w") as f:
    for row in ascii_map:
        f.write(row + "\n")

print("DONE")