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
        ("⚖️_Actes",            "⚖️ Actes"),
        ("📜_Lois",             "📜 Lois"),
        ("🧠_Memory",           "🧠 Memory"),
        ("📊_Rapports",         "📊 Rapports"),
        ("🚦_Status",           "🚦 Status"),

        # === ROOT of ⚖️_Actes (special: no emoji, just 00_ prefix) ===
        ("⚖️_Actes/00_Preuves_officielles", "⚖️ Actes/Preuves officielles"),

        # === LEVEL 2 under ⚖️ Actes ===
        ("⚖️ Actes/👤_Reel",    "⚖️ Actes/👤 Reel"),
        ("⚖️ Actes/📎_Annexes", "⚖️ Actes/📎 Annexes"),
        ("⚖️ Actes/🔑_Token",   "⚖️ Actes/🔑 Token"),

        # === LEVEL 2 under 📜 Lois ===
        ("📜 Lois/📊_Index",    "📜 Lois/📊 Index"),
        ("📜 Lois/📜_Jurisprudence", "📜 Lois/📜 Jurisprudence"),

        # === LEVEL 2 under 📊 Rapports ===
        ("📊 Rapports/🗄️_Archives", "📊 Rapports/🗄️ Archives"),

        # === LEVEL 3 under ⚖️ Actes/🔑 Token (00_ → 06_ prefix removal) ===
        ("⚖️ Actes/🔑 Token/00_📂_Preuves_officielles",   "⚖️ Actes/🔑 Token/📂 Preuves officielles"),
        ("⚖️ Actes/🔑 Token/01_⚖️_Actes_proceduraux",    "⚖️ Actes/🔑 Token/⚖️ Actes proceduraux"),
        ("⚖️ Actes/🔑 Token/02_✉️_Courriers",            "⚖️ Actes/🔑 Token/✉️ Courriers"),
        ("⚖️ Actes/🔑 Token/03_📚_Analyses_juridiques",  "⚖️ Actes/🔑 Token/📚 Analyses juridiques"),
        ("⚖️ Actes/🔑 Token/04_💰_Etudes_indemnisation", "⚖️ Actes/🔑 Token/💰 Etudes indemnisation"),
        ("⚖️ Actes/🔑 Token/05_🗂️_Organisation",         "⚖️ Actes/🔑 Token/🗂️ Organisation"),
        ("⚖️ Actes/🔑 Token/06_🗄️_Archives",             "⚖️ Actes/🔑 Token/🗄️ Archives"),

        # === LEVEL 3 under ⚖️ Actes/👤 Reel (00_ → 06_ prefix removal) ===
        ("⚖️ Actes/👤 Reel/00_📂_Preuves_officielles",   "⚖️ Actes/👤 Reel/📂 Preuves officielles"),
        ("⚖️ Actes/👤 Reel/01_⚖️_Actes_proceduraux",    "⚖️ Actes/👤 Reel/⚖️ Actes proceduraux"),
        ("⚖️ Actes/👤 Reel/02_✉️_Courriers",            "⚖️ Actes/👤 Reel/✉️ Courriers"),
        ("⚖️ Actes/👤 Reel/03_📚_Analyses_juridiques",  "⚖️ Actes/👤 Reel/📚 Analyses juridiques"),
        ("⚖️ Actes/👤 Reel/04_💰_Etudes_indemnisation", "⚖️ Actes/👤 Reel/💰 Etudes indemnisation"),
        ("⚖️ Actes/👤 Reel/05_🗂️_Organisation",         "⚖️ Actes/👤 Reel/🗂️ Organisation"),
        ("⚖️ Actes/👤 Reel/06_🗄️_Archives",             "⚖️ Actes/👤 Reel/🗄️ Archives"),

        # === LEVEL 3 under 📜 Lois — 📒_* dirs (prefix 📒_ → 📒 + underscores → spaces) ===
        ("📜 Lois/📒_Autres_codes",   "📜 Lois/📒 Autres codes"),
        ("📜 Lois/📒_Code_assurances", "📜 Lois/📒 Code assurances"),
        ("📜 Lois/📒_Code_civil",     "📜 Lois/📒 Code civil"),
        ("📜 Lois/📒_Code_commerce",  "📜 Lois/📒 Code commerce"),
        ("📜 Lois/📒_Code_general_des_collectivites_territoriales", "📜 Lois/📒 Code general des collectivites territoriales"),
        ("📜 Lois/📒_Code_penal",     "📜 Lois/📒 Code penal"),
        ("📜 Lois/📒_Code_procedure_civile", "📜 Lois/📒 Code procedure civile"),
        ("📜 Lois/📒_Code_procedure_penale", "📜 Lois/📒 Code procedure penale"),
    ]

    print(f"🏗️  HERMÈS — Renommage de {len(renames)} dossiers")
    print(f"{'='*60}\n")

    rename(renames)

    print(f"\n{'='*60}")
    print("✅ Renommage terminé !")


if __name__ == "__main__":
    main()
