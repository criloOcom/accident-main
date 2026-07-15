#!/usr/bin/env python3
"""
Vérifie l'invariant Token -> Reel du projet accident-main.

Règle (RULES.md #22) : tout fichier de la strate Reel doit avoir un Token
frère dans la strate Token. Le générateur generate_real_versions.py renomme
parfois les Reel (ex. Token "J+63 Projet Ordonnance Refere.md" -> Reel
"07 Projet Ordonnance Refere.md") et place parfois le Reel dans un dossier
miroir de nom légèrement différent. On tolère ces cas en comparant les
"slugs" (basename normalisé, emojis/espaces ignorés).

Usage :
    python3 .dev/app/check_reel_orphans.py
Sortie : 0 si invariant respecté, 1 sinon (liste les anomalies).
"""
import subprocess, os, sys, unicodedata, re

env = dict(os.environ)
env['LC_ALL'] = 'C.UTF-8'
env['LANG'] = 'C.UTF-8'

def git(*args):
    return subprocess.check_output(['git', '-c', 'core.quotePath=false'] + list(args),
                                   env=env).decode('utf-8', 'replace')

def slug(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-zA-Z0-9]', '', s)
    return s.lower()

paths = [p for p in git('ls-files').split('\n') if p]
TOKEN, REEL = 'Token', 'Reel'
token_files = [p for p in paths if TOKEN in p]
reel_files  = [p for p in paths if REEL in p]

# slugs des basenames Token (pour détection miroir insensible encodage)
token_slugs = {slug(os.path.basename(t)) for t in token_files}

# reel_path declares (tolérance renommage) : basename du Reel cible
def frontmatter_reel_path(path):
    try:
        txt = subprocess.check_output(
            ['git', '-c', 'core.quotePath=false', 'cat-file', '-p', 'HEAD:' + path],
            env=env).decode('utf-8', 'replace')
    except subprocess.CalledProcessError:
        return None
    if not txt.startswith('---'):
        return None
    end = txt.find('\n---', 3)
    fm = txt[3:end] if end != -1 else txt
    m = re.search(r'^reel_path:\s*(.+)$', fm, re.M)
    if not m:
        return None
    return os.path.basename(m.group(1).strip().strip('"\''))

reel_target_slugs = set()
for t in token_files:
    rp = frontmatter_reel_path(t)
    if rp:
        reel_target_slugs.add(slug(rp))

# Un Reel est couvert si :
#   - un Token a un basename de meme slug (miroir), OU
#   - un reel_path de Token cible un basename de meme slug.
orphans = []
for r in reel_files:
    bn = os.path.basename(r)
    if bn in ('README.md', '.gitkeep'):
        continue
    s = slug(bn)
    if s in token_slugs or s in reel_target_slugs:
        continue
    orphans.append(r)

print("Token files : %d" % len(token_files))
print("Reel files  : %d" % len(reel_files))
print("reel_path declares : %d" % len(reel_target_slugs))
print("Reels orphelins (sans Token frere ni reel_path) : %d" % len(orphans))
for r in orphans:
    print("  ORPHAN : %s" % r)

if orphans:
    print("\n⚠️  INVARIANT Token->Reel NON RESPECTE")
    sys.exit(1)
print("\n✅ Invariant Token->Reel respecte : aucun Reel orphelin.")
