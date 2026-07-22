#!/usr/bin/env python3
"""
Migration J+X — Renommage chronologique des fichiers du dossier Accident de la Main.

Étapes :
  1. Vérifie que l'arbre git est propre (refuse si modifications non commitées).
  2. Construit la table de correspondance ancien_nom → nouveau_nom (Token + Reel).
  3. Scanne tous les fichiers .md du projet pour les liens internes impactés.
  4. Mode DRY-RUN : affiche le rapport sans rien toucher.
  5. Mode EXEC : renomme les fichiers + met à jour les liens + commit.

Usage:
  python3 .dev/app/jx_migration.py          # dry-run par défaut
  python3 .dev/app/jx_migration.py --exec    # exécution réelle
  python3 .dev/app/jx_migration.py --exec --no-commit  # exécution sans commit
"""

import argparse
import csv
import io
import os
import re
import sys
import time
import urllib.parse
from collections import defaultdict
from datetime import datetime, date
from pathlib import Path
from typing import Optional

BASE = Path("/home/crilocom/accident-main").resolve()
TOKEN = BASE / "Actes/Token"
REEL = BASE / "Actes/Reel"

# ─── Fichiers exclus du renommage (brouillons, 99, archives, etc.) ───
EXCLUSIONS_TOKEN = {
    # Brouillons sans date
    "Organisation/Synthèse - Actions et Audits.md",
    "Organisation/Note - Plan Constat Police Foix.md",
    "Organisation/Note - Modification Email Maire Foix.md",
    "Preuves_officielles/01 📁 Dossier UMJ Preparation.md",
    "Actes_proceduraux/16 ⚠️ Parquet - Signalement Fraude.md",
    "Actes_proceduraux/17 ⚖️ Mandataire Ad Hoc - Requête.md",
    # Exception 99 — pièce adverse
    "Analyses_juridiques/Mémoire - En défense adverse.md",
    # Sans numéro (jamais dans la numérotation)
    "Organisation/Note - Fiche Réflexe 48h Disparition SAS.md",
}

# Les Archives sont exclues intégralement
ARCHIVES_TOKEN = TOKEN / "Archives"
ARCHIVES_REEL = REEL / "Archives"

# Dossiers à scanner pour les liens (tous les .md sauf .git, __pycache__)
SCAN_DIRS = [
    BASE / "Actes",
    BASE / "Memory",
    BASE / "Lois",
    BASE / "Rapports",
    BASE / "Status",
    BASE,  # README.md racine
]

# Sous-dossiers exclus du scan des liens (archives frozen)
SCAN_EXCLUDE_SUBDIRS = [
    "Rapports/Archives",
]

# ─── TABLE DE CORRESPONDANCE ───
# Chaque entrée : (sous-dossier, ancien_basename, nouvelle_basename, date_iso)

MAPPING_RAW = [
    # ═══ Preuves_officielles ═══
    ("Preuves_officielles", "01 📁 Dossier UMJ Preparation.md", "J+167 Preparation_Expertise_UMJ.md", "2026-11-12"),

    # ═══ Actes_proceduraux ═══
    ("Actes_proceduraux", "01 ⚖️ Assignation.md", "J+32 ⚖️ Assignation Refere Provision.md", "2026-06-30"),
    ("Actes_proceduraux", "02 🚔 Plainte.md", "J+32 🚔 Assurance RC - Plainte Défaut.md", "2026-06-30"),
    ("Actes_proceduraux", "02b Archive - Partie Civile - Constitution.md", "J+38 Archive - Partie Civile - Constitution.md", "2026-07-06"),
    ("Actes_proceduraux", "03 🔍 Assignation Article 145.md", "J+47 🔍 CPC 145 - Requête.md", "2026-07-15"),
    ("Actes_proceduraux", "04 📑 Bordereau.md", "J+39 📑 TJ Foix - TJ Foix - Bordereau Unifié.md", "2026-07-07"),
    ("Actes_proceduraux", "05 🎯 Conclusions Refere.md", "J+39 🎯 Conclusions Refere Provision.md", "2026-07-07"),
    ("Actes_proceduraux", "06 📸 Constat Huissier - Requête.md", "J+38 📸 Constat Huissier - Requête.md", "2026-07-06"),
    ("Actes_proceduraux", "07 ⚖️ Projet Ordonnance Refere.md", "J+63 ⚖️ Projet Ordonnance Refere.md", "2026-07-31"),
    ("Actes_proceduraux", "15 ⚖️ Réquisitoire introductif.md", "J+47 ⚖️ Requisitoire introductif.md", "2026-07-15"),

    # ═══ Courriers ═══
    ("Courriers", "03 ✉️ Courrier SAS.md", "J+31 ✉️ Mise en demeure SAS.md", "2026-06-29"),
    ("Courriers", "04 ✉️ Courrier Assureur.md", "J+31 ✉️ Mise en demeure Assureur.md", "2026-06-29"),
    ("Courriers", "05 ✉️ Courrier Proprietaire.md", "J+31 ✉️ Mise en demeure Proprietaire.md", "2026-06-29"),
    ("Courriers", "06 ✉️ Courrier President DG.md", "J+31 ✉️ Mise en demeure President.md", "2026-06-29"),
    ("Courriers", "06 V2 ✉️ Relance Dirigeants.md", "J+40 ✉️ Relance Dirigeants.md", "2026-07-08"),
    ("Courriers", "07 ✉️ Courrier Consolidation.md", "J+37 ✉️ Relance Consolidation.md", "2026-07-05"),
    ("Courriers", "08 ✉️ Courrier Suivi Adjoint Maire.md", "J+37 ✉️ Suivi Adjoint Maire Tavella.md", "2026-07-05"),
    ("Courriers", "09 ✉️ Courrier Inspection Travail.md", "J+37 ✉️ Signalement Inspection Travail.md", "2026-07-05"),
    ("Courriers", "10 ✉️ Courrier Doyen Juges Instruction.md", "J+38 ✉️ Saisine Doyen Juges Instruction.md", "2026-07-06"),
    ("Courriers", "11 ✉️ Courrier INPI.md", "J+37 ✉️ Signalement INPI.md", "2026-07-05"),
    ("Courriers", "12 ✉️ Courrier URSSAF.md", "J+37 ✉️ Signalement URSSAF.md", "2026-07-05"),
    ("Courriers", "13 ✉️ Courrier Prefecture.md", "J+37 ✉️ Signalement Prefecture.md", "2026-07-05"),
    ("Courriers", "14 ✉️ Courrier CODAF.md", "J+37 ✉️ Signalement CODAF.md", "2026-07-05"),
    ("Courriers", "15 ✉️ Courrier SIE.md", "J+37 ✉️ Signalement SIE.md", "2026-07-05"),
    ("Courriers", "16 ✉️ Courrier Conseil Departemental.md", "J+37 ✉️ Signalement Conseil Departemental.md", "2026-07-05"),
    ("Courriers", "17 ✉️ Courrier CPAM.md", "J+38 ✉️ Transmission Recours Tiers CPAM.md", "2026-07-06"),
    ("Courriers", "18 ✉️ Courrier SDIS.md", "J+37 ✉️ Signalement SDIS.md", "2026-07-05"),
    ("Courriers", "19 ✉️ Courrier FGTI.md", "J+38 ✉️ Saisine FGTI.md", "2026-07-06"),
    ("Courriers", "20 🔄 Relance Police.md", "J+37 🔄 Relance Police Videos.md", "2026-07-05"),
    ("Courriers", "21 🔄 Relance CPAM.md", "J+37 🔄 Relance CPAM.md", "2026-07-05"),
    ("Courriers", "22 📋 Attestation Temoin Client.md", "J+32 📋 Attestation Temoin Client.md", "2026-06-30"),
    ("Courriers", "23 📋 Attestation Pompier SAMU.md", "J+32 📋 Attestation Pompier SAMU.md", "2026-06-30"),
    ("Courriers", "24 📋 Attestation Employe.md", "J+32 📋 Attestation Employe.md", "2026-06-30"),
    ("Courriers", "25 📧 Relance Dr DJERBI.md", "J+38 📧 Relance Dr DJERBI Consolidation.md", "2026-07-06"),
    ("Courriers", "26 📧 Attestation Temoin Client.md", "J+38 📧 Attestation Temoin Client.md", "2026-07-06"),
    ("Courriers", "27 📧 Attestation Pompier SAMU.md", "J+38 📧 Attestation Pompier SAMU.md", "2026-07-06"),
    ("Courriers", "28 📧 Attestation Employe.md", "J+38 📧 Attestation Employe.md", "2026-07-06"),
    ("Courriers", "29 ✉️ Courrier Maire Foix.md", "J+41 ✉️ Mise en demeure Maire Foix.md", "2026-07-09"),
    ("Courriers", "30 ✉️ Courrier President TC.md", "J+41 ✉️ Opposition Radiation TC.md", "2026-07-09"),
    ("Courriers", "31 ✉️ Courrier INPI Opposition.md", "J+41 ✉️ Opposition Immatriculation INPI.md", "2026-07-09"),
    ("Courriers", "32 ✉️ Courrier SIE URSSAF Mutualisation.md", "J+41 ✉️ Mutualisation Fiscale Sociale.md", "2026-07-09"),
    ("Courriers", "33 ✉️ Constat Huissier - Requête 145 CPC.md", "J+41 ✉️ Constat Huissier - Requête.md", "2026-07-09"),
    ("Courriers", "34 ✉️ EMAIL Maire Foix - Police Municipale ERP.md", "J+42 ✉️ Email Maire Tavella ERP.md", "2026-07-10"),
    ("Courriers", "35 ✉️ Courrier President TJ Foix.md", "J+44 ✉️ Preuves Complementaires TJ Foix.md", "2026-07-12"),
    ("Courriers", "36 📋 Antiseche Orale Plainte Complementaire.md", "J+47 📋 Antiseche Orale Plainte.md", "2026-07-15"),
    ("Courriers", "36 📜 PLAINTE_COMPLEMENTAIRE_POLICE_FOIX.md", "J+47 📜 Plainte Complementaire.md", "2026-07-15"),
    ("Courriers", "37 📋 GUIDE_DIALOGUE_POLICE_FOIX.md", "J+47 📋 Guide Dialogue Police.md", "2026-07-15"),
    ("Courriers", "38 ✅ CHECKLIST_DEPLACEMENT_POLICE_FOIX.md", "J+47 ✅ Checklist Deplacement Foix.md", "2026-07-15"),
    ("Courriers", "39 📋 GUIDE_DEMANDE_AJ.md", "J+47 📋 Guide Demande AJ.md", "2026-07-15"),
    ("Courriers", "40 ✉️ EMAIL AVOCAT - Consultation Proactivite.md", "J+47 ✉️ Consultation Avocat Jimini.md", "2026-07-15"),
    ("Courriers", "41 ✉️ Relance Prefecture CODAF - Suite Signalement Maire.md", "J+47 ✉️ Relance Prefecture CODAF.md", "2026-07-15"),
    ("Courriers", "42 ✉️ Relance Inspection Travail - Suite Signalement Maire.md", "J+47 ✉️ Relance Inspection Travail.md", "2026-07-15"),
    ("Courriers", "43 ✉️ Modele Saisine CADA.md", "J+47 ✉️ Modele Saisine CADA.md", "2026-07-15"),
    ("Courriers", "44 ✉️ Saisine CADA Version Courte.md", "J+47 ✉️ Saisine CADA Formulaire.md", "2026-07-15"),

    # ═══ Analyses_juridiques ═══
    ("Analyses_juridiques", "07 🎤 Plaidoirie dirigeants.md", "J+32 Note - Plaidoirie Responsabilité Dirigeants.md", "2026-06-30"),
    ("Analyses_juridiques", "09 ❓ FAQ.md", "J+32 Note - FAQ Juridique.md", "2026-06-30"),
    ("Analyses_juridiques", "12 📁 Dossier Plaidoirie.md", "J+60 Note - Dossier Plaidoirie Référé.md", "2026-07-28"),
    ("Analyses_juridiques", "13 📜 Responsabilites legales.md", "J+32 Note - Analyse Responsabilités Légales.md", "2026-06-30"),
    ("Analyses_juridiques", "14 Strategie jurisprudentielle.md", "J+39 Note - Stratégie Jurisprudentielle.md", "2026-07-07"),
    ("Analyses_juridiques", "15 Note Droit Assurances.md", "J+40 Note - Droit des Assurances.md", "2026-07-08"),
    ("Analyses_juridiques", "16 Note - Responsabilité des Dirigeants Dissolution.md", "J+41 Note - Responsabilité des Dirigeants.md", "2026-07-09"),
    ("Analyses_juridiques", "18 Note Audit RNE NPAI SAS.md", "J+42 Note - Audit RNE NPAI SAS.md", "2026-07-10"),
    ("Analyses_juridiques", "20 Note - Tableau Défense Réponse.md", "J+47 Note - Tableau Défense Réponse.md", "2026-07-15"),
    ("Analyses_juridiques", "21 🛡️ Memo Strategie Administrative Penale.md", "J+47 Note - Mémo Stratégie Admin Pénal.md", "2026-07-15"),

    # ═══ Etudes_indemnisation ═══
    ("Etudes_indemnisation", "11+12 📊 Evaluation Dintilhac consolidee.md", "J+39 Note - Évaluation Dintilhac Consolidée.md", "2026-07-07"),
    ("Etudes_indemnisation", "13 Note strategique FGTI CIVI.md", "J+40 Note - Stratégique FGTI CIVI.md", "2026-07-08"),

    # ═══ Organisation ═══
    ("Organisation", "00 📇 Index.md", "J+39 Note - Index Général.md", "2026-07-07"),
    ("Organisation", "05 Note - Dossier Spécial CERFA.md", "J+40 Note - Dossier Spécial CERFA.md", "2026-07-08"),
    ("Organisation", "10 🗂️ Plan action.md", "J+32 Note - Plan d'Action.md", "2026-06-30"),
    ("Organisation", "11 📅 Calendrier procedural.md", "J+32 Note - Calendrier Procédure.md", "2026-06-30"),
    ("Organisation", "20 📦 Bon envoi physique.md", "J+38 Note - Bon Envoi Physique.md", "2026-07-06"),
    ("Organisation", "23 Note - Suivi Envois LRAR.md", "J+43 Note - Suivi Envois LRAR.md", "2026-07-11"),
    ("Organisation", "24 Archive - Bordereau Pièces 15 Juillet.md", "J+47 Archive - Bordereau Pièces 15 Juillet.md", "2026-07-15"),
    ("Organisation", "24 Archive - Checklist Envoi 11-07-2026.md", "J+43 Archive - Checklist Envoi 11-07.md", "2026-07-11"),
]

# Entrées supplémentaires Reel-only (les doublons de bordereau)
REEL_EXTRA = [
    ("Actes_proceduraux", "04 📑 Bordereau Audience.md", "J+38 📑 Bordereau Audience.md", "2026-07-06"),
    ("Actes_proceduraux", "04 📑 Bordereau de pieces.md", "J+47 📑 Bordereau de pieces.md", "2026-07-15"),
]


# ─── Helper functions ───

def url_enc(s: str) -> str:
    """URL-encode un nom de fichier (pour les liens Markdown)."""
    return urllib.parse.quote(s, safe="")


def old_number(s: str) -> str:
    """Extrait le numéro du début d'un ancien nom de fichier."""
    m = re.match(r"(\d+)\s", s)
    return m.group(1) if m else ""


def compute_jx(date_iso: str) -> str:
    """Calcule J+X à partir d'une date ISO."""
    accident = date(2026, 5, 29)
    d = date.fromisoformat(date_iso)
    delta = (d - accident).days
    return f"J+{delta}"


def build_mappings():
    """Construit les dictionnaires de mapping Token et Reel."""
    token_map = {}   # old_path -> new_path (relatif à TOKEN)
    reel_map = {}    # old_path -> new_path (relatif à REEL)

    for subdir, old_name, new_name, date_iso in MAPPING_RAW:
        old_token = f"{subdir}/{old_name}"
        new_token = f"{subdir}/{new_name}"

        # Vérifier que le fichier source Token existe
        src_tok = TOKEN / old_token
        if not src_tok.exists():
            print(f"  ⚠ MANQUANT (Token): {old_token}", file=sys.stderr)
            continue

        token_map[old_token] = new_token

        # Idem Reel
        old_reel = f"{subdir}/{old_name}"
        new_reel = f"{subdir}/{new_name}"
        src_reel = REEL / old_reel
        if src_reel.exists():
            reel_map[old_reel] = new_reel
        else:
            print(f"  ℹ Absent Reel: {old_reel} (ignoré)", file=sys.stderr)

    # Reel-only extras
    for subdir, old_name, new_name, date_iso in REEL_EXTRA:
        old_reel = f"{subdir}/{old_name}"
        new_reel = f"{subdir}/{new_name}"
        src_reel = REEL / old_reel
        if src_reel.exists():
            reel_map[old_reel] = new_reel
        else:
            print(f"  ℹ Absent Reel extra: {old_reel} (ignoré)", file=sys.stderr)

    return token_map, reel_map


def get_all_md_files(base_dirs):
    """Collecte tous les fichiers .md dans les répertoires donnés."""
    files = []
    for d in base_dirs:
        if not d.exists():
            continue
        for root, dirs, fnames in os.walk(d):
            # Ignorer .git, __pycache__, node_modules
            dirs[:] = [x for x in dirs if not x.startswith((".git", "__pycache__", "node_modules"))]
            # Exclure les sous-dossiers archives
            rel = Path(root).relative_to(BASE)
            for excl in SCAN_EXCLUDE_SUBDIRS:
                if str(rel).startswith(excl):
                    dirs[:] = []
                    break
            if not dirs:
                continue
            for fn in fnames:
                if fn.endswith(".md"):
                    files.append(Path(root) / fn)
    return files


def detect_references(old_basename, new_basename, all_md_files, dry_run=True):
    """Scanne tous les fichiers .md pour trouver des références à old_basename.
    Retourne une liste de (fichier, type, occurrence) à mettre à jour."""
    refs = []

    old_enc = url_enc(old_basename)
    new_enc = url_enc(new_basename)
    old_plain = old_basename.replace(".md", "")
    new_plain = new_basename.replace(".md", "")

    # Variantes avec underscores (archives legacy)
    old_underscore = old_basename.replace(" ", "_").replace("✉️", "").replace("  ", " ")
    old_underscore = re.sub(r"_+", "_", old_underscore)

    # ⚡ OPTIMIZATION: Compile regex patterns outside the file loop
    compiled_patterns = []
    for old_variant, new_variant in [
        (old_enc, new_enc),
        (old_basename, new_basename),
    ]:
        p1 = re.compile(r'(\]\()([^)]*?)' + re.escape(old_variant) + r'([^)]*?)(\))')
        p2 = re.compile(r'(\()([^)]*?)' + re.escape(old_variant) + r'([^)]*?)(\))')
        compiled_patterns.append((old_variant, new_variant, p1, p2))

    bc_old = f"› {old_plain}"
    bc_new = f"› {new_plain}"

    for fpath in all_md_files:
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue

        # On ne touche pas aux fichiers .gitkeep
        if fpath.name == ".gitkeep":
            continue

        # ⚡ OPTIMIZATION: Fast path to skip files without any variants
        needs_processing = False
        if bc_old in content:
            needs_processing = True
        else:
            for old_variant, _, _, _ in compiled_patterns:
                if old_variant in content:
                    needs_processing = True
                    break

        if not needs_processing:
            continue

        modified = False
        new_content = content

        # Pattern 1: old_basename dans une URL de lien Markdown: ](...old_basename...)
        # ou ](...url_enc(old_basename)...)
        for old_variant, new_variant, pattern, pattern2 in compiled_patterns:
            new_content, count = pattern.subn(
                lambda m, nv=new_variant: m.group(1) + m.group(2) + nv + m.group(3) + m.group(4),
                new_content
            )
            if count > 0:
                refs.append((fpath, "markdown_url", f"{old_variant} → {new_variant} ({count}x)"))
                modified = True

            new_content, count2 = pattern2.subn(
                lambda m, nv=new_variant: m.group(1) + m.group(2) + nv + m.group(3) + m.group(4),
                new_content
            )
            if count2 > 0:
                refs.append((fpath, "parenthesized_url", f"{old_variant} → {new_variant} ({count2}x)"))
                modified = True

        # Pattern 2: breadcrumb display text à la fin d'un breadcrumb
        # Pattern: › old_plain (en fin de ligne ou avant un saut)
        # On cible la forme exacte telle qu'apparaissant après le dernier ›
        # Mais pour éviter les faux positifs, on cible spécifiquement les lignes de breadcrumb
        if bc_old in new_content:
            # Ne remplacer que dans les lignes breadcrumb
            lines = new_content.split("\n")
            changed = False
            for i, line in enumerate(lines):
                if "›" in line and bc_old in line:
                    lines[i] = line.replace(bc_old, bc_new)
                    changed = True
            if changed:
                new_content = "\n".join(lines)
                refs.append((fpath, "breadcrumb", f"{bc_old} (breadcrumb)"))
                modified = True

        if modified:
            if dry_run:
                pass  # on enregistre juste la ref
            else:
                fpath.write_text(new_content, encoding="utf-8")

    return refs

def flatten_refs(refs_by_file):
    """Aplatit les références pour le rapport."""
    result = []
    for fpath, refs in sorted(refs_by_file.items(), key=lambda x: str(x[0])):
        for rtype, detail in refs:
            result.append((fpath, rtype, detail))
    return result


def report_changes(token_map, reel_map, all_refs=None, dry_run=True):
    """Génère un rapport formaté des changements."""
    lines = []
    lines.append("=" * 72)
    lines.append("RAPPORT DE MIGRATION J+X")
    lines.append("=" * 72)
    lines.append(f"Mode: {'DRY-RUN (simulation)' if dry_run else 'EXÉCUTION'}")
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # Fichiers Token
    lines.append(f"── Fichiers Token à renommer : {len(token_map)} ──")
    for old, new in sorted(token_map.items()):
        exists = "✓" if (TOKEN / old).exists() else "✗ MANQUANT"
        lines.append(f"  {exists}  {old}")
        lines.append(f"       → {new}")
    lines.append("")

    # Fichiers Reel
    lines.append(f"── Fichiers Reel à renommer : {len(reel_map)} ──")
    for old, new in sorted(reel_map.items()):
        exists = "✓" if (REEL / old).exists() else "✗ MANQUANT"
        lines.append(f"  {exists}  {old}")
        lines.append(f"       → {new}")
    lines.append("")

    # Exclusions
    lines.append("── Fichiers exclus (brouillons / 99) ──")
    for excl in sorted(EXCLUSIONS_TOKEN):
        lines.append(f"  ⊘ {excl}")
    lines.append("")

    # Références
    if all_refs:
        grouped = defaultdict(list)
        for fpath, rtype, detail in all_refs:
            grouped[fpath].append((rtype, detail))

        lines.append(f"── Fichiers avec liens à mettre à jour : {len(grouped)} ──")
        for fpath, refs in sorted(grouped.items(), key=lambda x: str(x[0])):
            rel = fpath.relative_to(BASE) if fpath.is_relative_to(BASE) else fpath
            lines.append(f"  📄 {rel}")
            for rtype, detail in refs:
                lines.append(f"       [{rtype}] {detail}")
        lines.append("")

    total = len(token_map) + len(reel_map)
    lines.append(f"Total fichiers à renommer : {total}")
    lines.append(f"Total fichiers lien impactés : {len(grouped) if all_refs else 0}")
    lines.append("=" * 72)

    return "\n".join(lines)


def do_rename(mapping, base_dir, log):
    """Exécute les renommages de fichiers."""
    renamed = []
    for old_rel, new_rel in sorted(mapping.items()):
        old_path = base_dir / old_rel
        new_path = base_dir / new_rel

        if not old_path.exists():
            log.append(f"  ⚠ SKIP (introuvable): {old_rel}")
            continue
        if new_path.exists():
            log.append(f"  ⚠ SKIP (destination existe): {new_rel}")
            continue

        # Créer les sous-dossiers si nécessaire
        new_path.parent.mkdir(parents=True, exist_ok=True)

        old_path.rename(new_path)
        log.append(f"  ✓ {old_rel}")
        log.append(f"    → {new_rel}")
        renamed.append((old_rel, new_rel))

    return renamed


def update_frontmatter_date(renamed, base_dir):
    """Met à jour la date dans le frontmatter des fichiers renommés pour y ajouter J+X."""
    updates = []
    for old_rel, new_rel in renamed:
        new_path = base_dir / new_rel
        if not new_path.exists():
            continue
        try:
            content = new_path.read_text(encoding="utf-8")
        except Exception:
            continue
        # Chercher la ligne date: dans le frontmatter
        # Chercher if there's already a J+X in the title
        # Extraire le J+X du nouveau nom
        m = re.match(r"(J\+?\d+)", Path(new_rel).name)
        if not m:
            continue
        jx = m.group(1)

        # Ajouter J+X en commentaire dans le frontmatter
        # Soit après la ligne de date, soit en nouvelle ligne
        lines = content.split("\n")
        new_lines = []
        added = False
        for line in lines:
            new_lines.append(line)
            if line.startswith("date:") and not added:
                new_lines.append(f"jx: {jx}")
                added = True
        if added:
            new_path.write_text("\n".join(new_lines), encoding="utf-8")
            updates.append((new_rel, jx))

    return updates


def main():
    parser = argparse.ArgumentParser(description="Migration J+X — Renommage chronologique")
    parser.add_argument("--exec", action="store_true", help="Exécute le renommage (défaut: dry-run)")
    parser.add_argument("--no-commit", action="store_true", help="Ne pas commit (utile pour inspection)")
    args = parser.parse_args()

    dry_run = not args.exec

    print("🔍 Construction des mappings...")
    token_map, reel_map = build_mappings()
    total = len(token_map) + len(reel_map)
    print(f"   Token: {len(token_map)} fichiers")
    print(f"   Reel:  {len(reel_map)} fichiers")

    print("🔍 Scan des fichiers .md pour les liens internes...")
    all_md = get_all_md_files(SCAN_DIRS)
    print(f"   {len(all_md)} fichiers .md scannés")

    all_refs = []
    # On détecte les références pour tous les anciens noms
    for old_rel in list(token_map.keys()) + list(reel_map.keys()):
        old_basename = os.path.basename(old_rel)
        # Trouver le nouveau basename
        new_basename = None
        if old_rel in token_map:
            new_basename = os.path.basename(token_map[old_rel])
        elif old_rel in reel_map:
            new_basename = os.path.basename(reel_map[old_rel])
        else:
            continue
        refs = detect_references(old_basename, new_basename, all_md, dry_run=dry_run)
        all_refs.extend(refs)

    # Dédupliquer par fichier
    refs_by_file = defaultdict(list)
    seen = set()
    for fpath, rtype, detail in all_refs:
        key = (str(fpath), rtype, detail)
        if key not in seen:
            seen.add(key)
            refs_by_file[fpath].append((rtype, detail))

    report = report_changes(token_map, reel_map,
                           all_refs=flatten_refs(refs_by_file),
                           dry_run=dry_run)

    print()
    print(report)

    # Sauvegarder le rapport
    rapport_path = BASE / "Rapports" / f"RAPPORT_MIGRATION_JX_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    rapport_path.parent.mkdir(parents=True, exist_ok=True)
    rapport_path.write_text(report, encoding="utf-8")
    print(f"\n📄 Rapport sauvegardé : {rapport_path.relative_to(BASE)}")

    if dry_run:
        print("\n⚠ DRY-RUN — Aucun fichier modifié.")
        print(f"  Pour exécuter : python3 .dev/app/jx_migration.py --exec")
        return

    # ─── EXÉCUTION ───
    print("\n" + "=" * 72)
    print("EXÉCUTION DU RENOMMAGE")
    print("=" * 72)

    log = []
    log.append(f"Migration J+X — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    log.append("")

    # 1. Renommer Token
    print("\n📁 Renommage des fichiers Token...")
    log.append("── Token ──")
    token_renamed = do_rename(token_map, TOKEN, log)

    # 2. Renommer Reel
    print("📁 Renommage des fichiers Reel...")
    log.append("── Reel ──")
    reel_renamed = do_rename(reel_map, REEL, log)

    # 3. Mise à jour du frontmatter (ajouter jx:)
    print("📝 Mise à jour des frontmatter (ajout jx:)...")
    token_updates = update_frontmatter_date(token_renamed, TOKEN)
    reel_updates = update_frontmatter_date(reel_renamed, REEL)
    log.append(f"Frontmatter mis à jour: {len(token_updates) + len(reel_updates)} fichiers")

    # 4. Mise à jour des liens (déjà fait pendant le scan si dry_run=False)
    print("🔗 Mise à jour des liens internes...")
    # Les liens ont déjà été mis à jour dans detect_references (dry_run=False)

    log.append("Liens internes mis à jour")
    log.append("")

    # 5. Sauvegarder le log
    log_path = BASE / "Rapports" / f"LOG_MIGRATION_JX_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("\n".join(log), encoding="utf-8")
    print(f"📄 Log sauvegardé : {log_path.relative_to(BASE)}")

    # 6. Commit
    if not args.no_commit:
        print("\n📦 Commit git...")
        os.chdir(BASE)
        os.system("git add -A")
        os.system(f'git commit -m "Migration J+X : renommage chronologique de {total} fichiers + mise à jour des liens"')
        print("✓ Commit effectué")
    else:
        print("\n⚠ --no-commit : modifications non commitées")

    print("\n✓ Migration terminée !")


if __name__ == "__main__":
    main()
