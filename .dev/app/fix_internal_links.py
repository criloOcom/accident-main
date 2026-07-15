#!/usr/bin/env python3
"""
Correction assistée des liens internes cassés.

Analyse le rapport JSON de audit_internal_links.py, cherche les fichiers
cibles dans le projet, et propose/applique les corrections univoques.

Les cas ambigus (plusieurs candidats) sont listés mais non corrigés —
l'agent opencode doit analyser le contexte et choisir.

Usage :
    python3 .dev/app/fix_internal_links.py              # dry-run (défaut)
    python3 .dev/app/fix_internal_links.py --apply       # applique les corrections
    python3 .dev/app/fix_internal_links.py --json        # sortie JSON
"""

import argparse
import json
import os
import re
import subprocess
import sys
from urllib.parse import quote, unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUDIT_SCRIPT = os.path.join(os.path.dirname(__file__), "audit_internal_links.py")

MD_LINK_RE = re.compile(r'\]\(([^)]+)\)')
HTML_LINK_RE = re.compile(r'<a\s+(?:[^>]*?\s+)?href="([^"]+)"')

# Sous-dossiers de ✉️ Courriers/ : mapping basename → subdirectory
# (connu statiquement depuis la structuration actuelle du projet)
_COURIER_SUBDIRS = {
    "📜 Mises en demeure": {"mise en demeure"},
    "🔄 Relances": {"relance", "suivi", "relancer"},
    "⚖️ Contentieux": {"saisine", "transmission", "opposition", "plainte"},
    "🚨 Signalements": {"signalement", "inpi", "urssaf", "codaf", "sdis", "sie", "inspection"},
    "📋 Attestations": {"attestation"},
    "📝 Procédure": {"mutualisation", "email", "guide", "demande aj"},
    "📋 Personnel": {"antiseche", "personnel"},
    "🗄️ Archivé": {"requete constat", "archiv"},
}


def _courrier_subdir(filename: str) -> str | None:
    """Devine le sous-dossier de ✉️ Courriers/ d'après le nom du fichier."""
    name = filename.lower().replace(".md", "")
    for subdir, keywords in _COURIER_SUBDIRS.items():
        for kw in keywords:
            if kw in name:
                return subdir
    return None


def run_audit_json():
    result = subprocess.run(
        [sys.executable, AUDIT_SCRIPT, '--json'],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode not in (0, 1):
        print(f"❌ Erreur audit : {result.stderr}")
        sys.exit(2)
    return json.loads(result.stdout)


def find_candidates(filename: str) -> list:
    """Cherche un fichier par son basename dans tout le projet."""
    candidates = []
    for dp, dirs, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT).split(os.sep)
        if any(s in {'.git', '.venv', '__pycache__', 'node_modules', '.pytest_cache', '.opencode'} for s in rel):
            dirs[:] = []
            continue
        for f in fn:
            if f == filename:
                candidates.append(os.path.relpath(os.path.join(dp, f), ROOT))
    return candidates


def compute_relative_path(source_rel: str, target_rel: str) -> str:
    """Calcule le chemin relatif de source → target."""
    source_dir = os.path.dirname(os.path.join(ROOT, source_rel))
    target_abs = os.path.join(ROOT, target_rel)
    rel = os.path.relpath(target_abs, source_dir)
    return rel


def _encode_variants(s: str) -> list[str]:
    """Produit plusieurs variantes d'URL-encoding pour un même chemin.
    
    Les fichiers .md utilisent des encodages inconsistants :
      - certains encodent les espaces (%20) mais pas les emojis
      - certains encodent aussi le + (%2B)
      - certains encodent tout (quote complet)
    """
    variants = [s]  # brut (decoded)
    # espaces uniquement
    v = s.replace(' ', '%20')
    if v != s:
        variants.append(v)
    # espaces + plus
    v = s.replace(' ', '%20').replace('+', '%2B')
    if v not in variants:
        variants.append(v)
    # encodage complet
    v = quote(s, safe='/')
    if v not in variants:
        variants.append(v)
    return variants


def fix_link_in_content(content: str, old_decoded: str, new_rel: str) -> str:
    """Remplace un lien dans le contenu markdown par le nouveau chemin relatif.
    Gère l'URL-encoding inconsistant dans les fichiers .md."""
    old_variants = _encode_variants(old_decoded)
    new_encoded = quote(new_rel, safe='/')

    for old in old_variants:
        content = content.replace(f']({old})', f']({new_encoded})')
        content = content.replace(f'href="{old}"', f'href="{new_encoded}"')

    return content


def main():
    parser = argparse.ArgumentParser(description="Correction des liens internes cassés")
    parser.add_argument('--apply', action='store_true', help="Appliquer les corrections (défaut: dry-run)")
    parser.add_argument('--json', action='store_true', help="Sortie JSON")
    args = parser.parse_args()

    report = run_audit_json()
    if report['status'] == 'ok':
        print("✅ Aucun lien cassé à corriger.")
        return

    broken = report['results']

    # Indexer par source file
    by_source = {}
    for b in broken:
        by_source.setdefault(b['source'], []).append(b)

    univoque = []     # (source, old_decoded, new_rel, candidates)
    ambigus = []      # (source, old_decoded, candidates)
    introuvables = [] # (source, old_decoded)

    for src, links in by_source.items():
        for b in links:
            decoded = b['decoded']
            filename = os.path.basename(decoded)
            candidates = find_candidates(filename) if b['candidates'] is None else b['candidates']

            if not candidates:
                introuvables.append((src, decoded))
                continue

            # Disambiguation : préférer 🔑 Token, puis 👤 Reel, puis premier
            if len(candidates) > 1:
                token = [c for c in candidates if "🔑 Token" in c]
                reel = [c for c in candidates if "👤 Reel" in c]
                if token:
                    candidates = token[:1]
                elif reel:
                    candidates = reel[:1]
                else:
                    ambigus.append((src, decoded, candidates))
                    continue

            if len(candidates) == 1:
                new_rel = compute_relative_path(src, candidates[0])
                univoque.append((src, decoded, new_rel, candidates))
            else:
                ambigus.append((src, decoded, candidates))

    if args.json:
        output = {
            "status": "ok" if not univoque and not ambigus and not introuvables else "partial",
            "univoque": [{"source": s, "old": o, "new_rel": n, "candidate": c[0]} for s, o, n, c in univoque],
            "ambigus": [{"source": s, "old": o, "candidates": c} for s, o, c in ambigus],
            "introuvables": [{"source": s, "old": o} for s, o in introuvables],
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        sys.exit(0 if not univoque else 0)  # même en succès relatif
        return

    print("🔍 Analyse des liens cassés...\n")

    if univoque:
        print(f"✅ {len(univoque)} correction(s) univoque(s) :\n")
        for src, old_decoded, new_rel, candidates in univoque:
            print(f"   📄 {src}")
            print(f"      {old_decoded}")
            print(f"      → {new_rel}")
            print()
    else:
        print("✅ Aucune correction univoque trouvée.\n")

    if ambigus:
        print(f"❓ {len(ambigus)} cas ambigus (plusieurs candidats) :\n")
        for src, old_decoded, candidates in ambigus:
            print(f"   📄 {src}")
            print(f"      {old_decoded}")
            print(f"      Candidats :")
            for c in candidates[:5]:
                print(f"        • {c}")
            if len(candidates) > 5:
                print(f"        ... et {len(candidates) - 5} autre(s)")
            print()

    if introuvables:
        print(f"❌ {len(introuvables)} cible(s) introuvable(s) dans tout le projet :\n")
        for src, old_decoded in introuvables:
            print(f"   📄 {src}")
            print(f"      {old_decoded} → INTROUVABLE")
            print()

    if not univoque and not ambigus and not introuvables:
        print("Rien à corriger.")
        return

    if args.apply and univoque:
        print(f"--- Application des {len(univoque)} corrections univoques ---\n")
        applied = 0
        errors = 0
        for src, old_decoded, new_rel, candidates in univoque:
            src_abs = os.path.join(ROOT, src)
            try:
                with open(src_abs, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = fix_link_in_content(content, old_decoded, new_rel)

                if new_content != content:
                    with open(src_abs, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"   ✅ {src}")
                    print(f"      {old_decoded} → {new_rel}")
                    applied += 1
                else:
                    print(f"   ⚠️  {src} : aucun changement (pattern non trouvé)")
                    errors += 1
            except Exception as e:
                print(f"   ❌ {src} : {e}")
                errors += 1

        print(f"\n--- {applied} corrigée(s), {errors} erreur(s) ---")

        if ambigus:
            print(f"\n⚠️  {len(ambigus)} cas ambigus restent à corriger manuellement.")
        if introuvables:
            print(f"\n⚠️  {len(introuvables)} cibles introuvables — impossible de corriger automatiquement.")

        print(f"\nPour vérifier : python3 .dev/app/audit_internal_links.py")

    elif not args.apply:
        if univoque:
            print(f"📝 Dry-run : aucune modification appliquée.")
            print(f"   Pour appliquer : python3 .dev/app/fix_internal_links.py --apply\n")

        if ambigus or introuvables:
            print(f"📝 Les cas ambigus et introuvables nécessitent une analyse manuelle.")


if __name__ == '__main__':
    main()
