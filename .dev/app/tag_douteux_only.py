#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Taggue [À VÉRIFIER] UNIQUEMENT sur les numéros d'articles dont Légifrance n'a
pas trouvé de correspondance (vrais douteux). N'injecte RIEN d'autre."""
import re, os
root="/home/crilocom/accident-main"
DOUTEUX = {"827","L725-4"}
TAG=" [À VÉRIFIER]"
ART=re.compile(r'\b(articles?|art\.)\s+((?:(?:L|R|D)\.?\s?)?\d+[\-\d]*)',re.IGNORECASE)
scope=["Actes/Token/Courriers","Actes/Token/Actes_proceduraux","Actes/Token/Analyses_juridiques"]
total=0
for r,dirs,fs in os.walk(root):
    dirs[:]=[d for d in dirs if d not in (".git",".dev",".opencode","node_modules","__pycache__")]
    rel=os.path.relpath(r,root)
    if not any(rel.startswith(s) for s in scope): continue
    for f in fs:
        if not f.endswith(".md") or f=="README.md": continue
        p=os.path.join(r,f); t=open(p,encoding="utf-8").read()
        out=[]; last=0
        for m in ART.finditer(t):
            e=m.end(); nn=re.sub(r'[\s.]','',m.group(2)).upper()
            # déjà une note ? ne pas tagguer
            if t[e:e+4].startswith("[^"):
                out.append(t[last:e]); last=e; continue
            if nn in DOUTEUX and t[e:e+len(TAG)]!=TAG:
                out.append(t[last:e]+TAG); last=e; total+=1
            else:
                out.append(t[last:e]); last=e
        out.append(t[last:])
        open(p,"w",encoding="utf-8").write("".join(out))
print(f"Tags [À VÉRIFIER] posés sur douteux: {total}")
