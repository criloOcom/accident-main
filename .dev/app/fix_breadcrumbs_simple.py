#!/usr/bin/env python3
"""
fix_breadcrumbs_simple.py — Ajoute/génère le fil d'Ariane (<!-- Breadcrumb -->)
dans les fichiers Article*.md sous 📜 Lois/.

Usage: python3 fix_breadcrumbs_simple.py
"""

from pathlib import Path

LOIS_DIR = Path("/home/crilocom/accident-main/📜 Lois")
SEP = " › "


def generate_breadcrumb(file_path):
    rel = file_path.relative_to(LOIS_DIR)
    parent = rel.parent
    depth = len(parent.parts) if parent != Path(".") else 0
    home = "../" * (depth + 1) + "README.md"
    leaf = file_path.name.replace(".md", "").replace("_", " ")

    parts = [f"[🏠]({home})"]
    parts.append(f"[📜 Lois](README.md)")

    if parent != Path("."):
        parts.append(f"[{parent.name}](./README.md)")

    breadcrumb = SEP.join(parts) + SEP + leaf
    return f"<!-- Breadcrumb -->\n{breadcrumb}\n<!-- /Breadcrumb -->"


def strip_legacy_breadcrumb(content):
    """Supprime un fil d'Ariane legacy (format >) ou HTML s'il existe."""
    import re
    # HTML format
    m = re.search(r'<!-- Breadcrumb -->.*?<!-- /Breadcrumb -->', content, re.DOTALL)
    if m:
        return (content[:m.start()] + content[m.end():]).strip("\n")
    # Legacy format with 🏠 and >
    for line in content.split("\n"):
        if line.strip().startswith("🏠") and ">" in line:
            content = content.replace(line, "", 1)
            break
    return content.strip("\n")


def main():
    article_files = list(LOIS_DIR.rglob("Article*.md"))
    print(f"Trouvé {len(article_files)} fichiers Article*.md")

    fixed = 0
    for fp in article_files:
        content = fp.read_text(encoding="utf-8")
        old_content = content

        # Strip existing breadcrumb (any format)
        content = strip_legacy_breadcrumb(content)

        # Generate new breadcrumb
        bc = generate_breadcrumb(fp)

        # Insert after YAML if present
        import re
        m_yaml = re.match(r'^---\s*\n.*?\n---\s*\n?', content, re.DOTALL)
        if m_yaml:
            yaml_block = m_yaml.group(0)
            after = content[m_yaml.end():]
            new_content = yaml_block + "\n" + bc + "\n\n" + after.lstrip("\n")
        else:
            new_content = bc + "\n\n" + content.lstrip("\n")

        if new_content != old_content:
            fp.write_text(new_content, encoding="utf-8")
            print(f"  ✅ {fp.name}")
            fixed += 1
        else:
            print(f"  ✓ {fp.name} — déjà à jour")

    print(f"\n✅ {fixed}/{len(article_files)} fichiers mis à jour")


if __name__ == "__main__":
    main()
