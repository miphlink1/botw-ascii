import json
from pathlib import Path

INPUT = Path("test/translation_key.json")
OUTPUT = Path("test/resolved_translation_key.json")


def resolve(symbol, key, seen=None):

    if seen is None:
        seen = set()

    if symbol in seen:
        raise RuntimeError(f"Circular mapping detected at '{symbol}'")

    seen.add(symbol)

    target = key.get(symbol, symbol)

    # reached stable endpoint
    if target == symbol:
        return symbol

    # recurse
    return resolve(target, key, seen)


def main():

    if not INPUT.exists():
        raise RuntimeError(f"Missing file: {INPUT}")

    with open(INPUT, "r") as f:
        key = json.load(f)

    resolved = {}

    for symbol in key:
        resolved[symbol] = resolve(symbol, key)

    with open(OUTPUT, "w") as f:
        json.dump(resolved, f, indent=2)

    print("Translation key resolved successfully")


if __name__ == "__main__":
    main()