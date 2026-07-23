#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3 : normalise UN fichier Token au format bloc-citation (blockquote 3 lignes),
en réutilisant /tmp/sources_dict.json (articles vérifiés Légifrance).
Garde-fous :
- ne traite QUE le corps hors zone <!-- Source -->.
- ignore les occurrences déjà dans un lien markdown [texte](url).
- code résolu : explicite adjacent OU mot-clé non ambigu dans fenêtre.
- n'injecte que si (num,code) dans le dictionnaire vérifié (zéro devinette)."""
import re, sys, os, json

DICT = json.load(open("/tmp/sources_dict.json", encoding="utf-8"))
by_num = {}
for key, e in DICT.items():
    num = key.split("|")[0]
    by_num.setdefault(re.sub(r'[\s.]', '', num).upper(), []).append((e["code"], e))

CODE_ALIASES = {
    "code de procédure civile": "Code de procédure civile",
    "code de procédure pénale": "Code de procédure pénale",
    "code civil": "Code civil",
    "code pénal": "Code pénal", "code penal": "Code pénal",
    "code des assurances": "Code des assurances",
    "code de la sécurité sociale": "Code de la sécurité sociale",
    "code du travail": "Code du travail",
    "code de commerce": "Code de commerce",
    "code de la santé publique": "Code de la santé publique",
    "code général des collectivités territoriales": "Code général des collectivités territoriales",
    "code des relations entre le public et l'administration": "Code des relations entre le public et l'administration",
}
def norm_code(raw):
    r = re.sub(r'\s+', ' ', raw.strip().lower()).rstrip('.')
    best=None
    for k,v in CODE_ALIASES.items():
        if (r.startswith(k) or k.startswith(r)) and len(r)>=6:
            if best is None or len(k)>len(best[0]): best=(k,v)
    return best[1] if best else None

KEYWORDS = {
    "code civil": "Code civil",
    "code pénal": "Code pénal", "code penal": "Code pénal",
    "code des assurances": "Code des assurances",
    "code de la sécurité sociale": "Code de la sécurité sociale",
    "code du travail": "Code du travail",
    "code de commerce": "Code de commerce",
    "code de la santé publique": "Code de la santé publique",
    "code général des collectivités": "Code général des collectivités territoriales",
    "code des relations entre le public": "Code des relations entre le public et l'administration",
}

ART = re.compile(
    r'\b(articles?|art\.)\s+'
    r'((?:(?:L|R|D)\.?\s?)?\d+[\-\d]*(?:\s*(?:et|,)\s*(?:(?:L|R|D)\.?\s?)?\d+[\-\d]*)*)'
    r'(?:\s+(?:du|de la|des|de l\')\s+(Code[\w\sé\'’]{3,55}?|CPC|CPP|CGCT|CRPA))?'
    r'(?=[\s,.;:\)\]«]|$)',
    re.IGNORECASE)

def process_file(path):
    raw = open(path, encoding="utf-8").read()
    had_src = "<!-- Source -->" in raw
    if had_src:
        m = re.search(r'<!-- Source -->.*?<!-- /Source -->', raw, flags=re.DOTALL)
        source_zone = m.group(0)
        body = raw[:m.start()] + raw[m.end():]
    else:
        body = raw
    # retrait des ancres hors zone source (déjà gérées)
    body = re.sub(r'\[\^\w+\]', '', body)
    # repère les positions à ignorer : liens markdown [..](..)
    # ignorer seulement l'INTÉRIEUR des liens [texte](url), pas le texte qui suit
    ignore_spans = []
    for mm in re.finditer(r'\[([^\]]*)\]\(([^)]*)\)', body):
        # intérieur du label [texte] et de l'url (url)
        ignore_spans.append((mm.start(1)-1, mm.end(1)+1))  # crochets du label
        ignore_spans.append((mm.start(2)-1, mm.end(2)+1))  # parenthèses de l'url
    def in_ignore(pos):
        return any(a <= pos < b for a,b in ignore_spans)
    assigned={}; order=[]; skipped=0
    def add(num_norm, code_exact):
        cands=by_num.get(num_norm,[])
        entry=next((e for c,e in cands if c==code_exact),None)
        if not entry: return None
        key=(num_norm,code_exact)
        if key not in assigned:
            tag=f"n{len(order)+1}"; assigned[key]=tag; order.append((key,entry))
        return assigned[key]
    def repl(m):
        nonlocal skipped
        if m is None:
            return ""
        s=m.start()
        if in_ignore(s): return m.group(0)
        nums_raw=m.group(2)
        code_explicit = norm_code(m.group(3)) if m.group(3) else None
        code = code_explicit
        if not code:
            win = " ".join(body[max(0,s-130):s].lower().split() + body[m.end():m.end()+60].lower().split())
            for kw,c in KEYWORDS.items():
                if kw in win: code=c; break
        if not code:
            skipped+=1; return m.group(0)
        nums=re.split(r'\s*(?:et|,)\s*', nums_raw)
        tags=[]
        for n in nums:
            nn=re.sub(r'[\s.]','',n).upper()
            t=add(nn,code)
            if not t: return m.group(0)
            tags.append(t)
        return m.group(0)+"".join(f"[^{t}]" for t in tags)
    new_body = ART.sub(repl, body)
    if not order:
        return ("SKIP_NONE", skipped)
    lines=["","<!-- Source -->","<hr><hr>","","## Sources Législation",""]
    for (k,entry) in order:
        tag=assigned[k]
        bl=entry["block"].split("\n")
        out=f"[^{tag}]: {bl[0]}\n"
        for extra in bl[1:]: out+=f"    {extra}\n"
        out=out.rstrip("\n")+" ↩"
        lines.append(out); lines.append("")
    src="\n".join(lines).rstrip()+"\n"
    if had_src:
        new_body = new_body.rstrip()+"\n"+src+"<!-- /Source -->\n"
    else:
        new_body = new_body.rstrip()+"\n"+src+"<!-- /Source -->\n"
    open(path,"w",encoding="utf-8").write(new_body)
    return (len(order), skipped)

if __name__=="__main__":
    p=sys.argv[1]
    res=process_file(p)
    if isinstance(res,tuple):
        print(f"  {os.path.basename(p)}: {res[0]} (nues restantes={res[1]})")
    else:
        print(f"  {os.path.basename(p)}: +{res} notes")
