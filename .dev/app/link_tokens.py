#!/usr/bin/env python3
"""
Link all unlinked **[Token]** occurrences in Actes/Token/ files
to their corresponding definition files in Memory/Tokens/.

Usage: python3 .dev/app/link_tokens.py
       python3 .dev/app/link_tokens.py --apply  (write changes — default dry-run)
"""

import os
import re
import sys
import argparse
import urllib.parse

REPO = "/home/crilocom/accident-main"
TOKEN_MAP_FILE = os.path.join(REPO, "Memory/TOKEN MAP.md")
TOKENS_DIR = os.path.join(REPO, "Memory/Tokens")
TARGET_DIR = os.path.join(REPO, "Actes/Token")


def extract_map():
    """Parse TOKEN MAP.md to build display_name → filename mapping."""
    mapping = {}
    with open(TOKEN_MAP_FILE) as f:
        content = f.read()

    # Pattern: [**[Display Name]**](path/token-filename.md)
    pattern = re.compile(r'\[(\*\*\[([^\]]+)\]\*\*)\]\([^)]*?([^/)]+\.md)\)')
    for match in pattern.finditer(content):
        full_bold = match.group(1)  # **[Display Name]**
        display = match.group(2)     # Display Name
        token_file = match.group(3)  # token-xxx.md
        mapping[display] = (full_bold, token_file)

    # Also handle the token section where value is display name without link
    # Check token files directly for display names from YAML or content
    return mapping


def extract_from_token_files():
    """Extract potential display names from token files."""
    # Token filenames -> display name heuristics
    mapping = {}
    for fname in os.listdir(TOKENS_DIR):
        if not fname.endswith('.md') or fname == 'README.md':
            continue
        fpath = os.path.join(TOKENS_DIR, fname)
        with open(fpath) as f:
            content = f.read()
        # Try to find the display name from the first H1
        for line in content.split('\n'):
            if line.startswith('# ') or line.startswith('#  '):
                # title might be the display name
                pass
        # Try YAML title
        yaml_match = re.search(r'^title:\s*"(.+)"', content, re.MULTILINE)
        if yaml_match:
            mapping[fname] = yaml_match.group(1)
    return mapping


def build_synonyms(mapping):
    """Build accent-insensitive and common variant synonyms."""
    synonyms = {}
    for display, (full_bold, token_file) in mapping.items():
        # Accent-insensitive version
        no_accent = (display
            .replace('é', 'e').replace('è', 'e').replace('ê', 'e')
            .replace('à', 'a').replace('â', 'a')
            .replace('ù', 'u').replace('û', 'u')
            .replace('ô', 'o')
            .replace('ï', 'i').replace('î', 'i')
            .replace('ç', 'c')
            .replace('É', 'E').replace('È', 'E').replace('Ê', 'E')
            .replace('À', 'A').replace('Â', 'A')
            .replace('Ù', 'U').replace('Û', 'U')
            .replace('Ô', 'O')
            .replace('Ï', 'I').replace('Î', 'I')
            .replace('Ç', 'C'))
        if no_accent != display:
            synonyms[no_accent] = (full_bold, token_file)
    return synonyms


def get_relative_path(file_path):
    """Calculate relative path from Token file to Memory/Tokens/."""
    file_dir = os.path.dirname(file_path)
    # Calculate depth
    rel = os.path.relpath(file_dir, TARGET_DIR)
    depth = len(rel.split(os.sep))
    # From the file location, go up to repo root, then down to Tokens
    # file_path is under TARGET_DIR
    # Count levels from file to repo root
    # E.g., Actes/Token/Actes_proceduraux/Contentieux_penal/file.md
    # → depth = 4 levels from TARGET_DIR
    # → ../../../../ to root → then Memory/Tokens/
    ups = os.path.relpath(TOKENS_DIR, file_dir)
    # Encode each component for URL
    parts = ups.split(os.sep)
    encoded = '/'.join(urllib.parse.quote(p, safe='') for p in parts)
    return encoded


def token_pattern_from_map(mapping, synonyms):
    """Build patterns and replacements for all known tokens."""
    replacements = []
    all_displays = list(mapping.keys()) + list(synonyms.keys())
    # Sort by length descending to match longer tokens first
    all_displays.sort(key=len, reverse=True)

    return all_displays, mapping, synonyms


def _split_yaml(content):
    m = re.match(r'^---\n.*?\n---\n', content, re.DOTALL)
    if m:
        return m.group(0), content[m.end():]
    return '', content


def scan_file(fpath, all_displays, mapping, synonyms, apply=False, dry_run=True):
    """Scan a single file and link unlinked tokens."""
    with open(fpath) as f:
        content = f.read()

    frontmatter, body = _split_yaml(content)
    content = body
    rel_path = get_relative_path(fpath)

    changes = 0
    skipped_not_in_map = []
    skipped_already_linked = []
    skipped_placeholder = []

    # First find all `**[...]**` that are already inside a markdown link
    # Pattern: [...](...) where ... is any content including **[token]**
    linked_spans = set()
    # A full markdown link: [...](...)
    link_pattern = re.compile(r'\[(?:[^\]]*?\*\*\[[^\]]*\]\*\*[^\]]*?|[^\]]*?)\]\([^)]*\)')
    for link in link_pattern.finditer(content):
        linked_spans.add((link.start(), link.end()))
    
    # Also check for the inverted format: **[text](url)**  — link INSIDE bold
    inverted_pattern = re.compile(r'\*\*\[([^\]]*?)\]\([^)]*\)\*\*')
    for link in inverted_pattern.finditer(content):
        linked_spans.add((link.start(), link.end()))

    def is_linked(pos, length):
        """Check if a span [pos, pos+length) overlaps with any linked span."""
        for start, end in linked_spans:
            if pos >= start and pos + length <= end:
                return True
        return False

    # Now find all raw `**[Token]**` occurrences
    # But careful: we need EXACT matches to the display names
    # Use regex to find `**[...]**` then check if content matches a known display

    # Build a pattern that matches **[...]** for known display names
    # Sort displays by length (desc) for greedy matching
    escaped_displays = [re.escape(d) for d in all_displays]

    # We process character by character to avoid overlapping issues
    # Find all **[...]** patterns
    raw_pattern = re.compile(r'\*\*\[([^\]]+)\]\*\*')

    modified = content
    offset = 0

    # Work in reverse order to preserve indices
    replacements_list = []

    for match in raw_pattern.finditer(content):
        display_text = match.group(1)
        start = match.start()
        end = match.end()

        # Check if already inside a link
        if is_linked(start, end - start):
            skipped_already_linked.append(display_text)
            continue

        # Check if this is a placeholder
        if display_text.startswith('À compléter') or display_text == ' ... ' or display_text == '…' or display_text == '...':
            skipped_placeholder.append(display_text)
            continue

        # Check if it's something like [N° [Dossier CPAM](path)] — nested
        if ']' in display_text or '[' in display_text:
            skipped_not_in_map.append(display_text)
            continue

        # Try exact match first
        token_file = None
        if display_text in mapping:
            _, token_file = mapping[display_text]
        elif display_text in synonyms:
            _, token_file = synonyms[display_text]

        if not token_file:
            skipped_not_in_map.append(display_text)
            continue

        # Build replacement
        link_target = rel_path.rstrip('/') + '/' + urllib.parse.quote(token_file, safe='')
        replacement = f'**[{display_text}]({link_target})**'

        replacements_list.append((start, end, replacement))

    # Apply replacements in reverse order
    for start, end, replacement in reversed(replacements_list):
        modified = modified[:start] + replacement + modified[end:]
        changes += 1

    if changes > 0:
        print(f"  {os.path.relpath(fpath, REPO)}: {changes} tokens linked")
        if apply:
            restored = frontmatter + modified
            with open(fpath, 'w') as f:
                f.write(restored)
    else:
        print(f"  {os.path.relpath(fpath, REPO)}: 0 changes")

    if skipped_not_in_map:
        print(f"    ⚠ Skipped (not in TOKEN MAP): {set(skipped_not_in_map)}")
    if skipped_already_linked:
        pass  # Normal, expected
    if skipped_placeholder:
        pass  # Normal

    return changes


def main():
    parser = argparse.ArgumentParser(description="Link unlinked tokens to their definition files")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    args = parser.parse_args()

    print("📖 Parsing TOKEN MAP...")
    mapping = extract_map()
    synonyms = build_synonyms(mapping)
    all_displays, _, _ = token_pattern_from_map(mapping, synonyms)

    print(f"   → {len(mapping)} tokens in map")
    print(f"   → {len(synonyms)} accent variants")
    print()

    # Scan all files
    total_changes = 0
    file_count = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        if '/.git/' in root or '__pycache__' in root:
            continue
        for fname in files:
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            changes = scan_file(fpath, all_displays, mapping, synonyms,
                                apply=args.apply, dry_run=not args.apply)
            if changes > 0:
                total_changes += changes
                file_count += 1

    mode = "APPLIED" if args.apply else "DRY-RUN"
    print(f"\n{'='*60}")
    print(f"📊 {mode}: {file_count} files, {total_changes} tokens linked")
    if not args.apply:
        print("   Run with --apply to write changes")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
