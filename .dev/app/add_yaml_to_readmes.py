#!/usr/bin/env python3
"""Ajoute un YAML frontmatter aux README.md qui n'en ont pas."""
import os, re, sys

ROOT = "/home/crilocom/accident-main"
SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', '.opencode'}

def extract_title(content):
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return m.group(1).strip().strip('*').strip() if m else ""

def extract_desc(content):
    lines = content.split("\n")
    in_body = False
    for line in lines:
        s = line.strip()
        if s.startswith("# "):
            in_body = True
            continue
        if not in_body: continue
        if s.startswith("#") or s.startswith("<!--") or s.startswith("---") or s.startswith(">") or s.startswith("- ") or s.startswith("* "): continue
        if s == "": continue
        clean = s.strip("* \t").strip('"')
        if clean and len(clean) > 5:
            return clean[:250].rstrip()
    return ""

dry_run = "--apply" not in sys.argv

count = 0
for dp, dn, fn in os.walk(ROOT):
    parts = os.path.relpath(dp, ROOT).split(os.sep)
    if any(p in SKIP_DIRS for p in parts): continue
    if "README.md" not in fn: continue
    fpath = os.path.join(dp, "README.md")
    rel = os.path.relpath(fpath, ROOT)
    content = open(fpath, encoding="utf-8").read()
    if content.startswith("---"):
        continue
    title = extract_title(content)
    desc = extract_desc(content)
    if not title:
        title = os.path.basename(dp).replace("_", " ")
    if not desc:
        desc = f"Index du dossier {os.path.basename(dp)}"
    yaml = f"---\ntitle: \"{title}\"\ndescription: \"{desc}\"\ntype: readme\n---\n\n"
    new_content = yaml + content
    if dry_run:
        print(f"  [DRY] {rel} → title: \"{title[:60]}\"")
    else:
        open(fpath, "w", encoding="utf-8").write(new_content)
        print(f"  [WROTE] {rel}")
    count += 1

print(f"\nRésumé : {count} README {'à modifier (dry-run)' if dry_run else 'mis à jour'}.")
