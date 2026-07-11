#!/usr/bin/env python3
"""
Audit d'intégrité des README.md — vérifie :
  1. Anomalies textuelles (balises non complétées, TODO)
  2. Statuts d'envoi frauduleux (Envoyé sans preuve LRAR/AR/dépôt)
  3. Alignement physique (fichiers déclarés existent-ils sur le disque ?)

Usage :
  python3 .dev/app/audit_readme_integrity.py
  python3 .dev/app/audit_readme_integrity.py --fix         # tentative de correction auto
  python3 .dev/app/audit_readme_integrity.py --ci          # sortie JSON pour CI

Exit codes : 0 = OK, 1 = erreurs critiques, 2 = avertissements
"""

import argparse
import json
import os
import re
import sys
from urllib.parse import unquote

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# ── patterns à exclure (fichiers volontairement incomplets)
KNOWN_GABARITS = {
    "22", "23", "24",  # attestations Cerfa
    "25", "26", "27", "28",  # emails brouillons
}
KNOWN_BROUILLONS = {
    "04", "07", "08", "09",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21",
}
KNOWN_PROJETS = {"32", "33"}

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"


def p(col, msg):
    print(f"{col}{msg}{RESET}")


def scan_readmes(root_dir=BASE_DIR):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        if any(p in root for p in (".git", "node_modules", "__pycache__", ".venv")):
            continue
        if "README.md" in files:
            paths.append(os.path.join(root, "README.md"))
    return paths


def load_content(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def find_files_in_text(content):
    """Analyse un README pour trouver les fichiers .md référencés.
    
    Retourne un tuple (bare_refs, url_refs) :
      - bare_refs (set) : fichiers mentionnés via [fichier.md] ou **fichier.md**
        → doivent exister dans le même dossier
      - url_refs  (set) : fichiers mentionnés via [texte](chemin/fichier.md)
        → doivent exister à l'endroit indiqué (relatif au README)
    
    Les regex évitent les sauts de ligne pour ne pas capturer du contenu
   跨-ligne en cas de markdown mal formé.
    """
    bare = set()
    urls = set()
    # 1) URLs dans les liens markdown : [texte](fichier.md) ou **[texte](fichier.md)**
    for m in re.finditer(r'\]\(([^)\n]+\.md)\)', content):
        url = unquote(m.group(1))
        urls.add(url)
    # 2) Références nues : [fichier.md] — sur UNE SEULE ligne
    for m in re.finditer(r'\[([^\]\n]+\.md)\]', content):
        bare.add(m.group(1))
    # 3) Gras simple : **fichier.md** — sur UNE SEULE ligne
    for m in re.finditer(r'\*\*([^*\n]+\.md)\*\*', content):
        bare.add(m.group(1))
    bare.discard("README.md")
    return bare, urls


def actual_files_in_dir(readme_path):
    d = os.path.dirname(readme_path)
    if not os.path.isdir(d):
        return set()
    return {f for f in os.listdir(d) if f.endswith(".md") and f != "README.md"}


def has_lrar_proof(content_or_filepath):
    """Vérifie présence d'un n° LRAR (format La Poste)."""
    if os.path.isfile(content_or_filepath):
        content = load_content(content_or_filepath)
    else:
        content = content_or_filepath
    return bool(re.search(r'\b8[67]00\d{11,13}[A-Z]?\b', content))


def has_ar_proof(content):
    return bool(re.search(r'(accus[eé][\s-]?de[\s-]?r[ée]ception|AR\s+sign[ée])', content, re.IGNORECASE))


def has_depot_proof(content):
    return bool(re.search(r'(d[ée]p[ôo]t[\s-]?(?:au|en|greffe)|d[ée]pos[ée]\s+(?:au|le))', content, re.IGNORECASE))


def has_envoi_evidence(content):
    """Détecte une preuve matérielle d'envoi dans le texte."""
    return has_lrar_proof(content) or has_ar_proof(content) or has_depot_proof(content)


def check_statut_declared_sent(content, readme_path, results):
    """Parcourt les tableaux de statuts et vérifie les ✅ Envoyé sans preuve."""
    rel_dir = os.path.relpath(readme_path, BASE_DIR)
    # 🚦_Status/README.md est un index de catégories, pas un tracker de documents
    if rel_dir == os.path.join("🚦_Status", "README.md"):
        return
    # cherche lignes avec "✅ Envoyé" ou "Envoyé" et vérifie si une preuve LRAR existe
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        if re.search(r'✅\s*Envoy[ée]|Envoy[ée]', line):
            # extrait le numéro de document s'il est dans la même ligne ou les 2 lignes précédentes
            block = "\n".join(lines[max(0, i - 3) : i + 1])
            if not has_envoi_evidence(block):
                n = ""
                m = re.search(r'\|?\s*(\d+)\s*\|', line)
                if m:
                    n = m.group(1)
                if n in KNOWN_BROUILLONS | KNOWN_PROJETS:
                    continue
                results.append({
                    "type": "statut_sent_sans_preuve",
                    "severity": "error",
                    "file": rel_dir,
                    "line": i,
                    "doc": n,
                    "msg": f"Document déclaré 'Envoyé' sans preuve LRAR/AR/dépôt (l. {i})"
                })


def check_text_anomalies(content, readme_path, results):
    rel_dir = os.path.relpath(readme_path, BASE_DIR)
    for i, line in enumerate(content.split("\n"), 1):
        # détection crochets non résolus (hors gabarits connus)
        if re.search(r'\[(?:À|A\s)?[cC]ompl[ée]ter\]', line):
            results.append({
                "severity": "error",
                "file": rel_dir,
                "line": i,
                "msg": f"Balise '[À compléter]' non résolue (l. {i})"
            })
        if re.search(r'\[Adresse[^\]]*\]', line) and "Mairie" not in line:
            results.append({
                "severity": "error",
                "file": rel_dir,
                "line": i,
                "msg": f"Balise '[Adresse...]' non résolue (l. {i})"
            })
        # détection TODO résiduels (hors Memory/ qui contient des TODOs volontaires)
        if re.search(r'\bTODO\b', line) and "TODOs volontaires" not in content and not re.search(r'TODO\.md', line):
            results.append({
                "severity": "warning",
                "file": rel_dir,
                "line": i,
                "msg": f"Mention 'TODO' résiduelle non commentée (l. {i})"
            })


def check_alignment(readme_path, results):
    rel_dir = os.path.relpath(readme_path, BASE_DIR)
    content = load_content(readme_path)
    bare, urls = find_files_in_text(content)
    actual = actual_files_in_dir(readme_path)
    readme_dir = os.path.dirname(readme_path)

    # ── 1) Vérifier les [fichier.md] / **fichier.md** (doivent être dans le même dossier)
    for f in sorted(bare):
        if f not in actual:
            results.append({
                "severity": "warning",
                "file": rel_dir,
                "msg": f"Fichier déclaré '{f}' introuvable dans {rel_dir}"
            })

    # ── 2) Vérifier les [texte](chemin/fichier.md) (résoudre le chemin relatif)
    for url in sorted(urls):
        # Ignorer les protocoles ou chemins absolus
        if url.startswith(("file://", "http://", "https://", "/")):
            continue
        full_path = os.path.join(readme_dir, url)
        if not os.path.isfile(full_path):
            # Fallback : chercher le nom de base dans le dossier
            bn = os.path.basename(url)
            if bn not in actual:
                results.append({
                    "severity": "warning",
                    "file": rel_dir,
                    "msg": f"Fichier déclaré '{url}' introuvable"
                })

    # ── 3) Fichiers réels non listés ?
    # Un fichier est considéré « listé » s'il apparaît dans bare, ou si son
    # basename apparaît dans une URL
    listed = bare.copy()
    for url in urls:
        listed.add(os.path.basename(url))
    extra = actual - listed - {"README.md"}
    for f in sorted(extra):
        results.append({
            "severity": "warning",
            "file": rel_dir,
            "msg": f"Fichier '{f}' présent mais non listé dans {rel_dir}"
        })


def check_envoi_34_ready(content, results):
    """Vérifie que le N°34 est bien prêt (pas de crochets)."""
    # trouve la section du tableau qui parle du N°34
    idx = content.find("N°34") if "N°34" in content else content.find("34")
    if idx == -1:
        return
    section = content[idx:idx + 600]
    if "Email Maire Foix" in section or "Maire Foix" in section:
        # ne vérifie que les crochets dans la section N°34, pas dans le reste
        if re.search(r'\[(À|A)\s*(completer|compléter)\]', section):
            results.append({
                "severity": "error",
                "file": "README.md (root)",
                "msg": "N°34 contient encore des [À compléter] — ne pas envoyer !"
            })


def run_audit(root_dir=BASE_DIR):
    results = []
    readmes = scan_readmes(root_dir)

    if not readmes:
        p(YELLOW, "⚠️  Aucun README.md trouvé.")
        return results

    for readme in readmes:
        content = load_content(readme)
        check_text_anomalies(content, readme, results)
        check_statut_declared_sent(content, readme, results)
        check_alignment(readme, results)

    # vérification spécifique README racine
    root_readme = os.path.join(root_dir, "README.md")
    if os.path.exists(root_readme):
        content = load_content(root_readme)
        check_envoi_34_ready(content, results)

    return results


def print_report(results, json_output=False):
    if json_output:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    errors = [r for r in results if r["severity"] == "error"]
    warnings = [r for r in results if r["severity"] == "warning"]
    infos = [r for r in results if r["severity"] == "info"]

    p(BLUE, f"\n{'='*65}")
    p(BOLD, "🔍 AUDIT D'INTÉGRITÉ DES README.md")
    p(BLUE, f"{'='*65}\n")

    for r in errors:
        loc = f"{r['file']}:{r.get('line','?')} " if r.get('file') != "README.md (root)" else ""
        p(RED, f"  ❌ {loc}{r['msg']}")
    for r in warnings:
        loc = f"{r['file']}:{r.get('line','?')} " if r.get('file') != "README.md (root)" else ""
        p(YELLOW, f"  ⚠️  {loc}{r['msg']}")
    for r in infos:
        loc = f"{r['file']}:{r.get('line','?')} " if r.get('file') != "README.md (root)" else ""
        p(BLUE, f"  ℹ️  {loc}{r['msg']}")

    p(BOLD, f"\n{'─'*65}")
    p(BOLD, f"  Bilan : {len(errors)} erreur(s), {len(warnings)} avertissement(s), {len(infos)} info(s)")
    p(BOLD, f"{'─'*65}\n")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Audit d'intégrité des README.md")
    parser.add_argument("--ci", action="store_true", help="Sortie JSON compatible CI")
    args = parser.parse_args()

    results = run_audit()
    errors, warnings = print_report(results, json_output=args.ci)

    if errors:
        sys.exit(1)
    if warnings:
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()