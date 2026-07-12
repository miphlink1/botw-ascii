import json
from pathlib import Path

INPUT = Path("data/underhangs/underhangs_openings_ids.json")
KEEP_OUTPUT = Path("data/underhangs/runtime_underhangs.json")
ARCHIVE_OUTPUT = Path("data/underhangs/archive_underhangs.json")


def size(uh):
    return sum(
        1
        for row in uh["artmap"]
        for c in row
        if c != "?"
    )


def has_openings(uh):
    # assumes later phase adds this field; safe fallback
    return bool(uh.get("openings"))


def main():
    with open(INPUT, "r") as f:
        underhangs = json.load(f)

    keep = []
    archive = []

    for uh in underhangs:
        s = size(uh)
        o = has_openings(uh)

        uh["_size"] = s

        if (not o) and (s <= 4):
            archive.append(uh)
        else:
            keep.append(uh)

    for uh in keep:
        uh.pop("_size", None)
    for uh in archive:
        uh.pop("_size", None)

    with open(KEEP_OUTPUT, "w") as f:
        json.dump(keep, f, indent=2)

    with open(ARCHIVE_OUTPUT, "w") as f:
        json.dump(archive, f, indent=2)

    print(f"Kept: {len(keep)}")
    print(f"Archived: {len(archive)}")


if __name__ == "__main__":
    main()