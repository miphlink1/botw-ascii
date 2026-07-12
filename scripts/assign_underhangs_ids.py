import json
from pathlib import Path

INPUT_PATH = Path("data/underhangs/underhangs_openings.json")
OUTPUT_PATH = Path("data/underhangs/underhangs_openings_ids.json")


def compute_size(uh):
    artmap = uh["artmap"]
    size = 0

    for row in artmap:
        for cell in row:
            if cell != "?":
                size += 1

    return size


def main():
    if not INPUT_PATH.exists():
        raise RuntimeError(f"Missing input file: {INPUT_PATH}")

    with open(INPUT_PATH, "r") as f:
        underhangs = json.load(f)

    if not isinstance(underhangs, list):
        raise RuntimeError("underhangs.json must be a list")

    # attach size
    for uh in underhangs:
        if "artmap" not in uh:
            raise RuntimeError(f"Malformed underhang (missing artmap): {uh}")

        uh["_size"] = compute_size(uh)

    # sort by size (largest first)
    underhangs.sort(key=lambda u: u["_size"], reverse=True)

    # assign IDs
    for i, uh in enumerate(underhangs):
        uh["id"] = i
        del uh["_size"]

    # write output
    with open(OUTPUT_PATH, "w") as f:
        json.dump(underhangs, f, indent=2)

    print(f"Assigned IDs to {len(underhangs)} underhangs")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()