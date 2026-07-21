#!/usr/bin/env python3
"""
Normalise les listes à puces Markdown en format "loose" :
  - item 1

  - item 2

  - item 3

Conformément à la règle CONVENTIONS.md :
  "Item à puce '- ...' → item à puce suivant '- ...' DOIT être séparé par une ligne vide."

Respecte :
  - Sous-listes indentées (même profondeur → loose, profondeur différente → tight)
  - Blocs de code (ignorés)
  - Commentaires HTML (ignorés)
  - Listes de tâches `- [ ]` / `- [x]`
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

BULLET_RE = re.compile(r'^(\s*)([-*]|\d+\.)\s')
TASK_RE = re.compile(r'^(\s*)[-*]\s+\[[ x]\]\s')

EXCLUDE_PREFIXES = {
    '.dev/jules_night_2026-07-14',
    '.dev/jules_coherence_2026-07-15',
    '.dev/jules_recommandations',
    '.git',
}

INSIDE_BLOCK_MARKERS = {
    '```': 'code_fence',
    '~~~': 'code_fence_tilde',
    '<!--': 'html_comment',
    '--!>': 'html_comment_end',
}


def normalize_file(filepath, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    result = []
    in_code_fence = False
    in_html_comment = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # --- Track code fences and HTML comments ---
        if stripped.startswith('```') or stripped.startswith('~~~'):
            in_code_fence = not in_code_fence

        if stripped.startswith('<!--'):
            in_html_comment = True
        if in_html_comment:
            if stripped.startswith('-->') or stripped.endswith('-->'):
                in_html_comment = False
            result.append(line)
            continue
        # --- end track ---

        result.append(line)

        if in_code_fence:
            continue

        # Check if we need to insert a blank line after this line
        if i + 1 < len(lines):
            nxt = lines[i + 1]
            nxt_stripped = nxt.strip()
            curr = line

            # Both current and next line must be bullets at same indent
            curr_match = BULLET_RE.match(curr) or TASK_RE.match(curr)
            nxt_match = BULLET_RE.match(nxt_stripped) or TASK_RE.match(nxt_stripped)

            if curr_match and nxt_match:
                curr_indent = len(curr_match.group(1))
                nxt_indent = len(nxt_match.group(1))

                if curr_indent == nxt_indent:
                    # Only insert if next line is not already blank or empty
                    # and neither is an HTML comment boundary
                    if nxt_stripped and curr.strip():
                        result.append('\n')
                        modified = True

    if modified:
        if dry_run:
            print(f"  ⚡ {filepath.relative_to(REPO)}")
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(result)
            print(f"  ✅ {filepath.relative_to(REPO)}")
    return modified


def check_file(filepath):
    """Check if a file has tight lists. Returns True if tight lists found."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_code_fence = False
    in_html_comment = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith('```') or stripped.startswith('~~~'):
            in_code_fence = not in_code_fence

        if stripped.startswith('<!--'):
            in_html_comment = True
        if in_html_comment:
            if stripped.startswith('-->') or stripped.endswith('-->'):
                in_html_comment = False
            continue

        if in_code_fence:
            continue

        if i + 1 < len(lines):
            nxt = lines[i + 1]
            nxt_stripped = nxt.strip()
            curr = line

            curr_match = BULLET_RE.match(curr) or TASK_RE.match(curr)
            nxt_match = BULLET_RE.match(nxt_stripped) or TASK_RE.match(nxt_stripped)

            if curr_match and nxt_match:
                curr_indent = len(curr_match.group(1))
                nxt_indent = len(nxt_match.group(1))

                if curr_indent == nxt_indent:
                    if nxt_stripped and curr.strip():
                        # Found tight list — no blank line between consecutive bullets
                        return True
    return False


def main():
    if '--check' in sys.argv:
        # Check mode for pre-commit hook
        files_arg = None
        if '--files' in sys.argv:
            idx = sys.argv.index('--files')
            if idx + 1 < len(sys.argv):
                files_arg = sys.argv[idx + 1].split()

        if files_arg:
            targets = [Path(f) for f in files_arg]
        else:
            targets = [REPO]
            if targets == [REPO]:
                targets = sorted(REPO.rglob('*.md'))
                # Apply exclusions
                filtered = []
                for f in targets:
                    rel = str(f.relative_to(REPO))
                    skip = any(rel.startswith(p) for p in EXCLUDE_PREFIXES)
                    if not skip:
                        filtered.append(f)
                targets = filtered

        found_tight = []
        for filepath in targets:
            rel = str(filepath.relative_to(REPO))
            skip = any(rel.startswith(p) for p in EXCLUDE_PREFIXES)
            if skip:
                continue
            if check_file(filepath):
                found_tight.append(filepath)

        if found_tight:
            print(f"❌ {len(found_tight)} fichier(s) avec listes tight (formatage invalide) :")
            for f in found_tight:
                print(f"     📄 {f.relative_to(REPO)}")
            print("   CORRIGER avec : .dev/app/normalize_list_spacing.py --apply")
            return 1
        else:
            print("✅ Toutes les listes à puces sont en format loose.")
            return 0

    dry_run = '--apply' not in sys.argv

    mode_str = "DRY-RUN" if dry_run else "APPLICATION"
    print(f"\n{'='*60}")
    print(f"  NORMALISATION LISTES À PUCES (format loose) — mode {mode_str}")
    print(f"{'='*60}\n")

    all_files = sorted(REPO.rglob('*.md'))
    files_modified = 0
    files_total = 0
    files_skipped = 0

    for filepath in all_files:
        rel = str(filepath.relative_to(REPO))
        skip = False
        for prefix in EXCLUDE_PREFIXES:
            if rel.startswith(prefix):
                skip = True
                break
        if skip:
            files_skipped += 1
            continue

        files_total += 1
        if normalize_file(filepath, dry_run):
            files_modified += 1

    print(f"\n{'='*60}")
    print(f"  BILAN : {files_modified}/{files_total} fichiers modifiés "
          f"({files_skipped} exclus)")
    if dry_run:
        print(f"  => Relancer avec --apply pour appliquer")
    print(f"{'='*60}\n")

    return 0


if __name__ == '__main__':
    main()
