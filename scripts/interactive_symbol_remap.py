import json
import shutil
from pathlib import Path

# =========================
# PATHS
# =========================

SOURCE_SURFACE = Path("data/surface/surface_art.txt")
SOURCE_UNDERHANGS = Path("data/underhangs/runtime_underhangs.json")

TEST_DIR = Path("test")

TEST_SURFACE = TEST_DIR / "surface_art.txt"
TEST_UNDERHANGS = TEST_DIR / "runtime_underhangs.json"
TRANSLATION_KEY = TEST_DIR / "translation_key.json"


# =========================
# SETUP TEST ENVIRONMENT
# =========================

def setup():
    TEST_DIR.mkdir(exist_ok=True)

    if not TEST_SURFACE.exists():
        shutil.copy(SOURCE_SURFACE, TEST_SURFACE)

    if not TEST_UNDERHANGS.exists():
        shutil.copy(SOURCE_UNDERHANGS, TEST_UNDERHANGS)

    if not TRANSLATION_KEY.exists():
        with open(TRANSLATION_KEY, "w") as f:
            json.dump({}, f, indent=2)


# =========================
# LOAD FILES
# =========================

def load_surface():
    with open(TEST_SURFACE, "r") as f:
        return [line.rstrip("\n") for line in f]


def save_surface(surface):
    with open(TEST_SURFACE, "w") as f:
        for row in surface:
            f.write(row + "\n")


def load_underhangs():
    with open(TEST_UNDERHANGS, "r") as f:
        return json.load(f)


def save_underhangs(underhangs):
    with open(TEST_UNDERHANGS, "w") as f:
        json.dump(underhangs, f, indent=2)


def load_translation_key():
    with open(TRANSLATION_KEY, "r") as f:
        return json.load(f)


def save_translation_key(key):
    with open(TRANSLATION_KEY, "w") as f:
        json.dump(key, f, indent=2)


# =========================
# REPLACE SYMBOLS
# =========================

def replace_surface(surface, old, new):
    return [row.replace(old, new) for row in surface]


def replace_underhangs(underhangs, old, new):
    for uh in underhangs:
        new_artmap = []

        for row in uh["artmap"]:
            new_artmap.append(row.replace(old, new))

        uh["artmap"] = new_artmap

    return underhangs


# =========================
# MAIN LOOP
# =========================

def main():
    setup()

    print("=== INTERACTIVE SYMBOL REMAPPER ===")
    print("Type 'quit' at any prompt to exit.\n")

    while True:

        old = input("Replace symbol: ")

        if old.lower() == "quit":
            break

        if len(old) != 1:
            print("ERROR: Must be exactly one character.")
            continue

        new = input("Replace with: ")

        if new.lower() == "quit":
            break

        if len(new) != 1:
            print("ERROR: Must be exactly one character.")
            continue

        # Load current state
        surface = load_surface()
        underhangs = load_underhangs()
        translation_key = load_translation_key()

        # Apply replacements
        surface = replace_surface(surface, old, new)
        underhangs = replace_underhangs(underhangs, old, new)

        # Save changes
        save_surface(surface)
        save_underhangs(underhangs)

        # Record translation
        translation_key[old] = new
        save_translation_key(translation_key)

        print(f"Replaced '{old}' -> '{new}'")

    print("\nDone.")


if __name__ == "__main__":
    main()