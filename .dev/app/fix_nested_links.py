#!/usr/bin/env python3
"""
fix_nested_links.py  —  Corrige les liens markdown imbriqués invalides.

Pattern détecté :  [[**[Token Name]**](TOKEN_MAP.md#anchor)](token-file.md)
Pattern cible  :  **[Token Name](token-file.md)**

Usage:
    python3 .dev/app/fix_nested_links.py [--dry-run] [--apply]
"""

import re
import sys
from pathlib import Path

BASE = Path("/home/crilocom/accident-main")

# Regex pour détecter [[**[Token]**](TOKEN_MAP.md#anchor)](token-file.md)
# Groupe 1: Token Name (ex: "La Victime")
# Groupe 2: TOKEN MAP URL (ex: "%F0%9F%A7%A0%20Memory/TOKEN%20MAP.md#personnes-physiques")
# Groupe 3: Token file URL (ex: "../../../../%F0%9F%A7%A0%20Memory/%F0%9F%97%82%EF%B8%8F%20Tokens/token-victime-nom.md")
NESTED_PATTERN = re.compile(
    r'\[\[\*\*\[([^\]]+)\]\*\*\]\(([^)]+)\)\]\(([^)]+)\)'
)


def fix_content(content: str) -> tuple[str, int]:
    """Replace nested markdown links with valid side-by-side links."""
    def replacement(m: re.Match) -> str:
        token_name = m.group(1)
        map_url = m.group(2)
        token_url = m.group(3)
        return f'**[{token_name}]({token_url})**'

    new_content, count = NESTED_PATTERN.subn(replacement, content)
    return new_content, count


def process_file(filepath: Path, dry_run: bool) -> int:
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [SKIP] Cannot read {filepath}: {e}")
        return 0

    new_content, count = fix_content(content)
    if count == 0:
        return 0

    if dry_run:
        rel = filepath.relative_to(BASE)
        print(f"  [DRY] {rel}: {count} remplacement(s)")
    else:
        filepath.write_text(new_content, encoding="utf-8")
        rel = filepath.relative_to(BASE)
        print(f"  [FIX] {rel}: {count} remplacement(s)")

    return count


def main():
    dry_run = "--apply" not in sys.argv

    mode = "DRY RUN" if dry_run else "APPLICATION"
    print(f"\n{'='*70}")
    print(f"  Correction liens imbriqués — MODE {mode}")
    print(f"{'='*70}\n")

    total_fixes = 0
    total_files = 0

    # Scan tout le dépôt (Token + Reel) en excluant .git, Archives, node_modules
    for md_file in sorted(BASE.rglob("*.md")):
        parts = md_file.relative_to(BASE).parts
        # Skip hidden dirs, Archives, node_modules
        if any(p.startswith('.') for p in parts):
            continue
        if "🗄️ Archives" in parts:
            continue
        if "node_modules" in parts:
            continue
        if md_file.name == "README.md":
            continue

        count = process_file(md_file, dry_run)
        if count > 0:
            total_fixes += count
            total_files += 1

    print(f"\n{'='*70}")
    if dry_run:
        print(f"  DRY RUN: {total_files} fichiers, {total_fixes} occurrences à corriger")
        print(f"  → Relancer avec --apply pour appliquer")
    else:
        print(f"  ✅ {total_files} fichiers corrigés, {total_fixes} remplacements")
    print(f"{'='*70}\n")

    return 0 if total_fixes == 0 else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
