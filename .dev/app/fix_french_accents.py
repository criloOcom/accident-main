#!/usr/bin/env python3
"""
fix_french_accents.py — Correction conservatrice de l'accentuation UTF-8 des
matrices Actes/Token/**.md.

Principe (Règle #16 précision absolue) :
- On ne corrige QUE des mots dont la forme désaccentuée est incontestablement
  fautive en français (liste blanche curée ci-dessous). Les mots corrects sans
  accent (entreprise, civiles, corporel, situation, modification, survenu...)
  ne figurent PAS dans la table et ne sont jamais touchés.
- Les cibles de liens Markdown `](...)`, les spans de code `` `...` `` et le
  frontmatter YAML (chemins de fichiers) sont masqués avant remplacement pour
  ne JAMAIS altérer un chemin/URL (ex. ..._AttestationDepot.md).
- Remplacement au mot entier (\b...\b), en préservant la casse (minuscule,
  Capitale, MAJUSCULE).

Usage :
  python3 .dev/app/fix_french_accents.py            # dry-run (diff résumé)
  python3 .dev/app/fix_french_accents.py --apply    # écrit les corrections
"""
import os
import re
import sys
import glob

ROOT = "/home/crilocom/accident-main"
TOKEN_BASE = os.path.join(ROOT, "Actes", "Token")

# Table blanche : forme_desaccentuee_minuscule -> forme_correcte_minuscule.
# N'inclure QUE des mots dont la version sans accent est fautive en français.
CORRECTIONS = {
    "presente": "présente",
    "presentes": "présentes",
    "adressee": "adressée",
    "adressees": "adressées",
    "societe": "société",
    "societes": "sociétés",
    "penale": "pénale",
    "penales": "pénales",
    "penal": "pénal",
    "reparation": "réparation",
    "prejudice": "préjudice",
    "prejudices": "préjudices",
    "immatriculee": "immatriculée",
    "coordonnees": "coordonnées",
    "engagees": "engagées",
    "engagee": "engagée",
    "etat": "état",
    "ete": "été",
    "etre": "être",
    "numero": "numéro",
    "numeros": "numéros",
    "apres": "après",
    "aupres": "auprès",
    "evaluation": "évaluation",
    "definitive": "définitive",
    "definitif": "définitif",
    "elements": "éléments",
    "element": "élément",
    "reception": "réception",
    "integration": "intégration",
    "estimes": "estimés",
    "estime": "estimé",
    "responsabilite": "responsabilité",
    "responsabilites": "responsabilités",
    "activite": "activité",
    "activites": "activités",
    "deja": "déjà",
    "prealable": "préalable",
    "necessaire": "nécessaire",
    "necessaires": "nécessaires",
    "proximite": "proximité",
    "securite": "sécurité",
    "verite": "vérité",
    "refere": "référé",
    "referes": "référés",
    "deces": "décès",
    "declaration": "déclaration",
    "declarations": "déclarations",
    "deposee": "déposée",
    "deposees": "déposées",
    "deposer": "déposer",
    "depot": "dépôt",
    "depots": "dépôts",
    "creee": "créée",
    "creees": "créées",
    "creation": "création",
    "complementaire": "complémentaire",
    "complementaires": "complémentaires",
    "proprietaire": "propriétaire",
    "proprietaires": "propriétaires",
    "caractere": "caractère",
    "regulier": "régulier",
    "reguliere": "régulière",
    "general": "général",
    "generale": "générale",
    "generaux": "généraux",
    "generales": "générales",
    "procedure": "procédure",
    "procedures": "procédures",
    "matiere": "matière",
    "matieres": "matières",
    "derniere": "dernière",
    "premiere": "première",
    "medical": "médical",
    "medicale": "médicale",
    "medicaux": "médicaux",
    "medicales": "médicales",
    "medecin": "médecin",
    "reserve": "réserve",
    "exploite": "exploité",
    "exploitee": "exploitée",
    "decision": "décision",
    "decisions": "décisions",
    "prevu": "prévu",
    "prevue": "prévue",
    "represente": "représente",
    "representee": "représentée",
    "consideration": "considération",
    "requerant": "requérant",
    "defini": "défini",
    "definie": "définie",
    "consolidee": "consolidée",
    "corporelle": "corporelle",  # already correct — placeholder no-op removed below
}
# Retirer les no-op (forme == correction)
CORRECTIONS = {k: v for k, v in CORRECTIONS.items() if k != v}


def case_variants(base_lower, corrected_lower):
    """Retourne [(pattern_word, replacement)] pour min/Capitale/MAJUSCULE."""
    out = []
    out.append((base_lower, corrected_lower))
    out.append((base_lower.capitalize(), corrected_lower.capitalize()))
    out.append((base_lower.upper(), corrected_lower.upper()))
    return out


# Construit une regex unique alternant tous les mots (toutes casses),
# la plus longue d'abord pour éviter les préfixes.
_pairs = []
for b, c in CORRECTIONS.items():
    _pairs.extend(case_variants(b, c))
_pairs = sorted(set(_pairs), key=lambda p: -len(p[0]))
_REPL = {b: c for b, c in _pairs}
_WORD_RE = re.compile(r"\b(" + "|".join(re.escape(b) for b, _ in _pairs) + r")\b")


def mask_protected(text):
    """Masque URLs de liens, code spans, et frontmatter YAML. Retourne (masked, restore)."""
    store = []

    def stash(m):
        store.append(m.group(0))
        return f"\x00{len(store)-1}\x00"

    # 1. frontmatter YAML complet (bloc --- ... ---) en tête
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", stash, text, count=1, flags=re.DOTALL)
    # 2. blocs HTML de breadcrumb
    text = re.sub(r"<!-- Breadcrumb -->.*?<!-- /Breadcrumb -->", stash, text, flags=re.DOTALL)
    # 2b. lignes de fil d'Ariane non balisées (générées par generate_breadcrumbs.py, Règle #14)
    text = re.sub(r"^\*?\[?🏠.*$", stash, text, flags=re.MULTILINE)
    # 3. cibles de liens Markdown : la partie (...) après ]
    text = re.sub(r"\]\((?:[^()]|\([^()]*\))*\)", stash, text)
    # 4. code spans inline `...`
    text = re.sub(r"`[^`]*`", stash, text)
    # 5. blocs code ``` ... ```
    text = re.sub(r"```.*?```", stash, text, flags=re.DOTALL)
    return text, store


def restore_protected(text, store):
    def unstash(m):
        return store[int(m.group(1))]
    return re.sub(r"\x00(\d+)\x00", unstash, text)


def fix_text(text):
    masked, store = mask_protected(text)
    count = [0]

    def repl(m):
        count[0] += 1
        return _REPL[m.group(1)]

    masked = _WORD_RE.sub(repl, masked)
    return restore_protected(masked, store), count[0]


def main():
    apply = "--apply" in sys.argv
    files = sorted(glob.glob(TOKEN_BASE + "/**/*.md", recursive=True))
    total_files = 0
    total_repl = 0
    for f in files:
        base = os.path.basename(f)
        if base in ("README.md", "INDEX.md"):
            continue
        txt = open(f, encoding="utf-8").read()
        new, n = fix_text(txt)
        if n and new != txt:
            total_files += 1
            total_repl += n
            print(f"  {os.path.relpath(f, ROOT)} : {n} correction(s)")
            if apply:
                open(f, "w", encoding="utf-8").write(new)
    print(f"\nMODE: {'APPLY' if apply else 'DRY-RUN'}")
    print(f"Fichiers concernés : {total_files} | corrections : {total_repl}")


if __name__ == "__main__":
    main()
