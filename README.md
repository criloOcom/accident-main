# Accident de la Main — Dossier Juridique

**Contentieux civil et pénal** suite à un accident survenu le 29 mai 2026 dans un commerce, avec défaut d'assurance responsabilité civile professionnelle, ITT et préjudices corporels.

## Arborescence

```
accident-main/
├── actes/                  ← 14 actes juridiques (.md avec YAML front matter)
├── pieces/                 ← 19 pièces originales (.md extraits des PDFs)
├── memory/                 ← Mémoire persistante pour les agents IA
│   ├── STATUS.md           ← État d'avancement détaillé
│   ├── RULES.md            ← Règles permanentes et interdictions
│   ├── STRICT_VARIABLES.md ← Source unique de vérité (dates, montants, faits)
│   ├── TOKEN_MAP.md        ← Correspondance jetons ↔ identités réelles
│   ├── PIECES_MAP.md       ← Mapping documents → pièces citées
│   ├── WORKFLOW.md         ← Procédure d'anonymisation et d'injection
│   ├── DECISIONS.md        ← Décisions d'architecture
│   └── DESIGN.md           ← Charte graphique Google Docs
├── app/                    ← Scripts Python (agent ADK, anonymisation, extraction, injection)
├── deployment/             ← Terraform (infrastructure GCP)
├── tests/                  ← Tests unitaires, intégration et evaluation
├── AGENTS.md               ← Point d'entrée pour les agents IA
├── JULES.md                ← Guide pour l'agent Google Jules
├── GEMINI.md               ← Guide pour l'agent Gemini Code Assist
└── .env.example            ← Variables d'environnement requises
```

## Actes (14)

Chaque fichier dans `actes/` est un document juridique au format markdown avec métadonnées YAML front matter (titre, date, type, catégorie, auteur, tags, statut, drive_id).

| # | Fichier | Statut |
|---|---------|--------|
| 01 | Assignation Référé-Provision et Expertise Médicale | `final` |
| 02 | Action Directe Assureur RC (Art. L.124-3) | `final` |
| 03 | Plainte Complément — Défaut d'Assurance RC | `final` |
| 04 | Projet d'Assignation Référé-Provision V1 (5000€) | `brouillon` |
| 05 | Constitution de Partie Civile | `final` |
| 06 | Dossier de Présentation | `final` |
| 07 | Étude d'Indemnisation Maximale (Dintilhac) | `final` |
| 08 | Index de l'État Final du Dossier | `final` |
| 09 | Plan d'Action et Chronologie | `final` |
| 10 | Synthèse Juridique et FAQ | `final` |
| 11 | Mémorandum — Audit Stratégique | `final` |
| 12 | Rapport — Analyse des Préjudices Corporels | `final` |
| 13 | Mémorandum — Responsabilité des Dirigeants | `final` |
| 14 | Analyse des Fondements de la Responsabilité | `final` |

## Pièces (19)

`pieces/` contient le contenu textuel extrait des 19 pièces originales PDF. Quatre pièces scannées ont été traitées par OCR français (`tesseract -l fra`). Chaque fichier est marqué d'un bandeau d'immutabilité et contient le `drive_id` permettant de retrouver le PDF original sur Google Drive.

## Pour les humains

- Consulter `memory/STRICT_VARIABLES.md` pour les dates, montants et faits vérifiés
- Consulter `memory/TOKEN_MAP.md` pour la correspondance des noms anonymisés
- Consulter `memory/STATUS.md` pour l'avancement global
- Les Google Docs originaux (versions UNIFIE_ANONYME) sont dans le Drive du projet

## Pour les agents IA

- **open-code** : lire `AGENTS.md` en premier, puis tous les fichiers dans `memory/`
- **Google Jules** : lire `JULES.md` pour le workflow d'injection et les MCP servers
- **Gemini Code Assist** : lire `GEMINI.md` pour le cycle de développement ADK
- **Respecter impérativement** `memory/RULES.md` (interdictions incluses)
- Ne jamais poser de question dont la réponse existe déjà dans les fichiers mémoire
- Ne jamais inventer de statut juridique (vérifier dans STRICT_VARIABLES.md)

## Conventions clés

| Règle | Description |
|-------|-------------|
| `=== PAGE BREAK ===` | Marqueur de saut de page dans les actes (split à l'injection) |
| `🔒 PIÈCE ORIGINALE` | Bandeau d'immutabilité sur les pièces — ne pas modifier le contenu textuel |
| YAML front matter | Métadonnées Obsidian sur tous les fichiers .md |
| Identifiant pièce | Triplet `(date, émetteur, objet)` — pas de numéro |
| Google Docs | Pas de regex/find/replace direct — passer par le workflow local markdown |

## Dépendances techniques

- Python 3.13+, uv
- Google ADK (`google-agents-cli`)
- Terraform (déploiement GCP)
- Tesseract OCR français (extraction pièces scannées)
- Poppler-utils / pdftotext (extraction PDF textuels)
