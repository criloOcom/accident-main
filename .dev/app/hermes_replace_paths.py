#!/usr/bin/env python3
"""
hermes_replace_paths.py — Mission Hermès Phase 3
Replace all OLD underscored directory paths with NEW space-separated paths
in all .md files across the repo.
"""

import os
import re

ROOT = "/home/crilocom/accident-main"
SKIP_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', '.pytest_cache', '.opencode', '.dev/.venv'}

# Ordered: top-level dirs first (they're prefixes in paths),
# then subdir names.
REPLACEMENTS = [
    # Top-level
    ("⚖️_Actes", "⚖️ Actes"),
    ("📜_Lois",  "📜 Lois"),
    ("🧠_Memory", "🧠 Memory"),
    ("📊_Rapports", "📊 Rapports"),
    ("🚦_Status", "🚦 Status"),

    # 00_Preuves_officielles (special: no emoji, just prefix)
    ("00_Preuves_officielles", "Preuves officielles"),

    # Level 2 dirs under ⚖️ Actes
    ("👤_Reel", "👤 Reel"),
    ("📎_Annexes", "📎 Annexes"),
    ("🔑_Token", "🔑 Token"),

    # Level 2 dirs under 📜 Lois
    ("📊_Index", "📊 Index"),
    ("📜_Jurisprudence", "📜 Jurisprudence"),

    # Level 2 under 📊 Rapports
    ("🗄️_Archives", "🗄️ Archives"),

    # Token/Reel subdirs (numeric prefix + emoji_underscore)
    ("00_📂_Preuves_officielles", "📂 Preuves officielles"),
    ("01_⚖️_Actes_proceduraux", "⚖️ Actes proceduraux"),
    ("02_✉️_Courriers", "✉️ Courriers"),
    ("03_📚_Analyses_juridiques", "📚 Analyses juridiques"),
    ("04_💰_Etudes_indemnisation", "💰 Etudes indemnisation"),
    ("05_🗂️_Organisation", "🗂️ Organisation"),
    ("06_🗄️_Archives", "🗄️ Archives"),

    # 📒_* dirs
    ("📒_Autres_codes", "📒 Autres codes"),
    ("📒_Code_assurances", "📒 Code assurances"),
    ("📒_Code_civil", "📒 Code civil"),
    ("📒_Code_commerce", "📒 Code commerce"),
    ("📒_Code_general_des_collectivites_territoriales", "📒 Code general des collectivites territoriales"),
    ("📒_Code_penal", "📒 Code penal"),
    ("📒_Code_procedure_civile", "📒 Code procedure civile"),
    ("📒_Code_procedure_penale", "📒 Code procedure penale"),
]

def collect_md_files():
    targets = []
    for dp, dn, fn in os.walk(ROOT):
        parts = os.path.relpath(dp, ROOT).split(os.sep)
        if any(p in SKIP_DIRS for p in parts):
            continue
        for f in fn:
            if f.endswith(".md"):
                targets.append(os.path.join(dp, f))
    return sorted(targets)

def main():
    files = collect_md_files()
    print(f"📄 {len(files)} fichiers .md à traiter\n")

    total_changes = 0
    changed_files = 0

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        for old, new in REPLACEMENTS:
            content = content.replace(old, new)

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            changes = sum(1 for old, _ in REPLACEMENTS if old in original)  # rough
            total_changes += 1
            changed_files += 1

    print(f"✅ {changed_files} fichiers modifiés")
    print(f"   (remplacement des anciens chemins vers les nouveaux)")


if __name__ == "__main__":
    main()
