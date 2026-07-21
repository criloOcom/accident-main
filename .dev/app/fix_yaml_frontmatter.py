#!/usr/bin/env python3
"""Correction batch des violations YAML frontmatter détectées par yaml_validator.py.

Usage :
    python3 .dev/app/fix_yaml_frontmatter.py --dry-run       # Aperçu (défaut)
    python3 .dev/app/fix_yaml_frontmatter.py --apply         # Appliquer
    python3 .dev/app/fix_yaml_frontmatter.py --apply --types-only   # Catégorie spécifique

Flags de scope :
    --reel-path, --dates, --types, --statuses, --all (défaut)
"""

import argparse
import json
import os
import re
import sys
import math

from yaml_utils import REPO_ROOT, CANONICAL_TYPES, CANONICAL_TYPES_SET, STATUT_VALUES

ROOT = REPO_ROOT

# ── Mappings de normalisation ────────────────────────────────────────

TYPE_MAP: dict[str, str] = {
    "acte_procedural": "document",
    "simulation": "projet",
    "acte": "document",
    "token": "memory",
    "analyse": "analyse_juridique",
    "erratum": "document",
    "projet": "projet",
    "modele": "fiche",
    "fiche_reunion": "fiche",
    "rapport_technique": "rapport",
    "strategie": "memory",
}

STATUS_MAP: dict[str, str] = {
    "simulation": "projet",
    "envoyé": "envoye",
    "consolide": "final",
}

# Statuts longs (contiennent un —) → extraire le premier mot seulement
LONG_STATUS_PREFIX: dict[str, str] = {
    "brouillon": "brouillon",
    "final": "final",
}

# ── Collecte des violations ──────────────────────────────────────────

def get_violations() -> dict:
    """Lance yaml_validator et parse les violations."""
    import subprocess
    r = subprocess.run(
        [sys.executable, ".dev/app/yaml_validator.py", "--json"],
        capture_output=True, text=True, cwd=ROOT
    )
    return json.loads(r.stdout)


def parse_details(details: list[str]) -> dict:
    """Transforme la liste de strings en catégories structurées."""
    by_file: dict[str, list[dict]] = {}
    for d in details:
        m = re.match(r'^([^:]+): (.+)$', d)
        if not m:
            continue
        fp = m.group(1)
        msg = m.group(2)
        by_file.setdefault(fp, []).append({"raw": d, "msg": msg})
    return by_file


# ── Opérations de correction ─────────────────────────────────────────

def fix_reel_path_in_reel(fp: str, content: str, dry_run: bool) -> list[str]:
    """Supprime reel_path dans 👤 Reel (ces fichiers SONT la version réelle)."""
    log = []
    m = re.search(r'^reel_path:\s*.+$', content, re.MULTILINE)
    if not m:
        return log

    new_content = content[:m.start()] + content[m.end():]

    # Aussi supprimer la ligne vide résiduelle si reel_path était seule dans un bloc
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)

    log.append(f"  🗑️  reel_path supprimé")
    if not dry_run:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(new_content)
    return log


def fix_reel_path_in_token(fp: str, content: str, dry_run: bool) -> list[str]:
    """Corrige la profondeur relative du reel_path dans 🔑 Token."""
    log = []
    m = re.search(r'^reel_path:\s*(.+)$', content, re.MULTILINE)
    if not m:
        return log

    current_path = m.group(1).strip()
    abs_fp = os.path.normpath(os.path.join(ROOT, fp))
    abs_dir = os.path.dirname(abs_fp)
    token_dir = os.path.join(ROOT, "⚖️ Actes", "🔑 Token")

    if not abs_dir.startswith(token_dir + os.sep) and abs_dir != token_dir:
        log.append(f"  ⚠️  fichier pas sous 🔑 Token, ignoré")
        return log

    # Déduire la cible 👤 Reel depuis le chemin actuel
    # current_path = ../../👤 Reel/rest/of/path.md
    # On extrait rest/of/path.md et on recalcule le relatif correct
    reel_m = re.search(r'👤 Reel/(.+)', current_path)
    if not reel_m:
        return log

    rest = reel_m.group(1)

    # Cible absolue
    target = os.path.normpath(os.path.join(ROOT, "⚖️ Actes", "👤 Reel", rest))
    new_path = os.path.relpath(target, abs_dir)

    if current_path == new_path:
        return log

    # Remplacer la ligne
    before = content[:m.start()]
    after = content[m.end():]
    new_content = before + f"reel_path: {new_path}" + after
    log.append(f"  📍 {current_path} → {new_path}")
    if not dry_run:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(new_content)
    return log


def add_missing_date(fp: str, content: str, yaml_dict: dict, violations: list[dict], dry_run: bool) -> list[str]:
    """Ajoute le champ date manquant ou upgrade FIXME quand possible."""
    log = []
    has_date_issue = any("date" in v.get("msg", "") for v in violations)
    if not has_date_issue:
        return log

    is_fixme = yaml_dict.get("date") == "FIXME"
    if not is_fixme and "date" in yaml_dict and yaml_dict["date"]:
        return log

    # Essayer d'extraire la date depuis le nom du fichier
    basename = os.path.basename(fp).replace(" ", "_")
    # Pattern 1: YYYY-MM-DD ou YYYY_MM_DD
    date_match = re.search(r'(\d{4}[-_]\d{2}[-_]\d{2})', basename)
    if date_match:
        clean = date_match.group(1).replace("_", "-")
        if len(clean.split("-")[0]) == 4:
            insert_date(content, fp, clean, dry_run, log)
            return log
    # Pattern 2: YYYYMMDD compact (ex: 20260711)
    date_match = re.search(r'(\d{8})', basename)
    if date_match:
        raw = date_match.group(1)
        clean = f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"
        insert_date(content, fp, clean, dry_run, log)
        return log

    # Essayer depuis le calendrier Google si non trouvé dans le nom
    # (trop lourd pour batch — on met un placeholder)
    
    # Pour 👤 Reel, essayer de trouver le Token correspondant
    if "👤 Reel" in fp:
        token_fp = fp.replace("👤 Reel", "🔑 Token")
        token_abs = os.path.join(ROOT, token_fp)
        if os.path.exists(token_abs):
            try:
                from yaml_utils import read_frontmatter
                token_meta = read_frontmatter(token_abs)
                if token_meta and token_meta.get("date"):
                    insert_date(content, fp, token_meta["date"], dry_run, log)
                    return log
            except Exception:
                pass

    log.append(f"  ⚠️  date non inférable (laisser FIXME)")
    insert_date(content, fp, "FIXME", dry_run, log)
    return log


def insert_date(content: str, fp: str, date_val: str, dry_run: bool, log: list):
    """Insère date: <val> si elle n'existe pas, ou remplace FIXME."""
    date_line = f"date: {date_val}"

    # Si date: FIXME existe déjà, le remplacer
    fixme_match = re.search(r'^date:\s*FIXME\s*$', content, re.MULTILINE)
    if fixme_match:
        new_content = content[:fixme_match.start()] + date_line + content[fixme_match.end():]
        log.append(f"  📅 FIXME → {date_val}")
        if not dry_run:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_content)
        return

    # Sinon, insérer après la ligne title:
    new_content = re.sub(
        r'^(title:.*)$',
        r'\1\n' + date_line,
        content,
        count=1,
        flags=re.MULTILINE
    )
    log.append(f"  📅 +{date_line}")
    if not dry_run:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(new_content)


def fix_type(fp: str, content: str, yaml_dict: dict, violations: list[dict], dry_run: bool) -> list[str]:
    """Normalise type non canonique."""
    log = []
    current_type = yaml_dict.get("type")
    if not current_type or current_type in CANONICAL_TYPES_SET:
        return log
    if current_type not in TYPE_MAP:
        log.append(f"  ⚠️  type '{current_type}' non mappé, ignoré")
        return log
    new_type = TYPE_MAP[current_type]
    new_content = re.sub(
        r'^type:\s*' + re.escape(current_type) + r'$',
        f"type: {new_type}",
        content,
        flags=re.MULTILINE
    )
    if new_content != content:
        log.append(f"  🏷️  type: {current_type} → {new_type}")
        if not dry_run:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_content)
    return log


def fix_status(fp: str, content: str, yaml_dict: dict, violations: list[dict], dry_run: bool) -> list[str]:
    """Normalise statut non canonique."""
    log = []
    current_status = yaml_dict.get("statut")
    if not current_status or current_status in STATUT_VALUES:
        return log

    new_status = None

    # Chercher dans STATUS_MAP
    if current_status in STATUS_MAP:
        new_status = STATUS_MAP[current_status]
    else:
        # Statuts longs avec — (tiret cadratin)
        for prefix, mapped in LONG_STATUS_PREFIX.items():
            if current_status.startswith(prefix + " —") or current_status.startswith(prefix + " -"):
                new_status = mapped
                break

    if not new_status:
        log.append(f"  ⚠️  statut '{current_status}' non mappé, ignoré")
        return log

    new_content = re.sub(
        r'^statut:\s*' + re.escape(current_status) + r'$',
        f"statut: {new_status}",
        content,
        flags=re.MULTILINE
    )
    if new_content != content:
        log.append(f"  📌 statut: {current_status} → {new_status}")
        if not dry_run:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_content)
    return log


# ── Processeur principal ─────────────────────────────────────────────

DATE_REQUIRED_TYPES = {"courrier", "assignation", "plainte", "attestation", "preuve", "rapport", "loi", "jurisprudence"}


def remove_unneeded_fixme(fp: str, content: str, yaml_dict: dict, dry_run: bool) -> list[str]:
    """Supprime date: FIXME des fichiers qui n'ont pas besoin de date."""
    log = []
    dtype = yaml_dict.get("type", "")
    if dtype in DATE_REQUIRED_TYPES:
        return log
    if yaml_dict.get("date") != "FIXME":
        return log

    new_content = re.sub(r'^date:\s*FIXME\s*\n', '', content, flags=re.MULTILINE)
    if new_content != content:
        log.append(f"  🗑️  date: FIXME supprimé (type '{dtype}' sans obligation de date)")
        if not dry_run:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_content)
    return log


def process_file(fp: str, violations: list[dict], args) -> list[str]:
    abs_fp = os.path.join(ROOT, fp)
    log = [f"{fp}:"]

    try:
        with open(abs_fp, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError) as e:
        log.append(f"  ❌ {e}")
        return log

    from yaml_utils import read_frontmatter
    meta = read_frontmatter(abs_fp)
    if meta is None:
        log.append(f"  ⏭️  pas de frontmatter YAML")
        return log

    if args.dates or args.all:
        log.extend(remove_unneeded_fixme(abs_fp, content, meta, args.dry_run))
        if not args.dry_run:
            with open(abs_fp, "r", encoding="utf-8") as f:
                content = f.read()
                meta = read_frontmatter(abs_fp) or meta

    if args.reel_path or args.all:
        if "👤 Reel" in fp and meta.get("reel_path"):
            log.extend(fix_reel_path_in_reel(abs_fp, content, args.dry_run))
            # Re-read content after modification
            if not args.dry_run:
                with open(abs_fp, "r", encoding="utf-8") as f:
                    content = f.read()
        elif "🔑 Token" in fp and meta.get("reel_path"):
            log.extend(fix_reel_path_in_token(fp, content, args.dry_run))
            if not args.dry_run:
                with open(abs_fp, "r", encoding="utf-8") as f:
                    content = f.read()

    if (args.dates or args.all) and any("date" in v.get("msg", "") for v in violations):
        log.extend(add_missing_date(fp, content, meta, violations, args.dry_run))
        if not args.dry_run:
            with open(abs_fp, "r", encoding="utf-8") as f:
                content = f.read()

    if args.types or args.all:
        log.extend(fix_type(fp, content, meta, violations, args.dry_run))
        if not args.dry_run:
            with open(abs_fp, "r", encoding="utf-8") as f:
                content = f.read()

    if args.statuses or args.all:
        log.extend(fix_status(fp, content, meta, violations, args.dry_run))
        if not args.dry_run:
            with open(abs_fp, "r", encoding="utf-8") as f:
                content = f.read()

    return log


def main():
    parser = argparse.ArgumentParser(description="Correction batch des violations YAML")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Aperçu seulement (défaut)")
    parser.add_argument("--apply", action="store_true", help="Appliquer les corrections")
    parser.add_argument("--all", action="store_true", default=True, help="Toutes les corrections")
    parser.add_argument("--reel-path", action="store_true", help="Corriger reel_path seulement")
    parser.add_argument("--dates", action="store_true", help="Ajouter dates manquantes seulement")
    parser.add_argument("--types", action="store_true", help="Normaliser types seulement")
    parser.add_argument("--statuses", action="store_true", help="Normaliser statuts seulement")
    args = parser.parse_args()

    if args.apply:
        args.dry_run = False

    # Si aucun scope spécifique, tout faire
    scoped = any([args.reel_path, args.dates, args.types, args.statuses])
    if not scoped:
        args.all = True

    print(f"{'🔍 DRY RUN' if args.dry_run else '🛠️  APPLY'} — corrections YAML\n")

    violations_data = get_violations()
    by_file = parse_details(violations_data.get("details", []))

    total_log = []
    files_changed = 0

    for fp in sorted(by_file.keys()):
        v = by_file[fp]
        log = process_file(fp, v, args)
        # Only show files that had actual changes
        change_lines = [l for l in log if l.startswith("  🗑️") or l.startswith("  📍") or l.startswith("  🏷️") or l.startswith("  📌") or l.startswith("  📅") or l.startswith("  ⚠️")]
        if change_lines:
            total_log.append(log)
            files_changed += 1
            print("\n".join(log))
            print()

    # Stats
    stats = {"reel_path_reel": 0, "reel_path_token": 0, "dates": 0, "types": 0, "statuses": 0}
    for log in total_log:
        for l in log:
            if "reel_path supprimé" in l:
                stats["reel_path_reel"] += 1
            elif l.startswith("  📍"):
                stats["reel_path_token"] += 1
            elif l.startswith("  📅"):
                stats["dates"] += 1
            elif l.startswith("  🏷️"):
                stats["types"] += 1
            elif l.startswith("  📌"):
                stats["statuses"] += 1

    print(f"{'='*50}")
    print(f"Fichiers modifiés : {files_changed}")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"Mode : {'DRY RUN' if args.dry_run else 'APPLIQUÉ'}")
    if args.dry_run:
        print(f"\nRelancer avec --apply pour appliquer ces corrections.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
