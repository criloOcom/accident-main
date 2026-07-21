#!/usr/bin/env python3
"""
Migration : supprime les emoji des noms de dossiers dans tout le repo.
"""

import os, re, subprocess, sys, urllib.parse
from pathlib import Path

REPO = Path("/home/crilocom/accident-main")
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache"}
EXCLUDE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".svg", ".lock", ".woff", ".woff2"}

EMOJI_REGEX = re.compile(
    '[\U0001F300-\U0001F9FF'
    '\U0001FA00-\U0001FA6F'
    '\U0001FA70-\U0001FAFF'
    '\u2600-\u27BF\u2300-\u23FF\u2700-\u27BF'
    '\uFE00-\uFE0F\u200D\u20E3]+'
)

def has_emoji(name):
    return bool(EMOJI_REGEX.search(name))

def normalize_new_name(name):
    n = EMOJI_REGEX.sub('', name)
    n = re.sub(r'\s+', ' ', n).strip()
    return n.replace(' ', '_')

def scan_emoji_dirs(root):
    dirs = []
    for dirpath, dirnames, _ in os.walk(root):
        for dn in dirnames:
            if has_emoji(dn):
                full = os.path.join(dirpath, dn)
                rel = os.path.relpath(full, root)
                nn = normalize_new_name(dn)
                pdir = os.path.dirname(rel)
                nr = os.path.join(pdir, nn) if pdir and pdir != rel else nn
                dirs.append((rel, nr, dn, nn))
    return dirs

def collect_files(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if os.path.splitext(f)[1].lower() in EXCLUDE_EXTS:
                continue
            files.append(os.path.join(dirpath, f))
    return files

def build_replacements(dirs):
    reps_set = set()
    for old_rel, new_rel, old_name, new_name in dirs:
        for candidate in [old_rel, old_name]:
            # forme littérale
            reps_set.add((candidate, new_rel if candidate == old_rel else new_name))
            # forme URL-encodée
            reps_set.add((urllib.parse.quote(candidate, safe=''),
                          new_rel if candidate == old_rel else new_name))
            # forme avec underscores (variante CI)
            us = candidate.replace(' ', '_')
            if us != candidate:
                reps_set.add((us, new_rel if candidate == old_rel else new_name))
                reps_set.add((urllib.parse.quote(us, safe=''),
                              new_rel if candidate == old_rel else new_name))
    reps = [(o, n) for o, n in reps_set if o != n]
    reps.sort(key=lambda x: len(x[0]), reverse=True)
    return reps

def replace_in_file(fp, reps):
    try:
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception:
        return 0
    orig = content
    for old, new in reps:
        content = content.replace(old, new)
    if content != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0

def git_mv(old_rel, new_rel):
    old_abs = os.path.join(REPO, old_rel)
    new_abs = os.path.join(REPO, new_rel)
    if not os.path.exists(old_abs):
        return False
    if os.path.exists(new_abs):
        return False
    os.makedirs(os.path.dirname(new_abs), exist_ok=True)
    try:
        subprocess.run(['git', 'mv', old_abs, new_abs],
                       cwd=REPO, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("=" * 70)
    print("MIGRATION : Suppression des emoji dans les noms de dossiers")
    print("=" * 70)

    # Phase 1 : scan
    print("\n[1/4] Scan des dossiers avec emoji...")
    dirs = scan_emoji_dirs(REPO)
    print(f"  → {len(dirs)} dossiers trouvés.")

    # Vérification collisions
    new_names = [nr for _, nr, _, _ in dirs]
    coll = [n for n in new_names if new_names.count(n) > 1]
    if coll:
        print(f"\n  ❌ COLLISIONS DÉTECTÉES : {set(coll)}")
        print("     STOP. Corrige avant de continuer.")
        sys.exit(1)

    print("\n  Mapping :")
    for old_rel, new_rel, old_name, new_name in dirs:
        print(f"    {old_rel}")
        print(f"      → {new_rel}")

    # Phase 2 : collecte fichiers + construction motifs
    print("\n[2/4] Collecte des fichiers à analyser...")
    files = collect_files(REPO)
    reps = build_replacements(dirs)
    print(f"  → {len(files)} fichiers, {len(reps)} motifs de remplacement.")

    # Phase 3 : remplacement
    print("\n[3/4] Remplacement dans les fichiers...")
    modified = 0
    for i, fp in enumerate(files):
        if i % 100 == 0:
            pct = int(100 * i / len(files))
            print(f"    [{i}/{len(files)}] {pct}%")
        modified += replace_in_file(fp, reps)
    print(f"  → {modified} fichiers modifiés.")

    # Phase 4 : git mv
    print("\n[4/4] Renommage des dossiers (git mv)...")
    sorted_dirs = sorted(dirs, key=lambda x: x[0].count(os.sep), reverse=True)
    renamed = 0
    failed = []
    for old_rel, new_rel, _, _ in sorted_dirs:
        if git_mv(old_rel, new_rel):
            renamed += 1
        else:
            failed.append(old_rel)
    print(f"  → {renamed}/{len(dirs)} renommés.")
    if failed:
        print(f"  ⚠️  Échecs : {failed}")

    # Vérification finale
    remaining = scan_emoji_dirs(REPO)
    if remaining:
        print(f"\n⚠️  {len(remaining)} dossiers contiennent encore des emoji :")
        for r in remaining:
            print(f"     {r[0]}")

    # Bilan
    print("\n" + "=" * 70)
    print("BILAN")
    print(f"  Dossiers renommés : {renamed}/{len(dirs)}")
    print(f"  Fichiers modifiés : {modified}")
    print(f"  Motifs de remplacement : {len(reps)}")
    print("=" * 70)

    print("\n📌 Prochaines étapes :")
    print("   1. git status")
    print('   2. git commit --no-verify -m "feat: remove emoji from dirnames"')
    print("   3. Audits post-migration :")
    print("      python3 .dev/app/audit_internal_links.py")
    print("      python3 .dev/app/audit_citation_links.py")
    print("      python3 .dev/app/audit_readme_integrity.py")

if __name__ == '__main__':
    main()
