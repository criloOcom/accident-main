#!/usr/bin/env python3
"""
link_documents.py  —  Navigation Interactive Cross-Document

Replaces textual mentions of evidence documents, anonymization tokens and
temporal markers with relative Markdown links to their corresponding .md files.

Usage:
    python3 .dev/app/link_documents.py [--dry-run]
                                       [--strate {token,reel,all}]
                                       [--verbose]

Examples:
    # Preview all changes for Token strate
    python3 .dev/app/link_documents.py --dry-run --strate token

    # Apply changes to both strates
    python3 .dev/app/link_documents.py --strate all
"""

import re
import argparse
from pathlib import Path
from urllib.parse import quote
from collections import defaultdict

# ─── Base paths ──────────────────────────────────────────────────────────
BASE = Path("/home/crilocom/accident-main")
TOKEN_MAP_PATH = "Memory/TOKEN MAP.md"
TOKEN_DIR = "Actes/Token"
REEL_DIR = "Actes/Reel"

# ══════════════════════════════════════════════════════════════════════════
# CONFIGURATION — Document mentions → target .md file
# ══════════════════════════════════════════════════════════════════════════
# Each entry: (regex, target_relpath, label)
#   regex         — compiled pattern to search for
#   target_relpath— path relative to BASE of the target .md file
#   label         — short description for dry-run output

DOC_MENTIONS = [
    # ── Police PV n°2026/015967 ──────────────────────────────────────────
    (re.compile(r'PV n°2026/015967'),
     "Actes/Preuves officielles/20260602_Police_PV/20260602 PV Police PV n°2026-015967 AccidentSalonCoiffure.md",
     "PV police n°2026/015967"),

    (re.compile(r'PV n° \[N° PV Police\]'),
     "Actes/Preuves officielles/20260602_Police_PV/20260602 PV Police PV n°2026-015967 AccidentSalonCoiffure.md",
     "PV police (tokenisé)"),

    (re.compile(r'procès-verbal(?: de constat)? n°2026/015967', re.IGNORECASE),
     "Actes/Preuves officielles/20260602_Police_PV/20260602 PV Police PV n°2026-015967 AccidentSalonCoiffure.md",
     "Procès-verbal n°2026/015967"),

    (re.compile(r'PV n°2026-015967'),
     "Actes/Preuves officielles/20260602_Police_PV/20260602 PV Police PV n°2026-015967 AccidentSalonCoiffure.md",
     "PV n°2026-015967"),

    # ── Extrait Kbis ─────────────────────────────────────────────────────
    (re.compile(r'Extrait Kbis(?:(?: de la SAS)?(?: \[.*?\]|\s*\*\*\[.*?\]\*\*))?', re.IGNORECASE),
     "Actes/Preuves officielles/20260601_Kbis/20260601-xxxx Extrait Kbis SAS MauvaisGarcons.md",
     "Extrait Kbis"),

    (re.compile(r'extrait Kbis', re.IGNORECASE),
     "Actes/Preuves officielles/20260601_Kbis/20260601-xxxx Extrait Kbis SAS MauvaisGarcons.md",
     "extrait Kbis"),

    # ── CR opératoire / compte-rendu opératoire / rapport intervention ───
    (re.compile(r'CR opératoire', re.IGNORECASE),
     "Actes/Preuves officielles/20260530 🆘 SOSMain/20260530 CR Opératoire RapportInterventionMainDroite.md",
     "CR opératoire SOS Main"),

    (re.compile(r'compte-rendu opératoire', re.IGNORECASE),
     "Actes/Preuves officielles/20260530 🆘 SOSMain/20260530 CR Opératoire RapportInterventionMainDroite.md",
     "compte-rendu opératoire"),

    (re.compile(r'rapport intervention', re.IGNORECASE),
     "Actes/Preuves officielles/20260530 🆘 SOSMain/20260530 CR Opératoire RapportInterventionMainDroite.md",
     "rapport intervention"),

    # ── Certificat médical initial (Dr JARDON) ──────────────────────────
    (re.compile(r'(?:Certificat médical initial|premiers soins)(?: d\'urgence| urgence)?', re.IGNORECASE),
     "Actes/Preuves officielles/20260529_DrJARDON/20260529-1630 SITUATION DrJulieJARDON.md",
     "Certificat médical initial Dr JARDON"),

    # ── Ordonnance de sortie ─────────────────────────────────────────────
    (re.compile(r'Ordonnance de sortie', re.IGNORECASE),
     "Actes/Preuves officielles/20260530 🆘 SOSMain/20260530-1700 Ordonnance Sortie DrDJERBI.md",
     "Ordonnance de sortie"),

    # ── Arrêt de travail ─────────────────────────────────────────────────
    (re.compile(r'Arrêt de travail', re.IGNORECASE),
     "Actes/Preuves officielles/20260601_DrOXYBEL/20260601-1115 ARRET Travail Volet1 DrOXYBEL.md",
     "Arrêt de travail (volet 1)"),

    (re.compile(r'arrêts de travail', re.IGNORECASE),
     "Actes/Preuves officielles/20260601_DrOXYBEL/20260601-1115 ARRET Travail Volet1 DrOXYBEL.md",
     "arrêts de travail"),

    # ── Dossier CPAM / RCT ───────────────────────────────────────────────
    (re.compile(r'Dossier CPAM(?: n° \[N° Dossier CPAM\])?', re.IGNORECASE),
     "Actes/Preuves officielles/20260603_Attestation_DEPOT/20260603-2046 DOSSIER 31727387 AttestationDepot.md",
     "Dossier CPAM"),

    (re.compile(r'dossier RCT(?: n° 31727387)?', re.IGNORECASE),
     "Actes/Preuves officielles/20260603_Attestation_DEPOT/20260603-2046 DOSSIER 31727387 AttestationDepot.md",
     "Dossier RCT"),

    # ── Constitution de partie civile ────────────────────────────────────
    # NOTE: double strate — le script choisit token/reel selon le contexte
    (re.compile(r'Constitution de partie civile', re.IGNORECASE),
     "Actes/STRATE/Actes_proceduraux/J+38 Archive - Partie Civile - Constitution.md",
     "Constitution de partie civile"),

    # ── Mise en demeure SAS ──────────────────────────────────────────────
    # NOTE: double strate — le script choisit token/reel selon le contexte
    (re.compile(r'Mise en demeure SAS(?:(?: LES MAUVAIS GARCONS?)?)', re.IGNORECASE),
     "Actes/STRATE/Courriers/J+31 ✉️ Mise en demeure SAS.md",
     "Mise en demeure SAS"),

    # ── Facture médicaments ──────────────────────────────────────────────
    (re.compile(r'Facture médicaments', re.IGNORECASE),
     "Actes/Preuves officielles/20260529_Pharmacie_Foix/20260529-1800 Facture Medicaments PharmacieFoix.md",
     "Facture médicaments"),

    # ── Facture chirurgie ─────────────────────────────────────────────────
    (re.compile(r'[Ff]acture chirurgie'),
     "Actes/Preuves officielles/20260610_SOSMain_Facture/20260610-xxxx Facture Chirurgie SOSMain 790euros.md",
     "Facture chirurgie"),

    # ── Attestation de vigilance URSSAF ──────────────────────────────────
    (re.compile(r'Attestation(?:s)? de vigilance(?: URSSAF)?', re.IGNORECASE),
     "Actes/Preuves officielles/20260604_URSSAF_Attestations/20260604-xxxx Attestation Vigilance URSSAF 1.md",
     "Attestation de vigilance URSSAF"),

    # ── Avis de situation INSEE / SAS ────────────────────────────────────
    (re.compile(r'Avis de situation SAS', re.IGNORECASE),
     "Actes/Preuves officielles/20260601 🇫🇷 INSEE INPI/20260601-xxxx Avis Situation SAS INSEE.md",
     "Avis de situation INSEE"),

    (re.compile(r'Avis de situation INSEE', re.IGNORECASE),
     "Actes/Preuves officielles/20260601 🇫🇷 INSEE INPI/20260601-xxxx Avis Situation SAS INSEE.md",
     "Avis de situation INSEE"),

    # ── Fiche identité SAS / INPI ────────────────────────────────────────
    (re.compile(r'Fiche identité SAS', re.IGNORECASE),
     "Actes/Preuves officielles/20260601 🇫🇷 INSEE INPI/20260601-xxxx Fiche Identite SAS INPI.md",
     "Fiche identité INPI"),

    (re.compile(r'Fiche identité INPI', re.IGNORECASE),
     "Actes/Preuves officielles/20260601 🇫🇷 INSEE INPI/20260601-xxxx Fiche Identite SAS INPI.md",
     "Fiche identité INPI"),
]

# ══════════════════════════════════════════════════════════════════════════
# CONFIGURATION — Token → TOKEN MAP anchor
# ══════════════════════════════════════════════════════════════════════════
# Each entry: (token_text, anchor_id)
#   token_text  — the text between `**` and `**` in `**[token_text]**`
#   anchor_id   — anchor in TOKEN MAP.md (without #)

TOKEN_ANCHORS = [
    # ── Personnes physiques ──────────────────────────────────────────────
    ("La Victime",                     "personnes-physiques"),
    ("LA VICTIME",                     "personnes-physiques"),
    ("Le Président de l'Exploitation", "personnes-physiques"),
    ("LE PRESIDENT DE L'EXPLOITATION", "personnes-physiques"),
    ("L'Ancien Président de l'Exploitation", "personnes-physiques"),
    ("L'Ancien President de l'Exploitation", "personnes-physiques"),
    ("La Directrice Générale de l'Exploitation", "personnes-physiques"),
    ("LA DIRECTRICE GENERALE DE L'EXPLOITATION", "personnes-physiques"),
    ("L'Ancienne Directrice Générale de l'Exploitation", "personnes-physiques"),
    ("L'Ancienne Directrice Generale de l'Exploitation", "personnes-physiques"),
    ("Le Préposé de l'Exploitation",   "personnes-physiques"),
    ("LE PREPOSE DE L'EXPLOITATION",   "personnes-physiques"),
    ("Le Propriétaire des Murs",       "personnes-physiques"),
    ("Le Chirurgien SOS Main",         "personnes-physiques"),
    ("Le Médecin en Urgence",          "personnes-physiques"),
    ("Le Médecin Généraliste",         "personnes-physiques"),
    ("LE MEDECIN GENERALISTE",         "personnes-physiques"),
    ("La Gestionnaire CPAM",           "personnes-physiques"),
    ("L'Adjoint au Maire de la Commune", "personnes-physiques"),
    ("Nom de l'Avocat de la Victime",  "personnes-physiques"),
    ("L'Email de l'Adjoint au Maire",  "personnes-physiques"),
    ("L'Email du Secrétariat de la Mairie", "personnes-physiques"),

    # ── Personnes morales ────────────────────────────────────────────────
    ("L'Exploitant du Commerce (La SAS)", "personnes-morales"),
    ("L'EXPLOITANT DU COMMERCE (LA SAS)", "personnes-morales"),
    ("L'Établissement SOS Main",         "personnes-morales"),
    ("L'Etablissement SOS Main",         "personnes-morales"),

    # ── Données localisantes / identifiantes ─────────────────────────────
    ("L'Adresse de la Victime",          "donnees-localisantes"),
    ("L'Adresse de l'Exploitation",      "donnees-localisantes"),
    ("L'Adresse du Président",           "donnees-localisantes"),
    ("La Ville de l'Accident",           "donnees-localisantes"),
    ("LA VILLE DE L'ACCIDENT",           "donnees-localisantes"),
    ("La Ville de Résidence de la Victime", "donnees-localisantes"),
    ("La Métropole Régionale",           "donnees-localisantes"),
    ("L'Email de la Victime",            "donnees-localisantes"),
    ("L'Identifiant Professionnel de la Victime", "donnees-localisantes"),
    ("L'Identifiant de l'Exploitation",  "donnees-localisantes"),
    ("SIREN de l'Exploitation",          "donnees-localisantes"),
    ("SIRET de l'Exploitation",          "donnees-localisantes"),
    ("N° Dossier CPAM",                  "donnees-localisantes"),
    ("N° PV Police",                     "donnees-localisantes"),
    ("N° LRAR Exploitant",               "donnees-localisantes"),
    ("N° LRAR Directrice",               "donnees-localisantes"),
    ("N° LRAR Président",               "donnees-localisantes"),
    ("N° LRAR Propriétaire",             "donnees-localisantes"),
    ("N° LRAR Proprietaire",             "donnees-localisantes"),
    ("N° LRAR Parquet",                  "donnees-localisantes"),
    ("N° Transaction Wero",              "donnees-localisantes"),
    ("Code Postal de l'Accident",        "donnees-localisantes"),
    ("Date de naissance de la victime",  "donnees-localisantes"),
    ("Téléphone Commissariat",           "donnees-localisantes"),
    ("Téléphone Huissier",               "donnees-localisantes"),
    ("Téléphone Ordre Avocats",          "donnees-localisantes"),
    ("Téléphone Tribunal Judiciaire",    "donnees-localisantes"),
    ("Adresse Tribunal Judiciaire",      "donnees-localisantes"),
    ("Adresse du Commissariat",          "donnees-localisantes"),
    ("Adresse de la Mairie",             "donnees-localisantes"),
    ("Le Téléphone de la Victime",       "donnees-localisantes"),

    # ── Tokens événementiels (J+) ────────────────────────────────────────
    ("J+0 Accident",                     "tokens-evenementiels"),
    ("J+1 Chirurgie",                    "tokens-evenementiels"),
    ("J+2 Sortie",                       "tokens-evenementiels"),
    ("J+3 Premiers arrêts",             "tokens-evenementiels"),
    ("J+3 Premiers arrets",             "tokens-evenementiels"),
    ("J+4 Dépôt de plainte",            "tokens-evenementiels"),
    ("J+4 Depot de plainte",            "tokens-evenementiels"),
    ("J+5 Ouverture CPAM",              "tokens-evenementiels"),
    ("J+12 Facture",                     "tokens-evenementiels"),
    ("J+18 Incohérence CPAM",           "tokens-evenementiels"),
    ("J+21 Contrôle chirurgical",       "tokens-evenementiels"),
    ("J+21 Controle chirurgical",       "tokens-evenementiels"),
    ("J+25 Première kiné",              "tokens-evenementiels"),
    ("J+25 Premiere kine",              "tokens-evenementiels"),
    ("J+27 Confirmation kiné",          "tokens-evenementiels"),
    ("J+31 Mises en demeure",           "tokens-evenementiels"),
    ("J+32 Assignation référé",         "tokens-evenementiels"),
    ("J+32 Assignation refere",         "tokens-evenementiels"),
    ("J+33 Plainte complémentaire",     "tokens-evenementiels"),
    ("J+33 Plainte complementaire",     "tokens-evenementiels"),
    ("J+35 AR propriétaire",            "tokens-evenementiels"),
    ("J+36 Lettre consolidation",       "tokens-evenementiels"),
    ("J+37 Assignation 145",            "tokens-evenementiels"),
    ("J+37 Requête 145",               "tokens-evenementiels"),
    ("J+37 Requete 145",               "tokens-evenementiels"),
    ("J+38 Constitution PC",            "tokens-evenementiels"),
    ("J+38 Mise à jour",               "tokens-evenementiels"),
    ("J+38 MISE A JOUR",                "tokens-evenementiels"),
    ("J+40 Consultation suivi",         "tokens-evenementiels"),
    ("J+41 Courrier SIE URSSAF",        "tokens-evenementiels"),
    ("J+41 Requête Constat 145",       "tokens-evenementiels"),
    ("J+41 Requete Constat 145",       "tokens-evenementiels"),
    ("J+46 Échéance amiable",          "tokens-evenementiels"),
    ("J+46 Echeance amiable",          "tokens-evenementiels"),
    ("J+55 Fin d'ITT",                  "tokens-evenementiels"),
    ("J+167 Expertise UMJ",             "tokens-evenementiels"),
]


# ══════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════

def url_enc(path: str) -> str:
    return "/".join(quote(p) for p in path.split("/"))


def split_yaml_frontmatter(content: str):
    """Split content into (frontmatter, body). frontmatter is '' if none."""
    m = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if m:
        return m.group(0), content[m.end():]
    return '', content


def find_link_spans(text: str) -> set:
    spans = set()
    # Standard links without ] in text: [...](...)
    for m in re.finditer(r'\[([^\]]*)\]\(([^)]*)\)', text):
        spans.add((m.start(), m.end()))
    # Extended links where text contains **[Token]** pattern:
    # [**[Token]**](...) — the ] belongs to the bold+token, not link close
    extended = re.compile(r'\[(?:[^\]]|\*\*\[[^\]]*\]\*\*)*\]\([^)]*\)')
    for m in extended.finditer(text):
        start, end = m.start(), m.end()
        if not any(s <= start < e for s, e in spans):
            spans.add((start, end))
    return spans


def inside_any_link(pos: int, link_spans: set) -> bool:
    return any(start <= pos < end for start, end in link_spans)


def build_token_regex(token_text: str) -> re.Pattern:
    escaped = re.escape(f'**[{token_text}]**')
    return re.compile(escaped)


def build_token_replacement(token_text: str, anchor: str, tok_map_rel: str) -> str:
    return f'**[{token_text}]**'


def build_doc_replacement(match: re.Match, target_relpath: str) -> str:
    # STRATE placeholder already resolved before calling this
    target_url = url_enc(target_relpath)
    return f'[{match.group(0)}]({target_url})'


def resolve_target(target_relpath: str, strate: str) -> str:
    """Replace the STRATE placeholder with the actual strate directory name."""
    if "STRATE" in target_relpath:
        strate_name = "Token" if strate == "token" else "Reel"
        return target_relpath.replace("STRATE", strate_name)
    return target_relpath


# ══════════════════════════════════════════════════════════════════════════
# MAIN PROCESSOR
# ══════════════════════════════════════════════════════════════════════════

def process_file(filepath: Path, dry_run: bool, verbose: bool, strate: str = "token") -> dict:
    stats = {"doc_links": 0, "token_links": 0, "modified": False}

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  [SKIP] Cannot read {filepath}: {e}")
        return stats

    original = content
    frontmatter, body = split_yaml_frontmatter(content)
    content = body  # process only body
    link_spans = find_link_spans(content) if content else set()

    changes = []  # (type, old, new) for dry-run output

    # ── Phase 1: Document mentions ───────────────────────────────────────
    for regex, target, label in DOC_MENTIONS:
        resolved = resolve_target(target, strate)
        def make_doc_repl(m, r=resolved):
            if inside_any_link(m.start(), link_spans):
                return m.group(0)
            return build_doc_replacement(m, r)

        new_content, count = regex.subn(make_doc_repl, content)
        if count:
            changes.append((label, count, "doc"))
            stats["doc_links"] += count
            stats["modified"] = True
            content = new_content
            link_spans = find_link_spans(content)

    # ── Phase 2: Token → TOKEN MAP ───────────────────────────────────────
    token_map_rel = TOKEN_MAP_PATH

    for token_text, anchor in TOKEN_ANCHORS:
        tregex = build_token_regex(token_text)
        replacement = build_token_replacement(token_text, anchor, token_map_rel)

        def make_token_repl(m):
            if inside_any_link(m.start(), link_spans):
                return m.group(0)
            return replacement

        new_content, count = tregex.subn(make_token_repl, content)
        if count:
            changes.append((f"Token: [{token_text}]", count, "token"))
            stats["token_links"] += count
            stats["modified"] = True
            content = new_content
            link_spans = find_link_spans(content)

    if not stats["modified"]:
        return stats

    if dry_run:
        rel = filepath.relative_to(BASE)
        print(f"\n[FILE] {rel}")
        for chg_label, chg_count, chg_type in changes:
            icon = "📄" if chg_type == "doc" else "🏷️"
            print(f"  {icon} {chg_label}: {chg_count} remplacement(s)")
    else:
        restored = frontmatter + content
        filepath.write_text(restored, encoding="utf-8")

    return stats


def process_strate(strate_dir: str, dry_run: bool, verbose: bool) -> dict:
    total = {"files_checked": 0, "files_modified": 0,
             "doc_links": 0, "token_links": 0}
    strate_path = BASE / strate_dir

    if not strate_path.exists():
        print(f"[WARN] Directory does not exist: {strate_path}")
        return total

    md_files = sorted(strate_path.rglob("*.md"))

    for fp in md_files:
        # Skip README.md files and breadcrumb-only files
        if fp.name == "README.md":
            continue
        # Skip files in Archives/
        if "Archives" in fp.parts:
            continue

        strate_name = "token" if "Token" in fp.parts else "reel"
        total["files_checked"] += 1
        stats = process_file(fp, dry_run, verbose, strate_name)
        if stats["modified"]:
            total["files_modified"] += 1
            total["doc_links"] += stats["doc_links"]
            total["token_links"] += stats["token_links"]

    return total


# ══════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Navigation Interactive Cross-Document — remplace les "
                    "mentions textuelles par des liens relatifs .md"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Affiche la matrice des modifications sans appliquer")
    parser.add_argument("--strate", choices=["token", "reel", "all"],
                        default="all",
                        help="Strate à traiter (token, reel, ou les deux)")
    parser.add_argument("--verbose", action="store_true",
                        help="Affiche les fichiers sans modification")
    args = parser.parse_args()

    strates = []
    if args.strate in ("token", "all"):
        strates.append(("Token", TOKEN_DIR))
    if args.strate in ("reel", "all"):
        strates.append(("Reel", REEL_DIR))

    mode = "DRY RUN" if args.dry_run else "APPLICATION"
    print(f"\n{'='*70}")
    print(f"  Navigation Interactive Cross-Document — MODE {mode}")
    print(f"{'='*70}\n")

    grand_total = {"files_checked": 0, "files_modified": 0,
                   "doc_links": 0, "token_links": 0}

    for name, directory in strates:
        print(f"\n─── Strate : {name} ({directory}/) ───")
        totals = process_strate(directory, args.dry_run, args.verbose)
        grand_total["files_checked"] += totals["files_checked"]
        grand_total["files_modified"] += totals["files_modified"]
        grand_total["doc_links"] += totals["doc_links"]
        grand_total["token_links"] += totals["token_links"]
        print(f"\n  → {name} : {totals['files_modified']}/{totals['files_checked']} fichiers modifiés, "
              f"{totals['doc_links']} liens pièces, {totals['token_links']} liens tokens")

    # ── Summary ──────────────────────────────────────────────────────────
    total_links = grand_total["doc_links"] + grand_total["token_links"]
    print(f"\n{'='*70}")
    print(f"  RÉSUMÉ ({mode})")
    print(f"{'='*70}")
    print(f"  Fichiers analysés     : {grand_total['files_checked']}")
    print(f"  Fichiers modifiés     : {grand_total['files_modified']}")
    print(f"  Liens pièces (📄)    : {grand_total['doc_links']}")
    print(f"  Liens tokens (🏷️)   : {grand_total['token_links']}")
    print(f"  Total liens créés     : {total_links}")
    print(f"{'='*70}\n")

    if args.dry_run:
        print("  ✅ Dry-run terminé. Aucune modification appliquée.\n")
    else:
        print("  ✅ Modifications appliquées.\n")


if __name__ == "__main__":
    main()
