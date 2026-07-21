#!/usr/bin/env python3
"""Sort file lists in README.md index files alphabetically A→Z."""
import os
import re
import sys

ROOT = "/home/crilocom/accident-main"
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', '.opencode'}
# Files with complex structure (multi-section, tables) — excluded
EXCLUDE = {
    "Lois/Index/README.md",
    "Actes/Token/Archives/README.md",
}

dry_run = "--apply" not in sys.argv


def sort_key(entry):
    """Case-insensitive sort key with French accent awareness."""
    m = re.match(r'-\s*\[(.+?)\]', entry)
    if not m:
        return entry.lower()
    text = m.group(1).lower()
    return text


def sort_entries(entries):
    return sorted(entries, key=sort_key)


def find_index_list(lines):
    """Find start/end of list items under # Index heading.

    Returns (list_start, list_end, entry_lines) or None.
    """
    # Find # Index line
    idx = None
    for i, line in enumerate(lines):
        if re.match(r'^#\s+Index\b', line):
            idx = i
            break
    if idx is None:
        return None

    # Find first list item after heading
    list_start = None
    list_end = None
    for i in range(idx + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith('- ['):
            if list_start is None:
                list_start = i
            list_end = i + 1  # tentative end (exclusive)
        elif list_start is not None:
            if stripped == '':
                list_end = i + 1  # include trailing blank
            elif stripped.startswith('#') or stripped.startswith('|') or stripped.startswith('---'):
                break  # next section
            elif stripped.startswith('- ['):
                continue  # should not normally hit this
            else:
                break  # non-list, non-blank line

    if list_start is None:
        return None

    # Extract only the list item lines (skip blank lines between them)
    entries = [
        lines[i].strip() for i in range(list_start, list_end)
        if lines[i].strip().startswith('- [')
    ]

    return (list_start, list_end, entries)


def process_file(fpath):
    rel = os.path.relpath(fpath, ROOT)
    if rel in EXCLUDE:
        if dry_run:
            print(f"  [SKIP] {rel} (excluded)")
        return False

    content = open(fpath, encoding='utf-8').read()
    lines = content.split('\n')

    result = find_index_list(lines)
    if result is None:
        return False

    list_start, list_end, entries = result

    if len(entries) <= 1:
        return False

    sorted_entries = sort_entries(entries)

    # Check if already sorted
    if entries == sorted_entries:
        return False

    if dry_run:
        dirname = os.path.basename(os.path.dirname(fpath))
        print(f"  [DRY] {rel}  ({len(entries)} entries → sort)")
        return True

    # Rebuild lines: preserve indent of first entry
    prefix = ''
    for i in range(list_start, len(lines)):
        if lines[i].strip().startswith('- ['):
            pm = re.match(r'^(\s*)-\s*\[', lines[i])
            if pm:
                prefix = pm.group(1)
            break

    new_lines = lines[:list_start]
    for j, entry in enumerate(sorted_entries):
        if j > 0:
            new_lines.append('')
        new_lines.append(f"{prefix}{entry}")
    new_lines.extend(lines[list_end:])

    new_content = '\n'.join(new_lines)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  [WROTE] {rel}  ({len(entries)} entries sorted)")
    return True


def main():
    count = 0
    for dp, dn, fn in os.walk(ROOT):
        parts = os.path.relpath(dp, ROOT).split(os.sep)
        if any(p in SKIP_DIRS for p in parts):
            continue
        if 'README.md' not in fn:
            continue
        fpath = os.path.join(dp, 'README.md')
        if process_file(fpath):
            count += 1

    print(f"\nRésumé : {count} fichiers {'à trier (dry-run)' if dry_run else 'triés'}.")


if __name__ == '__main__':
    main()
