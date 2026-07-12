import json
from pathlib import Path
from collections import deque

INPUT = Path("data/underhangs/runtime_underhangs.json")
OUTPUT = Path("data/underhangs/runtime_underhangs_with_entrances.json")


# 8-direction adjacency (Option B)
DIRS = [
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
]


def cluster_openings(openings):
    """
    openings: list of (x, z)
    returns: list of clusters [[(x,z), ...], ...]
    """
    unvisited = set(openings)
    clusters = []

    while unvisited:
        start = unvisited.pop()
        queue = deque([start])
        cluster = [start]

        while queue:
            x, z = queue.popleft()

            for dx, dz in DIRS:
                n = (x + dx, z + dz)

                if n in unvisited:
                    unvisited.remove(n)
                    queue.append(n)
                    cluster.append(n)

        clusters.append(cluster)

    return clusters


def centroid(tiles):
    x = sum(t[0] for t in tiles) / len(tiles)
    z = sum(t[1] for t in tiles) / len(tiles)
    return (x, z)


def main():
    if not INPUT.exists():
        raise RuntimeError(f"Missing file: {INPUT}")

    with open(INPUT, "r") as f:
        underhangs = json.load(f)

    next_id = 0

    for uh in underhangs:
        openings = uh.get("openings", [])

        # normalize format: ensure tuples
        openings = [tuple(o) for o in openings]

        clusters = cluster_openings(openings)

        entrances = []
        for c in clusters:
            entrances.append({
                "id": next_id,
                "underhang_id": uh["id"],
                "tiles": c,
                "centroid": centroid(c)
            })
            next_id += 1

        uh["entrances"] = entrances

    with open(OUTPUT, "w") as f:
        json.dump(underhangs, f, indent=2)

    print(f"Processed {len(underhangs)} underhangs")
    print(f"Generated {next_id} entrances total")


if __name__ == "__main__":
    main()