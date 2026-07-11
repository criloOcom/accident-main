#!/usr/bin/env python3
"""
hermes_replace_py_paths.py — Apply the same old→new path mappings
to all .py files (excluding venv and __pycache__).
"""

import os

ROOT = "/home/crilocom/accident-main"
SKIP_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', '.pytest_cache', '.opencode', '.dev/.venv'}

REPLACEMENTS = [
    ("⚖️_Actes", "⚖️ Actes"),
    ("📜_Lois",  "📜 Lois"),
    ("🧠_Memory", "🧠 Memory"),
    ("📊_Rapports", "📊 Rapports"),
    ("🚦_Status", "🚦 Status"),
    ("00_Preuves_officielles", "Preuves officielles"),
    ("👤_Reel", "👤 Reel"),
    ("📎_Annexes", "📎 Annexes"),
    ("🔑_Token", "🔑 Token"),
    ("📊_Index", "📊 Index"),
    ("📜_Jurisprudence", "📜 Jurisprudence"),
    ("🗄️_Archives", "🗄️ Archives"),
    ("00_📂_Preuves_officielles", "📂 Preuves officielles"),
    ("01_⚖️_Actes_proceduraux", "⚖️ Actes proceduraux"),
    ("02_✉️_Courriers", "✉️ Courriers"),
    ("03_📚_Analyses_juridiques", "📚 Analyses juridiques"),
    ("04_💰_Etudes_indemnisation", "💰 Etudes indemnisation"),
    ("05_🗂️_Organisation", "🗂️ Organisation"),
    ("06_🗄️_Archives", "🗄️ Archives"),
    ("📒_Autres_codes", "📒 Autres codes"),
    ("📒_Code_assurances", "📒 Code assurances"),
    ("📒_Code_civil", "📒 Code civil"),
    ("📒_Code_commerce", "📒 Code commerce"),
    ("📒_Code_general_des_collectivites_territoriales", "📒 Code general des collectivites territoriales"),
    ("📒_Code_penal", "📒 Code penal"),
    ("📒_Code_procedure_civile", "📒 Code procedure civile"),
    ("📒_Code_procedure_penale", "📒 Code procedure penale"),
]


def main():
    changed = 0
    for dp, dn, fn in os.walk(ROOT):
        parts = os.path.relpath(dp, ROOT).split(os.sep)
        if any(p in SKIP_DIRS for p in parts):
            continue
        for f in fn:
            if not f.endswith(".py"):
                continue
            if f.startswith("hermes_"):
                continue
            fp = os.path.join(dp, f)
            with open(fp, 'r', encoding='utf-8') as fh:
                content = fh.read()
            original = content
            for old, new in REPLACEMENTS:
                content = content.replace(old, new)
            if content != original:
                with open(fp, 'w', encoding='utf-8') as fh:
                    fh.write(content)
                print(f"  ✅ {os.path.relpath(fp, ROOT)}")
                changed += 1

    print(f"\n✅ {changed} fichiers .py mis à jour")


if __name__ == "__main__":
    main()
