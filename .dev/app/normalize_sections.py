#!/usr/bin/env python3
"""
normalize_sections.py — Normalise les séparateurs de section au format <hr><hr>.

Règles appliquées :
  1. <hr><hr> AVANT chaque section de premier niveau (sauf la 1ère)
  2. --- (HR) dans le corps → <hr><hr>
  3. <hr> simple dans le corps → <hr><hr>
  4. Concaténation des <hr><hr> consécutifs
  5. Respect du YAML front matter et des code blocks

Sections de premier niveau détectées :
  - ## <tout> (tout H2 est une section majeure)
  - ### suivi d'un chiffre romain (### I., ### II., etc.)
  - ### suivi d'un mot-clé connu (### EXPOSÉ, ### PAR CES MOTIFS, etc.)

Usage:
    python3 .dev/app/normalize_sections.py          # dry-run (ne modifie rien)
    python3 .dev/app/normalize_sections.py --apply   # applique les modifications
    python3 .dev/app/normalize_sections.py --apply --reel   # applique aux Reel seulement
    python3 .dev/app/normalize_sections.py --apply --token  # applique aux Token seulement
"""

import os
import re
import sys
from collections import defaultdict

BASE = "/home/crilocom/accident-main"
TOKEN = os.path.join(BASE, "Actes", "Token")
REEL = os.path.join(BASE, "Actes", "Reel")

# Dossiers à ignorer (pièces brutes sans YAML)
SKIP_PARENTS = {"Preuves_officielles"}

# Mots-clés de sections de premier niveau (pour les ### sans chiffre romain)
KW = {
    "EXPOSÉ", "EXPOSE", "EXPOSÉ DES FAITS",
    "MOTIFS", "DISCUSSION",
    "PAR CES MOTIFS", "DISPOSITIF",
    "INTRODUCTION", "OBJET", "DEMANDES",
    "CONCLUSIONS", "PRÉTENTIONS",
    "PIÈCES JOINTES", "PIECES JOINTES", "PIÈCE JOINTE",
    "ANNEXE", "ANNEXES",
    "MOYENS", "PRÉAMBULE", "PREAMBULE",
    "IDENTIFICATION",
    "SOURCES", "TEXTES DE LOI", "TEXTES",
    "JURISPRUDENCE", "DOCTRINE",
    "FAITS", "RAPPEL", "RAPPEL DES OBLIGATIONS",
    "CONSTATS", "RECOMMANDATIONS",
    "PROCÉDURES", "PROCEDURES",
    "CONTEXTE", "OBJET DU SIGNALEMENT",
    "STRATÉGIE", "STRATEGIE",
    "TABLEAU DE BORD", "SYNTHÈSE", "SYNTHESE",
    "LÉGENDE", "LEGENDE",
    "INSTRUCTIONS",
}

ROMAN = r"(?:I{1,3}|IV|V?I{0,3}|IX|X[I]{0,2})"


def is_first_level(line: str) -> bool:
    """Une ligne est une section de premier niveau si :
    - ## <tout>  (tout H2)
    - ### <romain> (H3 avec chiffre romain)
    - ### <mot-clé> (H3 avec mot-clé)
    """
    m = re.match(r"^(#{2,3})\s+(.+)", line)
    if not m:
        return False
    level = len(m.group(1))
    text = m.group(2).strip()
    upper = text.upper()

    if level == 2:
        # Exclure les sous-titres/annotations (## (Note), ## [Complément])
        if re.match(r'^[\(\[\—–\-]', text):
            return False
        # Exclure les lignes très courtes sans majuscule de section
        if len(text) < 10 and not re.match(r'^[A-Z\u00C0-\u00DC]', text):
            return False
        return True

    # level == 3
    if re.match(r"^" + ROMAN + r"[\.\—–]\s", upper):
        return True
    for kw in KW:
        if upper.startswith(kw):
            return True
    return False


def parse_regions(lines: list[str]) -> tuple[int, int, list[tuple[int, int]]]:
    """Retourne (yaml_end, body_start, [(code_start, code_end), ...])"""
    yaml_end = -1
    code_blocks: list[tuple[int, int]] = []
    in_yaml = False
    in_code = False
    code_start = -1

    for i, line in enumerate(lines):
        s = line.strip()

        if not in_yaml and not in_code and i == 0 and s == "---":
            in_yaml = True
            continue
        if in_yaml:
            if s == "---":
                in_yaml = False
                yaml_end = i
            continue
        if s.startswith("```"):
            if not in_code:
                in_code = True
                code_start = i
            else:
                in_code = False
                code_blocks.append((code_start, i))

    if yaml_end < 0:
        yaml_end = -1  # pas de YAML

    body_start = yaml_end + 1 if yaml_end >= 0 else 0

    return yaml_end, body_start, code_blocks


def in_code_block(line_no: int, blocks: list[tuple[int, int]]) -> bool:
    for s, e in blocks:
        if s <= line_no <= e:
            return True
    return False


def process_file(path: str, apply: bool = False) -> int:
    """Traite un fichier. Retourne le nombre de changements."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return 0

    # Skip si aucun en-tête YAML (fichier brut)
    if not content.startswith("---"):
        return 0

    original = content
    lines = content.split("\n")
    yaml_end, body_start, code_blocks = parse_regions(lines)
    n = len(lines)

    # ---- Phase 1 : remplacer --- et <hr> dans le corps ----
    phase1 = list(lines)  # on va modifier phase1 in-place

    for i in range(body_start, n):
        if i <= yaml_end:
            continue
        if in_code_block(i, code_blocks):
            continue
        s = phase1[i].strip()

        # ---  → <hr><hr>
        if re.match(r"^-{3,}\s*$", s):
            phase1[i] = "<hr><hr>"

    # ---- Phase 2 : Normaliser les séparateurs avant chaque section ----
    output: list[str] = []
    section_count = 0
    found_first = False
    i = 0

    while i < n:
        line = phase1[i]

        # Zone YAML : inchangé
        if i <= yaml_end:
            output.append(line)
            i += 1
            continue

        # Code blocks : inchangés
        if in_code_block(i, code_blocks):
            output.append(line)
            i += 1
            continue

        # Section de premier niveau détectée ?
        if is_first_level(line):
            section_count += 1
            if not found_first:
                found_first = True
                # 1ère section : nettoyer tout <hr> résiduel avant elle
                while output and output[-1].strip() in ("", "<hr>", "<hr><hr>"):
                    output.pop()
                output.append(line)
                i += 1
                continue

            # Section N (N≥2) : remplacer l'ancien séparateur par <hr><hr>
            while output and output[-1].strip() in ("", "<hr>", "<hr><hr>"):
                output.pop()
            output.append("<hr><hr>")
            output.append("")
            output.append(line)
            i += 1
            continue

        output.append(line)
        i += 1

    # ---- Phase 3 : Déduplication et coalescence ----
    final: list[str] = []
    i = 0
    # On doit re-connaître les code blocks dans la sortie finale
    _, _, cb2 = parse_regions(output)

    while i < len(output):
        s = output[i].strip()
        lno = i  # ligne dans la sortie finale

        if in_code_block(lno, cb2):
            final.append(output[i])
            i += 1
            continue

        # <hr> solitaire → <hr><hr>
        # Sauf le <hr> du breadcrumb (entouré de <!-- Breadcrumb --> /<!-- /Breadcrumb -->)
        if s == "<hr>" and i > yaml_end:
            is_breadcrumb = False
            for j in range(max(0, i - 5), min(len(output), i + 5)):
                if "Breadcrumb" in output[j]:
                    is_breadcrumb = True
                    break
            if not is_breadcrumb:
                final.append("<hr><hr>")
                i += 1
                continue

        # Concaténer <hr><hr> consécutifs
        if s == "<hr><hr>":
            final.append(output[i])
            i += 1
            while i < len(output) and output[i].strip() == "<hr><hr>":
                i += 1
            continue

        final.append(output[i])
        i += 1

    # ---- Phase 4 : Nettoyer les <hr><hr> finaux ----
    while final and final[-1].strip() in ("", "<hr>", "<hr><hr>"):
        final.pop()

    result = "\n".join(final)

    # Nettoyer : supprimer les lignes vides entre YAML et breadcrumb
    # (peut arriver après coalescence)

    if result == original:
        return 0

    if apply:
        with open(path, "w", encoding="utf-8") as f:
            f.write(result)

    # Compter les différences visibles
    diff_count = 0
    orig_lines = original.split("\n")
    res_lines = final
    max_len = max(len(orig_lines), len(res_lines))
    for j in range(max_len):
        o = orig_lines[j] if j < len(orig_lines) else ""
        r = res_lines[j] if j < len(res_lines) else ""
        if o != r:
            diff_count += 1

    return max(diff_count, 1)


def collect_files(root: str) -> list[str]:
    files: list[str] = []
    for dp, dirs, fns in os.walk(root):
        rel = os.path.relpath(dp, root)
        # Skip les dossiers d'exclusion
        skip = False
        for part in dp.split(os.sep):
            if part in SKIP_PARENTS:
                skip = True
                break
        if skip:
            continue
        for fn in fns:
            if fn.endswith(".md") and fn != "README.md":
                files.append(os.path.join(dp, fn))
    return sorted(files)


def main():
    apply = "--apply" in sys.argv
    token_only = "--token" in sys.argv
    reel_only = "--reel" in sys.argv

    if token_only and reel_only:
        print("ERROR: --token et --reel sont exclusifs.")
        sys.exit(1)

    targets: list[str] = []

    if not reel_only:
        targets.extend(collect_files(TOKEN))
    if not token_only:
        targets.extend(collect_files(REEL))

    mode = "DRY RUN" if not apply else "APPLYING"
    print(f"\n{'='*70}")
    print(f"  NORMALIZE SECTIONS — {mode}")
    print(f"{'='*70}\n")

    total = 0
    by_dir: defaultdict[str, int] = defaultdict(int)

    for path in targets:
        c = process_file(path, apply=apply)
        if c > 0:
            rel = os.path.relpath(path, BASE)
            total += c
            parent = os.path.dirname(rel)
            by_dir[parent] += c
            print(f"  {'✓' if apply else ' ~'} {c:3d}  {rel}")

    print(f"\n{'='*70}")
    print(f"  TOTAL : {total} fichier(s) modifié(s)")
    if apply:
        print(f"  Changements appliqués.")
    else:
        print(f"  Re-run with --apply to execute.")
    print(f"{'='*70}")

    if by_dir:
        print(f"\n  Répartition par dossier :")
        for d in sorted(by_dir):
            print(f"    {by_dir[d]:3d}  {d}")

    if apply and total > 0:
        print(f"\n  ✅ Done. Run `git diff --stat` to review.\n")
    elif not apply and total == 0:
        print(f"  Rien à normaliser.\n")


if __name__ == "__main__":
    main()
