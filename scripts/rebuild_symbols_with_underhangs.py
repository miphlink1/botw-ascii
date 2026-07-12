import json
from collections import Counter

IN_COUNTS = "data/block_counts_raw.json"
IN_SYMBOLS = "data/symbol_map.json"
OUT_SYMBOLS = "data/symbol_map.json"

with open(IN_COUNTS) as f:
    counts = json.load(f)

with open(IN_SYMBOLS) as f:
    symbols = json.load(f)

# NOTHING SILENT
all_seen = Counter(counts)

# ensure no block is missing
for b in all_seen:
    if b not in symbols:
        raise SystemExit(f"Missing block in symbol map: {b}")

print("SYMBOLS VERIFIED")