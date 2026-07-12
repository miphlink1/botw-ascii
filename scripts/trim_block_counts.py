import json
from collections import Counter

IN_FILE = "data/block_counts_raw.json"
OUT_FILE = "data/block_counts_trimmed.json"

# size limit (your symbol set capacity)
SYMBOL_CAPACITY = 9 + 26 + 26  # 61 symbols total

with open(IN_FILE, "r") as f:
    counts = Counter(json.load(f))

# sort by frequency (descending)
sorted_blocks = sorted(counts.items(), key=lambda x: -x[1])

kept = sorted_blocks[:SYMBOL_CAPACITY]
dropped = sorted_blocks[SYMBOL_CAPACITY:]

trimmed = dict(kept)

with open(OUT_FILE, "w") as f:
    json.dump(trimmed, f, indent=2)

print(f"KEPT: {len(kept)} blocks")
print(f"DROPPED: {len(dropped)} blocks")

if dropped:
    print("\nWARNING: Dropped blocks (mapped to fallback '?'):")
    for b, c in dropped[:20]:
        print(b, c)