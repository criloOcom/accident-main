#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dedup_citation_text.py — Supprime les doublons de texte dans les blocs de citation.

Bug introduit par normalize_blocks.py : certains blocs se sont retrouvés avec la
ligne `> « texte » <br>` DUPLIQUÉE (2 lignes identiques consécutives). Ce script
supprime toute ligne blockquote `> « ... » <br>` strictement identique à la ligne
précédente (et laisse le reste intact). Idempotent et sans risque.

Usage :
  python3 dedup_citation_text.py --dry-run [fichier]
  python3 dedup_citation_text.py --apply   [fichier]
"""
import os
import re
import sys

TOKEN = "/home/crilocom/accident-main/Actes/Token"
TEXT = re.compile(r"^>\s*« .+ »\s*<br>\s*$")


def process(path, apply=False):
    L = open(path, encoding="utf-8").read().split("\n")
    out = []
    removed = 0
    prev = None
    for l in L:
        s = l.strip()
        if TEXT.match(s) and prev is not None and s == prev.strip():
            removed += 1  # on saute cette ligne (doublon)
            continue
        out.append(l)
        prev = l
    if apply and removed:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out))
    return removed


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
            print(f"  {'SUPPRIMÉ' if apply else 'à supprimer'} {c:2d}  {os.path.relpath(p, TOKEN)}")
    print(f"\nTOTAL {'supprimés' if apply else 'à supprimer'}: {total}")


if __name__ == "__main__":
    main()
