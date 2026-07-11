#!/usr/bin/env python3
"""
add_drive_links.py — Ajoute un lien cliquable vers Google Drive dans le corps
de chaque fichier .md dont le YAML contient un `drive_id`.

Le YAML front matter n'est pas rendu cliquable sur GitHub ; on ajoute donc
une ligne de lien dans le corps (apres le premier titre #), du type :
  > 🔗 Source Google Drive : [1W-C6nM5...](https://drive.google.com/open?id=1W-C6nM5...)

Usage :
  python3 .dev/app/add_drive_links.py           # dry-run
  python3 .dev/app/add_drive_links.py --apply     # ecrit
"""
import os
import re
import sys
import argparse

ROOT = "/home/crilocom/accident-main"
SKIP_DIRS = {'.git', '.pytest_cache', '.venv', 'node_modules', '__pycache__', '.opencode'}

DRIVE_RE = re.compile(r'^\s*drive_id\s*:\s*([^\s]+)\s*$', re.MULTILINE)
HAS_LINK_RE = re.compile(r'drive\.google\.com/open\?id=')


def extract_yaml_drive_id(content):
    if not content.startswith('---'):
        return None
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n?', content, re.DOTALL)
    if not m:
        return None
    yml = m.group(1)
    dm = DRIVE_RE.search(yml)
    return dm.group(1).strip().strip('"').strip("'") if dm else None


def add_link(content, drive_id):
    # deja present ?
    if HAS_LINK_RE.search(content):
        return None
    url = f"https://drive.google.com/open?id={drive_id}"
    short = drive_id[:12] + "…" if len(drive_id) > 12 else drive_id
    link_line = f"\n> 🔗 Source Google Drive : [{short}]({url})\n"
    L = content.split('\n')
    # trouve le 1er titre # pour inserer apres
    insert_at = None
    for i, ln in enumerate(L):
        if ln.startswith('# '):
            insert_at = i + 1
            break
    if insert_at is None:
        # pas de titre : insere apres le YAML
        for i, ln in enumerate(L):
            if ln.strip() == '---' and i > 0:
                insert_at = i + 1
                break
    if insert_at is None:
        insert_at = 0
    L.insert(insert_at, link_line.strip())
    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    dry = not args.apply
    total = 0
    for dp, _, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT).split(os.sep)
        if any(s in SKIP_DIRS for s in rel):
            continue
        for f in fn:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f)
            txt = open(p, encoding='utf-8').read()
            did = extract_yaml_drive_id(txt)
            if not did:
                continue
            if HAS_LINK_RE.search(txt):
                continue
            if dry:
                total += 1
                if total <= 15:
                    print(f"  [DRY] {os.path.relpath(p, ROOT)} :: {did[:20]}…")
                continue
            new = add_link(txt, did)
            if new:
                open(p, 'w', encoding='utf-8').write(new)
                total += 1
    print(f"\n{'DRY-RUN' if dry else 'APPLY'} : {total} fichiers avec lien Drive ajouté.")


if __name__ == '__main__':
    main()
