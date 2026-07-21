#!/usr/bin/env python3
"""Valide les frontmatter YAML de tous les fichiers .md du périmètre.

Usage :
    python3 .dev/app/yaml_validator.py                  # scan complet
    python3 .dev/app/yaml_validator.py --path dossier/  # ciblé
    python3 .dev/app/yaml_validator.py --json           # sortie JSON
    python3 .dev/app/yaml_validator.py --quiet          # silence si OK

Retourne :
    0 = tout valide
    1 = violations détectées
"""

import argparse
import json
import os
import sys
from pathlib import Path

from yaml_utils import (
    REPO_ROOT,
    CANONICAL_TYPES_SET,
    STATUT_VALUES,
    DATE_RE,
    read_frontmatter,
    in_perimeter,
    is_excluded,
)


def walk_md_files(path: str | None = None) -> list[str]:
    """Parcourt les fichiers .md du périmètre (ou d'un chemin spécifique)."""
    if path:
        target = os.path.abspath(path)
        if os.path.isfile(target):
            return [target] if target.endswith(".md") else []
        results = []
        for root, _, files in os.walk(target):
            for f in files:
                if f.endswith(".md"):
                    results.append(os.path.join(root, f))
        return results

    results = []
    for root, _, files in os.walk(REPO_ROOT):
        for f in files:
            fp = os.path.join(root, f)
            if not f.endswith(".md"):
                continue
            if is_excluded(fp):
                continue
            if in_perimeter(fp):
                results.append(fp)
    return sorted(results)


def validate_file(filepath: str) -> list[str]:
    """Valide le YAML frontmatter d'un fichier. Retourne une liste de violations."""
    violations = []
    rel = os.path.relpath(filepath, REPO_ROOT)

    fm = read_frontmatter(filepath)
    if fm is None:
        violations.append(f"{rel}: YAML frontmatter manquant ou invalide")
        return violations

    dtype = fm.get("type", "")
    if not dtype:
        violations.append(f"{rel}: champ 'type' manquant")
    elif dtype not in CANONICAL_TYPES_SET:
        violations.append(f"{rel}: type non canonique '{dtype}'")

    statut = fm.get("statut", "")
    if statut and statut not in STATUT_VALUES:
        violations.append(f"{rel}: statut non canonique '{statut}'")

    date_val = fm.get("date")
    if date_val:
        date_str = str(date_val) if not isinstance(date_val, str) else date_val
        if date_str == "FIXME":
            pass  # Sentinel accepté en attendant une date réelle
        elif not DATE_RE.match(date_str):
            violations.append(f"{rel}: format date invalide '{date_str}' (attendu YYYY-MM-DD)")
    elif dtype in ("courrier", "assignation", "plainte", "attestation", "preuve", "rapport", "loi", "jurisprudence"):
        violations.append(f"{rel}: champ 'date' manquant (requis pour type '{dtype}')")

    reel_path = fm.get("reel_path")
    if reel_path:
        resolved = os.path.normpath(os.path.join(os.path.dirname(filepath), str(reel_path)))
        if not os.path.exists(resolved):
            violations.append(f"{rel}: reel_path '{reel_path}' → fichier introuvable ({resolved})")

    calendar_id = fm.get("calendar_event_id")
    if calendar_id and not isinstance(calendar_id, str):
        violations.append(f"{rel}: calendar_event_id doit être une chaîne")

    jx = fm.get("jx")
    if jx:
        jx_str = str(jx)
        if not jx_str.startswith("J") or len(jx_str) < 2:
            violations.append(f"{rel}: format jx invalide '{jx_str}' (attendu J±XX)")

    legiarti = fm.get("legiarti")
    if legiarti and not str(legiarti).startswith("LEGIARTI"):
        violations.append(f"{rel}: legiarti doit commencer par LEGIARTI")

    juritext = fm.get("juritext")
    if juritext and not str(juritext).startswith("JURITEXT"):
        violations.append(f"{rel}: juritext doit commencer par JURITEXT")

    return violations


def main():
    parser = argparse.ArgumentParser(description="Validateur YAML frontmatter")
    parser.add_argument("--path", help="Cibler un fichier ou dossier spécifique")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    parser.add_argument("--quiet", action="store_true", help="Silencieux si OK")
    args = parser.parse_args()

    files = walk_md_files(args.path)
    all_violations: list[str] = []

    for fp in files:
        violations = validate_file(fp)
        all_violations.extend(violations)

    if args.json:
        print(json.dumps({
            "files_scanned": len(files),
            "violations": len(all_violations),
            "details": all_violations,
        }, indent=2, ensure_ascii=False))
    else:
        if all_violations:
            print(f"🔴 {len(all_violations)} violation(s) YAML détectée(s) :\n")
            for v in all_violations:
                print(f"   {v}")
        elif not args.quiet:
            print(f"✅ {len(files)} fichier(s) scanné(s) — aucune violation YAML")

    return 1 if all_violations else 0


if __name__ == "__main__":
    sys.exit(main())
