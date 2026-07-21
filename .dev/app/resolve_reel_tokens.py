#!/usr/bin/env python3
"""
resolve_reel_tokens.py — Replace remaining anonymization tokens in Reel files.

Patterns handled:
  [**[TOKEN TEXT]**](relative/path.md)  →  linked form
  [**[TOKEN TEXT]**]                     →  unlinked form
  [**[N° [Dossier CPAM](path)]**]       →  complex nested CPAM form

Unknown tokens (no mapping) are left as-is and reported.
"""

import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REEL_DIR = os.path.join(PROJECT_ROOT, 'Actes', 'Reel')
REPORT_PATH = os.path.join(PROJECT_ROOT, '.dev', 'app', 'resolve_reel_tokens_report.md')

SIMPLE_TOKENS = {
    "**[Capital Social de l'Exploitation]**": "1 000 €",
    "**[Prénom de la Victime]**": "Sébastien",
    "**[Date de naissance de la Victime]**": "18 janvier 1982",
    "**[Date de naissance de la victime]**": "18 janvier 1982",
    "**[Date de Naissance de la Victime]**": "18 janvier 1982",
    "**[Âge de la Victime]**": "44 ans",
    "**[L'EXPLOITANT DU COMMERCE (LA SAS)]**": "SAS HB BARBER",
    "**[L'Exploitant du Commerce (La SAS)]**": "SAS HB BARBER",
    "**[SIRET]**": "104 103 262 00010",
    "**[Code Postal Accident]**": "09000",
    "**[Code Postal de l'Accident]**": "09000",
    "**[LA VILLE DE L'ACCIDENT]**": "Foix",
    "**[La Ville de l'Accident]**": "Foix",
    "**[LA VICTIME]**": "Sébastien GRAZIDE",
    "**[La Victime]**": "Sébastien GRAZIDE",
    "**[J+38 Mise à jour]**": "6 juillet 2026",
    "**[J+27 Confirmation kiné]**": "25 juin 2026",
    "**[J+37 Requête 145]**": "5 juillet 2026",
    "**[J+37 Assignation 145]**": "5 juillet 2026",
    "**[J+3 Premiers arrets]**": "1er juin 2026",
    "**[J+21 Controle chirurgical]**": "19 juin 2026",
    "**[J+4 Depot de plainte]**": "2 juin 2026",
    "**[J+32 Assignation refere]**": "30 juin 2026",
    "**[J+41 Courrier SIE URSSAF]**": "9 juillet 2026",
    "**[J+38 Date CPC]**": "6 juillet 2026",
    "**[Dr JARDON]**": "Dr Julie Jardon",
    "**[J+63 Assignation 145]**": "31 juillet 2026",
    "**[J+47 Date Requisitoire]**": "15 juillet 2026",
    "**[N° Dossier CPAM]**": "31727387",
    "**[N° Dossier CPAM erroné]**": "2631103960",
}

CPAM_NESTED_PATTERNS = [
    (
        re.compile(
            r'\[\*\*\[N°\s*\[Dossier CPAM\]\([^)]+\)\]\*\*\](?:\([^)]+\))?'
        ),
        '31727387',
        '[**[N° [Dossier CPAM](path)]**] (linked)',
    ),
    (
        re.compile(
            r'\[\*\*\[N°\s*\[Dossier CPAM\]\([^)]+\)\s*erroné\]\*\*\](?:\([^)]+\))?'
        ),
        '2631103960',
        '[**[N° [Dossier CPAM](path) erroné]**] (linked)',
    ),
    (
        re.compile(r'\*\*\[N°\s*\[Dossier CPAM\]\([^)]+\)\]\*\*'),
        '31727387',
        '**[N° [Dossier CPAM](path)]** (bold only)',
    ),
    (
        re.compile(r'\*\*\[N°\s*\[Dossier CPAM\]\([^)]+\)\s*erroné\]\*\*'),
        '2631103960',
        '**[N° [Dossier CPAM](path) erroné]** (bold only)',
    ),
]

UNKNOWN_TOKENS = [
    "**[L'Assureur RC]**",
    "**[Adresse Tribunal Judiciaire]**",
    "**[Adresse du Commissariat]**",
    "**[Adresse Commissariat]**",
    "**[Téléphone Tribunal Judiciaire]**",
    "**[Téléphone Commissariat]**",
    "**[Téléphone Ordre Avocats]**",
    "**[Téléphone Huissier]**",
    "**[Nom Huissier]**",
    "**[Adresse de la Mairie]**",
    "**[Date Ordonnance Référé]**",
    "**[Expert Désigné]**",
    "**[Centre Hospitalier]**",
    "**[Date Dépôt Conclusions]**",
    "**[Nom Commercial de l'Exploitation]**",
]


def build_simple_patterns():
    patterns = []
    for token_text, real_val in SIMPLE_TOKENS.items():
        escaped = re.escape(token_text)
        pattern = re.compile(r'\[' + escaped + r'\](?:\([^)]+\))?')
        patterns.append((pattern, real_val, token_text))
    return patterns


def build_unknown_patterns():
    patterns = []
    for token_text in UNKNOWN_TOKENS:
        escaped = re.escape(token_text)
        pattern = re.compile(r'\[' + escaped + r'\](?:\([^)]+\))?')
        patterns.append((pattern, token_text))
    return patterns


def find_line_number(content, pos):
    return content[:pos].count('\n') + 1


def main():
    simple_patterns = build_simple_patterns()
    unknown_patterns = build_unknown_patterns()

    total_replacements = 0
    total_files = 0
    modified_files = 0
    unresolved = []
    all_lines = []

    for root, dirs, files in os.walk(REEL_DIR):
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue

            fpath = os.path.join(root, fname)
            rel_path = os.path.relpath(fpath, PROJECT_ROOT)

            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            original = content
            file_replacements = 0
            file_unresolved = []

            for pattern, real_val, token_text in simple_patterns:
                for match in pattern.finditer(content):
                    file_replacements += 1
                content = pattern.sub(real_val, content)

            for pattern, real_val, desc in CPAM_NESTED_PATTERNS:
                for match in pattern.finditer(content):
                    file_replacements += 1
                content = pattern.sub(real_val, content)

            if file_replacements > 0:
                modified_files += 1
                total_replacements += file_replacements

            for pattern, token_text in unknown_patterns:
                for match in pattern.finditer(content):
                    pos = match.start()
                    line_no = find_line_number(content, pos)
                    snippet = match.group()[:80]
                    file_unresolved.append((token_text, line_no, snippet))

            if file_unresolved:
                unresolved.append((rel_path, file_unresolved))

            if original != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)

            total_files += 1
            if file_replacements or file_unresolved:
                all_lines.append((rel_path, file_replacements, len(file_unresolved)))

    print(f"{'='*60}")
    print(f"Résolution des tokens dans Reel")
    print(f"{'='*60}")
    print(f"Fichiers parcourus : {total_files}")
    print(f"Fichiers modifiés  : {modified_files}")
    print(f"Remplacements      : {total_replacements}")
    print()

    if all_lines:
        print(f"{'Fichier':<65} {'Remplacements':<15} {'Non résolus':<12}")
        print(f"{'-'*65} {'-'*15} {'-'*12}")
        for rel_path, repl, unk in all_lines:
            print(f"{rel_path:<65} {repl:<15} {unk:<12}")
        print()

    if unresolved:
        print(f"⚠  {len(unresolved)} fichier(s) avec tokens non résolus :")
        for rel_path, tokens in unresolved:
            print(f"  {rel_path}")
            for token_text, line_no, snippet in tokens:
                display = snippet.replace('\n', ' ').replace('\r', '')
                print(f"    L{line_no}: {display}")
        print()

    report_lines = [
        "# Rapport de résolution des tokens\n",
        f"**Date** : —  \n",
        f"**Fichiers parcourus** : {total_files}  \n",
        f"**Fichiers modifiés**  : {modified_files}  \n",
        f"**Remplacements**      : {total_replacements}  \n",
        "\n",
    ]

    if unresolved:
        report_lines.append("## Tokens non résolus\n\n")
        report_lines.append(
            "Ces tokens n'ont pas de correspondance dans TOKEN MAP.md "
            "et ont été laissés intacts.\n\n"
        )
        report_lines.append("| Fichier | Ligne | Token |\n")
        report_lines.append("|---------|------:|-------|\n")
        for rel_path, tokens in unresolved:
            for token_text, line_no, snippet in tokens:
                esc_token = token_text.replace('|', '\\|')
                report_lines.append(
                    f"| {rel_path} | {line_no} | `{esc_token}` |\n"
                )
        report_lines.append("\n")

    report_body = ''.join(report_lines)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report_body)
    print(f"Rapport sauvegardé : {REPORT_PATH}")


if __name__ == '__main__':
    main()
