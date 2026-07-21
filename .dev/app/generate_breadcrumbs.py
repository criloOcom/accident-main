#!/usr/bin/env python3
"""
generate_breadcrumbs.py — (Ré)génère le fil d'Ariane HIÉRARCHIQUE de tous les
fichiers .md du dépôt /home/crilocom/accident-main.

Convention (Règle #13 / #15 / #16) :
  - Balises <!-- Breadcrumb --> ... <!-- /Breadcrumb --> sur les lignes 1-3.
  - Fil d'Ariane COMPLET : tous les dossiers parents (racine -> parent direct)
    affichés et CLIQUABLES via chemins relatifs corrects.
  - Dernier élément (dossier courant pour un README, fichier courant sinon) :
    affiché en TEXTE (non cliquable).
  - Séparateur : " › " (espace, chevron U+203A, espace).
  - AUCUN lien absolu. Un niveau n'est cliquable QUE si son README.md existe
    réellement (sinon texte brut -> zéro lien mort, Règle #16).

Usage :
  python3 .dev/app/generate_breadcrumbs.py            # dry-run (défaut)
  python3 .dev/app/generate_breadcrumbs.py --apply     # applique les modifs
"""
import os
import re
import sys

ROOT = "/home/crilocom/accident-main"
SKIP_DIRS = {'.git', '.pytest_cache', '.venv', 'node_modules', '__pycache__', '.opencode'}

SEP = " › "


def link_for_ups(ups):
    """Renvoie le chemin relatif vers un README.md situé 'ups' niveaux au-dessus."""
    if ups <= 0:
        return "./README.md"
    return "../" * ups + "README.md"


def read_yaml_field(readme_path, field):
    """Lit un champ YAML dans le frontmatter. Retourne None si absent."""
    if not os.path.isfile(readme_path):
        return None
    try:
        txt = open(readme_path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.search(r'^---\s*\n.*?^' + re.escape(field) + r':\s*(.+?)$', txt, re.MULTILINE | re.DOTALL)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def read_title(readme_path):
    """Lit le titre d'un README depuis son YAML (champ 'title')."""
    return read_yaml_field(readme_path, "title")


def read_breadcrumb_label(readme_path):
    """Lit le libellé court pour le fil d'Ariane (champ 'breadcrumb' uniquement)."""
    return read_yaml_field(readme_path, "breadcrumb")


def dir_label(dirname):
    """Label lisible d'un dossier : underscore -> espace."""
    return dirname.replace("_", " ").strip()


def file_label(fname):
    """Label lisible d'un fichier : retire .md, underscore -> espace."""
    base = os.path.splitext(fname)[0]
    return base.replace("_", " ").strip()


def build_breadcrumb(rel_md_path):
    abs_p = os.path.join(ROOT, rel_md_path)
    d = os.path.dirname(abs_p)
    rel_dir = os.path.relpath(d, ROOT)
    segs = [] if rel_dir == "." else rel_dir.split(os.sep)
    N = len(segs)  # profondeur du dossier contenant le fichier
    is_readme = os.path.basename(rel_md_path) == "README.md"

    levels = []  # (label, lien_ou_None)

    # Racine
    levels.append(("🏠", link_for_ups(N)))

    # Ancêtres (profondeur 1 .. N-1) -> exclus le dossier courant
    for k in range(N - 1):
        ancestor_dir = os.path.join(ROOT, *segs[: k + 1])
        rpath = os.path.join(ancestor_dir, "README.md")
        ups = N - k - 1
        if os.path.isfile(rpath):
            title = read_breadcrumb_label(rpath)
            label = title if title else dir_label(segs[k])
            levels.append((label, link_for_ups(ups)))
        else:
            levels.append((dir_label(segs[k]), None))

    # Dossier courant
    if is_readme:
        if N == 0:
            return "<!-- Breadcrumb -->\n*[🏠](README.md)*\n<hr>\n<!-- /Breadcrumb -->"
        own_bc = read_breadcrumb_label(os.path.join(d, "README.md"))
        leaf_label = own_bc if own_bc else dir_label(segs[-1])
    else:
        if N == 0:
            # fichier à la racine (ex. AGENTS.md) : pas de dossier parent
            pass
        else:
            cur_readme = os.path.join(d, "README.md")
            if os.path.isfile(cur_readme):
                t = read_breadcrumb_label(cur_readme)
                levels.append((t if t else dir_label(segs[-1]), "./README.md"))
            else:
                levels.append((dir_label(segs[-1]), None))
        leaf_label = file_label(os.path.basename(rel_md_path))

    parts = [f"[{lab}]({lnk})" if lnk else lab for lab, lnk in levels]
    if is_readme:
        parts.append(leaf_label)
    line = SEP.join(parts)
    return f"<!-- Breadcrumb -->\n*{line}*\n<hr>\n<!-- /Breadcrumb -->"


def apply_to_file(rel_md_path, dry_run):
    abs_p = os.path.join(ROOT, rel_md_path)
    try:
        content = open(abs_p, encoding="utf-8").read()
    except Exception as e:
        return ("skip", f"lecture impossible: {e}")
    new_bc = build_breadcrumb(rel_md_path)
    # Remplace l'ancien breadcrumb IN SITU (minimal diff)
    m = re.search(r'<!-- Breadcrumb -->.*?<!-- /Breadcrumb -->', content, re.DOTALL)
    if m:
        new_content = content[:m.start()] + new_bc + content[m.end():]
    else:
        # Pas d'ancien breadcrumb : insérer après le YAML
        m_yaml = re.match(r'^---\s*\n.*?\n---\s*\n?', content, re.DOTALL)
        if m_yaml:
            yaml_block = m_yaml.group(0)
            new_content = yaml_block + new_bc + "\n\n" + content[m_yaml.end():].lstrip("\n")
        else:
            new_content = new_bc + "\n\n" + content.lstrip("\n")
    if new_content == content:
        return ("unchanged", None)
    if not dry_run:
        open(abs_p, "w", encoding="utf-8").write(new_content)
    return ("changed", new_bc)


def main():
    dry_run = "--apply" not in sys.argv
    targets = []
    missing_parent = set()
    for dp, dn, fn in os.walk(ROOT):
        parts = os.path.relpath(dp, ROOT).split(os.sep)
        if any(p in SKIP_DIRS for p in parts):
            continue
        for f in fn:
            if f.endswith(".md"):
                rel = os.path.relpath(os.path.join(dp, f), ROOT)
                targets.append(rel)
                # détecte dossiers parents sans README (pour rapport)
                d = os.path.dirname(os.path.join(ROOT, rel))
                rel_dir = os.path.relpath(d, ROOT)
                if rel_dir != ".":
                    for i in range(1, len(rel_dir.split(os.sep))):
                        anc = os.path.join(ROOT, *rel_dir.split(os.sep)[:i], "README.md")
                        if not os.path.isfile(anc):
                            missing_parent.add(os.path.relpath(anc, ROOT))
    targets.sort()
    changed = 0
    unchanged = 0
    skipped = 0
    samples = []
    for rel in targets:
        status, info = apply_to_file(rel, dry_run)
        if status == "changed":
            changed += 1
            if len(samples) < 6:
                samples.append((rel, info))
        elif status == "unchanged":
            unchanged += 1
        else:
            skipped += 1
    print(f"MODE: {'DRY-RUN' if dry_run else 'APPLY'}")
    print(f"Fichiers .md trouvés : {len(targets)}")
    print(f"  modifiés : {changed}")
    print(f"  déjà OK  : {unchanged}")
    print(f"  ignorés  : {skipped}")
    print(f"Dossiers parents sans README.md (niveaux en texte brut) : {len(missing_parent)}")
    print("\n--- ÉCHANTILLONS DE BREADCRUMBS GÉNÉRÉS ---")
    for rel, bc in samples:
        print(f"\n* {rel}")
        print(bc)
    if missing_parent:
        print("\n--- PARENTS SANS README (extrait) ---")
        for m in sorted(missing_parent)[:15]:
            print("  ", m)


if __name__ == "__main__":
    main()
