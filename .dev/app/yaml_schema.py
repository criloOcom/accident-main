#!/usr/bin/env python3
"""
Schéma YAML canonique pour tous les fichiers .md du projet accident-main.

Chaque fichier .md doit avoir un front matter YAML EN LIGNE 1 (première
ligne du fichier), puis le fil d'Ariane (commentaire HTML), puis le contenu.
Cet ordre est imposé pour que la prévisualisation GitHub des fichiers .md
rende correctement le bloc YAML (un commentaire HTML devant le YAML empêche
GitHub de le parser comme front matter).

Structure:
    ---
    title: "..."
    description: "..."
    type: "..."
    date: YYYY-MM-DD
    tags: [...]
    statut: "..."
    ---

    <!-- Breadcrumb -->
    [🏠](README.md) › ...
    <!-- /Breadcrumb -->

    # Titre du document
"""

from __future__ import annotations
import os
import re

CANONICAL_TYPES: dict[str, str] = {
    "loi": "Article de code juridique",
    "jurisprudence": "Décision de justice (arrêt)",
    "courrier": "Courrier / correspondance",
    "assignation": "Acte d'assignation en justice",
    "plainte": "Plainte pénale",
    "analyse_juridique": "Analyse ou mémorandum juridique",
    "etude_indemnisation": "Étude d'indemnisation (Dintilhac)",
    "rapport": "Rapport d'audit ou d'expertise",
    "readme": "Fichier d'index / porte d'entrée",
    "memory": "Fichier mémoire du projet",
    "status": "Suivi d'état d'envoi",
    "preuve": "Pièce de preuve brute",
    "archive": "Document archivé",
    "fiche": "Fiche réflexe / note",
    "document": "Document général",
}

DIR_TYPE_MAP: dict[str, str] = {
    "📜_Lois": "loi",
    "📜_Jurisprudence": "jurisprudence",
    "📊_Index": "readme",
    "🔑_Token": "readme",
    "👤_Reel": "readme",
    "00_📂_Preuves_officielles": "preuve",
    "01_⚖️_Actes_proceduraux": "assignation",
    "02_✉️_Courriers": "courrier",
    "03_📚_Analyses_juridiques": "analyse_juridique",
    "04_💰_Etudes_indemnisation": "etude_indemnisation",
    "05_🗂️_Organisation": "readme",
    "06_🗄️_Archives": "archive",
    "📎_Annexes": "archive",
    "🧠_Memory": "memory",
    "🚦_Status": "status",
    "📊_Rapports": "rapport",
    ".dev": "readme",
}

TAG_EXTRACTORS: list[str] = [
    "destinataire", "auteur", "reel_path", "token_path",
    "source", "drive_id", "legiarti", "juritext",
    "pourvoi", "code", "article", "jurisdiction",
    "ecli", "last_verified",
]


def detect_type(filepath: str) -> str:
    basename = os.path.basename(filepath)
    if basename.lower() == "readme.md":
        return "readme"
    parts = filepath.replace("\\", "/").split("/")
    loisdir_idx = -1
    for i, part in enumerate(parts):
        if "📜_Lois" in part or "📜_Lois" in part.replace("%20", " "):
            loisdir_idx = i
    if loisdir_idx >= 0:
        for j in range(loisdir_idx, len(parts)):
            p = parts[j]
            if "Jurisprudence" in p:
                return "jurisprudence"
        if loisdir_idx < len(parts) - 1:
            return "loi"
    # Process deepest parts first (backward) for specificity
    for part in reversed(parts):
        if part in DIR_TYPE_MAP:
            return DIR_TYPE_MAP[part]
        for prefix, dtype in DIR_TYPE_MAP.items():
            if part.startswith(prefix):
                return dtype
    return "document"


def extract_title_from_content(content: str) -> str:
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if m:
        return m.group(1).strip().strip('*').strip()
    return ""


def extract_first_paragraph(content: str, max_chars: int = 250) -> str:
    lines = content.split("\n")
    in_body = False
    for line in lines:
        s = line.strip()
        if s.startswith("# "):
            in_body = True
            continue
        if not in_body:
            continue
        if s.startswith("#") or s.startswith("<!--") or s.startswith("---") or s.startswith(">"):
            continue
        if s == "":
            continue
        clean = s.strip("* \t").strip('"')
        if clean and len(clean) > 5:
            return clean[:max_chars].rstrip()
    return ""


def make_yaml(title: str, description: str, dtype: str,
              date_str: str | None = None,
              tags: list[str] | None = None,
              statut: str | None = None,
              extra: dict[str, str] | None = None) -> str:
    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f'description: "{description}"')
    lines.append(f"type: {dtype}")
    if date_str:
        lines.append(f"date: {date_str}")
    if tags:
        items = "\n".join(f"  - {t}" for t in tags)
        lines.append(f"tags:\n{items}")
    if statut:
        lines.append(f"statut: {statut}")
    if extra:
        for k, v in extra.items():
            if v:
                lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def parse_simple_yaml(text: str) -> dict[str, str | list[str]]:
    """Parse simple YAML key: value pairs (no nesting)."""
    result: dict[str, str | list[str]] = {}
    current_key = None
    current_list: list[str] = []
    for line in text.split("\n"):
        m = re.match(r'^(\w[\w_-]*)\s*:\s*(.*)', line)
        if m:
            if current_key and current_list:
                result[current_key] = current_list
                current_list = []
            key = m.group(1)
            val = m.group(2).strip().strip('"').strip("'")
            if val.startswith("[") and val.endswith("]"):
                # Inline list
                items = [x.strip().strip('"').strip("'") for x in val[1:-1].split(",") if x.strip()]
                result[key] = items
            elif val:
                result[key] = val
            current_key = key if not val else None
        elif line.strip().startswith("- ") and current_key:
            current_list.append(line.strip()[2:].strip().strip('"').strip("'"))
    if current_key and current_list:
        result[current_key] = current_list
    return result


def get_first_line(content: str) -> str:
    idx = content.find("\n")
    return content[:idx] if idx >= 0 else content


def extract_breadcrumb_anywhere(content):
    """Extrait le bloc fil d'Ariane (commentaire HTML) à n'importe quelle position.
    Retourne (breadcrumb_block, content_sans_breadcrumb)."""
    m = re.search(r'<!-- Breadcrumb -->.*?<!-- /Breadcrumb -->', content, re.DOTALL)
    if not m:
        # ancien format monobloc <!-- ... -->
        m2 = re.search(r'<!--\s*\[🏠\].*?-->', content, re.DOTALL)
        if not m2:
            return "", content
        m = m2
    bc = m.group(0).strip()
    rest = (content[:m.start()] + content[m.end():]).strip("\n")
    return bc, rest


def update_yaml_header(filepath: str, dry_run: bool = False) -> str | None:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Extraire le breadcrumb (peu importe sa position : ligne 1 ou apres YAML)
    breadcrumb, rest = extract_breadcrumb_anywhere(content)

    # 2. Strip leading whitespace for reliable YAML detection
    rest_stripped = rest.lstrip("\n")

    # 3. Detect existing YAML (maintenant en ligne 1)
    yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n?', rest_stripped, re.DOTALL)
    existing_yaml = yaml_match.group(1) if yaml_match else ""
    if yaml_match:
        rest = rest_stripped[yaml_match.end():]

    dtype = detect_type(filepath)
    extra: dict[str, str] = {}

    if existing_yaml:
        existing = parse_simple_yaml(existing_yaml)
        title = existing.get("title") or existing.get("titre") or extract_title_from_content(rest)
        if isinstance(title, list):
            title = str(title[0]) if title else ""
        elif not isinstance(title, str):
            title = str(title) if title else ""

        desc = existing.get("description", "")
        if isinstance(desc, list):
            desc = str(desc[0]) if desc else ""
        if not desc or desc in ("null", "None"):
            desc = extract_first_paragraph(rest)

        date_str = existing.get("date", "")
        if isinstance(date_str, list):
            date_str = str(date_str[0]) if date_str else ""
        date_str = str(date_str) if not isinstance(date_str, str) else date_str

        statut = existing.get("statut", "")
        if isinstance(statut, list):
            statut = str(statut[0]) if statut else ""
        statut = str(statut) if not isinstance(statut, str) else statut
        if statut in ("null", "None"):
            statut = ""

        tags_raw = existing.get("tags", [])
        if isinstance(tags_raw, str):
            tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        elif isinstance(tags_raw, list):
            tags = [str(t).strip('"').strip("'") for t in tags_raw if t]
        else:
            tags = None
        if tags and all(t in ("null", "None", "") for t in tags):
            tags = None

        for k in TAG_EXTRACTORS:
            v = existing.get(k)
            if v:
                if isinstance(v, list):
                    v = str(v[0])
                v = str(v)
                if v not in ("null", "None", ""):
                    extra[k] = v
    else:
        title = extract_title_from_content(rest)
        desc = extract_first_paragraph(rest)
        date_str = ""
        statut = ""
        tags = None

    if not title:
        title = os.path.splitext(os.path.basename(filepath))[0]
    title = str(title) if not isinstance(title, str) else title
    desc = str(desc) if not isinstance(desc, str) else desc
    if not desc:
        desc = f"Document de type {dtype}"

    new_yaml = make_yaml(title, desc, dtype,
                         date_str=date_str or None,
                         tags=tags or None,
                         statut=statut or None,
                         extra=extra if extra else None)

    # ORDRE CANONIQUE : YAML (ligne 1) puis breadcrumb puis contenu
    new_content = new_yaml + "\n\n"
    if breadcrumb:
        new_content += breadcrumb + "\n\n"
    new_content += rest.lstrip("\n")

    if new_content == content:
        return None

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return new_content
