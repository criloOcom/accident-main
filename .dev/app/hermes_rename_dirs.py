#!/usr/bin/env python3
"""
hermes_rename_dirs.py — Mission Hermès: rename directories (git mv)
Removes underscores and numeric prefixes (00_, 01_, ...) from directory names.
Run from repo root: python3 .dev/app/hermes_rename_dirs.py
"""

import os
import subprocess
import sys

ROOT = "/home/crilocom/accident-main"

def rename(steps_todo):
    for old, new in steps_todo:
        old_abs = os.path.join(ROOT, old)
        new_abs = os.path.join(ROOT, new)
        if not os.path.isdir(old_abs):
            print(f"  ⏭️  {old} → introuvable, skip")
            continue
        if os.path.isdir(new_abs):
            print(f"  ⏭️  {old} → {new} existe déjà, skip")
            continue
        print(f"  🔄 {old}  →  {new}")
        r = subprocess.run(["git", "mv", old_abs, new_abs], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ❌ git mv failed: {r.stderr}")
        else:
            print(f"  ✅")


def main():
    renames = [
        # === TOP-LEVEL (underscores → spaces) ===
        ("Actes",            "Actes"),
        ("Lois",             "Lois"),
        ("Memory",           "Memory"),
        ("Rapports",         "Rapports"),
        ("Status",           "Status"),

        # === ROOT of Actes (special: no emoji, just 00_ prefix) ===
        ("Actes/00_Preuves_officielles", "Actes/Preuves officielles"),

        # === LEVEL 2 under Actes ===
        ("Actes/Reel",    "Actes/Reel"),
        ("Actes/📎_Annexes", "Actes/📎 Annexes"),
        ("Actes/Token",   "Actes/Token"),

        # === LEVEL 2 under Lois ===
        ("Lois/Index",    "Lois/Index"),
        ("Lois/Jurisprudence", "Lois/Jurisprudence"),

        # === LEVEL 2 under Rapports ===
        ("Rapports/Archives", "Rapports/Archives"),

        # === LEVEL 3 under Actes/Token (00_ → 06_ prefix removal) ===
        ("Actes/Token/00_Preuves_officielles",   "Actes/Token/Preuves_officielles"),
        ("Actes/Token/01_Actes_proceduraux",    "Actes/Token/Actes_proceduraux"),
        ("Actes/Token/02_Courriers",            "Actes/Token/Courriers"),
        ("Actes/Token/03_Analyses_juridiques",  "Actes/Token/Analyses_juridiques"),
        ("Actes/Token/04_Etudes_indemnisation", "Actes/Token/Etudes_indemnisation"),
        ("Actes/Token/05_Organisation",         "Actes/Token/Organisation"),
        ("Actes/Token/06_Archives",             "Actes/Token/Archives"),

        # === LEVEL 3 under Actes/Reel (00_ → 06_ prefix removal) ===
        ("Actes/Reel/00_Preuves_officielles",   "Actes/Reel/Preuves_officielles"),
        ("Actes/Reel/01_Actes_proceduraux",    "Actes/Reel/Actes_proceduraux"),
        ("Actes/Reel/02_Courriers",            "Actes/Reel/Courriers"),
        ("Actes/Reel/03_Analyses_juridiques",  "Actes/Reel/Analyses_juridiques"),
        ("Actes/Reel/04_Etudes_indemnisation", "Actes/Reel/Etudes_indemnisation"),
        ("Actes/Reel/05_Organisation",         "Actes/Reel/Organisation"),
        ("Actes/Reel/06_Archives",             "Actes/Reel/Archives"),

        # === LEVEL 3 under Lois — 📒_* dirs (prefix 📒_ → 📒 + underscores → spaces) ===
        ("Lois/Autres_codes",   "Lois/Autres_codes"),
        ("Lois/Code_assurances", "Lois/Code_assurances"),
        ("Lois/Code_civil",     "Lois/Code civil"),
        ("Lois/Code_commerce",  "Lois/Code_commerce"),
        ("Lois/Code_general_des_collectivites_territoriales", "Lois/Code general des collectivites territoriales"),
        ("Lois/Code_penal",     "Lois/Code penal"),
        ("Lois/Code_procedure_civile", "Lois/Code procedure civile"),
        ("Lois/Code_procedure_penale", "Lois/Code procedure penale"),
    ]

    print(f"🏗️  HERMÈS — Renommage de {len(renames)} dossiers")
    print(f"{'='*60}\n")

    rename(renames)

    print(f"\n{'='*60}")
    print("✅ Renommage terminé !")


if __name__ == "__main__":
    main()
