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

ROOT = "/app"
SKIP_DIRS = {'.git', '.pytest_cache', '.venv', 'node_modules', '__pycache__', '.opencode'}

SEP = " › "


def link_for_ups(ups):
