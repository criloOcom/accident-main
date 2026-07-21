#!/usr/bin/env python3
"""
hermes_replace_py_paths.py — Apply the same old→new path mappings
to all .py files (excluding venv and __pycache__).
"""

import os

ROOT = "/home/crilocom/accident-main"
SKIP_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', '.pytest_cache', '.opencode', '.dev/.venv'}

REPLACEMENTS = [
    ("Actes", "Actes"),
    ("Lois",  "Lois"),
    ("Memory", "Memory"),
    ("Rapports", "Rapports"),
    ("Status", "Status"),
    ("00_Preuves_officielles", "Preuves officielles"),
    ("Reel", "Reel"),
    ("📎_Annexes", "📎 Annexes"),
    ("Token", "Token"),
    ("Index", "Index"),
    ("Jurisprudence", "Jurisprudence"),
    ("Archives", "Archives"),
    ("00_Preuves_officielles", "Preuves_officielles"),
    ("01_Actes_proceduraux", "Actes_proceduraux"),
    ("02_Courriers", "Courriers"),
    ("03_Analyses_juridiques", "Analyses_juridiques"),
    ("04_Etudes_indemnisation", "Etudes_indemnisation"),
    ("05_Organisation", "Organisation"),
    ("06_Archives", "Archives"),
    ("Autres_codes", "Autres_codes"),
    ("Code_assurances", "Code_assurances"),
    ("Code_civil", "Code_civil"),
    ("Code_commerce", "Code_commerce"),
    ("Code_general_des_collectivites_territoriales", "Code general des collectivites territoriales"),
    ("Code_penal", "Code penal"),
    ("Code_procedure_civile", "Code procedure civile"),
    ("Code_procedure_penale", "Code procedure penale"),
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
