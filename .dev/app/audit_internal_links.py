#!/usr/bin/env python3
"""
Audit des liens internes relatifs — vérifie qu'aucun lien `.md`→`.md` n'est cassé.

Parcourt tous les fichiers `.md` du projet, extrait les liens relatifs internes
(ceux qui commencent par `../`, `./` ou un dossier racine du projet), résout le
chemin et teste l'existence de la cible.

Usage :
    python3 .dev/app/audit_internal_links.py          # sortie humaine
    python3 .dev/app/audit_internal_links.py --json   # sortie JSON (pour fix_internal_links.py)
    python3 .dev/app/audit_internal_links.py --ci     # sortie JSON compatible CI

Exit codes : 0 = tout OK, 1 = au moins un lien cassé
"""

import argparse
import json
import os
import re
import sys
from urllib.parse import unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKIP_DIRS = {'.git', '.venv', '__pycache__', 'node_modules', '.pytest_cache', '.opencode'}
# Fichiers contenant des exemples volontaires de liens (faux positifs)
SKIP_FILES = {
    'CONVENTIONS.md', 'VACCIN.md', 'DECISIONS.md', 'DESIGN.md',
    'STRICT VARIABLES.md',
}
ROOT_DIRS = ('Actes', 'Lois', 'Memory', 'Rapports', 'Annexes', '.dev')

MD_LINK_RE = re.compile(r'\]\(([^)]+)\)')
HTML_LINK_RE = re.compile(r'<a\s+(?:[^>]*?\s+)?href="([^"]+)"')


def build_basename_index():
    """Construit un index basename -> [chemins relatifs] pour tout le projet."""
    index = {}
    for dp, dirs, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT).split(os.sep)
        if any(s in SKIP_DIRS for s in rel):
            dirs[:] = []
            continue
        for f in fn:
            if not f.endswith('.md'):
                continue
            index.setdefault(f, []).append(
                os.path.relpath(os.path.join(dp, f), ROOT)
            )
    return index


def is_internal(link: str) -> bool:
    if link.startswith(('http://', 'https://', 'file://', '#')):
        return False
    return True


def link_is_protocol_relative(link: str) -> bool:
    return link.startswith('//')


def resolve_path(link: str, source_dir: str) -> str:
    link_stripped = unquote(link.split('#')[0])
    if not link_stripped:
        return None
    first_seg = link_stripped.split('/')[0]
    if first_seg and first_seg in ROOT_DIRS:
        candidate = os.path.normpath(os.path.join(ROOT, link_stripped))
    else:
        candidate = os.path.normpath(os.path.join(source_dir, link_stripped))
    return candidate


def check_link(link: str, source_file: str, basename_index: dict) -> dict:
    source_dir = os.path.dirname(source_file)
    resolved = resolve_path(link, source_dir)
    if resolved is None:
        return None

    decoded = unquote(link.split('#')[0])
    exists = os.path.exists(resolved)

    candidates = None
    if not exists:
        basename = os.path.basename(decoded)
        if basename in basename_index:
            candidates = basename_index[basename]

    return {
        "source": os.path.relpath(source_file, ROOT),
        "link": link,
        "decoded": decoded,
        "resolved": os.path.relpath(resolved, ROOT) if resolved.startswith(ROOT + '/') or resolved == ROOT else resolved,
        "exists": exists,
        "candidates": candidates,
    }


def scan_file(filepath: str, basename_index: dict) -> list:
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return results

    for m in MD_LINK_RE.finditer(content):
        link = m.group(1).strip()
        if is_internal(link):
            r = check_link(link, filepath, basename_index)
            if r is not None and not r['exists']:
                results.append(r)

    for m in HTML_LINK_RE.finditer(content):
        link = m.group(1).strip()
        if is_internal(link):
            r = check_link(link, filepath, basename_index)
            if r is not None and not r['exists']:
                results.append(r)

    return results


def run_audit(basename_index: dict) -> list:
    all_broken = []
    for dp, dirs, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT).split(os.sep)
        if any(s in SKIP_DIRS for s in rel):
            dirs[:] = []
            continue
        for f in fn:
            if not f.endswith('.md'):
                continue
            if f in SKIP_FILES:
                continue
            filepath = os.path.join(dp, f)
            all_broken.extend(scan_file(filepath, basename_index))
    return all_broken


def main():
    parser = argparse.ArgumentParser(description="Audit des liens internes .md")
    parser.add_argument('--json', action='store_true', help="Sortie JSON détaillée")
    parser.add_argument('--ci', action='store_true', help="Sortie JSON pour CI")
    args = parser.parse_args()

    basename_index = build_basename_index()
    broken = run_audit(basename_index)

    if args.json or args.ci:
        output = {
            "status": "broken" if broken else "ok",
            "total_broken": len(broken),
            "results": broken,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        if not broken:
            print(f"✅ {len(broken)} liens cassés — tous les liens internes sont valides.")
            sys.exit(0)

        print(f"❌ {len(broken)} lien(s) cassé(s) :\n")
        by_file = {}
        for b in broken:
            by_file.setdefault(b['source'], []).append(b)

        for src, links in sorted(by_file.items()):
            print(f"  📄 {src}")
            for l in links:
                print(f"     {l['decoded']} → INTROUVABLE")
                if l['candidates']:
                    n = len(l['candidates'])
                    print(f"       ({n} candidat(s) : {', '.join(l['candidates'][:3])}{'...' if n > 3 else ''})")
            print()

        print("---")
        print(f"Correction : python3 .dev/app/fix_internal_links.py")
        print(f"Forcer le commit : git commit --no-verify")
        sys.exit(1)


if __name__ == '__main__':
    main()
