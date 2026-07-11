---
title: "Documentation des scripts de l'application (.dev/app/)"
description: "Ce dossier contient les scripts fonctionnels utilisés pour le traitement, l'anonymisation, le déploiement et la gestion du dossier Accident de la Main."
type: readme
---

# Documentation des scripts de l'application (.dev/app/)

Ce dossier contient les scripts fonctionnels utilisés pour le traitement, l'anonymisation, le déploiement et la gestion du dossier Accident de la Main.

| Script | Description | Usage | Dépendances |
|--------|-------------|-------|-------------|
| **agent.py** | Point d'entrée principal définissant l'agent IA (multi-agent ADK). | `python3 .dev/app/agent.py` | Google ADK, mcp_bridge, app_utils |
| **anonymize_doc.py** | Script basique de remplacement des entités nominatives par des tokens (obsolète/test remplacé par batch_anonymize). | `python3 .dev/app/anonymize_doc.py <input_file>` | `re`, `sys` |
| **batch_anonymize.py** | Script officiel d'anonymisation en masse avec la table maîtresse des tokens (cf. TOKEN MAP.md). | `python3 .dev/app/batch_anonymize.py <input> <output>` | `re`, `sys`, `os` |
| **batch_link_legifrance.py** | Script d'ajout en masse de liens hypertextes Légifrance (inline) dans les actes. | `python3 .dev/app/batch_link_legifrance.py` | `re`, `os` |
| **check_consistency.py** | Outil essentiel de vérification cross-document (liens, tokens, frontmatter, etc.). | `python3 .dev/app/check_consistency.py` | `re`, `os`, `sys`, `pathlib` |
| **consolidate_sheet.py** | Script consolidant les données d'étapes de travail dans le Google Sheet dédié. | `python3 .dev/app/consolidate_sheet.py` | `google-api-python-client`, `app.drive_auth` |
| **drive_auth.py** | Module de gestion de l'authentification et des credentials Google Drive API. | N/A (module importé) | `google-auth`, `google-api-python-client` |
| **drive_client.py** | CLI client pour interagir avec Google Drive (télécharger/uploader des fichiers). | `python3 .dev/app/drive_client.py list --folder-id <ID>` | `google-api-python-client`, `app.drive_auth` |
| **extract_legal_refs.py** | Extrait les références légales et contient la base des URL valides. | `python3 .dev/app/extract_legal_refs.py` | `re`, `sys` |
| **fast_api_app.py** | Application FastAPI exposant l'agent ADK et l'adaptateur Reasoning Engine (A2A). | `uvicorn app.fast_api_app:app --host 0.0.0.0 --port 8000` | FastAPI, Google ADK, uvicorn |
| **injection.py** | Script d'injection du Markdown transformé (et paginé) vers l'API Google Docs. | N/A (module importé) | `google-api-python-client`, `app.drive_auth` |
| **scratch_merge_chronologies.py** | Outil de fusion et synchronisation des chronologies vers Google Drive. | `python3 .dev/app/scratch_merge_chronologies.py` | `google-api-python-client`, `app.drive_auth` |
| **tools.py** | Outils personnalisés appelant le bridge MCP (Légifrance, Judilibre, souverain). | N/A (module importé) | mcp_bridge, json |

## Règles de développement
- Ne jamais exécuter de web scraping direct (toujours utiliser MCP).
- Conserver la standardisation du shebang `#!/usr/bin/env python3` sur tous les scripts principaux.
- Lors de l'ajout d'un nouveau script, documenter ici.
