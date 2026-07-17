#!/usr/bin/env python3
"""
Unify heading numbering across ⚖️ Actes/🔑 Token/ and 📊 Rapports/.

Hierarchical format:
  H2  →  ## I — TITRE         (Roman numerals)
  H3  →  ### I.1 — Titre     (Parent Roman + Arabic)
  H4  →  #### I.1.a — Titre  (Parent Roman + Arabic + letter)

Special sections (PIECES JOINTES, Sources Législation, PAR CES MOTIFS,
BORDEREAU, VISA, EXPOSÉ, MOTIFS, etc.) are excluded and left unchanged.

Usage:
    python3 .dev/app/auto_number_headings.py             # dry-run
    python3 .dev/app/auto_number_headings.py --apply     # apply
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRY_RUN = "--apply" not in sys.argv

# ---------------------------------------------------------------------------
# Targeted directories (only Token acts and Reports; skip Reel/Preuves)
# ---------------------------------------------------------------------------

TARGET_DIRS = [
    ROOT / "⚖️ Actes/🔑 Token",
    ROOT / "📊 Rapports",
]

EXCLUDE_DIR_PARTS = ("🗄️ Archives", "/Archives")

# ---------------------------------------------------------------------------
# Prefix patterns — ONLY match if followed by a clear separator
# ---------------------------------------------------------------------------

# All variants of separator: ". ", " — ", " – ", ". — ", " —", " . — "
SEP = r'(?:[.\s]*[—–.\s]\s+|[.\s]*—[.\s]*|\.\s+)'

H2_ROMAN_RE = re.compile(
    r'^(##)\s+([IVXLCDM]+)' + SEP + r'(.*)$'
)
H2_ARABIC_RE = re.compile(
    r'^(##)\s+(\d+)' + SEP + r'(.*)$'
)

H3_ROMAN_RE = re.compile(
    r'^(###)\s+([IVXLCDM]+)' + SEP + r'(.*)$'
)
H3_ARABIC_RE = re.compile(
    r'^(###)\s+(\d+)' + SEP + r'(.*)$'
)
H3_LETTER_RE = re.compile(
    r'^(###)\s+([A-D])' + SEP + r'(.*)$'
)

H4_ROMAN_RE = re.compile(
    r'^(####)\s+([IVXLCDMivxlcdm]+)' + SEP + r'(.*)$'
)
H4_ARABIC_RE = re.compile(
    r'^(####)\s+(\d+(?:\.\d+)*)' + SEP + r'(.*)$'
)
H4_LETTER_RE = re.compile(
    r'^(####)\s+([a-dA-D])[).]\s+(.*)$'
)

# ---------------------------------------------------------------------------
# Excluded headings (never renumbered)
# ---------------------------------------------------------------------------

EXCLUDED_H2_TITLES = {
    "pièces jointes", "pieces jointes",
    "bordereau des pièces invoquées", "bordereau de pièces annexées",
    "sources législation", "sources legislation",
    "par ces motifs", "note de référence", "sommaire",
}

EXCLUDED_H3_TITLES = {
    "par ces motifs", "note méthodologique", "annexe",
    "visa", "exposé du litige", "exposé succinct", "motifs",
}

def is_excluded_h2(line: str, title: str) -> bool:
    t = title.strip().lower().rstrip(".")
    if not t:
        return False
    if t in EXCLUDED_H2_TITLES:
        return True
    if t.startswith("pièce") or t.startswith("piece"):
        return True
    return False

def is_excluded_h3(line: str, title: str) -> bool:
    t = title.strip().lower().rstrip(".")
    if not t:
        return False
    if t in EXCLUDED_H3_TITLES:
        return True
    if t.startswith("pièce n°") or t.startswith("piece n°"):
        return True
    return False

def is_excluded_h4(line: str, title: str) -> bool:
    return False

# ---------------------------------------------------------------------------
# Roman numeral helpers
# ---------------------------------------------------------------------------

ROMAN_VALUES = [
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (8, "VIII"), (7, "VII"),
    (6, "VI"), (5, "V"), (4, "IV"), (3, "III"), (2, "II"), (1, "I"),
]

def int_to_roman(n: int) -> str:
    result = []
    for value, numeral in ROMAN_VALUES:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)

# ---------------------------------------------------------------------------
# Parse one heading line
# Returns (level, clean_title) or None
# ---------------------------------------------------------------------------

def parse_heading(line: str):
    stripped = line.rstrip()

    # H2
    if stripped.startswith("## ") and not stripped.startswith("### "):
        m = H2_ROMAN_RE.match(stripped)
        if m:
            title = m.group(3).strip()
            # Skip standalone single-letter prefixes like "I" used as labels
            # Only valid if followed by proper content
            return (2, title) if not is_excluded_h2(stripped, title) else None
        m = H2_ARABIC_RE.match(stripped)
        if m:
            title = m.group(3).strip()
            return (2, title) if not is_excluded_h2(stripped, title) else None
        title = stripped[3:].strip()
        if is_excluded_h2(stripped, title):
            return None
        return (2, title)

    # H3
    if stripped.startswith("### ") and not stripped.startswith("#### "):
        m = H3_ROMAN_RE.match(stripped)
        if m:
            title = m.group(3).strip()
            return (3, title) if not is_excluded_h3(stripped, title) else None
        m = H3_ARABIC_RE.match(stripped)
        if m:
            title = m.group(3).strip()
            return (3, title) if not is_excluded_h3(stripped, title) else None
        m = H3_LETTER_RE.match(stripped)
        if m:
            title = m.group(3).strip()
            return (3, title) if not is_excluded_h3(stripped, title) else None
        title = stripped[4:].strip()
        if is_excluded_h3(stripped, title):
            return None
        return (3, title)

    # H4
    if stripped.startswith("#### "):
        m = H4_ROMAN_RE.match(stripped)
        if m:
            title = m.group(3).strip()
            return (4, title) if not is_excluded_h4(stripped, title) else None
        m = H4_ARABIC_RE.match(stripped)
        if m:
            title = m.group(3).strip()
            return (4, title) if not is_excluded_h4(stripped, title) else None
        m = H4_LETTER_RE.match(stripped)
        if m:
            title = m.group(3).strip()
            return (4, title) if not is_excluded_h4(stripped, title) else None
        title = stripped[5:].strip()
        if is_excluded_h4(stripped, title):
            return None
        return (4, title)

    return None

# ---------------------------------------------------------------------------
# Process one file
# ---------------------------------------------------------------------------

def process_file(filepath: Path) -> list:
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [ERROR] {filepath}: {e}")
        return []

    lines = text.split("\n")

    headings = []
    for idx, line in enumerate(lines):
        info = parse_heading(line)
        if info is None:
            continue
        level, title = info
        headings.append((level, idx, title))

    if not headings:
        return []

    h2_counter = 0
    h3_counter = 0
    h4_counter = 0
    changes = []

    for level, idx, title in headings:
        if level == 2:
            h2_counter += 1
            h3_counter = 0
            h4_counter = 0
            roman = int_to_roman(h2_counter)
            new = f"## {roman} — {title}"
            old = lines[idx].rstrip()
            if new != old:
                changes.append((old, new, 2, title))
                if not DRY_RUN:
                    lines[idx] = new

        elif level == 3:
            h3_counter += 1
            h4_counter = 0
            if h2_counter == 0:
                h2_counter = 1
            roman = int_to_roman(h2_counter)
            new = f"### {roman}.{h3_counter} — {title}"
            old = lines[idx].rstrip()
            if new != old:
                changes.append((old, new, 3, title))
                if not DRY_RUN:
                    lines[idx] = new

        elif level == 4:
            h4_counter += 1
            if h2_counter == 0:
                h2_counter = 1
            if h3_counter == 0:
                h3_counter = 1
            roman = int_to_roman(h2_counter)
            letter = chr(96 + h4_counter)
            new = f"#### {roman}.{h3_counter}.{letter} — {title}"
            old = lines[idx].rstrip()
            if new != old:
                changes.append((old, new, 4, title))
                if not DRY_RUN:
                    lines[idx] = new

    if changes and not DRY_RUN:
        filepath.write_text("\n".join(lines), encoding="utf-8")

    return changes

# ---------------------------------------------------------------------------
# Walk targeted files
# ---------------------------------------------------------------------------

def find_md_files() -> list:
    files = []
    for d in TARGET_DIRS:
        if not d.exists():
            print(f"  [WARN] Directory not found: {d}")
            continue
        for root, dirs, fns in os.walk(d):
            root_path = Path(root)
            if any(p in root for p in EXCLUDE_DIR_PARTS):
                continue
            for fn in fns:
                if fn == "README.md" or not fn.endswith(".md"):
                    continue
                files.append(root_path / fn)
    return sorted(files)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    mode = "DRY RUN" if DRY_RUN else "APPLY"
    print(f"\n{'='*70}")
    print(f"  AUTO NUMBER HEADINGS — {mode}")
    print(f"  Directories: {', '.join(str(d.relative_to(ROOT)) for d in TARGET_DIRS)}")
    print(f"{'='*70}\n")

    files = find_md_files()
    print(f"  Found {len(files)} .md files to scan\n")

    by_file = {}
    total_changes = 0
    for fp in files:
        rel = fp.relative_to(ROOT)
        changes = process_file(fp)
        if changes:
            by_file[rel] = changes
            total_changes += len(changes)

    print(f"  {len(by_file)} file(s) with changes ({total_changes} heading(s))\n")

    if not by_file:
        print("  No changes needed.\n")
        return

    for rel in sorted(by_file):
        print(f"  📄 {rel}")
        for old, new, level, title in by_file[rel]:
            print(f"      H{level}: {old}")
            print(f"           → {new}")
        print()

    print(f"  {'DRY RUN' if DRY_RUN else 'APPLIED'} — "
          f"{total_changes} heading(s) in {len(by_file)} file(s)\n")

if __name__ == "__main__":
    main()
