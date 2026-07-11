#!/usr/bin/env python3
"""
Génère des fils d'Ariane dans les fichiers .md.
Format (commentaire HTML, ligne 1) :
<!-- [🏠](../README.md) > 📁 [Dossier](../README.md) > 📄 [Fichier](./fichier.md) -->
"""

import os
import re
from pathlib import Path

ROOT = "/home/crilocom/accident-main"


def generate_breadcrumb(file_path):
    full_path = Path(file_path)
    root = Path(ROOT)
    try:
        relative_path = full_path.relative_to(root)
    except ValueError:
        return None

    parts = list(relative_path.parts)
    breadcrumb_parts = ["[🏠](../README.md)"]

    for i, part in enumerate(parts[:-1]):
        relative_link = os.path.join(".." * (len(parts) - i - 1), "README.md")
        breadcrumb_parts.append(f"📁 [ {part} ]({relative_link})")

    filename = parts[-1]
    breadcrumb_parts.append(f"📄 [ {filename} ](.{filename})")

    return " > ".join(breadcrumb_parts)


# Patterns de blocs breadcrumb pour suppression
_BREADCRUMB_PATTERNS = [
    # Code block avec breadcrumb
    re.compile(r'```\s*\n.*?🏠\s*\[.*?```', re.DOTALL),
    # HTML comment avec breadcrumb
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
    breadcrumb = generate_breadcrumb(file_path)
    if not breadcrumb:
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()
    except Exception as e:
        print(f"Erreur de lecture {file_path}: {e}")
        return False

    cleaned = strip_all_breadcrumbs(original)
    new_html = f"<!-- {breadcrumb} -->"

    if cleaned != original.strip():
        # Il y avait des breadcrumbs à supprimer
        new_content = f"{new_html}\n\n{cleaned}\n"
    else:
        # Pas de breadcrumb trouvé — juste insérer en ligne 1
        new_content = f"{new_html}\n\n{original}"

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
