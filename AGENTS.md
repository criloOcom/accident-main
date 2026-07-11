<!-- Breadcrumb -->
[🏠](./README.md) › AGENTS
<!-- /Breadcrumb -->

---
title: "AGENTS — Documentation Partagée"
description: "Ce fichier est le point d'entrée pour tous les agents (opencode, anti-gravity, etc.) travaillant sur le dossier Accident de la Main."
type: document
---

# AGENTS — Documentation Partagée

Ce fichier est le point d'entrée pour tous les agents (opencode, anti-gravity, etc.) travaillant sur le dossier Accident de la Main.

## Structure du projet

```
/home/crilocom/accident-main/
├── AGENTS.md              ← Ce fichier — point d'entrée des agents
├── README.md              ← Porte d'entrée publique — MAINTENIR À JOUR
├── ⚖️_Actes/                 ← Actes juridiques (double strate token/reel)
│   ├── token/                 ← Versions tokenisées (travail courant)
│   │   ├── 00_📂_Preuves_officielles/  ← Preuves brutes + inventaire
│   │   ├── 01_⚖️_Actes_proceduraux/
│   │   ├── 02_✉️_Courriers/
│   │   ├── 03_📚_Analyses_juridiques/
│   │   ├── 04_💰_Etudes_indemnisation/
│   │   ├── 05_🗂️_Organisation/
│   │   └── 06_🗄️_Archives/
│   ├── 00_📂_Preuves_officielles/  ← Pièces brutes (source) — lié à la PIECES MAP
│   └── reel/                  ← Versions réelles (générées par .dev/app/generate_real_versions.py)
├── 📜_Lois/                  ← Textes de loi et jurisprudence (cités dans les actes)
├── 🧠_Memory/                ← Mémoire persistante partagée entre tous les agents
│   ├── VACCIN.md          ← 🔴 À LIRE EN PREMIER — obligatoire avant toute action
│   ├── STATUS.md          ← État d'avancement détaillé
│   ├── TODO.md            ← Plans restants et priorités
│   ├── WORKFLOW.md        ← Procédure d'anonymisation
│   ├── TOKEN MAP.md       ← Correspondance jeton ↔ identité réelle
│   ├── DECISIONS.md       ← Décisions d'architecture et règles
│   ├── RULES.md           ← Règles permanentes (INTERDICTIONS incluses)
│   ├── STRICT VARIABLES.md ← Source Unique de Vérité (dates, montants, faits)
│   ├── PIECES MAP.md      ← Correspondance document → pièces citées
│   ├── JURITEXT_PROTOCOL.md ← 🔴 PROTOCOLE STRICT vérification JURITEXT
│   └── RAPPORT_*.md       ← Rapports d'audits, vérifications, synthèses
├── 📊_Rapports/               ← Rapports d'audit, évaluations, plans d'action (lecture humaine)
└── .dev/                  ← Développement, scripts, tests, déploiement (technique)
    ├── app/               ← Scripts Python (agents, outils, pipelines)
    │   ├── agent.py           ← Définition du multi-agent ADK
    │   ├── batch_anonymize.py ← Script d'anonymisation
    │   ├── tools.py           ← Outils MCP (Légifrance, Judilibre, Drive)
    │   ├── check_consistency.py
    │   ├── generate_real_versions.py
    │   ├── sync_readme_listings.py  ← Synchronise READMEs fichiers manquants
    │   └── ...
    ├── tests/             ← Tests unitaires, intégration, évaluation
    ├── deployment/        ← Terraform, déploiement
    ├── Dockerfile
    ├── pyproject.toml
    └── ...
```

## NotebookLM (MCP)

Le projet dispose d'un notebook **Google NotebookLM** dédié (`accident-main`) qui contient les sources versées. Il est accessible via le MCP `notebooklm` configuré dans `opencode.jsonc`.

- **Notebook ID** : `accident-main`
- **URL** : `https://notebooklm.google.com/notebook/3dbe69da-5e8a-4f23-bc0c-d277bcf993d6`
- **Commande** : `notebooklm_ask_question` (conserver le `session_id` pour le contexte conversationnel)
- **Audio Overview** : `notebooklm_generate_audio` + `notebooklm_get_audio_status` + `notebooklm_download_audio`

**Tout agent** peut et doit interroger ce notebook pour obtenir des réponses contextuelles ancrées dans les sources du projet (lois, documents, pièces). Utiliser `notebooklm_ask_question` avec `notebook_id: "accident-main"` après chaque source ajoutée pour valider que le contenu est bien indexé.

## Règles essentielles

0. 🔴 **Lire [🧠_Memory/VACCIN.md](🧠_Memory/VACCIN.md) AVANT toute action** — protocole de vaccination
   obligatoire. Ne pas le lire constitue une faute professionnelle.
1. **Toute mémoire persistante** doit être dans [/home/crilocom/accident-main/🧠_Memory](/home/crilocom/accident-main/🧠_Memory/README.md) — **PAS** dans un dossier privé d'agent
2. **Toute modification** de document Google Docs doit suivre le workflow décrit dans [🧠_Memory/WORKFLOW.md](🧠_Memory/WORKFLOW.md)
3. **Les tokens d'anonymisation** sont définis dans `.dev/app/batch_anonymize.py` — toute modification des tokens doit être faite dans les DEUX endroits (script + TOKEN MAP.md)
4. **Compétences MCP** disponibles :
   - `notebooklm` (MCP serveur) — interroger NotebookLM sur les sources du projet
   - `google-docs-linking` (skill) — insertion de liens Légifrance/Judilibre
   - `google-docs-design` (skill) — mise en page professionnelle
   - `accident-main-legal-research` (skill) — recherche juridique
   - `document-anonymization` (skill) — règles d'anonymisation
5. **Interdiction absolue** d'utiliser du markdown brut, regex, ou find/replace direct sur les Google Docs — toujours passer par le workflow local puis `replaceDocumentWithMarkdown`
6. **Google Sheets — RÈGLE ABSOLUE** : ne JAMAIS supposer la structure des colonnes. Avant d'écrire dans une feuille, **lis la ligne d'en-tête** et **3 lignes de données** pour valider le mapping exact. Supposer = cracher à la gueule de l'utilisateur.
7. **Double strate token/reel** : les fichiers dans [⚖️_Actes/🔑_Token](⚖️_Actes/🔑_Token/README.md) (dossiers 00-06) DOIVENT toujours rester tokenisés (identités anonymisées). Les versions réelles (noms, adresses, email réels) sont générées dans [⚖️_Actes/👤_Reel](⚖️_Actes/👤_Reel/README.md) via `.dev/app/generate_real_versions.py` — ne JAMAIS écrire de version réelle dans [⚖️_Actes/🔑_Token](⚖️_Actes/🔑_Token/README.md).
8. **GitHub Token** : stocké dans Google Secret Manager (`projects/crilo-prod-automation/secrets/GITHUB_TOKEN`). En local, il est aussi dans `~/.git-credentials` (solution de repli). Tout agent DOIT lire depuis Secret Manager, pas depuis une variable d'environnement ou un fichier `.dev/.env`.
9. **README.md** : doit être maintenu à jour après chaque modification de la structure du projet. C'est une consigne absolue — toute création/déplacement/suppression de dossier ou fichier notable doit être répercuté dans README.md.
10. **RÉPERTOIRE SOUVERAIN ABSOLU** : `/home/crilocom/accident-main/` est le SEUL et UNIQUE répertoire de travail local. Aucun agent ne doit créer, cloner, ou travailler dans un autre répertoire (notamment `/tmp/opencode/`, `/tmp/`, ou tout autre chemin). Toute action locale (lecture, écriture, git, scripts) se fait DEPUIS CE DOSSIER. Aucune exception.
11. **VÉRIFICATION JURITEXT OBLIGATOIRE** : Lire [🧠_Memory/JURITEXT_PROTOCOL.md](🧠_Memory/JURITEXT_PROTOCOL.md) avant toute insertion/modification de JURITEXT. Vérification en 2 étapes (Légifrance-prod PUIS OpenLegi) SANS EXCEPTION. Ne JAMAIS deviner un JURITEXT — si introuvable, marquer "À VÉRIFIER" et signaler. Ne JAMAIS se fier à une coche "✓" dans un fichier. Propagation : si une JURITEXT est fausse, chercher et corriger TOUTES les occurrences.
12. **CLÔTURE DES SESSIONS JULES** : Toute session Jules (qu'elle soit terminée, bloquée, ou en échec) DOIT recevoir un message de clôture explicite avant d'être abandonnée. L'API REST Jules n'a pas de delete/archive — le message de clôture est le seul mécanisme pour libérer l'agent. Google archive automatiquement les sessions clôturées. Voir `🧠_Memory/RULES.md #12` et [🧠_Memory/DECISIONS.md](🧠_Memory/DECISIONS.md).
13. **PROPRETÉ DU PROJET** :
    - **Fils d'Ariane** : commentaire HTML `` ligne 1. Script `.dev/app/generate_breadcrumbs.py`. Pas de "Accueil", pas de doublons.
    - **Scripts** : tout `.py` dans `.dev/app/`, jamais à la racine.
    - **Rapports** : tout `.md` de rapport dans [📊_Rapports](📊_Rapports/README.md), jamais à la racine.
    - **Caches** : supprimer `__pycache__` et `.pytest_cache` après exécution de scripts.
    - **PRs** : fermer sans merge les PRs déjà intégrées dans `main`. Supprimer les branches. Voir `🧠_Memory/RULES.md #14` et [🧠_Memory/DECISIONS.md](🧠_Memory/DECISIONS.md).

## Workflow création d'un document

1. Lire l'original (readDocument) → `/tmp/`
2. Anonymiser (batch_anonymize.py) → `/tmp/`
3. Vérifier noms résiduels
4. Structurer en markdown (titres #, tokens **en gras**, sauts de ligne après points)
5. Injecter dans Google Docs (replaceDocumentWithMarkdown)
6. Appliquer styles (applyParagraphStyle JUSTIFIED, tailles police)
7. Ajouter hyperliens juridiques (applyTextStyle linkUrl) + vérifier avec MCP Légifrance
8. Vérifier (readDocument)
9. **Générer version réelle** : si le document doit exister en version réelle, le créer dans `⚖️_Actes/🔑_Token/{dossier}/` puis lancer `python3 .dev/app/generate_real_versions.py`
10. **Mettre à jour README.md** si nouveau fichier notable ajouté

## Workflow maintien du dossier

1. Avant toute action : lire [🧠_Memory/VACCIN.md](🧠_Memory/VACCIN.md) + `AGENTS.md` + [🧠_Memory/STATUS.md](🧠_Memory/STATUS.md)
2. Après toute modification de structure : **mettre à jour README.md**
3. Après toute création de document tokenisé : **générer version réelle** si nécessaire
4. Token GitHub indisponible ? Vérifier dans Secret Manager avant d'utiliser le fallback `~/.git-credentials`
5. **INTERDICTION FORMELLE des liens absolus en interne** : tout lien pointant vers un fichier du dépôt DOIT être un chemin relatif. Seuls les liens externes (Légifrance, Judilibre, sites web) peuvent être des URL absolues `https://...`. Voir `🧠_Memory/RULES.md #15`.
6. **LIENS OBLIGATOIRES SUR TOUTE CITATION INTERNE** : toute citation d'un dossier ou fichier du dépôt (`⚖️_Actes/...`, `📜_Lois/...`, `🧠_Memory/...`, `📊_Rapports/...`, `📎_Annexes/...`) DOIT être un lien relatif cliquable (Markdown `[texte](chemin)`), jamais un simple texte entre backticks sans lien. Dossier cité → lien vers son `README.md` ; fichier cité → lien vers le fichier. Voir `🧠_Memory/RULES.md #17`. Scripts de vérification : `.dev/app/linkify_citations.py` (corrige, dry-run par défaut) et `.dev/app/audit_citation_links.py` (signale les citations non liées).
