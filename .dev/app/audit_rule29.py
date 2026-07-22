#!/usr/bin/env python3
"""
Audit Rule #29 compliance in .md files.

Rule #29 requires:
1. <!-- Auteur --> / <!-- /Auteur --> around the auteur block
2. <!-- Destinataire --> / <!-- /Destinataire --> around the destinataire block
3. <!-- PJ --> / <!-- /PJ --> around the Pièces Jointes section
4. <!-- Source --> / <!-- /Source --> around the Sources Législation section
5. --- (horizontal rules) before and after the Objet block

Usage:
    python3 audit_rule29.py                    # dry-run (audit only)
    python3 audit_rule29.py --apply            # apply fixes
    python3 audit_rule29.py --apply --token    # Token only
    python3 audit_rule29.py --apply --reel     # Reel only
"""

import os
import re
import sys
import argparse

ROOT = '/home/crilocom/accident-main'

DIRS = {
    'token': [
        'Actes/Token/Courriers',
        'Actes/Token/Actes_proceduraux',
    ],
    'reel': [
        'Actes/Reel/Courriers',
        'Actes/Reel/Actes_proceduraux',
    ],
}

# Tags that Rule #29 requires paired opening/closing
REQUIRED_TAGS = [
    ('<!-- Auteur -->', '<!-- /Auteur -->'),
    ('<!-- Destinataire -->', '<!-- /Destinataire -->'),
    ('<!-- PJ -->', '<!-- /PJ -->'),
    ('<!-- Source -->', '<!-- /Source -->'),
]


def find_md_files(dirs):
    """Find all .md files (excluding README.md) in given directories."""
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


def audit_file(filepath):
    """Audit a single file for Rule #29 compliance. Returns list of issues."""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        issues.append(f"  ERROR reading: {e}")
        return issues

    # Check paired tags
    for open_tag, close_tag in REQUIRED_TAGS:
        opens = [i for i, line in enumerate(lines) if open_tag in line]
        closes = [i for i, line in enumerate(lines) if close_tag in line]

        if opens and not closes:
            issues.append(f"  MISSING closing tag: {close_tag} (found {len(opens)} opening)")
        elif closes and not opens:
            issues.append(f"  ORPHAN closing tag: {close_tag} (no opening found)")
        elif len(opens) > 1:
            issues.append(f"  DUPLICATE opening tag: {open_tag} ({len(opens)} found)")
        elif len(closes) > 1:
            issues.append(f"  DUPLICATE closing tag: {close_tag} ({len(closes)} found)")
        elif opens and closes and opens[0] > closes[0]:
            issues.append(f"  REVERSED: {close_tag} (line {closes[0]+1}) appears before {open_tag} (line {opens[0]+1})")

    # Check --- around Objet block
    # Find the Objet line (after YAML, after breadcrumb)
    objet_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('**Objet') or stripped.startswith('Objet :'):
            objet_lines.append(i)

    if not objet_lines:
        # No Objet found - check if this is a procedural document that needs one
        pass  # Some documents (notes, memorandums) don't have Objet blocks
    else:
        for objet_line_idx in objet_lines:
            # Check for --- before Objet
            has_hr_before = False
            for j in range(max(0, objet_line_idx - 3), objet_line_idx):
                if lines[j].strip() == '---':
                    has_hr_before = True
                    break

            # Check for --- after Objet (typically after LRAR line or next blank line)
            has_hr_after = False
            for j in range(objet_line_idx + 1, min(len(lines), objet_line_idx + 5)):
                if lines[j].strip() == '---':
                    has_hr_after = True
                    break

            if not has_hr_before:
                issues.append(f"  MISSING --- before Objet (line {objet_line_idx + 1})")
            if not has_hr_after:
                issues.append(f"  MISSING --- after Objet (line {objet_line_idx + 1})")

    return issues


def fix_file(filepath):
    """Fix Rule #29 violations in a file. Returns (fixed_content, changes_made)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    changes_made = []
    modified = False

    # Find the end of YAML front matter
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
        return content, changes_made

    # Find the end of breadcrumb section
    breadcrumb_end = yaml_end
    for i in range(yaml_end + 1, min(yaml_end + 10, len(lines))):
        if '<!-- /Breadcrumb -->' in lines[i]:
            breadcrumb_end = i
            break

    # Work on the content after breadcrumb
    search_start = breadcrumb_end + 1

    # Find Auteur block (look for pattern: name, address, email)
    # Typically: <!-- Auteur --> should be placed around the sender block
    # The sender block is usually right after the breadcrumb/title

    # Find where the sender address block is
    # It's typically after the first <hr><hr> and contains victim's info
    auteur_open_found = any('<!-- Auteur -->' in l for l in lines)
    destinataire_open_found = any('<!-- Destinataire -->' in l for l in lines)

    # Check if we need to add missing tags
    for open_tag, close_tag in REQUIRED_TAGS:
        opens = [i for i, line in enumerate(lines) if open_tag in line]
        closes = [i for i, line in enumerate(lines) if close_tag in line]

        if opens and not closes:
            # Find the appropriate closing position
            open_idx = opens[0]
            # For Auteur/Destinataire, the block ends at the next blank line or next section
            # For PJ, it ends at the end of the list
            # For Source, it ends at the end of the footnotes

            if open_tag == '<!-- Auteur -->':
                # Find the end of the auteur block (next blank line after address)
                close_idx = open_idx + 1
                for j in range(open_idx + 1, min(open_idx + 10, len(lines))):
                    if lines[j].strip() == '' and j + 1 < len(lines) and lines[j + 1].strip() == '':
                        close_idx = j
                        break
                    elif lines[j].strip().startswith('<!-- ') and 'Auteur' not in lines[j]:
                        close_idx = j
                        break
                lines.insert(close_idx, close_tag)
                changes_made.append(f"Added <!-- /Auteur --> at line {close_idx + 1}")
                modified = True

            elif open_tag == '<!-- Destinataire -->':
                close_idx = open_idx + 1
                for j in range(open_idx + 1, min(open_idx + 10, len(lines))):
                    if lines[j].strip() == '' and j + 1 < len(lines) and lines[j + 1].strip() == '':
                        close_idx = j
                        break
                    elif lines[j].strip().startswith('<!-- ') and 'Destinataire' not in lines[j]:
                        close_idx = j
                        break
                lines.insert(close_idx, close_tag)
                changes_made.append(f"Added <!-- /Destinataire --> at line {close_idx + 1}")
                modified = True

            elif open_tag == '<!-- PJ -->':
                # PJ block ends at the next <!-- or next ## or end of list
                close_idx = len(lines)
                for j in range(open_idx + 1, len(lines)):
                    if lines[j].strip().startswith('## ') or lines[j].strip().startswith('<!-- Source'):
                        close_idx = j
                        break
                    elif lines[j].strip().startswith('<!-- /'):
                        close_idx = j
                        break
                lines.insert(close_idx, close_tag)
                changes_made.append(f"Added <!-- /PJ --> at line {close_idx + 1}")
                modified = True

            elif open_tag == '<!-- Source -->':
                close_idx = len(lines)
                for j in range(open_idx + 1, len(lines)):
                    if lines[j].strip().startswith('## ') or lines[j].strip() == '':
                        # Check if next non-empty line is not a footnote
                        next_content = ''
                        for k in range(j + 1, min(j + 3, len(lines))):
                            if lines[k].strip():
                                next_content = lines[k].strip()
                                break
                        if not next_content.startswith('[^'):
                            close_idx = j
                            break
                lines.insert(close_idx, close_tag)
                changes_made.append(f"Added <!-- /Source --> at line {close_idx + 1}")
                modified = True

    # Check for --- around Objet
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('**Objet') or stripped.startswith('Objet :'):
            # Check before
            has_hr_before = False
            for j in range(max(0, i - 3), i):
                if lines[j].strip() == '---':
                    has_hr_before = True
                    break
            if not has_hr_before:
                lines.insert(i, '---')
                changes_made.append(f"Added --- before Objet at line {i + 1}")
                modified = True
                i += 1  # Adjust index

            # Check after (look for LRAR line or next content)
            has_hr_after = False
            for j in range(i + 1, min(len(lines), i + 5)):
                if lines[j].strip() == '---':
                    has_hr_after = True
                    break
            if not has_hr_after:
                # Find the end of the Objet/LRAR block
                insert_after = i + 1
                for j in range(i + 1, min(len(lines), i + 5)):
                    if lines[j].strip().startswith('**N°') or lines[j].strip().startswith('**Nº'):
                        insert_after = j + 1
                        break
                    elif lines[j].strip() == '':
                        insert_after = j
                        break
                lines.insert(insert_after, '---')
                changes_made.append(f"Added --- after Objet at line {insert_after + 1}")
                modified = True

    if modified:
        content = '\n'.join(lines)

    return content, changes_made


def main():
    parser = argparse.ArgumentParser(description='Audit Rule #29 compliance')
    parser.add_argument('--apply', action='store_true', help='Apply fixes')
    parser.add_argument('--token', action='store_true', help='Token directories only')
    parser.add_argument('--reel', action='store_true', help='Reel directories only')
    args = parser.parse_args()

    # Determine which directories to scan
    scan_dirs = []
    if args.token:
        scan_dirs = DIRS['token']
    elif args.reel:
        scan_dirs = DIRS['reel']
    else:
        scan_dirs = DIRS['token'] + DIRS['reel']

    files = find_md_files(scan_dirs)
    print(f"Scanning {len(files)} files...")

    total_issues = 0
    files_with_issues = 0
    files_fixed = 0

    for fp in files:
        rel_path = os.path.relpath(fp, ROOT)
        issues = audit_file(fp)

        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"\n{rel_path}:")
            for issue in issues:
                print(f"  {issue}")

            if args.apply:
                fixed_content, changes = fix_file(fp)
                if changes:
                    with open(fp, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    files_fixed += 1
                    print(f"  FIXED: {len(changes)} changes")
                    for change in changes:
                        print(f"    - {change}")

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Files scanned: {len(files)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Total issues: {total_issues}")
    if args.apply:
        print(f"Files fixed: {files_fixed}")
    else:
        print(f"\nRun with --apply to fix issues")


if __name__ == '__main__':
    main()
