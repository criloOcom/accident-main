#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Injecte les notes de bas de page législatives dans un sous-dossier Token.
Sûreté: n'injecte QUE si un code est explicitement adjacent à l'article (pas de devinette).
Réutilise /tmp/sources_dict.json (dictionnaire vérifié Légifrance)."""
import re, os, sys, json

DICT = json.load(open("/tmp/sources_dict.json", encoding="utf-8"))
# index par numéro normalisé -> liste de (code, entry)
by_num = {}
for key, e in DICT.items():
    num = key.split("|")[0]
    by_num.setdefault(re.sub(r'[\s.]', '', num).upper(), []).append((e["code"], e))

# alias code affiché -> nom exact du dict
CODE_ALIASES = {
    "cpc": "Code de procédure civile",
    "code de procédure civile": "Code de procédure civile",
    "cpp": "Code de procédure pénale",
    "code de procédure pénale": "Code de procédure pénale",
    "code civil": "Code civil",
    "code pénal": "Code pénal", "code penal": "Code pénal",
    "code des assurances": "Code des assurances",
    "code de la sécurité sociale": "Code de la sécurité sociale",
    "code du travail": "Code du travail",
    "code de commerce": "Code de commerce",
    "code de la santé publique": "Code de la santé publique",
    "code général des collectivités territoriales": "Code général des collectivités territoriales",
    "cgct": "Code général des collectivités territoriales",
    "code des relations entre le public et l'administration": "Code des relations entre le public et l'administration",
    "crpa": "Code des relations entre le public et l'administration",
}

def norm_code(raw):
    r = re.sub(r'\s+', ' ', raw.strip().lower()).rstrip('.')
    # match par préfixe le plus long
    best = None
    for k, v in CODE_ALIASES.items():
        if r.startswith(k) or k.startswith(r) and len(r) >= 6:
            if best is None or len(k) > len(best[0]):
                best = (k, v)
    return best[1] if best else None

# regex: article(s) NUM [du] CODE   — code obligatoire et adjacent
ART = re.compile(
    r'\b(articles?|art\.)\s+'
    r'((?:(?:L|R|D)\.?\s?)?\d+[\-\d]*(?:\s*(?:et|,)\s*(?:(?:L|R|D)\.?\s?)?\d+[\-\d]*)*)'
    r'\s+(?:du|de la|des|de l\')\s+'
    r'(Code[\w\sé\'’]{3,55}?|CPC|CPP|CGCT|CRPA)'
    r'(?=[\s,.;:\)\]]|$)',
    re.IGNORECASE)

def has_source_zone(txt):
    return '<!-- Source -->' in txt

def process_file(path):
    raw = open(path, encoding="utf-8").read()
    # ne pas toucher si déjà une zone Source (on complèterait plus tard manuellement)
    body = raw
    # zone d'exclusion: si déjà footnotes/liens légifrance sur la même occurrence
    assigned = {}   # (num,code_exact) -> tag
    order = []
    def repl(m):
        lead, nums_raw, code_raw = m.group(1), m.group(2), m.group(3)
        # si déjà suivi d'un [^ ou lien legifrance juste après -> laisser
        tail = body[m.end():m.end()+15]
        if tail.lstrip().startswith('[^'):
            return m.group(0)
        code_exact = norm_code(code_raw)
        if not code_exact:
            return m.group(0)
        nums = re.split(r'\s*(?:et|,)\s*', nums_raw)
        tags = []
        for n in nums:
            nn = re.sub(r'[\s.]', '', n).upper()
            cands = by_num.get(nn, [])
            entry = next((e for c, e in cands if c == code_exact), None)
            if not entry:
                return m.group(0)  # article/code non vérifié -> ne rien toucher
            k = (nn, code_exact)
            if k not in assigned:
                tag = f"loi-{len(order)+1}"
                assigned[k] = tag
                order.append((k, entry))
            tags.append(assigned[k])
        return m.group(0) + "".join(f"[^{t}]" for t in tags)
    new_body = ART.sub(repl, body)
    if not order:
        return None  # rien injecté
    # construire section source
    lines = ["", "<!-- Source -->", "<hr><hr>", "", "## Sources Législation", ""]
    for (k, entry) in order:
        tag = assigned[k]
        block = entry["block"]
        # indenter les lignes 2 et 3 sous la note + ↩
        bl = block.split("\n")
        out = f"[^{tag}]: {bl[0]}\n"
        for extra in bl[1:]:
            out += f"    {extra}\n"
        out = out.rstrip("\n") + " ↩"
        lines.append(out)
        lines.append("")
    src = "\n".join(lines).rstrip() + "\n"
    # si zone source existe déjà, insérer avant <!-- /Source -->, sinon ajouter à la fin
    if has_source_zone(new_body):
        return ("SKIP_HAS_SOURCE", None)
    new_body = new_body.rstrip() + "\n" + src + "<!-- /Source -->\n"
    open(path, "w", encoding="utf-8").write(new_body)
    return len(order)

if __name__ == "__main__":
    subdir = sys.argv[1]
    base = os.path.join("/home/crilocom/accident-main/Actes/Token/Courriers", subdir)
    total_files = 0; total_notes = 0; skipped = []
    for r, dirs, fs in os.walk(base):
        for f in sorted(fs):
            if not f.endswith(".md") or f == "README.md":
                continue
            p = os.path.join(r, f)
            res = process_file(p)
            if res is None:
                continue
            if isinstance(res, tuple):
                skipped.append((os.path.relpath(p, base), res[0]))
                continue
            total_files += 1; total_notes += res
            print(f"  +{res} notes  {os.path.relpath(p, base)}")
    print(f"\n{subdir}: {total_files} fichiers enrichis, {total_notes} notes injectées")
    if skipped:
        print("SKIP (zone Source déjà présente, à compléter manuellement):")
        for s, why in skipped: print("   -", s)
