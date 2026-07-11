#!/usr/bin/env python3
"""
Génère des fils d'Ariane dans les fichiers .md.
Format (3 lignes, ligne 1-3) :
<!-- Breadcrumb -->
[🏠](../README.md)
<!-- /Breadcrumb -->
"""

import os
import re
from pathlib import Path

ROOT = "/home/crilocom/accident-main"


def compute_root_link(file_path):
    """Retourne le chemin relatif vers README.md racine."""
    full_path = Path(file_path)
    root = Path(ROOT)
    try:
        relative_path = full_path.relative_to(root)
    except ValueError:
        return None

    parts = list(relative_path.parts)
    depth = len(parts) - 1  # nombre de niveaux de dossiers
    if depth <= 0:
        return "README.md"
    return os.path.join(*([".."] * depth + ["README.md"]))


# Patterns de blocs breadcrumb pour suppression (anciens + nouveau format)
_BREADCRUMB_PATTERNS = [
    # Code block avec breadcrumb
    re.compile(r'```\s*\n.*?🏠\s*\[.*?```', re.DOTALL),
    # Nouveau format : <!-- Breadcrumb --> ... <!-- /Breadcrumb -->
    re.compile(r'<!-- Breadcrumb -->.*?<!-- /Breadcrumb -->', re.DOTALL),
    # Ancien format : <!-- [🏠](...) > ... -->
    re.compile(r'<!--\s*\[?🏠.*?-->', re.DOTALL),
    # Ligne plain text commençant par 🏠 [
    re.compile(r'^🏠\s*\[.*$', re.MULTILINE),
    # Ligne avec → contenant 🏠
    re.compile(r'^.*🏠.*→.*$', re.MULTILINE),
    # Format broken accident-main
    re.compile(r'^🏠\s*>\s*\[.*$', re.MULTILINE),
]


def strip_all_breadcrumbs(content):
    """Supprime TOUS les breadcrumbs (où qu'ils soient dans le fichier)."""
    new_content = content
    for pattern in _BREADCRUMB_PATTERNS:
        new_content = pattern.sub('', new_content)
    # Nettoyer lignes vides multiples résultant des suppressions
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    return new_content.strip()


def add_breadcrumb_to_file(file_path):
    root_link = compute_root_link(file_path)
    if not root_link:
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()
    except Exception as e:
        print(f"Erreur de lecture {file_path}: {e}")
        return False

    cleaned = strip_all_breadcrumbs(original)
    breadcrumb_block = f"<!-- Breadcrumb -->\n[🏠]({root_link})\n<!-- /Breadcrumb -->"

    new_content = f"{breadcrumb_block}\n\n{cleaned}\n"

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Erreur d'écriture {file_path}: {e}")
        return False


def process_all_markdown_files():
    stats = {'total_files': 0, 'modified_files': 0, 'skipped_files': 0, 'errors': 0}
    md_files = []

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.venv', '.dev', '__pycache__', '.git', 'node_modules', '.opencode')]
        for f in files:
            if f.endswith('.md'):
                md_files.append(os.path.join(root, f))

    stats['total_files'] = len(md_files)

    for fp in md_files:
        try:
            if add_breadcrumb_to_file(fp):
                stats['modified_files'] += 1
                print(f"✅ {fp}")
            else:
                stats['skipped_files'] += 1
        except Exception as e:
            stats['errors'] += 1
            print(f"❌ {fp}: {e}")

    return stats


if __name__ == "__main__":
    print("🚀 Génération des fils d'Ariane...")
    print("=" * 60)
    st = process_all_markdown_files()
    print("\n" + "=" * 60)
    print(f"📊  Fichiers: {st['total_files']} | Modifiés: {st['modified_files']} | Ignorés: {st['skipped_files']} | Erreurs: {st['errors']}")
    print("✅ Terminé!")
