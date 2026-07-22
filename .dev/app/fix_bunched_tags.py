#!/usr/bin/env python3
"""
Fix the bunched-tags bug from fix_rule29.py.

The bug inserted all HTML comment tags (PJ, Signature, LRAR, Objet, Date,
Destinataire, /PJ, /Destinataire, Auteur, /Auteur) in a block between
the YAML frontmatter and the Breadcrumb, instead of wrapping the actual
content sections.

The fix: remove the bunched-tags block. The correct tags already exist
in the body of the document.
"""

import os
import re
import argparse

ROOT = '/home/crilocom/accident-main'

DIRS = [
    'Actes/Token/Courriers',
    'Actes/Token/Actes_proceduraux',
    'Actes/Reel/Courriers',
    'Actes/Reel/Actes_proceduraux',
]

# Tags that were incorrectly bunched together
BUNCH_TAGS = [
    '<!-- PJ -->',
    '<!-- Signature -->',
    '<!-- LRAR -->',
    '<!-- Objet -->',
    '<!-- Date -->',
    '<!-- Destinataire -->',
    '<!-- /PJ -->',
    '<!-- /Destinataire -->',
    '<!-- Auteur -->',
    '<!-- /Auteur -->',
    '<!-- Source -->',
    '<!-- /Source -->',
]


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


def has_bunched_tags(lines):
    """Check if file has the bunched-tags bug (tags grouped after YAML, before Breadcrumb)."""
    # Find end of YAML frontmatter
    yaml_end = -1
    in_yaml = False
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_yaml:
                in_yaml = True
            else:
                yaml_end = i
                break

    if yaml_end == -1:
        return False, -1, -1

    # Check if there's a block of bunched tags between YAML and Breadcrumb
    # Look for 3+ consecutive lines that are only HTML comment tags
    tag_lines = []
    for i in range(yaml_end + 1, min(yaml_end + 20, len(lines))):
        stripped = lines[i].strip()
        if stripped in BUNCH_TAGS:
            tag_lines.append(i)
        elif stripped == '':
            continue  # skip empty lines
        elif stripped.startswith('<!-- Breadcrumb'):
            break  # reached breadcrumb
        else:
            break  # hit non-tag content

    if len(tag_lines) >= 3:
        # Found bunched tags - find the extent of the block
        start = tag_lines[0]
        # Look back for the empty line before the first tag
        if start > yaml_end + 1 and lines[start - 1].strip() == '':
            start = start - 1
        # Look forward for the empty line after the last tag
        end = tag_lines[-1]
        if end + 1 < len(lines) and lines[end + 1].strip() == '':
            end = end + 1
        return True, start, end

    return False, -1, -1


def fix_file(filepath):
    """Fix the bunched-tags bug in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    has_bug, start, end = has_bunched_tags(lines)

    if not has_bug:
        return content, False

    # Remove the bunched-tags block
    new_lines = lines[:start] + lines[end + 1:]
    new_content = '\n'.join(new_lines)

    return new_content, True


def main():
    parser = argparse.ArgumentParser(description='Fix bunched-tags bug')
    parser.add_argument('--apply', action='store_true', help='Apply fixes')
    args = parser.parse_args()

    files = find_md_files(DIRS)
    print(f"Scanning {len(files)} files...")

    total_fixed = 0

    for fp in files:
        rel_path = os.path.relpath(fp, ROOT)
        fixed_content, was_fixed = fix_file(fp)

        if was_fixed:
            total_fixed += 1
            print(f"  FIXED: {rel_path}")

            if args.apply:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Files scanned: {len(files)}")
    print(f"Files with bunched-tags bug: {total_fixed}")
    if not args.apply:
        print(f"\nRun with --apply to apply fixes")


if __name__ == '__main__':
    main()
