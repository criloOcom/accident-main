#!/usr/bin/env python3
"""Unify all section headings in Token documents to `## I — TITRE` format.

Usage:
    python3 .dev/app/unify_headings.py        # dry-run (show changes)
    python3 .dev/app/unify_headings.py --apply  # apply changes

Lot A — Regex `## I. TITRE` → `## I — TITRE` (21 files)
Lot B — Arabic `## 1. TITRE` → `## I — TITRE`  (15 files)
Lot C — Named `## TITRE` → `## I — TITRE`      (13 files)
Special — Dintilhac decimal subsections         (1 file)
"""

import os
import re
import sys

TOKEN_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "⚖️ Actes", "🔑 Token",
)

DRY_RUN = "--apply" not in sys.argv


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ROMAN_MAP = [
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (8, "VIII"), (7, "VII"),
    (6, "VI"), (5, "V"), (4, "IV"), (3, "III"), (2, "II"), (1, "I"),
]


def int_to_roman(n: int) -> str:
    result = []
    for value, numeral in ROMAN_MAP:
        while n >= value:
            result.append(numeral)
            n -= value
    return "".join(result)


def resolve_path(rel: str) -> str:
    return os.path.join(TOKEN_DIR, rel)


def safe_read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def safe_write(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def apply_and_report(path: str, old: str, new: str, label: str, changes: list):
    if old == new:
        return
    if old not in new:
        print(f"  [WARN] {label}: old string not found — skipping")
        return
    rel = os.path.relpath(path, TOKEN_DIR)
    changes.append((rel, label))


def edit_file(path: str, old: str, new: str, label: str, changes: list) -> bool:
    content = safe_read(path)
    if old not in content:
        print(f"  [WARN] {label}: pattern not found in {os.path.relpath(path, TOKEN_DIR)}")
        return False
    new_content = content.replace(old, new)
    if content == new_content:
        return False
    rel = os.path.relpath(path, TOKEN_DIR)
    changes.append((rel, label))
    if not DRY_RUN:
        safe_write(path, new_content)
    return True


def edit_file_multi(path: str, replacements: list, changes: list) -> int:
    """Apply multiple (old, new, label) replacements to one file."""
    content = safe_read(path)
    count = 0
    for old, new, label in replacements:
        if old not in content:
            print(f"  [WARN] {label}: not found in {os.path.relpath(path, TOKEN_DIR)}")
            continue
        content = content.replace(old, new)
        rel = os.path.relpath(path, TOKEN_DIR)
        changes.append((rel, label))
        count += 1
    if count > 0 and not DRY_RUN:
        safe_write(path, content)
    return count


# ===================================================================
# LOT A — Regex: `## I. TITRE` → `## I — TITRE`
# Pattern: H2 followed by roman numeral + period + space
# ===================================================================

ROMAN = r"IV|VII|VIII|IX|XI|XII|VI|III?|V?"
# More explicit to avoid false matches
LOT_A_PATTERN = re.compile(r"^(## (?:I{1,3}|IV|V?I{0,3}|IX|X[I]{0,2}))\. (?!\d)", re.MULTILINE)


def lot_a_regex(content: str) -> str:
    """Replace `## I. TITLE` with `## I — TITLE` using regex."""
    def repl(m):
        return m.group(1) + " — "
    return LOT_A_PATTERN.sub(repl, content)


# ===================================================================
# LOT B — Arabic `## 1. TITRE` → `## I — TITRE`
# Per-file mapping
# ===================================================================

# Format: (relative_path, [(old_full_heading, new_full_heading), ...])
LOT_B_MAP = [
    # --- Analyse juridique ---
    ("📚 Analyses juridiques/Note - Qualification Pénale Disparition SAS.md", [
        ("## 1. ORGANISATION FRAUDULEUSE", "## I — ORGANISATION FRAUDULEUSE"),
        ("## 2. ESCROQUERIE", "## II — ESCROQUERIE"),
        ("## 3. BANQUEROUTE", "## III — BANQUEROUTE"),
    ]),
    ("📚 Analyses juridiques/J+47 Note - Mémo Stratégie Admin Pénal.md", [
        ("## 1. SCHÉMA RÉCAPITULATIF", "## I — SCHÉMA RÉCAPITULATIF"),
        ("## 2. VOIE ADMINISTRATIVE", "## II — VOIE ADMINISTRATIVE"),
        ("## 3. VOIE PÉNALE", "## III — VOIE PÉNALE"),
        ("## 4. ARTICULATION STRATÉGIQUE", "## IV — ARTICULATION STRATÉGIQUE"),
        ("## 5. RAPPEL DES TEXTES", "## V — RAPPEL DES TEXTES"),
    ]),
    ("📚 Analyses juridiques/J+60 Note - Dossier Plaidoirie Référé.md", [
        ("## 1. FICHE SYNTHÉTIQUE", "## I — FICHE SYNTHÉTIQUE"),
        ("## 2. CHRONOLOGIE DES FAITS", "## II — CHRONOLOGIE DES FAITS"),
        ("## 3. DISCUSSION JURIDIQUE STRUCTURÉE", "## III — DISCUSSION JURIDIQUE STRUCTURÉE"),
        ("## 4. JURISPRUDENCE CLÉ", "## IV — JURISPRUDENCE CLÉ"),
        ("## 5. PIÈCES À CITER IMPÉRATIVEMENT", "## V — PIÈCES À CITER IMPÉRATIVEMENT"),
        ("## 6. MONTANTS DEMANDÉS", "## VI — MONTANTS DEMANDÉS"),
        ("## 7. QUESTIONS PROBABLES DU JUGE ET RÉPONSES PRÉPARÉES", "## VII — QUESTIONS PROBABLES DU JUGE ET RÉPONSES PRÉPARÉES"),
    ]),
    # --- Actes ---
    ("⚖️ Actes proceduraux/J+38 📸 Constat Huissier - Requête.md", [
        ("## 1. IDENTIFICATION", "## I — IDENTIFICATION"),
        ("## 2. EXPOSÉ", "## II — EXPOSÉ"),
        ("## 3. FONDEMENTS", "## III — FONDEMENTS"),
        ("## 4. OBJET", "## IV — OBJET"),
        ("## 5. DISPOSITIF", "## V — DISPOSITIF"),
    ]),
    # --- Organisation ---
    ("🗂️ Organisation/J+40 Note - Dossier Spécial CERFA.md", [
        ("## 1. SYNTHÈSE DES FORMULAIRES CERFA", "## I — SYNTHÈSE DES FORMULAIRES CERFA"),
        ("## 2. DÉTAIL DU CERFA N° 11527*03 (ATTESTATION DE TÉMOIN)", "## II — DÉTAIL DU CERFA N° 11527*03 (ATTESTATION DE TÉMOIN)"),
        ("## 3. DÉTAIL DU CERFA N° 16160*01 (SAISINE DE LA CIVI)", "## III — DÉTAIL DU CERFA N° 16160*01 (SAISINE DE LA CIVI)"),
        ("## 4. DÉTAIL DU CERFA N° 16146*03 (DEMANDE D'AIDE JURIDICTIONNELLE)", "## IV — DÉTAIL DU CERFA N° 16146*03 (DEMANDE D'AIDE JURIDICTIONNELLE)"),
    ]),
    ("🗂️ Organisation/Note - Plan Constat Police Foix.md", [
        ("## 1. Analyse de Faisabilité Juridique", "## I — Analyse de Faisabilité Juridique"),
        ("## 2. Plan d'Action Proposé", "## II — Plan d'Action Proposé"),
        ("## 3. Modèle de Mail", "## III — Modèle de Mail"),
    ]),
    ("🗂️ Organisation/J+43 Archive - Checklist Envoi 11-07.md", [
        ("## 1. AVANT DEPART", "## I — AVANT DEPART"),
        ("## 2. A LA POSTE", "## II — A LA POSTE"),
        ("## 3. EMAILS", "## III — EMAILS"),
        ("## 4. ARCHIVAGE", "## IV — ARCHIVAGE"),
        ("## 5. RAPPELS", "## V — RAPPELS"),
    ]),
    ("🗂️ Organisation/Synthèse - Actions et Audits.md", [
        ("## 1. 🟥 CE QU'IL RESTE À FAIRE", "## I — 🟥 CE QU'IL RESTE À FAIRE"),
        ("## 2. 🟩 CE QUI A ÉTÉ CORRIGÉ", "## II — 🟩 CE QUI A ÉTÉ CORRIGÉ"),
    ]),
    ("🗂️ Organisation/Note - Modification Email Maire Foix.md", [
        ("## 1. Objectifs de la réécriture", "## I — Objectifs de la réécriture"),
        ("## 2. Nouveau modèle d'e-mail", "## II — Nouveau modèle d'e-mail"),
    ]),
    # --- Courriers ---
    ("✉️ Courriers/J+47 📋 Guide Demande AJ.md", [
        ("## 1. SUIS-JE ÉLIGIBLE ?", "## I — SUIS-JE ÉLIGIBLE ?"),
        ("## 2. CE QUE COUVRE L'AJ TOTALE", "## II — CE QUE COUVRE L'AJ TOTALE"),
        ("## 3. PIÈCES À FOURNIR", "## III — PIÈCES À FOURNIR"),
        ("## 4. COMMENT REMPLIR LE FORMULAIRE", "## IV — COMMENT REMPLIR LE FORMULAIRE"),
        ("## 5. DÉMARCHE AU TJ", "## V — DÉMARCHE AU TJ"),
        ("## 6. APRÈS L'AJ", "## VI — APRÈS L'AJ"),
        ("## 7. CONSEILS POUR LE 15 JUILLET", "## VII — CONSEILS POUR LE 15 JUILLET"),
    ]),
    ("✉️ Courriers/J+47 ✉️ Modele Saisine CADA.md", [
        ("## 1. Identité du demandeur", "## I — Identité du demandeur"),
        ("## 2. Administration(s) concernée(s)", "## II — Administration(s) concernée(s)"),
        ("## 3. Rappel des demandes initiales", "## III — Rappel des demandes initiales"),
        ("## 4. Réponse de l'administration", "## IV — Réponse de l'administration"),
        ("## 5. Objet exact de la saisine", "## V — Objet exact de la saisine"),
        ("## 6. Pièces jointes", "## VI — Pièces jointes"),
    ]),
    # --- Études indemnisation ---
    ("💰 Etudes indemnisation/J+40 Note - Stratégique FGTI CIVI.md", [
        ("## 1. CONDITIONS D'ACCÈS AU FGTI (Art. 706-3 CPP)", "## I — CONDITIONS D'ACCÈS AU FGTI (Art. 706-3 CPP)"),
        ("## 2. ARTICULATION AVEC LES AUTRES PROCÉDURES ET ASSURANCES", "## II — ARTICULATION AVEC LES AUTRES PROCÉDURES ET ASSURANCES"),
        ("## 3. PROCÉDURE DÉTAILLÉE DEVANT LA CIVI", "## III — PROCÉDURE DÉTAILLÉE DEVANT LA CIVI"),
        ("## 4. DÉLAIS", "## IV — DÉLAIS"),
        ("## 5. MONTANT ESTIMÉ ET PLAFOND FGTI", "## V — MONTANT ESTIMÉ ET PLAFOND FGTI"),
        ("## 6. PIÈCES NÉCESSAIRES POUR LA DEMANDE CIVI", "## VI — PIÈCES NÉCESSAIRES POUR LA DEMANDE CIVI"),
        ("## 7. RECOMMANDATION FINALE : Y ALLER OU PAS ?", "## VII — RECOMMANDATION FINALE : Y ALLER OU PAS ?"),
    ]),
    # --- Archives ---
    ("🗄️ Archives/Archive - Stratégie Contentieux Pénal.md", [
        ("## 1. PRÉSENTATION", "## I — PRÉSENTATION"),
        ("## 2. INFRACTIONS CONSTITUÉES", "## II — INFRACTIONS CONSTITUÉES"),
        ("## 3. PROCÉDURE PÉNALE", "## III — PROCÉDURE PÉNALE"),
        ("## 4. CALENDRIER", "## IV — CALENDRIER"),
        ("## 5. RÉCAPITULATIF", "## V — RÉCAPITULATIF"),
    ]),
    ("🗄️ Archives/Archive - Stratégie Contentieux Civil.md", [
        ("## 1. PRÉSENTATION", "## I — PRÉSENTATION"),
        ("## 2. FONDEMENTS JURIDIQUES", "## II — FONDEMENTS JURIDIQUES"),
        ("## 3. VOIES DE PROCÉDURE ENGAGÉES", "## III — VOIES DE PROCÉDURE ENGAGÉES"),
        ("## 4. ÉVALUATION DES PRÉJUDICES", "## IV — ÉVALUATION DES PRÉJUDICES"),
        ("## 5. CALENDRIER PROCÉDURAL", "## V — CALENDRIER PROCÉDURAL"),
        ("## 6. RÉCAPITULATIF DES PIÈCES", "## VI — RÉCAPITULATIF DES PIÈCES"),
    ]),
]

# ===================================================================
# SPECIAL — Dintilhac: `## 1.1 FAITS` → `## I.1 — FAITS`
# Only main number changes to roman, subsection and title stay.
# ===================================================================

DINTILHAC_PATH = resolve_path(
    "💰 Etudes indemnisation/J+39 Note - Évaluation Dintilhac Consolidée.md"
)
DINTILHAC_MAIN = re.compile(r"^(## )(\d+)\.(\d+) (.+)$", re.MULTILINE)


def lot_dintilhac(content: str) -> str:
    def repl(m):
        prefix, main_num, sub_num, title = m.groups()
        roman = int_to_roman(int(main_num))
        return f"{prefix}{roman}.{sub_num} — {title}"
    return DINTILHAC_MAIN.sub(repl, content)


# ===================================================================
# LOT C — Named sections → Roman numerals
# ===================================================================

LOT_C_MAP = [
    # --- Courriers ---
    ("✉️ Courriers/J+37 ✉️ Signalement Inspection Travail.md", [
        ("## PROCEDURES EN COURS", "## I — PROCÉDURES EN COURS"),
        ("## CONTEXTE DE LA SAISINE DE VOS SERVICES", "## II — CONTEXTE DE LA SAISINE DE VOS SERVICES"),
    ]),
    ("✉️ Courriers/J+37 ✉️ Signalement SDIS.md", [
        ("## OBJET DU SIGNALEMENT", "## I — OBJET DU SIGNALEMENT"),
    ]),
    ("✉️ Courriers/J+37 🔄 Relance Police Videos.md", [
        ("## OBJET DE LA RELANCE", "## I — OBJET DE LA RELANCE"),
    ]),
    ("✉️ Courriers/J+40 ✉️ Relance Dirigeants.md", [
        ("## PRÉAMBULE — ABSENCE DE RÉPONSE", "## I — PRÉAMBULE — ABSENCE DE RÉPONSE"),
        ("## RAPPEL DE LA DEMANDE D'ASSURANCE", "## II — RAPPEL DE LA DEMANDE D'ASSURANCE"),
        ("## DEMANDE D'ADRESSE DE CORRESPONDANCE", "## III — DEMANDE D'ADRESSE DE CORRESPONDANCE"),
        ("## ANNEXE JURIDIQUE", "## IV — ANNEXE JURIDIQUE"),
    ]),
    ("✉️ Courriers/J+31 ✉️ Mise en demeure President.md", [
        ("## RAPPEL DES OBLIGATIONS LÉGALES", "## I — RAPPEL DES OBLIGATIONS LÉGALES"),
    ]),
    ("✉️ Courriers/J+31 ✉️ Mise en demeure Proprietaire.md", [
        ("### Rappel des obligations légales", "## I — RAPPEL DES OBLIGATIONS LÉGALES"),
        ("### Transparence sur la suite donnée au dossier", "## II — TRANSPARENCE SUR LA SUITE DONNÉE AU DOSSIER"),
    ]),
    ("✉️ Courriers/J+47 ✉️ Consultation Avocat Jimini.md", [
        ("## Faits et situation actuelle", "## I — Faits et situation actuelle"),
        ("## Démarches déjà faites", "## II — Démarches déjà faites"),
        ("## Questions à l'avocat", "## III — Questions à l'avocat"),
    ]),
    # --- Analyses ---
    ("📚 Analyses juridiques/Note - Conservation Preuves Numériques.md", [
        ("## PROBLÉMATIQUE", "## I — PROBLÉMATIQUE"),
        ("## FONDEMENT JURIDIQUE", "## II — FONDEMENT JURIDIQUE"),
        ("## ARGUMENTATION ET STRATÉGIE DE COLLECTE", "## III — ARGUMENTATION ET STRATÉGIE DE COLLECTE"),
        ("## CONCLUSION ET RECOMMANDATIONS", "## IV — CONCLUSION ET RECOMMANDATIONS"),
    ]),
    ("📚 Analyses juridiques/J+39 Note - Stratégie Jurisprudentielle.md", [
        ("## LES 3 PILIERS DE LA DÉMONSTRATION", "## I — LES 3 PILIERS DE LA DÉMONSTRATION"),
        ("## HIÉRARCHIE ARGUMENTATIVE", "## II — HIÉRARCHIE ARGUMENTATIVE"),
        ("## TABLEAU DE CORRESPONDANCE", "## III — TABLEAU DE CORRESPONDANCE"),
        ("## ANTICIPATION DES MOYENS DE LA DÉFENSE", "## IV — ANTICIPATION DES MOYENS DE LA DÉFENSE"),
        ("## SYNTHÈSE DES FORCES ET FAIBLESSES", "## V — SYNTHÈSE DES FORCES ET FAIBLESSES"),
        ("## STRATÉGIE FINANCIÈRE", "## VI — STRATÉGIE FINANCIÈRE"),
        ("## RÉFÉRENCES CROISÉES", "## VII — RÉFÉRENCES CROISÉES"),
    ]),
    # --- Organisation ---
    ("🗂️ Organisation/Note - Fiche Réflexe 48h Disparition SAS.md", [
        ("## PROBLÉMATIQUE", "## I — PROBLÉMATIQUE"),
        ("## FONDEMENT ET DÉPENDANCES CRITIQUES", "## II — FONDEMENT ET DÉPENDANCES CRITIQUES"),
        ("## ARGUMENTATION ET PLAN D'ACTION SÉQUENTIEL", "## III — ARGUMENTATION ET PLAN D'ACTION SÉQUENTIEL"),
        ("## CONCLUSION", "## IV — CONCLUSION"),
    ]),
    ("🗂️ Organisation/J+43 Note - Suivi Envois LRAR.md", [
        ("## TABLEAU DE BORD", "## I — TABLEAU DE BORD"),
        ("## SYNTHESE FINANCIERE", "## II — SYNTHESE FINANCIERE"),
        ("## LEGENDE", "## III — LEGENDE"),
    ]),
    ("🗂️ Organisation/J+38 Note - Bon Envoi Physique.md", [
        ("## DOCUMENTS À IMPRIMER", "## I — DOCUMENTS À IMPRIMER"),
        ("## DESTINATAIRE UNIQUE", "## II — DESTINATAIRE UNIQUE"),
        ("## PIÈCES JUSTIFICATIVES", "## III — PIÈCES JUSTIFICATIVES"),
        ("## INSTRUCTIONS", "## IV — INSTRUCTIONS"),
        ("## RAPPELS", "## V — RAPPELS"),
    ]),
]

# ===================================================================
# EXECUTION
# ===================================================================

HEADER = f"{'DRY RUN' if DRY_RUN else 'APPLYING'} — {'no files will be modified' if DRY_RUN else 'files WILL be modified'}"
SEP = "=" * 70
print(f"\n{SEP}")
print(f"  UNIFY HEADINGS — {HEADER}")
print(f"{SEP}\n")

all_changes = []

# ---- LOT A: regex scan all .md files under TOKEN_DIR ----
print("--- LOT A: Period→Em Dash ---")
lot_a_files = 0
for root, dirs, files in os.walk(TOKEN_DIR):
    # Skip README.md
    for fn in files:
        if not fn.endswith(".md") or fn == "README.md":
            continue
        path = os.path.join(root, fn)
        content = safe_read(path)
        new_content = lot_a_regex(content)
        if content != new_content:
            rel = os.path.relpath(path, TOKEN_DIR)
            # Count changes
            old_matches = LOT_A_PATTERN.findall(content)
            new_matches = LOT_A_PATTERN.findall(new_content)
            diff_count = len(old_matches) - len(new_matches)
            all_changes.append((rel, f"Lot A: period→em dash ({diff_count} heading(s))"))
            lot_a_files += 1
            if not DRY_RUN:
                safe_write(path, new_content)

print(f"  → {lot_a_files} fichier(s) touché(s) par Lot A\n")

# ---- LOT B: Arabic → Roman ----
print("--- LOT B: Arabic→Roman ---")
lot_b_count = 0
for rel_path, replacements in LOT_B_MAP:
    path = resolve_path(rel_path)
    if not os.path.exists(path):
        print(f"  [SKIP] {rel_path} — not found")
        continue
    for old, new in replacements:
        if edit_file(path, old, new, f"Lot B: {old.strip()}", all_changes):
            lot_b_count += 1
print(f"  → {lot_b_count} remplacement(s) Lot B\n")

# ---- SPECIAL Dintilhac ----
print("--- SPECIAL: Dintilhac decimal subsections ---")
dint_content = safe_read(DINTILHAC_PATH)
dint_new = lot_dintilhac(dint_content)
if dint_content != dint_new:
    rel = os.path.relpath(DINTILHAC_PATH, TOKEN_DIR)
    diff_count = len(DINTILHAC_MAIN.findall(dint_content))
    all_changes.append((rel, f"Dintilhac: decimal→romain ({diff_count} subsection(s))"))
    if not DRY_RUN:
        safe_write(DINTILHAC_PATH, dint_new)
    print(f"  → {diff_count} subsection(s) convertie(s)")
else:
    print("  → Aucun changement (déjà fait ?)")
print()

# ---- LOT C: Named → Roman ----
print("--- LOT C: Named→Roman ---")
lot_c_count = 0
for rel_path, replacements in LOT_C_MAP:
    path = resolve_path(rel_path)
    if not os.path.exists(path):
        print(f"  [SKIP] {rel_path} — not found")
        continue
    for old, new in replacements:
        if edit_file(path, old, new, f"Lot C: {old.strip()[:50]}", all_changes):
            lot_c_count += 1
print(f"  → {lot_c_count} remplacement(s) Lot C\n")

# ---- Summary ----
SEP2 = "-" * 70
print(SEP2)
if DRY_RUN:
    print(f"  DRY RUN — {len(all_changes)} changement(s) détecté(s) dans {len(set(c[0] for c in all_changes))} fichier(s)")
    print(f"  Re-run with --apply to execute.")
else:
    print(f"  APPLIED — {len(all_changes)} changement(s) dans {len(set(c[0] for c in all_changes))} fichier(s)")
print(SEP2)

# Group by file for readable output
from collections import defaultdict
by_file = defaultdict(list)
for rel, label in all_changes:
    by_file[rel].append(label)

print()
for rel in sorted(by_file):
    print(f"  📄 {rel}")
    for label in by_file[rel]:
        print(f"      {label}")
print()

if DRY_RUN:
    sys.exit(0)
else:
    print("  ✅ Done. Run `git diff --stat` to review.")
