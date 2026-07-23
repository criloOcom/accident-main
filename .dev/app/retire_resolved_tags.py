#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Passe 2 robuste : pour chaque fichier du périmètre sortant,
1) retire tous les '[À VÉRIFIER]' existants,
2) réinjecte les notes de bas de page pour articles résolubles (inject_footnotes_v2),
3) remet '[À VÉRIFIER]' UNIQUEMENT sur les citations restées nues (non résolubles).
Idempotent et sans doublon."""
import re, os, sys, json
root="/home/crilocom/accident-main"
sys.path.insert(0, os.path.join(root,".dev/app"))
import inject_footnotes_v2 as inj
DICT=json.load(open("/tmp/sources_dict.json",encoding="utf-8"))
by_num={}
for key,e in DICT.items():
    nn=re.sub(r'[\s.]','',key.split("|")[0]).upper()
    by_num.setdefault(nn,set()).add(e["code"])
KEYWORDS=inj.KEYWORDS
MAPCODE={"code de procédure civile":"Code de procédure civile","code de procédure pénale":"Code de procédure pénale"}
ART=re.compile(r'\b(articles?|art\.)\s+((?:(?:L|R|D)\.?\s?)?\d+[\-\d]*)',re.IGNORECASE)
TAG=" [À VÉRIFIER]"
scope=["Actes/Token/Courriers","Actes/Token/Actes_proceduraux","Actes/Token/Analyses_juridiques"]

def resolvable(t, s, e):
    m=ART.match(t, s)
    if not m: return False
    nn=re.sub(r'[\s.]','',m.group(2)).upper()
    code=None
    em=re.match(r'\s+(?:du|de la|des|de l\')\s+(Code[\w\sé\'’]{3,55}?|CPC|CPP)',t[e:e+40],re.I)
    if em:
        rc=em.group(1).lower(); code=MAPCODE.get(rc) or ("Code de procédure civile" if "procédure civile" in rc else "Code de procédure pénale" if "procédure pénale" in rc else None)
    if not code:
        win=" ".join(t[max(0,s-130):s].lower().split()+t[e:e+60].lower().split())
        for kw,c in KEYWORDS.items():
            if kw in win: code=c; break
    return nn in by_num and (code in by_num[nn] if code else len(by_num[nn])==1)

retired=0; retagged=0
for r,dirs,fs in os.walk(root):
    dirs[:]=[d for d in dirs if d not in (".git",".dev",".opencode","node_modules","__pycache__")]
    rel=os.path.relpath(r,root)
    if not any(rel.startswith(s) for s in scope): continue
    for f in fs:
        if not f.endswith(".md") or f=="README.md": continue
        p=os.path.join(r,f)
        t=open(p,encoding="utf-8").read()
        # 1) retirer tous les tags existants SUR DISQUE
        t=t.replace(TAG,"")
        open(p,"w",encoding="utf-8").write(t)
        # 2) réinjecter (remet les notes pour articles résolubles, laisse nues le reste)
        inj.process_file(p)
        # relire le résultat post-injection
        t2=open(p,encoding="utf-8").read()
        # 3) remettre [À VÉRIFIER] sur citations nues restantes (non couvertes par une note)
        out=[]
        last=0
        for m in ART.finditer(t2):
            e=m.end()
            # déjà doté d'une note ? regarder si [^..] collé juste après (hors zone Source)
            if t2[e:e+4].startswith("[^"):
                out.append(t2[last:e]); last=e; continue
            # sinon tagger si non résolvable
            if not resolvable(t2, m.start(), e):
                out.append(t2[last:e]+TAG); last=e; retagged+=1
            else:
                out.append(t2[last:e]); last=e
        out.append(t2[last:])
        open(p,"w",encoding="utf-8").write("".join(out))
print(f"Tags retirés puis re-taggués sur non-résolus: {retagged}")
