#!/usr/bin/env python3
"""
fix_breadcrumbs_lois.py — Génère les fils d'Ariane (<!-- Breadcrumb -->)
pour les fichiers Article*.md sous 📜 Lois/.
Conforme au protocole : YAML en ligne 1, puis breadcrumb, puis contenu.

Usage: python3 fix_breadcrumbs_lois.py
"""

from pathlib import Path
import re

LOIS_DIR = Path("/home/crilocom/accident-main/📜 Lois")
SEP = " › "


def generate_breadcrumb(file_path):
    rel = file_path.relative_to(LOIS_DIR)
    parent = rel.parent
    depth = len(parent.parts) if parent != Path(".") else 0
    home = "../" * (depth + 1) + "README.md"
    leaf = file_path.name.replace(".md", "").replace("_", " ")

    parts = [f"[🏠]({home})", f"[📜 Lois](README.md)"]

    if parent != Path("."):
        pname = parent.name.replace("_", " ")
        parts.append(f"[{pname}](./README.md)")

    breadcrumb = SEP.join(parts) + SEP + leaf
    return f"<!-- Breadcrumb -->\n{breadcrumb}\n<!-- /Breadcrumb -->"


def strip_legacy_breadcrumb(content):
    m = re.search(r'<!-- Breadcrumb -->.*?<!-- /Breadcrumb -->', content, re.DOTALL)
    if m:
        return (content[:m.start()] + content[m.end():]).strip("\n")
    for line in content.split("\n"):
        if line.strip().startswith("🏠") and ">" in line:
            content = content.replace(line, "", 1).strip("\n")
            break
    return content.strip("\n")


def fix_breadcrumb_in_file(file_path):
    content = file_path.read_text(encoding="utf-8")
    original = content

    content = strip_legacy_breadcrumb(content)

    bc = generate_breadcrumb(file_path)
    m_yaml = re.match(r'^---\s*\n.*?\n---\s*\n?', content, re.DOTALL)
    if m_yaml:
        yaml_block = m_yaml.group(0)
        after = content[m_yaml.end():]
        new_content = yaml_block + "\n" + bc + "\n\n" + after.lstrip("\n")
    else:
        new_content = bc + "\n\n" + content.lstrip("\n")

    if new_content == original:
        print(f"  ✓ {file_path.name} — déjà à jour")
        return False

    file_path.write_text(new_content, encoding="utf-8")
    print(f"  ✅ {file_path.name}")
    return True


def main():
    article_files = list(LOIS_DIR.rglob("Article*.md"))
    print(f"Trouvé {len(article_files)} fichiers Article*.md")

    fixed = sum(1 for fp in article_files if fix_breadcrumb_in_file(fp))

    print(f"\n✅ {fixed}/{len(article_files)} fichiers mis à jour")


if __name__ == "__main__":
    main()
