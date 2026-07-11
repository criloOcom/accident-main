#!/usr/bin/env python3
"""
audit_citation_links.py — Vérifie que toute citation interne de dossier/fichier
est un lien relatif cliquable (Règle #17).

Signale en avertissement toute citation backtick interne non liée.
Usage :
  python3 .dev/app/audit_citation_links.py
"""
import os
import re

ROOT = "/home/crilocom/accident-main"
SKIP_DIRS = {'.git', '.pytest_cache', '.venv', 'node_modules', '__pycache__', '.opencode'}
CITATION_KEYWORDS = ('Actes', 'Lois', 'Memory', 'Rapports', 'Annexes')
CITATION_RE = re.compile(r'`([^`]*?(?:' + '|'.join(CITATION_KEYWORDS) + r')[^\n`]*?)`')
LINK_RE = re.compile(r'\]\(([^)]+)\)')


def resolve_target(cand, base_dir):
    """Renvoie True si la cible existe (depuis base_dir pour les chemins relatifs)."""
    cand = cand.rstrip('/')
    # chemin relatif si premier segment n'est pas un dossier racine connu du depot
    first = cand.split('/')[0]
    ROOT_KEYS = ('⚖️ Actes', '📜 Lois', '🧠 Memory', '📊 Rapports', '📎 Annexes', '.dev')
    if cand.startswith(('.', '../', './')) or first not in ROOT_KEYS:
        target = os.path.normpath(os.path.join(base_dir, cand))
    else:
        target = os.path.join(ROOT, cand)
    if os.path.isfile(target):
        return True
    if os.path.isdir(target):
        return True
    if '{token,reel}' in cand:
        for subst in ('🔑 Token', '👤 Reel'):
            c2 = cand.replace('{token,reel}', subst)
            t2 = os.path.join(ROOT, c2)
            if os.path.isfile(t2) or os.path.isdir(t2):
                return True
    return False


def main():
    warnings = 0
    files_with = 0
    for dp, _, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT).split(os.sep)
        if any(s in SKIP_DIRS for s in rel):
            continue
        for f in fn:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f)
            text = open(p, encoding='utf-8').read()
            rel_path = os.path.relpath(p, ROOT)
            linked = set(m.group(1) for m in LINK_RE.finditer(text))
            file_warn = []
            for m in CITATION_RE.finditer(text):
                cand = m.group(1).rstrip('/')
                s = m.start()
                if s > 0 and text[s - 1] in '])':
                    continue  # deja dans un lien
                if any(cand == l or cand in l or l in cand for l in linked):
                    continue
                # cible introuvable OU non liee -> warning
                file_warn.append(cand)
            if file_warn:
                files_with += 1
                warnings += len(file_warn)
                if files_with <= 20:
                    print(f"⚠️  {rel_path}")
                    for c in file_warn[:6]:
                        base = os.path.dirname(p)
                        ok = "existe" if resolve_target(c, base) else "INTROUVABLE"
                        print(f"     `{c}` ({ok})")

    print(f"\nBilan : {warnings} citation(s) interne(s) non liée(s) dans {files_with} fichier(s).")
    if warnings == 0:
        print("✅ Toutes les citations internes sont cliquables.")


if __name__ == '__main__':
    main()
