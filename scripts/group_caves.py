import json
from collections import deque

IN_FILE = "data/air_voxels.json"
OUT_FILE = "data/caves.json"

with open(IN_FILE) as f:
    air_voxels = set(tuple(v) for v in json.load(f))

visited = set()
caves = []

dirs = [(1,0,0),(-1,0,0),(0,0,1),(0,0,-1),(0,1,0),(0,-1,0)]

def flood(start):
    q = deque([start])
    group = []

    while q:
        v = q.popleft()
        if v in visited:
            continue
        visited.add(v)
        group.append(v)

        x,y,z = v

        for dx,dy,dz in dirs:
            nv = (x+dx,y+dy,z+dz)
            if nv in air_voxels and nv not in visited:
                q.append(nv)

    return group

for v in air_voxels:
    if v not in visited:
        caves.append(flood(v))

with open(OUT_FILE, "w") as f:
    json.dump(caves, f)

print("CAVES GROUPED")