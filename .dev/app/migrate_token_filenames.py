#!/usr/bin/env python3
"""
migrate_token_filenames.py — Migration unique : renomme 34 fichiers tokens
vers une nomenclature préfixée par entités.

Usage: python3 .dev/app/migrate_token_filenames.py [--dry-run]
"""

import os, sys
from collections import OrderedDict

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
JETONS_DIR = os.path.join(BASE, "Memory", "Tokens")
DRY_RUN = "--dry-run" in sys.argv

# ─── Mapping old base → new base (without .md) ───────────────────
MIGRATION = OrderedDict([
    # --- Bloc Victime ---
    ("token-la-victime", "token-victime-nom-complet"),
    ("token-prenom-de-la-victime", "token-victime-prenom"),
    ("token-age-de-la-victime", "token-victime-age"),
    ("token-date-de-naissance-de-la-victime", "token-victime-date-naissance"),
    ("token-l-adresse-de-la-victime", "token-victime-adresse"),
    ("token-la-ville-de-residence-de-la-victime", "token-victime-ville-residence"),
    ("token-le-telephone-de-la-victime", "token-victime-telephone"),
    ("token-l-email-de-la-victime", "token-victime-email"),
    ("token-l-identifiant-professionnel-de-la-victime", "token-victime-id-professionnel"),
    ("token-le-medecin-generaliste", "token-victime-medecin-generaliste"),
    ("token-nom-de-l-avocat-de-la-victime", "token-victime-avocat-nom"),
    # --- Bloc Exploitation ---
    ("token-le-president-de-l-exploitation", "token-exploitation-president-nom"),
    ("token-la-directrice-generale-de-l-exploitation", "token-exploitation-dg-nom"),
    ("token-le-prepose-de-l-exploitation", "token-exploitation-prepose-nom"),
    ("token-l-exploitant-du-commerce-la-sas", "token-exploitation-raison-sociale"),
    ("token-siren-de-l-exploitation", "token-exploitation-siren"),
    ("token-l-identifiant-de-l-exploitation", "token-exploitation-id"),
    ("token-l-adresse-de-l-exploitation", "token-exploitation-adresse"),
    ("token-l-adresse-du-president", "token-exploitation-president-adresse"),
    ("token-le-proprietaire-des-murs", "token-exploitation-bailleur-nom"),
    ("token-date-reouverture-boutique", "token-exploitation-date-reouverture"),
    ("token-capital-social-de-l-exploitation", "token-exploitation-capital-social"),
    # --- Bloc Accident & Géographie ---
    ("token-code-postal-de-l-accident", "token-accident-code-postal"),
    ("token-la-ville-de-l-accident", "token-accident-ville"),
    ("token-la-metropole-regionale", "token-accident-metropole"),
    ("token-date-relance-v2", "token-accident-date-relance-v2"),
    # --- Bloc Hôpital / Médical ---
    ("token-l-etablissement-sos-main", "token-hopital-sosmain-nom"),
    ("token-le-chirurgien-sos-main", "token-hopital-sosmain-chirurgien"),
    ("token-la-ville-de-l-etablissement-sos-main", "token-hopital-sosmain-ville"),
    ("token-le-medecin-en-urgence", "token-hopital-urgence-medecin"),
    # --- Bloc Autorités / Mairie / CPAM ---
    ("token-l-adjoint-au-maire-de-la-commune", "token-mairie-adjoint-nom"),
    ("token-l-email-de-l-adjoint-au-maire", "token-mairie-adjoint-email"),
    ("token-l-email-du-secretariat-de-la-mairie", "token-mairie-secretariat-email"),
    ("token-la-gestionnaire-cpam", "token-cpam-gestionnaire-nom"),
])

# Build both bare and .md variants
REPLACE_BARE = {k + "'": v + "'" for k, v in MIGRATION.items()}
REPLACE_MD = {k + ".md": v + ".md" for k, v in MIGRATION.items()}
# Also quote-surrounded bare (for Python dict values: 'token-xxx')
REPLACE_QUOTED = {"'" + k: "'" + v for k, v in MIGRATION.items()}


def rename_physical_files():
    renamed = 0
    for old_base, new_base in MIGRATION.items():
        old_path = os.path.join(JETONS_DIR, old_base + ".md")
        new_path = os.path.join(JETONS_DIR, new_base + ".md")
        if not os.path.isfile(old_path):
            # might already be renamed
            if os.path.isfile(new_path):
                continue
            print(f"  ⚠️  Introuvable : {old_base}.md")
            continue
        if DRY_RUN:
            print(f"  ~ Renomme : {old_base}.md → {new_base}.md")
        else:
            os.rename(old_path, new_path)
            print(f"  ✅ Renomme : {old_base}.md → {new_base}.md")
        renamed += 1
    print(f"  → {renamed} fichiers renommés" + (" (dry-run)" if DRY_RUN else ""))
    return renamed


def replace_in_file(filepath, replacements):
    """Apply a dict of old→new replacements to a file. Return count."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return 0

    original = content
    count = 0
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            count += content.count(new) - original.count(new) + original.count(old) - content.count(old)
            # Simpler: count changes
            # Actually, just track by comparing original vs new
    changes = 0
    for old, new in replacements.items():
        if old in original and old not in content:
            # It was replaced
            changes += 1
    # Better approach: count total replacements
    total = 0
    for old, new in replacements.items():
        c = original.count(old)
        if c > 0:
            total += c
    
    if content != original:
        if DRY_RUN:
            rel = os.path.relpath(filepath, BASE)
            print(f"  ~ {rel}: {total} remplacement(s)")
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            rel = os.path.relpath(filepath, BASE)
            if total > 0:
                print(f"  ✅ {rel}: {total} remplacement(s)")
        return total
    return 0


def migrate_all_files():
    total_replacements = 0
    total_files = 0

    # Build combined replacements map
    md_replacements = {}
    md_replacements.update(REPLACE_MD)

    py_replacements = {}
    py_replacements.update(REPLACE_MD)
    py_replacements.update(REPLACE_QUOTED)

    for root, dirs, filenames in os.walk(BASE):
        skip_dirs = {'.git', '__pycache__', '.pytest_cache'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for fn in filenames:
            fp = os.path.join(root, fn)

            if fn.endswith('.md'):
                reps = md_replacements
            elif fn.endswith('.py'):
                reps = py_replacements
            else:
                continue

            count = replace_in_file(fp, reps)
            if count > 0:
                total_replacements += count
                total_files += 1

    print(f"\n→ {total_files} fichiers modifiés, {total_replacements} remplacements" +
          (" (dry-run)" if DRY_RUN else ""))


def main():
    print("=== Migration des 34 fichiers tokens ===")
    if DRY_RUN:
        print("🔍 MODE DRY-RUN — Aucune modification\n")
    else:
        print("🔄 Application réelle\n")

    rename_physical_files()
    migrate_all_files()

    if DRY_RUN:
        print("\n🔍 Dry-run terminé. Passez --dry-run pour appliquer.")


if __name__ == '__main__':
    main()
