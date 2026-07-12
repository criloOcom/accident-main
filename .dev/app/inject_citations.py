#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inject_citations.py — Insère les blocs de citation Légifrance sous chaque citation
d'article non encore suivie de son bloc (comble les « trous »).

Entrée : /tmp/glossaire.json (produit via legifrance_citation) mappant
         "<num>||<Code>" -> {"block": "...", "etat": "..."}.
Cible  : fichiers .md sous ⚖️ Actes/🔑 Token.

Règles :
- On ne touche jamais le YAML (entre les deux premiers '---'), ni les lignes de
  titre (#) ou déjà en blockquote (>).
- On insère le bloc juste APRÈS la ligne contenant la citation, uniquement si les
  4 lignes suivantes ne contiennent pas déjà un lien legifrance vers ce numéro.
- ABROGE_DIFF : mention « (abrogation différée) » ajoutée en fin de filiation.

Usage :
  python3 inject_citations.py --dry-run [fichier_relatif]
  python3 inject_citations.py --apply   [fichier_relatif]
"""
import json
import os
import re
import sys

ROOT = "/home/crilocom/accident-main"
TOKEN = os.path.join(ROOT, "⚖️ Actes/🔑 Token")
GLOSS = "/tmp/glossaire.json"

ALIASES = [
    ("procédure civile", "Code de procédure civile"),
    ("procedure civile", "Code de procédure civile"),
    ("procédure pénale", "Code de procédure pénale"),
    ("procedure penale", "Code de procédure pénale"),
    ("sécurité sociale", "Code de la sécurité sociale"),
    ("securite sociale", "Code de la sécurité sociale"),
    ("des assurances", "Code des assurances"),
    ("du travail", "Code du travail"),
    ("de commerce", "Code de commerce"),
    ("santé publique", "Code de la santé publique"),
    ("de la route", "Code de la route"),
    ("de la consommation", "Code de la consommation"),
    ("général des collectivités", "Code général des collectivités territoriales"),
    ("pénal", "Code pénal"),
    ("penal", "Code pénal"),
    ("civil", "Code civil"),
]
ART_RE = re.compile(
    r"[Aa]rticles?\s+((?:[LRD]\.?\s?)?\d[\d\-\.\s]*?\d|\d+)\s+du\s+[Cc]ode\s+([^,.;:)\]\n«»\"]+)"
)


def norm(s):
    return re.sub(r"[^0-9A-Za-z\-]", "", s.replace(" ", "").replace(".", "")).upper()


def resolve_code(frag):
    f = frag.lower()
    for alias, full in ALIASES:
        if alias in f:
            return full
    return None


def load_gloss():
    g = json.load(open(GLOSS))
    # index par (normnum, code)
    idx = {}
    for k, v in g.items():
        num, code = k.split("||")
        idx[(norm(num), code)] = v
    return idx


def process_file(path, idx, apply=False):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    out = []
    in_yaml = False
    inserts = 0
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        out.append(line)
        if i == 0 and s == "---":
            in_yaml = True
            i += 1
            continue
        if in_yaml:
            if s == "---":
                in_yaml = False
            i += 1
            continue
        if s.startswith(">") or s.startswith("#"):
            i += 1
            continue
        # chercher citations dans la ligne
        matches = list(ART_RE.finditer(line))
        if matches:
            # déjà un bloc juste après ?
            nxt = "".join(lines[i + 1:i + 5])
            blocks_to_add = []
            for m in matches:
                num = re.sub(r"\s+", "", m.group(1))
                code = resolve_code(m.group(2))
                if not code:
                    continue
                if "legifrance" in nxt and norm(num) in norm(nxt):
                    continue
                v = idx.get((norm(num), code))
                if not v:
                    continue
                block = v["block"]
                if v.get("etat") == "ABROGE_DIFF":
                    block = block.replace(".** <br>", " — abrogation différée.** <br>", 1)
                blocks_to_add.append(block)
            if blocks_to_add:
                # insérer une ligne vide puis les blocs
                addition = "\n" + "\n>\n".join(blocks_to_add) + "\n"
                out.append(addition)
                inserts += len(blocks_to_add)
        i += 1
    if apply and inserts:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(out)
    return inserts


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    idx = load_gloss()
    targets = []
    if args:
        targets = [os.path.join(TOKEN, args[0])]
    else:
        for dp, _, fns in os.walk(TOKEN):
            for fn in fns:
                if fn.endswith(".md"):
                    targets.append(os.path.join(dp, fn))
    total = 0
    for p in sorted(targets):
        c = process_file(p, idx, apply=apply)
        if c:
            total += c
            print(f"  {'INSÉRÉ' if apply else 'à insérer'} {c:3d}  {os.path.relpath(p, TOKEN)}")
    print(f"\nTOTAL {'insérés' if apply else 'à insérer'}: {total}")


if __name__ == "__main__":
    main()
