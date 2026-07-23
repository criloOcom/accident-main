#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Marque les citations d'articles nues restantes avec ' [À VÉRIFIER]' (Règle #11:
jamais deviner un JURITEXT). Ne touche pas aux citations déjà dotées d'une note ou d'un lien."""
import re, os, sys, json
root="/home/crilocom/accident-main"
DICT=json.load(open("/tmp/sources_dict.json",encoding="utf-8"))
by_num={}
for key,e in DICT.items():
    nn=re.sub(r'[\s.]','',key.split("|")[0]).upper()
    by_num.setdefault(nn,set()).add(e["code"])
KEYWORDS={"code civil":"Code civil","code pénal":"Code pénal","code des assurances":"Code des assurances",
 "code de la sécurité sociale":"Code de la sécurité sociale","code du travail":"Code du travail",
 "code de commerce":"Code de commerce","code de la santé publique":"Code de la santé publique",
 "code général des collectivités":"Code général des collectivités territoriales",
 "code des relations entre le public":"Code des relations entre le public et l'administration"}
MAPCODE={"code de procédure civile":"Code de procédure civile","code de procédure pénale":"Code de procédure pénale"}
ART=re.compile(r'\b(articles?|art\.)\s+((?:(?:L|R|D)\.?\s?)?\d+[\-\d]*)',re.IGNORECASE)
TAG=" [À VÉRIFIER]"

def strip(t):
    t=re.sub(r'<!-- Source -->.*?<!-- /Source -->','',t,flags=re.DOTALL)
    return re.sub(r'\[\^[^\]]+\]:.*$','',t,flags=re.MULTILINE)

def process(path):
    raw=open(path,encoding="utf-8").read()
    if "<!-- Source -->" in raw:
        m=re.search(r'<!-- Source -->.*?<!-- /Source -->',raw,flags=re.DOTALL)
        body=raw[:m.start()]+raw[m.end():]
    else:
        body=raw
    body=re.sub(r'\[\^\w+\]','',body)
    # ignorer liens markdown existants
    ignore=[(mm.start(),mm.end()) for mm in re.finditer(r'\[[^\]]*\]\([^)]*\)',body)]
    def in_ig(p): return any(a<=p<b for a,b in ignore)
    count=0
    def repl(m):
        nonlocal count
        s=m.start()
        if in_ig(s): return m.group(0)
        nn=re.sub(r'[\s.]','',m.group(2)).upper()
        code=None
        em=re.match(r'\s+(?:du|de la|des|de l\')\s+(Code[\w\sé\'’]{3,55}?|CPC|CPP)',body[m.end():m.end()+40],re.I)
        if em:
            rawc=em.group(1).lower()
            code=MAPCODE.get(rawc) or ("Code de procédure civile" if "procédure civile" in rawc else "Code de procédure pénale" if "procédure pénale" in rawc else None)
        if not code:
            win=" ".join(body[max(0,s-130):s].lower().split()+body[m.end():m.end()+60].lower().split())
            for kw,c in KEYWORDS.items():
                if kw in win: code=c; break
        covered = nn in by_num and (code in by_num[nn] if code else len(by_num[nn])==1)
        if covered: return m.group(0)
        # déjà taggé ?
        if body[m.end():m.end()+12].lstrip().startswith("[À VÉRIFIER]"): return m.group(0)
        count+=1
        return m.group(0)+TAG
    new_body=ART.sub(repl,body)
    if count:
        if "<!-- Source -->" in raw:
            new_full=new_body.rstrip()+"\n"+raw[raw.index("<!-- Source -->"):]
        else:
            new_full=new_body
        open(path,"w",encoding="utf-8").write(new_full)
    return count

if __name__=="__main__":
    total=0
    for r,dirs,fs in os.walk(root):
        dirs[:]=[d for d in dirs if d not in (".git",".dev",".opencode","node_modules","__pycache__")]
        rel=os.path.relpath(r,root)
        if not (rel.startswith("Actes/Token/Courriers") or rel.startswith("Actes/Token/Actes_proceduraux") or rel.startswith("Actes/Token/Analyses_juridiques")): continue
        for f in fs:
            if not f.endswith(".md") or f=="README.md": continue
            c=process(os.path.join(r,f))
            if c: total+=c; print(f"  +{c} À VÉRIFIER  {os.path.relpath(os.path.join(r,f),root)}")
    print(f"\nTotal citations tagguées À VÉRIFIER: {total}")
