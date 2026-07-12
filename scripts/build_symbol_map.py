import json
import string
from collections import defaultdict

SURFACE_FILE = "data/block_counts_surface.json"
UNDERHANG_FILE = "data/block_counts_underhangs.json"

OUTPUT_FILE = "data/key.json"
DROPPED_FILE = "diagnostics/dropped_blocks_final.json"

# -------------------------
# SYMBOL POOL
# -------------------------
symbols = (
    list("123456789") +
    list(string.ascii_lowercase) +
    list(string.ascii_uppercase)
)

# anything beyond this becomes "!"
FALLBACK_SYMBOL = "!"

# -------------------------
# LOAD DATA
# -------------------------
with open(SURFACE_FILE, "r") as f:
    surface = json.load(f)

with open(UNDERHANG_FILE, "r") as f:
    under = json.load(f)

# -------------------------
# MERGE COUNTS
# -------------------------
counts = defaultdict(int)

for k, v in surface.items():
    counts[k] += v

for k, v in under.items():
    counts[k] += v

# -------------------------
# SORT BY FREQUENCY
# -------------------------
sorted_blocks = sorted(counts.items(), key=lambda x: x[1], reverse=True)

# -------------------------
# ASSIGN SYMBOLS
# -------------------------
key_map = {}
dropped = {}

for i, (block, count) in enumerate(sorted_blocks):

    if i < len(symbols):
        key_map[block] = symbols[i]
    else:
        key_map[block] = FALLBACK_SYMBOL
        dropped[block] = count

# -------------------------
# SAVE KEY
# -------------------------
with open(OUTPUT_FILE, "w") as f:
    json.dump(key_map, f, indent=2)

# -------------------------
# SAVE DROPPED BLOCKS
# -------------------------
import os
os.makedirs("diagnostics", exist_ok=True)

with open(DROPPED_FILE, "w") as f:
    json.dump(dropped, f, indent=2)

# -------------------------
# REPORT
# -------------------------
print(f"Total blocks: {len(sorted_blocks)}")
print(f"Mapped with unique symbols: {min(len(sorted_blocks), len(symbols))}")
print(f"Dropped into '!': {len(dropped)}")
print("Key generation complete.")