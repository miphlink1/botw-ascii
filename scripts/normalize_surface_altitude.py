import json
from pathlib import Path

PATH = Path("data/surface/surface_altitude.json")


def main():
    if not PATH.exists():
        raise RuntimeError(f"Missing file: {PATH}")

    with open(PATH, "r") as f:
        data = json.load(f)

    # Validate structure
    if not isinstance(data, list) or not data:
        raise RuntimeError("Surface altitude must be a non-empty 2D list")

    width = len(data[0])

    for z, row in enumerate(data):
        if not isinstance(row, list):
            raise RuntimeError(f"Row {z} is not a list")

        if len(row) != width:
            raise RuntimeError(
                f"Non-rectangular surface_altitude at row {z}: "
                f"{len(row)} != {width}"
            )

        for x, val in enumerate(row):
            try:
                row[x] = int(val)
            except Exception:
                raise RuntimeError(
                    f"Invalid altitude value at ({x},{z}): {val}"
                )

    # Write back normalized version
    with open(PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Normalized surface_altitude.json ({len(data)}x{width})")


if __name__ == "__main__":
    main()