import json
from pathlib import Path

PATH = Path("data/underhangs/runtime_underhangs.json")


def normalize_altmap(altmap, uh_id):
    if not isinstance(altmap, list) or not altmap:
        raise RuntimeError(f"Invalid altmap in underhang {uh_id}")

    width = None
    normalized = []

    for z, row in enumerate(altmap):

        # CASE 1: row is a CSV string (your current format)
        if isinstance(row, str):
            row = [v.strip() for v in row.split(",")]

        # CASE 2: row is already list (future-proofing)
        elif isinstance(row, list):
            pass
        else:
            raise RuntimeError(
                f"Altmap row invalid type in underhang {uh_id}, row {z}: {type(row)}"
            )

        if width is None:
            width = len(row)

        if len(row) != width:
            raise RuntimeError(
                f"Non-rectangular altmap in underhang {uh_id} at row {z}"
            )

        try:
            normalized.append([int(v) for v in row])
        except Exception:
            raise RuntimeError(
                f"Bad alt value in underhang {uh_id} at row {z}: {row}"
            )

    return normalized


def main():
    if not PATH.exists():
        raise RuntimeError(f"Missing file: {PATH}")

    with open(PATH, "r") as f:
        underhangs = json.load(f)

    if not isinstance(underhangs, list):
        raise RuntimeError("runtime_underhangs.json must be a list")

    for uh in underhangs:
        if "id" not in uh:
            raise RuntimeError("Underhang missing id")

        if "altmap" not in uh:
            raise RuntimeError(f"Underhang {uh['id']} missing altmap")

        uh["altmap"] = normalize_altmap(uh["altmap"], uh["id"])

    with open(PATH, "w") as f:
        json.dump(underhangs, f, indent=2)

    print(f"Normalized altmaps for {len(underhangs)} underhangs")


if __name__ == "__main__":
    main()