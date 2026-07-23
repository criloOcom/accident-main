#!/usr/bin/env python3
"""Normalize all filenames/dirnames: remove accents, &, spaces, parens, etc."""

import os
import re
import unicodedata

BASE = "/home/crilocom/accident-main"
TARGETS = [
    "Actes/Token",
    "Actes/Reel",
]

EXCLUDE_DIRS = {".git", "__pycache__", ".pytest_cache"}


def normalize(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_bytes = nfkd.encode("ascii", "ignore")
    safe = ascii_bytes.decode("ascii")
    safe = safe.replace("&", "et")
    safe = safe.replace("'", "")
    safe = safe.replace("\u2014", "-")
    safe = re.sub(r'[\s\(\)]+', '_', safe)
    safe = re.sub(r'_+', '_', safe)
    safe = safe.strip('_')
    return safe


def collect_renames(root_dir: str) -> list:
    pending = []
    root = os.path.join(BASE, root_dir)

    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        parts = rel.split(os.sep)
        if any(p in EXCLUDE_DIRS for p in parts):
            continue

        for fname in filenames:
            if fname == ".gitkeep":
                continue
            new_name = normalize(fname)
            if new_name != fname:
                old = os.path.join(dirpath, fname)
                new = os.path.join(dirpath, new_name)
                pending.append((old, new))

    for dirpath, dirnames, _ in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        parts = rel.split(os.sep)
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        for dname in dirnames:
            new_name = normalize(dname)
            if new_name != dname:
                old = os.path.join(dirpath, dname)
                new = os.path.join(dirpath, new_name)
                pending.append((old, new))

    pending.sort(key=lambda x: x[0].count(os.sep), reverse=True)
    return pending


def main():
    all_renames = []
    for t in TARGETS:
        all_renames.extend(collect_renames(t))

    seen = set()
    unique = []
    for old, new in all_renames:
        if old not in seen:
            seen.add(old)
            unique.append((old, new))

    if not unique:
        print("No files/dirs need renaming.")
        return

    print(f"Collected {len(unique)} rename operations:\n")
    for old, new in unique:
        print(f"  mv {os.path.relpath(old, BASE)}")
        print(f"     {os.path.relpath(new, BASE)}\n")

    import sys
    if "--yes" not in sys.argv:
        confirm = input("Execute? (yes/no): ")
        if confirm.lower() != "yes":
            print("Aborted.")
            return

    print("Executing renames...")
    for old, new in unique:
        if os.path.exists(new):
            print(f"  SKIP (exists): {os.path.relpath(new, BASE)}")
            continue
        os.makedirs(os.path.dirname(new), exist_ok=True)
        os.rename(old, new)
        print(f"  OK: {os.path.relpath(old, BASE)}")

    print("\nDone. Run 'git add -A && git commit'.")


if __name__ == "__main__":
    main()
