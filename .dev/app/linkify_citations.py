#!/usr/bin/env python3
"""
linkify_citations.py — Rend cliquables toutes les citations internes de dossiers/fichiers.

Règle #17 (Memory/RULES.md) : toute citation interne (`Actes/...`, `Lois/...`,
`Memory/...`, `Rapports/...`, `📎 Annexes/...`, `.dev/...`) écrite entre backticks
sans lien doit devenir un lien relatif Markdown :
  - dossier cité  -> lien vers son README.md
  - fichier cité  -> lien vers le fichier

Usage :
  python3 .dev/app/linkify_citations.py            # dry-run (défaut)
  python3 .dev/app/linkify_citations.py --apply     # applique les modifications
"""
import os
import re
import sys

ROOT = "/home/crilocom/accident-main"
SKIP_DIRS = {'.git', '.pytest_cache', '.venv', 'node_modules', '__pycache__', '.opencode'}

# Citation interne : backtick contenant un des mots-clés de dossiers du dépôt
# (approche par mots-clés pour être robuste à l'encodage des emojis).
CITATION_KEYWORDS = ('Actes', 'Lois', 'Memory', 'Rapports', 'Annexes')
CITATION_RE = re.compile(r'`([^`]*?(?:' + '|'.join(CITATION_KEYWORDS) + r')[^\n`]*?)`')


def resolve_target(cand):
    """Renvoie le chemin relatif (depuis ROOT) à lier, ou None si introuvable."""
    cand = cand.rstrip('/')
    target = os.path.join(ROOT, cand)
    # 1. fichier exact
    if os.path.isfile(target):
        return cand
    # 2. dossier exact -> vers son README.md si present, sinon vers le dossier
    if os.path.isdir(target):
        readme = os.path.join(target, 'README.md')
        if os.path.isfile(readme):
            return os.path.join(cand, 'README.md')
        return cand  # lien vers le dossier (valide sur GitHub)
    # 3. tentative resolution convention historique {token,reel}
    if '{token,reel}' in cand:
        for subst in ('Token', 'Reel'):
            c2 = cand.replace('{token,reel}', subst)
            t2 = os.path.join(ROOT, c2)
            if os.path.isfile(t2):
                return c2
            if os.path.isdir(t2):
                r2 = os.path.join(t2, 'README.md')
                if os.path.isfile(r2):
                    return os.path.join(c2, 'README.md')
                return c2
    return None


def linkify_text(text, rel_path):
    """Transforme les citations non liées en liens. rel_path = chemin relatif du fichier courant."""
    changes = []
    source_dir = os.path.dirname(os.path.join(ROOT, rel_path))

    def repl(m):
        cand = m.group(1).rstrip('/')
        start = m.start()
        if start > 0 and text[start - 1] in '])':
            return m.group(0)
        resolved = resolve_target(cand)
        if resolved is None:
            return m.group(0)
        target_abs = os.path.join(ROOT, resolved)
        rel_link = os.path.relpath(target_abs, source_dir)
        changes.append((cand, resolved))
        return f'[{cand}]({rel_link})'

    new_text = CITATION_RE.sub(repl, text)
    return new_text, changes


def main():
    dry_run = '--apply' not in sys.argv
    total_changes = 0
    warnings = 0
    modified_files = 0
    for dp, _, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT).split(os.sep)
        if any(s in SKIP_DIRS for s in rel):
            continue
        for f in fn:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f)
            rel_path = os.path.relpath(p, ROOT)
            text = open(p, encoding='utf-8').read()
            new_text, changes = linkify_text(text, rel_path)
            if changes:
                modified_files += 1
                total_changes += len(changes)
                if modified_files <= 12:
                    print(f"\n* {rel_path} ({len(changes)} liens)")
                    for cand, resolved in changes[:5]:
                        print(f"    `{cand}` -> [{cand}]({resolved})")
                if not dry_run:
                    open(p, 'w', encoding='utf-8').write(new_text)
            # signale les cibles introuvables (non liees)
            for m in CITATION_RE.finditer(text):
                cand = m.group(1).rstrip('/')
                if resolve_target(cand) is None:
                    # deja dans un lien ?
                    s = m.start()
                    if s > 0 and text[s - 1] in '])':
                        continue
                    warnings += 1
                    if warnings <= 15:
                        print(f"  ⚠️  CIBLE INTROUVABLE (non liée) : {rel_path} :: `{cand}`")

    print(f"\n{'MODE DRY-RUN' if dry_run else 'MODE APPLY'}")
    print(f"Fichiers modifiés : {modified_files}")
    print(f"Liens créés : {total_changes}")
    print(f"Citations vers cibles introuvables (à corriger manuellement) : {warnings}")


if __name__ == '__main__':
    main()
