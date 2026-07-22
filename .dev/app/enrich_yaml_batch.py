"""
Enrichit le YAML frontmatter des fichiers Rapports/ et Lois/
avec les champs subtitle, objective, summary, key_points, legal_basis, recipient.

Utilise des heuristiques basées sur le nom de fichier, le titre,
la description et le contenu pour déduire les valeurs.

Usage:
    python3 .dev/app/enrich_yaml_batch.py              # dry-run
    python3 .dev/app/enrich_yaml_batch.py --apply       # applique
    python3 .dev/app/enrich_yaml_batch.py --dir Lois    # cible un dossier
"""

import os
import re
import sys
import json

DRY_RUN = "--apply" not in sys.argv
TARGET_DIRS = []
for arg in sys.argv[1:]:
    if arg == "--apply":
        continue
    if arg.startswith("--dir="):
        TARGET_DIRS.append(arg.split("=", 1)[1])

if not TARGET_DIRS:
    TARGET_DIRS = ["Rapports", "Lois"]

INPUT_BASE = "/home/crilocom/accident-main"

def parse_yaml_frontmatter(content):
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return {}, content
    raw = m.group(1)
    body = content[m.end():]
    yaml = {}
    for line in raw.split('\n'):
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith('#'):
            continue
        if ':' in line_stripped:
            key, _, val = line_stripped.partition(':')
            key = key.strip()
            val = val.strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            if val == '' or val == '""' or val == "''":
                val = None
            yaml[key] = val
    return yaml, body

def extract_h1(body):
    m = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if m:
        text = m.group(1).strip()
        text = re.sub(r'<br\s*/?>', ' — ', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    return None

def extract_section_headings(body):
    headings = re.findall(r'^##\s+(.+)$', body, re.MULTILINE)
    return [h.strip() for h in headings if h.strip()]

def rebuild_yaml(yaml):
    lines = ["---"]
    for k, v in yaml.items():
        if v is None:
            lines.append(f"{k}:")
        elif isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        elif isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
        else:
            sv = str(v)
            if ':' in sv or sv.startswith('[') or sv.startswith('- '):
                lines.append(f'{k}: "{sv}"')
            else:
                lines.append(f"{k}: {sv}")
    lines.append("---")
    return "\n".join(lines)

def classify_file_type(filename, content_lower):
    if filename.startswith("NW_"):
        return "nightwatch"
    if filename.startswith("REPORT_JULES_"):
        return "jules"
    if filename.startswith("RAPPORT_AUDIT_") or "audit" in filename.lower():
        return "audit"
    if "synthèse" in filename.lower() or "synthese" in filename.lower() or "synthesis" in filename.lower():
        return "synthesis"
    if "health" in filename.lower():
        return "health"
    if "scenario" in filename.lower():
        return "scenario"
    if "checklist" in filename.lower() or "todo" in filename.lower() or "action" in filename.lower():
        return "planning"
    if "guide" in filename.lower() or "fiche" in filename.lower() or "memo" in filename.lower():
        return "guide"
    if "cartographie" in filename.lower() or "frise" in filename.lower():
        return "planning"
    if filename.startswith("M0"):
        return "research"
    if "jurisprudence" in filename.lower():
        return "jurisprudence"
    return "report"

def guess_subtitle(filename, title, file_type):
    subtitles = {
        "nightwatch": "Mission de contrôle Night Watch",
        "jules": "Rapport de mission Jules",
        "audit": "Audit de conformité et de qualité",
        "synthesis": "Synthèse et vue d'ensemble",
        "health": "Rapport de santé du projet",
        "scenario": "Analyse de scénarios et simulations",
        "planning": "Plan d'action et suivi",
        "guide": "Guide de référence et documentation",
        "research": "Recherche et analyse documentaire",
        "report": "Rapport d'analyse",
        "jurisprudence": "Analyse jurisprudentielle",
    }
    return subtitles.get(file_type, "Rapport d'analyse")

def guess_tags(filename, content_lower, file_type):
    tags = []
    tag_map = {
        "nightwatch": ["nightwatch", "controle", "qualite"],
        "jules": ["jules", "mission", "automatisation"],
        "audit": ["audit", "conformite", "qualite"],
        "synthesis": ["synthese", "global"],
        "health": ["health", "etat", "projet"],
        "scenario": ["scenario", "simulation", "strategie"],
        "planning": ["planning", "action", "suivi"],
        "guide": ["guide", "documentation", "reference"],
        "research": ["recherche", "analyse", "documentation"],
        "jurisprudence": ["jurisprudence", "analyse", "droit"],
    }
    tags = tag_map.get(file_type, ["rapport"])

    content_check = filename.lower() + " " + content_lower[:2000]
    if "dintilhac" in content_check:
        tags.extend(["dintilhac", "indemnisation"])
    if "responsabilite" in content_check or "responsabilité" in content_check:
        tags.append("responsabilite")
    if "penal" in content_check or "pénal" in content_check:
        tags.append("penal")
    if "preuve" in content_check:
        tags.append("preuve")
    if "avocat" in content_check or "avocat" in content_check:
        tags.append("avocat")
    if "token" in content_check:
        tags.append("token")
    if "legifrance" in content_check or "juritext" in content_check:
        tags.append("legifrance")

    return list(dict.fromkeys(tags))  # deduplicate preserving order

def guess_key_points(content, content_lower):
    kp = []
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- **') and ':' in stripped:
            text = stripped.strip('- **:')
            if len(text) > 5 and len(text) < 200:
                kp.append(text.strip())
        if stripped.startswith('- ') and not stripped.startswith('- [') and not stripped.startswith('- *'):
            text = stripped[2:].strip()
            if text and len(text) > 10 and len(text) < 200 and ':' in text:
                kp.append(text)
    return kp[:6]

def guess_objective(filename, title, file_type, content_lower):
    prefix_patterns = {
        "nightwatch": "Contrôler et auditer",
        "jules": "Analyser et rapporter",
        "audit": "Auditer et vérifier la conformité de",
        "synthesis": "Synthétiser et présenter une vue d'ensemble de",
        "health": "Évaluer l'état et la santé de",
        "scenario": "Simuler et analyser les scénarios possibles pour",
        "planning": "Planifier et organiser le suivi de",
        "guide": "Fournir un guide de référence pour",
        "research": "Rechercher et analyser",
        "jurisprudence": "Analyser la jurisprudence relative à",
    }
    prefix = prefix_patterns.get(file_type, "Analyser")
    clean_title = title
    # Remove emojis
    clean_title = re.sub(r'[^\x00-\x7F\u00C0-\u024F\u1E00-\u1EFF]', '', clean_title)
    # Remove HTML tags
    clean_title = re.sub(r'<[^>]+>', ' — ', clean_title)
    # Collapse whitespace
    clean_title = re.sub(r'\s+', ' ', clean_title).strip()
    # Remove leading/trailing dashes
    clean_title = clean_title.strip('— –- ')
    if not clean_title:
        clean_title = filename
    return f"{prefix} {clean_title[:150]}".strip()

def guess_recipient(filename, file_type, content_lower):
    if "avocat" in filename.lower() or "avocat" in content_lower[:1000]:
        return "Avocat"
    if "juge" in content_lower[:2000] or "tribunal" in content_lower[:2000] or "TJ Foix" in content_lower:
        return "Tribunal judiciaire"
    if "procureur" in content_lower[:2000] or "parquet" in content_lower[:2000]:
        return "Parquet"
    if "maire" in content_lower[:2000] or "mairie" in content_lower[:2000]:
        return "Mairie de Foix"
    if file_type == "jules":
        return "Équipe projet"
    return None

def guess_legal_basis(content_lower):
    bases = []
    patterns = [
        (r'article\s*l\.?\s*124[0-4][ -]?\d*', "Code civil"),
        (r'article\s*l\.?\s*113[ -]?2', "Code des assurances"),
        (r'article\s*l\.?\s*114[ -]?3', "Code des assurances"),
        (r'article\s*l\.?\s*227[ -]?8', "Code de commerce"),
        (r'article\s*l\.?\s*225[ -]?251', "Code de commerce"),
        (r'article\s*l\.?\s*111[ -]?1', "Code de la consommation"),
        (r'article\s*l\.?\s*217[ -]?1', "Code de la consommation"),
        (r'article\s*l\.?\s*4121[ -]?1', "Code du travail"),
        (r'article\s*835\s*cpc', "Code de procédure civile"),
        (r'article\s*145\s*cpc', "Code de procédure civile"),
        (r'article\s*202\s*cpc', "Code de procédure civile"),
        (r'article\s*700\s*cpc', "Code de procédure civile"),
        (r'article\s*1240', "Code civil"),
        (r'article\s*1241', "Code civil"),
        (r'article\s*1242', "Code civil"),
    ]
    found = set()
    for pattern, code in patterns:
        if re.search(pattern, content_lower):
            if code not in found:
                bases.append(code)
                found.add(code)
    return bases[:4] if bases else None

def enrich_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    yaml, body = parse_yaml_frontmatter(content)
    if not yaml or yaml.get('type') == 'readme':
        return None, "skipped-readme"

    filename = os.path.basename(filepath)
    title = yaml.get('title', filename)
    file_type = classify_file_type(filename, content.lower())
    h1 = extract_h1(body)
    headings = extract_section_headings(body)
    content_lower = content.lower()

    changed = []

    if 'subtitle' not in yaml:
        if h1:
            yaml['subtitle'] = h1[:200]
        else:
            # Si on a une description mais pas de H1, l'utiliser
            desc = yaml.get('description', '')
            if desc and len(desc) > 10:
                yaml['subtitle'] = desc[:200]
            else:
                yaml['subtitle'] = guess_subtitle(filename, title, file_type)
        changed.append('subtitle')

    if 'objective' not in yaml:
        obj_title = h1 if h1 else title
        yaml['objective'] = guess_objective(filename, obj_title, file_type, content_lower)
        changed.append('objective')

    if 'summary' not in yaml:
        desc = yaml.get('description', '')
        if desc and len(desc) > 10:
            summary = desc[:200]
        elif h1:
            # Utiliser le H1 + contexte
            summary = h1[:200]
        else:
            summary = f"Rapport: {title}"[:200]
        yaml['summary'] = summary
        changed.append('summary')

    if 'key_points' not in yaml:
        kp = []
        # Priorité 1: section headings
        for h in headings:
            kp.append(h[:150])
        # Priorité 2: bullet points si pas assez de headings
        if len(kp) < 3:
            kp2 = guess_key_points(body, content_lower)
            kp.extend(kp2)
        if kp:
            yaml['key_points'] = kp[:6]
            changed.append('key_points')

    if 'recipient' not in yaml:
        rec = guess_recipient(filename, file_type, content_lower)
        if rec:
            yaml['recipient'] = rec
            changed.append('recipient')

    if 'tags' not in yaml:
        tags = guess_tags(filename, content_lower, file_type)
        yaml['tags'] = tags
        changed.append('tags')

    if 'legal_basis' not in yaml:
        lb = guess_legal_basis(content_lower)
        if lb:
            yaml['legal_basis'] = lb
            changed.append('legal_basis')

    if not changed:
        return None, "no-change"

    new_content = rebuild_yaml(yaml) + body
    rel = os.path.relpath(filepath, INPUT_BASE)

    if DRY_RUN:
        print(f"  [DRY-RUN] {rel} — +{', '.join(changed)}")
        return None, "dry-run"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"  [MODIFIED] {rel} — +{', '.join(changed)}")
    return None, "modified"

def main():
    total = 0
    modified = 0
    skipped = 0

    for target in TARGET_DIRS:
        base = os.path.join(INPUT_BASE, target)
        if not os.path.isdir(base):
            print(f"Directory not found: {base}")
            continue

        for dirpath, _, filenames in os.walk(base):
            for fn in sorted(filenames):
                if not fn.endswith('.md'):
                    continue
                if fn in ('README.md', 'INDEX.md'):
                    continue

                fp = os.path.join(dirpath, fn)
                total += 1
                _, status = enrich_file(fp)
                if status == "modified":
                    modified += 1
                elif status == "skipped-readme":
                    skipped += 1

    mode = "DRY-RUN" if DRY_RUN else "APPLY"
    print(f"\n=== {mode} ===")
    print(f"Fichiers scannés: {total}")
    print(f"Modifiés: {modified}")
    print(f"Ignorés (readme): {skipped}")
    print(f"Reste inchangé: {total - modified - skipped}")
    if DRY_RUN:
        print("\n🔴 DRY-RUN — aucune modification. Relancer avec --apply pour appliquer.")

if __name__ == '__main__':
    main()
