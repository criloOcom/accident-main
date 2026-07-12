#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_blocks.py — Approche B : uniformise les blocs de citation au format
canonique (texte > filiation > lien) dans les fichiers Token.

Cible : blocs "inversés" de l'ancien format :
   > « texte » <br>          (ou sur ligne séparée)
   > [Article X](url) <br>
   > **Code > ...**          (filiation en 3e position)
Réorganisés en :
   > « texte » <br>
   > **Code > ...** <br>
   > [Article X](url)

Usage :
  python3 normalize_blocks.py --dry-run [fichier]
  python3 normalize_blocks.py --apply   [fichier]
"""
import os
import re
import sys

TOKEN = "/home/crilocom/accident-main/⚖️ Actes/🔑 Token"
LINK = re.compile(r">\s*\[Article[^\n]*\]\(https?://www\.legifrance\.gouv\.fr/codes/article_lc/([^\s)]+)\)\s*(<br>)?\s*$", re.M)
FIL = re.compile(r">\s*\*\*([^*].*?)\*\*\s*(<br>)?\s*$")


def is_bq(l):
    return l.lstrip().startswith(">")


def normalize_block(lines):
    """lines = groupe de lignes blockquote consécutives contenant un lien legifrance.
    Retourne la liste réordonnée au format canonique."""
    texte = filiation = lien = None
    for l in lines:
        s = l.strip()
        if "legifrance.gouv.fr/codes/article_lc" in s:
            lien = l.rstrip()
            if not lien.endswith("<br>"):
                lien = lien + " <br>" if not lien.endswith("<br") else lien
            # on vire le <br> final pour le reconstruire proprement
            lien = re.sub(r"\s*<br>\s*$", "", lien)
            lien = lien + " <br>"
        elif s.startswith(">**") and s.rstrip().endswith("**") or (
            s.startswith("> **") and "**" in s[4:]
        ):
            # filiation
            m = re.match(r">\s*\*\*(.+?)\*\*\s*$", s)
            if m:
                filiation = "> **" + m.group(1).rstrip(".") + ".** <br>"
        elif "«" in s and "»" in s:
            texte = l.rstrip()
            if not texte.endswith("<br>"):
                texte = re.sub(r"\s*<br>\s*$", "", texte) + " <br>"
    if lien is None:
        return lines  # pas un bloc citation, on laisse tel quel
    out = []
    if texte:
        out.append(texte)
    if filiation:
        out.append(filiation)
    out.append(lien)
    return out


def process(path, apply=False):
    L = open(path, encoding="utf-8").read().split("\n")
    out = []
    i = 0
    changed = 0
    n = len(L)
    while i < n:
        # detecter un bloc: une ligne bq avec lien legifrance (eventuellement précédée d'un > « texte »)
        if is_bq(L[i]) and "legifrance.gouv.fr/codes/article_lc" in L[i]:
            start = i
            if start > 0 and is_bq(L[start - 1]) and "«" in L[start - 1] and "legifrance" not in L[start - 1]:
                start -= 1
            j = i
            while j + 1 < n and is_bq(L[j + 1]):
                j += 1
            grp = L[start:j + 1]
            new = normalize_block(grp)
            if new != grp:
                changed += 1
            out.extend(new)
            i = j + 1
        else:
            out.append(L[i])
            i += 1
    if apply and changed:
        open(path, "w", encoding="utf-8").writelines("\n".join(out) if False else "")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out))
    return changed


def main():
    apply = "--apply" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        p0 = args[0]
        targets = [p0 if os.path.isabs(p0) else os.path.join(TOKEN, p0)]
    else:
        targets = []
        for dp, _, fns in os.walk(TOKEN):
            for fn in fns:
                if fn.endswith(".md"):
                    targets.append(os.path.join(dp, fn))
    total = 0
    for p in sorted(targets):
        c = process(p, apply=apply)
        if c:
            total += c
            print(f"  {'NORMALISÉ' if apply else 'à normaliser'} {c:2d}  {os.path.relpath(p, TOKEN)}")
    print(f"\nTOTAL {'normalisés' if apply else 'à normaliser'}: {total}")


if __name__ == "__main__":
    main()
