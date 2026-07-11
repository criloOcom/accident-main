#!/usr/bin/env python3
"""
Génère des README.md dans les dossiers qui n'en ont pas encore.

Parcourt l'arborescence, identifie les dossiers sans README.md,
liste les fichiers .md présents, lit leurs YAML (title + description),
et génère un README.md avec liste à puces.

Usage:
    python3 .dev/app/generate_readmes.py                  # génère tout
    python3 .dev/app/generate_readmes.py --dry-run        # preview
    python3 .dev/app/generate_readmes.py --path "📜 Lois"  # cible
"""

from __future__ import annotations
import os
import sys
import re
import argparse
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(PROJECT_ROOT, ".dev", "app"))
import yaml as pyyaml

EXCLUDE_DIRS = {".venv", ".git", "node_modules", "__pycache__",
                ".pytest_cache", ".opencode", ".obsidian"}


def generate_breadcrumb_for_readme(dir_path: str) -> str:
    """Build HTML-comment breadcrumb for a README at dir_path."""
    full = Path(dir_path)
    root = Path(PROJECT_ROOT)
    try:
        rel = full.relative_to(root)
    except ValueError:
        return ""
    parts = list(rel.parts)
    breadcrumbs = ["[🏠](../README.md)"]
    for i, p in enumerate(parts):
        depth = len(parts) - i
        link = ("../" * depth + "README.md") if depth > 0 else "README.md"
        breadcrumbs.append(f"📁 [ {p} ]({link})")
    breadcrumbs.append("📄 [ README.md ](README.md)")
    return "<!-- " + " > ".join(breadcrumbs) + " -->"


def read_yaml_from_file(filepath: str) -> dict:
    """Extract YAML front matter from a .md file (skip breadcrumb on line 1)."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return {}
    # Skip first line if it's a breadcrumb comment
    first_nl = content.find("\n")
    first = content[:first_nl] if first_nl >= 0 else content
    rest = content[first_nl + 1:] if first.strip().startswith("<!--") else content
    # Skip leading empty lines
    rest = rest.lstrip("\n")
    m = re.match(r'^---\s*\n(.*?)\n---', rest, re.DOTALL)
    if not m:
        return {}
    try:
        return pyyaml.safe_load(m.group(1)) or {}
    except Exception:
        return {}


def parent_readme_link(dir_path: str) -> str:
    """Generate a relative link to parent README."""
    parent = os.path.dirname(dir_path.rstrip("/"))
    if parent == PROJECT_ROOT:
        return "[🏠](../README.md)"
    parent_name = os.path.basename(parent)
    return f"[📁 {parent_name}](../README.md)"


def collect_missing_dirs() -> list[str]:
    """Find all directories that lack a README.md."""
    missing: list[str] = []
    for root_dir, dirnames, _ in os.walk(PROJECT_ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        if root_dir == PROJECT_ROOT:
            continue  # root already has README
        readme_path = os.path.join(root_dir, "README.md")
        if not os.path.exists(readme_path):
            # Only care about dirs with .md files
            has_md = any(
                f.endswith(".md") for f in os.listdir(root_dir)
                if os.path.isfile(os.path.join(root_dir, f))
            )
            if has_md:
                missing.append(root_dir)
    return sorted(missing)


def generate_readme_for_dir(dir_path: str) -> str | None:
    """Generate README content for a directory. Returns None if empty."""
    entries: list[tuple[str, str, str]] = []  # (filename, title, description)
    for fn in sorted(os.listdir(dir_path)):
        if fn.endswith(".md") and fn != "README.md":
            fp = os.path.join(dir_path, fn)
            yaml_data = read_yaml_from_file(fp)
            title = yaml_data.get("title") or os.path.splitext(fn)[0]
            desc = yaml_data.get("description") or ""
            entries.append((fn, str(title), str(desc)))

    if not entries:
        return None

    breadcrumb = generate_breadcrumb_for_readme(os.path.join(PROJECT_ROOT, dir_path))
    dir_name = os.path.basename(dir_path)

    lines = [breadcrumb, "", f"# 📁 {dir_name}", "",]

    # Link to parent
    parent = os.path.dirname(dir_path.rstrip("/"))
    if parent != PROJECT_ROOT:
        parent_name = os.path.basename(parent)
        lines.append(f"🔙 [📁 {parent_name}](../README.md)")
        lines.append("")

    lines.append("## 📄 Contenu")
    lines.append("")

    for fn, title, desc in entries:
        safe_fn = fn.replace(" ", "%20").replace("(", "%28").replace(")", "%29")
        if desc:
            lines.append(f"- **[{title}]({safe_fn})** — {desc}")
        else:
            lines.append(f"- **[{title}]({safe_fn})**")

    lines.append("")
    lines.append("---")
    lines.append(
        f"*README généré automatiquement le 11 juillet 2026*"
    )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--path", type=str, default=None)
    args = parser.parse_args()

    if args.path:
        target = os.path.join(PROJECT_ROOT, args.path)
        if not os.path.isdir(target):
            print(f"❌ Target not found: {target}")
            sys.exit(1)
        missing = [target]
    else:
        missing = collect_missing_dirs()

    created = 0
    skipped = 0

    for d in missing:
        content = generate_readme_for_dir(d)
        if content is None:
            skipped += 1
            print(f"  ⚠️  {os.path.relpath(d, PROJECT_ROOT)} — aucun fichier .md")
            continue

        readme_path = os.path.join(d, "README.md")
        print(f"  {'🆕' if not args.dry_run else '🔍'} "
              f"{os.path.relpath(d, PROJECT_ROOT)}")
        if not args.dry_run:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            created += 1

    print(f"\n✅ {created} README créés, {skipped} ignorés")


if __name__ == "__main__":
    main()
