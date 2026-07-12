import json

AIR = "universal_minecraft:air"
DIM = "minecraft:overworld"


# ----------------------------
# LOAD DATA
# ----------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


underhangs = load_json("data/underhangs.json")
surface_alt = load_json("data/surface_altitude.json")


# ----------------------------
# AMULET INTERFACE (assumed external)
# ----------------------------

# world.get_block(dimension, x, y, z)
# MUST EXIST OR WE CRASH IMMEDIATELY
world = None
try:
    from amulet import load_level
    world = load_level("world/")
except Exception as e:
    raise RuntimeError("FAILED TO LOAD AMULET WORLD") from e


def get_block(x, y, z):
    block = world.get_block(x, y, z, DIM)
    if block is None:
        raise RuntimeError(f"NULL BLOCK AT {(x,y,z)}")
    return block.namespaced_name

# ----------------------------
# HELPERS
# ----------------------------

def is_air(x, y, z):
    x = int(x)
    y = int(y)
    z = int(z)
    return get_block(x, y, z) == AIR


SURFACE_X0 = 3709
SURFACE_Z0 = 5391

def surface_height(x, z):
    dx = x - SURFACE_X0
    dz = z - SURFACE_Z0

    # outside surface map
    if dx < 0 or dz < 0:
        return None

    if dz >= len(surface_alt):
        return None

    if dx >= len(surface_alt[dz]):
        return None

    try:
        return int(surface_alt[dz][dx])
    except Exception:
        raise RuntimeError(
            f"INVALID SURFACE ALT world={(x,z)} grid={(dx,dz)}"
        )


def neighbors_2d(x, z):
    return [
        (x+1, z),
        (x-1, z),
        (x, z+1),
        (x, z-1),
    ]


def in_region(underhang, x, z):
    local_x = x - underhang["x"]
    local_z = z - underhang["z"]

    artmap = underhang["artmap"]

    # outside vertical bounds
    if local_z < 0 or local_z >= len(artmap):
        return False

    row = artmap[local_z]

    # outside horizontal bounds
    if local_x < 0 or local_x >= len(row):
        return False

    return row[local_x] != "?"


# ----------------------------
# CORE LOGIC
# ----------------------------

def is_opening(uh, x, z, y):
    """
    A tile is an opening if:
    - it is boundary-adjacent to cave region
    - there is adjacent air outside region
    - there is a vertical air column to surface
    """

    for nx, nz in neighbors_2d(x, z):

        # must be outside region
        if in_region(uh, nx, nz):
            continue

        sy = surface_height(nx, nz)
        if sy is None:
            continue

        # must have adjacent air voxel at cave level
        try:
            if not is_air(nx, y, nz):
                continue
        except Exception as e:
            raise RuntimeError(f"AMULET FAIL AT {(nx,y,nz)}") from e

        # upward scan (strict)
        yy = y
        while yy <= sy:
            if not is_air(nx, yy, nz):
                break
            yy += 1
        else:
            # reached surface cleanly
            return [nx, nz]

    return None


# ----------------------------
# PROCESS UNDERHANGS
# ----------------------------

for uh in underhangs:

    x0, z0 = uh["x"], uh["z"]
    openings = set()

    artmap = uh["artmap"]
    altmap = uh["altmap"]

    for dz, row in enumerate(artmap):
        for dx, cell in enumerate(row):

            if cell == "?":
                continue

            x = x0 + dx
            z = z0 + dz

            raw_row = altmap[dz]

            try:
                values = [v.strip() for v in raw_row.split(",")]

                if len(values) != len(artmap[dz]):
                    raise RuntimeError(
                        f"ROW LENGTH MISMATCH at row {dz}: "
                        f"altmap={len(values)} artmap={len(artmap[dz])}"
                    )

                y = int(values[dx])

            except Exception:
                raise RuntimeError(f"BAD ALTMAP AT {(x,z)} ROW={raw_row}")

            # boundary check (4-neighbour)
            boundary = False
            for nx, nz in neighbors_2d(x, z):
                if not in_region(uh, nx, nz):
                    boundary = True
                    break

            if not boundary:
                continue

            opening = is_opening(uh, x, z, y)

            if opening:
                openings.add(tuple(opening))

    uh["openings"] = [list(o) for o in openings]


# ----------------------------
# OUTPUT
# ----------------------------

out_path = "data/underhangs_with_openings.json"

with open(out_path, "w") as f:
    json.dump(underhangs, f, indent=2)

print("OPENINGS GENERATED SUCCESSFULLY")