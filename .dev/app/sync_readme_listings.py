#!/usr/bin/env python3
"""
sync_readme_listings.py — Ajoute les fichiers .md manquants dans les README.md.

Détecte le format de listing utilisé dans chaque README et ajoute des entrées
pour les fichiers présents sur le disque mais non listés.

Formats supportés :
  - bold_link : `- **[Titre](fichier.md)**`  (Format B — produit `- **[nom](url)**`)
  - link      : `- [Titre](fichier.md)`       (Formats C/D)
  - bold_name : `- **fichier.md**`            (Format E — produit `- **[nom](url)**`)
  - none      : section de liste absente      (Format F)
  - table     : tableau markdown              (Format A → ignoré, signalé)

Sélection des cibles :
  - Pas de glob : le script parcourt récursivement TOUS les README.md
    (os.walk, hors .git/.pytest_cache/.venv), puis compare avec le disque.
  - `--target CHEMIN/README.md` cible un seul fichier (pas un pattern glob).

Usage :
  python3 .dev/app/sync_readme_listings.py              # dry-run (défaut)
  python3 .dev/app/sync_readme_listings.py --apply       # appliquer
  python3 .dev/app/sync_readme_listings.py --no-backup   # sans backup
  python3 .dev/app/sync_readme_listings.py --target DIR/README.md  # ciblé
"""

import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from urllib.parse import unquote

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKUP_DIR = os.path.join(BASE_DIR, ".dev", ".readme_backups")

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"


def scan_readmes(root_dir=BASE_DIR):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        if any(p in root for p in (".git", "node_modules", "__pycache__", ".venv", ".pytest_cache")):
            continue
        if "README.md" in files:
            paths.append(os.path.join(root, "README.md"))
    return sorted(paths)


def find_listed_files(content):
    """Même logique que audit_readme_integrity.py — retourne l'ensemble
    des basenames de fichiers .md référencés dans le README."""
    found = set()
    # URLs dans les liens markdown : [texte](fichier.md)
    for m in re.finditer(r'\]\(([^)\n]+\.md)\)', content):
        url = unquote(m.group(1))
        found.add(os.path.basename(url))
    # Références nues : [fichier.md]
    for m in re.finditer(r'\[([^\]\n]+\.md)\]', content):
        found.add(m.group(1))
    # Gras simple : **fichier.md**
    for m in re.finditer(r'\*\*([^*\n]+\.md)\*\*', content):
        found.add(m.group(1))
    found.discard("README.md")
    return found


def actual_files_in_dir(readme_path):
    d = os.path.dirname(readme_path)
    if not os.path.isdir(d):
        return set()
    return {f for f in os.listdir(d) if f.endswith(".md") and f != "README.md"}


def determine_format(content):
    """Détecte le format de listing utilisé dans un README.
    Retourne : 'table', 'bold_link', 'link', 'bold_name', 'none'
    """
    lines = content.split("\n")

    # 1) Test format tableau (au moins 2 lignes | contenant du .md lié)
    count_table = 0
    for line in lines:
        s = line.strip()
        if s.startswith("|") and ".md" in s and ("[" in s or "]" in s):
            # Vérifier que ce n'est pas un séparateur |---|---|
            if not re.match(r"^\|[-:\s]+\|", s):
                count_table += 1
    if count_table >= 2:
        return "table"

    # 2) Parcours inversé : chercher la dernière ligne de listing
    for line in reversed(lines):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("---") or s.startswith(">"):
            continue
        # bold_link : - **[texte](fichier.md)**
        if re.match(r"^- \*\*\[", s):
            return "bold_link"
        # link : - [texte](fichier.md)
        if re.match(r"^- \[.+\]\([^)]+\.md\)", s):
            return "link"
        # bold_name : - **fichier.md** — description
        if re.match(r"^- \*\*.+\.md\*\*", s):
            return "bold_name"

    return "none"


def find_insertion_point(content, fmt):
    """Trouve la ligne d'insertion (0-based) pour les nouvelles entrées."""
    lines = content.split("\n")

    if fmt in ("bold_link", "link", "bold_name"):
        # Chercher la dernière ligne de listing du bas
        for i in range(len(lines) - 1, -1, -1):
            s = lines[i].strip()
            match = False
            if fmt == "bold_link" and re.match(r"^- \*\*\[", s):
                match = True
            elif fmt == "link" and re.match(r"^- \[.+\]\([^)]+\.md\)", s):
                match = True
            elif fmt == "bold_name" and re.match(r"^- \*\*[^*]+\.md\*\*", s):
                match = True
            if match:
                return i + 1
        # Fallback : après le dernier bloc de contenu
        return len(lines)

    # Format none : chercher une section ## Liste / ## Fichiers / ## Contenu
    for i, line in enumerate(lines):
        s = line.strip()
        if re.match(r"^## (Liste|Fichiers|Contenu|Structure)", s):
            # Trouver la fin de cette section
            for j in range(i + 1, len(lines)):
                if lines[j].strip().startswith("## ") or lines[j].strip().startswith("---"):
                    return j
            return len(lines)
    return len(lines)


def generate_entries(files, fmt):
    """Génère les lignes de listing pour les fichiers manquants.

    Les formats 'bold_link' et 'bold_name' produisent la même sortie valide
    '- **[nom](url)**' (le gras interne de bold_link était mal formé : voir fix).
    """
    entries = []
    for f in sorted(files):
        name = f.replace(".md", "")
        url = f.replace(" ", "%20")
        if fmt in ("bold_link", "bold_name"):
            entries.append(f"- **[{name}]({url})**")
        else:  # link, none
            entries.append(f"- [{name}]({url})")
    return entries


def sync_readme(readme_path, dry_run=True, backup=True):
    """Analyse un README et ajoute les entrées manquantes. Retourne un message."""
    rel = os.path.relpath(readme_path, BASE_DIR)
    content = open(readme_path, "r", encoding="utf-8").read()

    listed = find_listed_files(content)
    actual = actual_files_in_dir(readme_path)
    missing = sorted(actual - listed)

    if not missing:
        return f"  {GREEN}✓{RESET} {rel} : à jour"

    fmt = determine_format(content)
    if fmt == "table":
        return (
            f"  {YELLOW}⏭️ {rel} : {len(missing)} fichier(s) non listé(s), "
            f"format tableau ignoré (ajout manuel requis){RESET}"
        )

    insert_at = find_insertion_point(content, fmt)
    new_entries = generate_entries(missing, fmt)

    if dry_run:
        msg = (
            f"  {BLUE}📋 {rel} : {len(missing)} à ajouter "
            f"(format={fmt}, ligne={insert_at}){RESET}"
        )
        for e in new_entries[:3]:
            msg += f"\n    {e}"
        if len(new_entries) > 3:
            msg += f"\n    ... et {len(new_entries) - 3} autre(s)"
        return msg

    # Backup
    if backup:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe = rel.replace("/", "_").replace(" ", "_")
        shutil.copy2(readme_path, os.path.join(BACKUP_DIR, f"{safe}.{stamp}.bak"))

    # Insertion
    lines = content.split("\n")
    # Sauter les lignes vides en fin de fichier
    while insert_at < len(lines) and lines[insert_at].strip() == "":
        insert_at += 1
    for entry in reversed(new_entries):
        lines.insert(insert_at, entry)

    new_content = "\n".join(lines)
    open(readme_path, "w", encoding="utf-8").write(new_content)

    return f"  {GREEN}✅ {rel} : {len(missing)} ajouté(s){RESET}"


def main():
    parser = argparse.ArgumentParser(
        description="Synchronise les listings .md dans les README.md"
    )
    parser.add_argument("--apply", action="store_true", help="Appliquer les changements")
    parser.add_argument("--no-backup", action="store_true", help="Ne pas créer de backup")
    parser.add_argument(
        "--target",
        help="Cibler un README spécifique (chemin relatif depuis la racine)",
    )
    args = parser.parse_args()

    if args.target:
        readmes = [os.path.join(BASE_DIR, args.target)]
        if not os.path.isfile(readmes[0]):
            print(f"{RED}❌ Fichier introuvable : {readmes[0]}{RESET}")
            sys.exit(1)
    else:
        readmes = scan_readmes()

    results = []
    for r in readmes:
        results.append(sync_readme(r, dry_run=not args.apply, backup=not args.no_backup))

    print(f"\n{'=' * 60}")
    title = "DRY-RUN" if not args.apply else "APPLICATION"
    print(f"{BOLD}🔍 SYNCHRONISATION README — {title}{RESET}")
    print(f"{'=' * 60}\n")

    for r in results:
        print(r)

    # Stats
    done = sum(1 for r in results if "✅" in r or "✓" in r)
    skipped = sum(1 for r in results if "⏭️" in r)
    pending = sum(1 for r in results if "📋" in r)

    print(f"\n{'─' * 60}")
    print(f"  À jour : {done}  |  Ignorés (tableau) : {skipped}  |  À ajouter : {pending}")
    if not args.apply and pending:
        print(f"  {YELLOW}💡 Relancer avec --apply pour appliquer les changements{RESET}")
    print(f"{'─' * 60}\n")


if __name__ == "__main__":
    main()
