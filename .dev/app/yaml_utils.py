#!/usr/bin/env python3
"""Utilitaires YAML partagés — parsing frontmatter, types canoniques, validation.

Usage :
    from yaml_utils import read_frontmatter, CANONICAL_TYPES, STATUT_VALUES
"""

import os
import re
import yaml

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))

CANONICAL_TYPES: dict[str, str] = {
    "loi": "Article de code juridique",
    "jurisprudence": "Décision de justice (arrêt)",
    "courrier": "Courrier / correspondance",
    "assignation": "Acte d'assignation en justice",
    "plainte": "Plainte pénale",
    "analyse_juridique": "Analyse ou mémorandum juridique",
    "etude_indemnisation": "Étude d'indemnisation (Dintilhac)",
    "rapport": "Rapport d'audit ou d'expertise",
    "projet": "Projet, simulation ou version de travail",
    "readme": "Fichier d'index / porte d'entrée",
    "memory": "Fichier mémoire du projet",
    "status": "Suivi d'état d'envoi",
    "preuve": "Pièce de preuve brute",
    "archive": "Document archivé",
    "fiche": "Fiche réflexe / note",
    "document": "Document général",
    "directory": "Index de répertoire",
    "attestation": "Attestation de témoin",
}

CANONICAL_TYPES_SET: set[str] = set(CANONICAL_TYPES.keys())

STATUT_VALUES: set[str] = {
    "final", "projet", "brouillon", "preparation",
    "envoye", "archive", "fusionne", "recueillie",
}

# Dossiers soumis à validation YAML stricte
PERIMETER_DIRS: list[str] = [
    "⚖️ Actes/🔑 Token",
    "⚖️ Actes/👤 Reel",
    "📜 Lois",
    "🧠 Memory",
    "📊 Rapports",
]

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

YAML_FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL | re.MULTILINE)


def read_frontmatter(filepath: str) -> dict | None:
    """Parse le YAML frontmatter d'un fichier .md avec PyYAML.

    Retourne un dict ou None (pas de YAML, ou YAML invalide).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return None

    m = YAML_FRONT_RE.match(content)
    if not m:
        return None

    raw = m.group(1)
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        return None

    if not isinstance(data, dict):
        return None
    return data


def validate_date_format(date_str: str) -> bool:
    """Vérifie qu'une date est au format YYYY-MM-DD."""
    return bool(DATE_RE.match(str(date_str)))


def in_perimeter(filepath: str) -> bool:
    """Vérifie si un fichier est dans le périmètre de validation."""
    rel = os.path.relpath(filepath, REPO_ROOT).replace("\\", "/")
    for d in PERIMETER_DIRS:
        if rel.startswith(d) or rel.startswith(d.replace(" ", "%20")):
            return True
    return False


def is_excluded(filepath: str) -> bool:
    """Fichiers à exclure de la validation."""
    name = os.path.basename(filepath)
    if name.lower() == "readme.md":
        return True
    if name == "CARNET_RDV_UTILISATEUR.md":
        return True
    rel = os.path.relpath(filepath, REPO_ROOT).replace("\\", "/")
    excluded_patterns = [".git/", "__pycache__", "node_modules/", ".dev/"]
    return any(p in rel for p in excluded_patterns)
