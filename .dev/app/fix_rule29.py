#!/usr/bin/env python3
"""
Fix Rule #29 violations in .md files.

Adds missing closing tags (<!-- /Auteur -->, <!-- /Destinataire -->, <!-- /PJ -->, <!-- /Source -->)
and missing --- around Objet blocks.

Usage:
    python3 fix_rule29.py                    # dry-run
    python3 fix_rule29.py --apply            # apply fixes
"""

import os
import re
import sys
import argparse

ROOT = '/home/crilocom/accident-main'

DIRS = [
    '⚖️ Actes/🔑 Token/✉️ Courriers',
    '⚖️ Actes/🔑 Token/⚖️ Actes proceduraux',
    '⚖️ Actes/👤 Reel/✉️ Courriers',
    '⚖️ Actes/👤 Reel/⚖️ Actes proceduraux',
]

# Required paired tags
TAGS = {
    '<!-- Auteur -->': '<!-- /Auteur -->',
    '<!-- Destinataire -->': '<!-- /Destinataire -->',
    '<!-- PJ -->': '<!-- /PJ -->',
    '<!-- Source -->': '<!-- /Source -->',
}


def find_md_files(dirs):
    files = []
    for d in dirs:
        full = os.path.join(ROOT, d)
        if not os.path.exists(full):
            continue
        for dp, _, fnames in os.walk(full):
            for f in fnames:
                if f.endswith('.md') and f != 'README.md':
                    files.append(os.path.join(dp, f))
    return sorted(files)


def find_closing_position(lines, open_idx, tag_name):
    """Find the appropriate position to insert a closing tag after an opening tag."""
    open_line = lines[open_idx].strip()

    if tag_name == 'Auteur':
        # Auteur block: ends at the next blank line followed by content,
        # or the next HTML comment that isn't /Auteur
        for j in range(open_idx + 1, min(open_idx + 15, len(lines))):
            stripped = lines[j].strip()
            # Blank line followed by another blank line or a comment or ## section
            if stripped == '':
                # Check if next non-empty line is a separator, comment, or section
                for k in range(j + 1, min(j + 4, len(lines))):
                    next_stripped = lines[k].strip()
                    if next_stripped == '<!-- Destinataire -->':
                        return j
                    elif next_stripped.startswith('<!-- ') and '/Auteur' not in next_stripped:
                        return j
                    elif next_stripped.startswith('## '):
                        return j
                    elif next_stripped.startswith('**[') or next_stripped.startswith('Monsieur') or next_stripped.startswith('Madame'):
                        return j
                    elif next_stripped == '---':
                        return j
                # If no clear end found after blank line, use this blank line
                return j
            # If we hit another HTML comment, end before it
            elif stripped.startswith('<!-- ') and stripped != '<!-- /Auteur -->':
                return j
            # If we hit a section header
            elif stripped.startswith('## '):
                return j
        return open_idx + 3  # fallback

    elif tag_name == 'Destinataire':
        # Destinataire block: similar to Auteur
        for j in range(open_idx + 1, min(open_idx + 15, len(lines))):
            stripped = lines[j].strip()
            if stripped == '':
                for k in range(j + 1, min(j + 4, len(lines))):
                    next_stripped = lines[k].strip()
                    if next_stripped.startswith('**[') or next_stripped.startswith('Monsieur') or next_stripped.startswith('Madame'):
                        return j
                    elif next_stripped.startswith('<!-- ') and '/Destinataire' not in next_stripped:
                        return j
                    elif next_stripped.startswith('## '):
                        return j
                    elif next_stripped == '---':
                        return j
                    elif next_stripped.startswith('PLAISE'):
                        return j
                return j
            elif stripped.startswith('<!-- ') and stripped != '<!-- /Destinataire -->':
                return j
            elif stripped.startswith('## '):
                return j
            elif stripped.startswith('PLAISE'):
                return j
        return open_idx + 3

    elif tag_name == 'PJ':
        # PJ block: ends at the next ## section or <!-- Source --> or end of list
        for j in range(open_idx + 1, len(lines)):
            stripped = lines[j].strip()
            if stripped.startswith('## ') and 'PIECES' not in stripped.upper() and 'PJ' not in stripped:
                return j
            elif stripped.startswith('<!-- Source -->'):
                return j
            elif stripped.startswith('<!-- /'):
                return j
        return len(lines) - 1

    elif tag_name == 'Source':
        # Source block: ends at the end of footnotes or next ## section
        in_footnotes = False
        for j in range(open_idx + 1, len(lines)):
            stripped = lines[j].strip()
            if stripped.startswith('[^'):
                in_footnotes = True
            elif in_footnotes and stripped == '':
                # Check if there are more footnotes
                has_more = False
                for k in range(j + 1, min(j + 5, len(lines))):
                    if lines[k].strip().startswith('[^'):
                        has_more = True
                        break
                if not has_more:
                    return j
            elif stripped.startswith('## ') and in_footnotes:
                return j
            elif stripped.startswith('<!-- /'):
                return j
        return len(lines) - 1

    return open_idx + 3


def fix_file(filepath):
    """Fix Rule #29 violations in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    changes = []
    modified = False

    # Fix 1: Add missing closing tags
    for open_tag, close_tag in TAGS.items():
        tag_name = open_tag.replace('<!-- ', '').replace(' -->', '')
        opens = [i for i, line in enumerate(lines) if open_tag in line]
        closes = [i for i, line in enumerate(lines) if close_tag in line]

        if opens and not closes:
            # Find where to insert the closing tag
            open_idx = opens[0]
            close_idx = find_closing_position(lines, open_idx, tag_name)
            lines.insert(close_idx, close_tag)
            changes.append(f"Added {close_tag} at line {close_idx + 1}")
            modified = True

    # Fix 2: Add --- around Objet block
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('**Objet') or stripped.startswith('Objet :'):
            # Check for --- before
            has_hr_before = False
            for j in range(max(0, i - 3), i):
                if lines[j].strip() == '---':
                    has_hr_before = True
                    break

            if not has_hr_before:
                lines.insert(i, '---')
                changes.append(f"Added --- before Objet at line {i + 1}")
                modified = True
                i += 1  # Adjust index

            # Check for --- after (after Objet + optional LRAR line)
            has_hr_after = False
            for j in range(i + 1, min(len(lines), i + 5)):
                if lines[j].strip() == '---':
                    has_hr_after = True
                    break

            if not has_hr_after:
                # Find end of Objet/LRAR block
                insert_after = i + 1
                for j in range(i + 1, min(len(lines), i + 5)):
                    if lines[j].strip().startswith('**N°') or lines[j].strip().startswith('**Nº'):
                        insert_after = j + 1
                        break
                    elif lines[j].strip() == '':
                        insert_after = j
                        break
                lines.insert(insert_after, '---')
                changes.append(f"Added --- after Objet at line {insert_after + 1}")
                modified = True

    if modified:
        content = '\n'.join(lines)

    return content, changes


def main():
    parser = argparse.ArgumentParser(description='Fix Rule #29 violations')
    parser.add_argument('--apply', action='store_true', help='Apply fixes')
    args = parser.parse_args()

    files = find_md_files(DIRS)
    print(f"Scanning {len(files)} files...")

    total_fixed = 0
    total_changes = 0

    for fp in files:
        rel_path = os.path.relpath(fp, ROOT)
        fixed_content, changes = fix_file(fp)

        if changes:
            total_fixed += 1
            total_changes += len(changes)
            print(f"\n{rel_path}:")
            for change in changes:
                print(f"  {change}")

            if args.apply:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Files scanned: {len(files)}")
    print(f"Files with fixes: {total_fixed}")
    print(f"Total changes: {total_changes}")
    if not args.apply:
        print(f"\nRun with --apply to apply fixes")


if __name__ == '__main__':
    main()
