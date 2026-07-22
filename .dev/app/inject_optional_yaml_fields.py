#!/usr/bin/env python3
"""
inject_optional_yaml_fields.py — Injection sélective des champs optionnels
dans les en-têtes YAML des fichiers .md du dépôt accident-main.

Champs injectés (selon le type de fichier) :
  - date_creation    : pour les courriers, actes, analyses, études (si date existe)
  - date_modification : idem (si différente de date_creation)
  - proof_delivery    : uniquement pour courriers/actes avec statut: final ou envoye
  - last_verified     : pour les fichiers source: Légifrance ou jurisprudence

Usage :
    python3 .dev/app/inject_optional_yaml_fields.py           # dry-run
    python3 .dev/app/inject_optional_yaml_fields.py --apply     # écrit
    python3 .dev/app/inject_optional_yaml_fields.py --type courrier,assignation  # filtre par type
"""

import os
import re
import sys
import glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

YAML_MATCH = re.compile(r'^---\s*\n(.*?)\n---\s*\n?', re.DOTALL)

# Types qui reçoivent les champs temporels
TYPES_WITH_TEMPORAL = {"courrier", "assignation", "plainte", "analyse_juridique",
                       "etude_indemnisation", "rapport", "preuve"}

# Types qui reçoivent proof_delivery
TYPES_WITH_DELIVERY = {"courrier", "assignation", "plainte"}

# Types qui reçoivent last_verified
TYPES_WITH_VERIFIED = {"loi", "jurisprudence"}


def parse_yaml(yaml_text):
    """Parse simple YAML key: value pairs into a dict."""
    result = {}
    for line in yaml_text.split('\n'):
        m = re.match(r'^(\w[\w_-]*)\s*:\s*(.*)', line)
        if m:
            result[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return result


def find_key_line(lines, key):
    """Find the line index of a key in YAML lines."""
    for i, line in enumerate(lines):
        m = re.match(r'^(\w[\w_-]*)\s*:', line)
        if m and m.group(1) == key:
            return i
    return None


def update_yaml(yaml_text, updates):
    """Add or update fields in YAML text."""
    lines = yaml_text.split('\n')
    existing_keys = set()
    for line in lines:
        m = re.match(r'^(\w[\w_-]*)\s*:', line)
        if m:
            existing_keys.add(m.group(1))

    for key, value in updates.items():
        if value is None:
            continue
        idx = find_key_line(lines, key)
        if idx is not None:
            lines[idx] = f'{key}: {value}'
        else:
            # Insérer avant 'tags' si présent, sinon avant la dernière ligne non-vide
            tags_idx = find_key_line(lines, 'tags')
            if tags_idx is not None:
                lines.insert(tags_idx, f'{key}: {value}')
            else:
                # Trouver la dernière ligne significative avant le ---
                insert_at = len(lines)
                while insert_at > 0 and lines[insert_at - 1].strip() in ('', '---'):
                    insert_at -= 1
                lines.insert(insert_at, f'{key}: {value}')

    return '\n'.join(lines)


def main():
    dry_run = "--apply" not in sys.argv
    type_filter = None
    for arg in sys.argv[1:]:
        if arg.startswith("--type="):
            type_filter = set(arg.split("=", 1)[1].split(","))

    print(f"{'DRY-RUN' if dry_run else 'APPLY'} — Injection sélective des champs YAML optionnels")

    md_files = glob.glob(os.path.join(BASE, "**/*.md"), recursive=True)
    total_updated = 0
    total_skipped = 0

    for fp in sorted(md_files):
        rel = os.path.relpath(fp, BASE)
        if "/.git/" in fp or "/__pycache__/" in fp or "/node_modules/" in fp:
            continue

        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()

        m = YAML_MATCH.match(content)
        if not m:
            total_skipped += 1
            continue

        yaml_text = m.group(1)
        yaml_data = parse_yaml(yaml_text)
        dtype = yaml_data.get('type', '')
        statut = yaml_data.get('statut', '')

        # Filtrer par type si spécifié
        if type_filter and dtype not in type_filter:
            total_skipped += 1
            continue

        updates = {}

        # Champs temporels (date_creation, date_modification)
        if dtype in TYPES_WITH_TEMPORAL or dtype in TYPES_WITH_VERIFIED:
            date_val = yaml_data.get('date', '')
            if date_val and date_val not in ('null', 'None', ''):
                if 'date_creation' not in yaml_data:
                    updates['date_creation'] = date_val

        # proof_delivery : pour courriers/actes final ou envoye
        if dtype in TYPES_WITH_DELIVERY and statut in ('final', 'envoye'):
            if 'proof_delivery' not in yaml_data:
                updates['proof_delivery'] = 'À compléter'

        # last_verified : pour lois et jurisprudence
        if dtype in TYPES_WITH_VERIFIED:
            if 'last_verified' not in yaml_data:
                updates['last_verified'] = 'À vérifier'

        if not updates:
            total_skipped += 1
            continue

        new_yaml = update_yaml(yaml_text, updates)
        new_content = content[:m.start()] + f'---\n{new_yaml}\n---' + content[m.end():]

        if dry_run:
            print(f"  [DRY] {rel} → {updates}")
        else:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✓ {rel} → {updates}")

        total_updated += 1

    print(f"\nRésumé : {total_updated} fichiers modifiés, {total_skipped} ignorés "
          f"({'dry-run' if dry_run else 'écriture effectuée'}).")


if __name__ == '__main__':
    main()
