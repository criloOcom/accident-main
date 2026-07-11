#!/usr/bin/env python3
"""
Injecte ou normalise le front matter YAML dans tous les fichiers .md
du projet accident-main.

Insère YAML en ligne 1 (devant le fil d'Ariane), avant le contenu.
Préserve le fil d'Ariane (<!-- [🏠] ... -->) quel que soit son emplacement.
Ordre canonique : YAML (ligne 1) → breadcrumb → contenu (pour prévisualisation GitHub).
Normalise les champs existants (titre → title, categorie → tags, etc.)
Ajoute un description automatique si absent.

Usage:
    python3 .dev/app/inject_yaml_frontmatter.py              # run
    python3 .dev/app/inject_yaml_frontmatter.py --dry-run    # preview
    python3 .dev/app/inject_yaml_frontmatter.py --path "📜 Lois/📒 Code civil"  # cible
"""

from __future__ import annotations
import os
import sys
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))  # accident-main/
sys.path.insert(0, SCRIPT_DIR)

from yaml_schema import update_yaml_header  # noqa: E402


def collect_md_files(root_dir: str) -> list[str]:
    """Collect all .md files (excluding .venv, .git, node_modules)."""
    files: list[str] = []
    exclude_dirs = {".venv", ".git", "node_modules", "__pycache__",
                    ".pytest_cache", ".opencode"}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Prune excluded dirs
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for fn in filenames:
            if fn.endswith(".md"):
                files.append(os.path.join(dirpath, fn))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description="Inject YAML frontmatter into .md files")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no changes")
    parser.add_argument("--path", type=str, default=None,
                        help="Target subpath (e.g. '📜 Lois/📒 Code civil')")
    args = parser.parse_args()

    root = PROJECT_ROOT
    if args.path:
        target = os.path.join(root, args.path)
        if not os.path.isdir(target):
            print(f"❌ Target not found: {target}")
            sys.exit(1)
        all_files = collect_md_files(target)
    else:
        all_files = collect_md_files(root)

    total = len(all_files)
    updated = 0
    skipped = 0
    errors = 0

    print(f"📄 {total} fichiers .md trouvés")
    if args.dry_run:
        print("🔍 DRY RUN — aucun fichier ne sera modifié\n")
    else:
        print("⚙️  Injection YAML en cours...\n")

    for fpath in all_files:
        try:
            result = update_yaml_header(fpath, dry_run=args.dry_run)
            rel = os.path.relpath(fpath, root)
            if result is None:
                skipped += 1
                if args.dry_run:
                    print(f"  • {rel} (OK)")
            else:
                updated += 1
                if args.dry_run:
                    print(f"  🔄 {rel}")
        except Exception as e:
            errors += 1
            print(f"  ❌ {os.path.relpath(fpath, root)} — {e}")

    print(f"\n{'🔍 DRY RUN' if args.dry_run else '✅ Terminé'}"
          f" — {updated} modifiés, {skipped} inchangés, {errors} erreurs")


if __name__ == "__main__":
    main()
