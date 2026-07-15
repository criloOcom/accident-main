---
title: "AGENTS — Documentation Partagée"
description: "Ce fichier est le point d'entrée pour tous les agents (opencode, anti-gravity, etc.) travaillant sur le dossier Accident de la Main."
type: preuve
---

<!-- Breadcrumb -->
*[🏠](./README.md) › AGENTS*
<hr>
<!-- /Breadcrumb -->

# AGENTS<br>Documentation Partagée

Ce fichier est le point d'entrée pour tous les agents (opencode, anti-gravity, etc.) travaillant sur le dossier Accident de la Main.

## Structure du projet

```
/home/crilocom/accident-main/
├── AGENTS.md              ← Ce fichier — point d'entrée des agents
├── README.md              ← Porte d'entrée publique — MAINTENIR À JOUR
├── ⚖️ Actes/                 ← Actes juridiques (double strate 🔑 Token/👤 Reel)
│   ├── 🔑 Token/                 ← Versions tokenisées (travail courant)
│   │   ├── 📂 Preuves officielles/  ← Preuves brutes + inventaire
│   │   ├── ⚖️ Actes proceduraux/
│   │   ├── ✉️ Courriers/              ← 44 docs rangés par type d'acte (📜 Mises en demeure, 🚨 Signalements, 🔄 Relances, ⚖️ Contentieux, 📋 Attestations, 📝 Procédure, 📋 Personnel, 🗄️ Archivé)
│   │   ├── 📚 Analyses juridiques/
│   │   ├── 💰 Etudes indemnisation/
│   │   ├── 🗂️ Organisation/
│   │   └── 🗄️ Archives/
│   ├── 📂 Preuves officielles/  ← Pièces brutes (source) — lié à la PIECES MAP
│   └── 👤 Reel/                  ← Versions réelles (générées par .dev/app/generate_real_versions.py)
├── 📜 Lois/                  ← Textes de loi et jurisprudence (cités dans les actes)
├── 🧠 Memory/                ← Mémoire persistante partagée entre tous les agents
│   ├── VACCIN.md          ← 🔴 À LIRE EN PREMIER — obligatoire avant toute action
│   ├── STATUS.md          ← État d'avancement détaillé
│   ├── TODO.md            ← Plans restants et priorités
│   ├── WORKFLOW.md        ← Procédure d'anonymisation
│   ├── TOKEN MAP.md       ← Correspondance token ↔ identité réelle (tableau maître)
│   ├── 🗂️ Tokens/            ← 56 fiches individuelles enrichies par token
│   ├── CONVENTIONS.md     ← 🔴 Conventions de formatage unifiées (ordre canonique, séparateurs `<hr><hr>`, citations)
│   ├── DECISIONS.md       ← Décisions d'architecture et règles
│   ├── RULES.md           ← Règles permanentes (INTERDICTIONS incluses)
│   ├── STRICT VARIABLES.md ← Source Unique de Vérité (dates, montants, faits)
│   ├── PIECES MAP.md      ← Correspondance document → pièces citées
│   ├── JURITEXT_PROTOCOL.md ← 🔴 PROTOCOLE STRICT vérification JURITEXT
│   └── RAPPORT_*.md       ← Rapports d'audits, vérifications, synthèses
├── 📊 Rapports/               ← Rapports d'audit, évaluations, plans d'action (lecture humaine)
└── .dev/                  ← Développement, scripts, tests, déploiement (technique)
    ├── app/               ← Scripts Python (agents, outils, pipelines)
    │   ├── agent.py           ← Définition du multi-agent ADK
    │   ├── batch_anonymize.py ← Script d'anonymisation
    │   ├── tools.py           ← Outils MCP (Légifrance, Judilibre, Drive)
    │   ├── check_consistency.py
    │   ├── generate_real_versions.py
    │   ├── normalize_sections.py    ← Normalise séparateurs `<hr><hr>` (Token/Reel)
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

0. 🔴 **Lire [🧠 Memory/VACCIN.md](%F0%9F%A7%A0%20Memory/VACCIN.md) AVANT toute action** — protocole de vaccination
   obligatoire. Ne pas le lire constitue une faute professionnelle.
1. **Toute mémoire persistante** doit être dans [/home/crilocom/accident-main/🧠 Memory](/home/crilocom/accident-main/%F0%9F%A7%A0%20Memory/README.md) — **PAS** dans un dossier privé d'agent
2. **Toute modification** de document Google Docs doit suivre le workflow décrit dans [🧠 Memory/WORKFLOW.md](%F0%9F%A7%A0%20Memory/WORKFLOW.md)
3. **Les tokens d'anonymisation** sont définis dans [`.dev/app/batch_anonymize.py`](.dev/app/batch_anonymize.py) — toute modification des tokens doit être faite dans les DEUX endroits (script + TOKEN MAP.md)
4. **Compétences MCP** disponibles :
   - `notebooklm` (MCP serveur) — interroger NotebookLM sur les sources du projet
   - `google-docs-linking` (skill) — insertion de liens Légifrance/Judilibre
   - `google-docs-design` (skill) — mise en page professionnelle
   - `accident-main-legal-research` (skill) — recherche juridique
   - `document-anonymization` (skill) — règles d'anonymisation
5. **Interdiction absolue** d'utiliser du markdown brut, regex, ou find/replace direct sur les Google Docs — toujours passer par le workflow local puis `replaceDocumentWithMarkdown`
6. **Google Sheets — RÈGLE ABSOLUE** : ne JAMAIS supposer la structure des colonnes. Avant d'écrire dans une feuille, **lis la ligne d'en-tête** et **3 lignes de données** pour valider le mapping exact. Supposer = cracher à la gueule de l'utilisateur.
7. **Double strate 🔑 Token/👤 Reel** : les fichiers dans [⚖️ Actes/🔑 Token](%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) (dossiers 📂 Preuves officielles, ⚖️ Actes proceduraux, ✉️ Courriers, 📚 Analyses juridiques, 💰 Etudes indemnisation, 🗂️ Organisation, 🗄️ Archives) DOIVENT toujours rester tokenisés (identités anonymisées). Les versions réelles (noms, adresses, email réels) sont générées dans [⚖️ Actes/👤 Reel](%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/README.md) via [`.dev/app/generate_real_versions.py`](.dev/app/generate_real_versions.py) — ne JAMAIS écrire de version réelle dans [⚖️ Actes/🔑 Token](%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md).
8. **GitHub Token** : stocké dans Google Secret Manager (`projects/crilo-prod-automation/secrets/GITHUB_TOKEN`). En local, il est aussi dans `~/.git-credentials` (solution de repli). Tout agent DOIT lire depuis Secret Manager, pas depuis une variable d'environnement ou un fichier `.dev/.env`.
9. **README.md** : doit être maintenu à jour après chaque modification de la structure du projet. C'est une consigne absolue — toute création/déplacement/suppression de dossier ou fichier notable doit être répercuté dans README.md.
10. **RÉPERTOIRE SOUVERAIN ABSOLU** : `/home/crilocom/accident-main/` est le SEUL et UNIQUE répertoire de travail local. Aucun agent ne doit créer, cloner, ou travailler dans un autre répertoire (notamment `/tmp/opencode/`, `/tmp/`, ou tout autre chemin). Toute action locale (lecture, écriture, git, scripts) se fait DEPUIS CE DOSSIER. Aucune exception.
11. **VÉRIFICATION JURITEXT OBLIGATOIRE** : Lire [🧠 Memory/JURITEXT_PROTOCOL.md](%F0%9F%A7%A0%20Memory/JURITEXT_PROTOCOL.md) avant toute insertion/modification de JURITEXT. Vérification en 2 étapes (Légifrance-prod PUIS OpenLegi) SANS EXCEPTION. Ne JAMAIS deviner un JURITEXT — si introuvable, marquer "À VÉRIFIER" et signaler. Ne JAMAIS se fier à une coche "✓" dans un fichier. Propagation : si une JURITEXT est fausse, chercher et corriger TOUTES les occurrences.
12. **SESSIONS JULES — PARAMÈTRES OBLIGATOIRES** : Tout appel à `jules_create_session` DOIT inclure les trois paramètres suivants, sous peine de créer une session "repoless" (sans lien au dépôt) : `repo: "criloOcom/accident-main"`, `branch: "main"`, `autoPr: true`. Lire [🧠 Memory/JULES_MCP_GUIDELINES.md](%F0%9F%A7%A0%20Memory/JULES_MCP_GUIDELINES.md) avant tout appel. Voir aussi #12.b pour la clôture.
13. **CLÔTURE DES SESSIONS JULES** : Toute session Jules (qu'elle soit terminée, bloquée, ou en échec) DOIT recevoir un message de clôture explicite avant d'être abandonnée. L'API REST Jules n'a pas de delete/archive — le message de clôture est le seul mécanisme pour libérer l'agent. Google archive automatiquement les sessions clôturées. Voir [🧠 Memory/RULES.md](%F0%9F%A7%A0%20Memory/RULES.md) #12 et [🧠 Memory/DECISIONS.md](%F0%9F%A7%A0%20Memory/DECISIONS.md).
14. **PROPRETÉ DU PROJET** :
    - **Fils d'Ariane** : commentaire HTML placé APRÈS le bloc YAML (ligne 1 = `---`). Le YAML doit rester en première ligne pour la prévisualisation GitHub. Script [`.dev/app/generate_breadcrumbs.py`](.dev/app/generate_breadcrumbs.py). Pas de "Accueil", pas de doublons.
    - **Scripts** : tout `.py` dans `.dev/app/`, jamais à la racine.
    - **Rapports** : tout `.md` de rapport dans [📊 Rapports](%F0%9F%93%8A%20Rapports/README.md), jamais à la racine.
    - **Caches** : supprimer `__pycache__` et `.pytest_cache` après exécution de scripts.
    - **PRs** : fermer sans merge les PRs déjà intégrées dans `main`. Supprimer les branches. Voir [🧠 Memory/RULES.md](%F0%9F%A7%A0%20Memory/RULES.md) #14 et [🧠 Memory/DECISIONS.md](%F0%9F%A7%A0%20Memory/DECISIONS.md).

## Workflow création d'un document

1. Lire l'original (readDocument) → `/tmp/`
2. Anonymiser (batch_anonymize.py) → `/tmp/`
3. Vérifier noms résiduels
4. Structurer en markdown (titres #, tokens **en gras**, **ligne vide entre chaque bloc de paragraphe**, sauts de ligne après points)
5. Injecter dans Google Docs (replaceDocumentWithMarkdown)
6. Appliquer styles (applyParagraphStyle JUSTIFIED, tailles police)
7. Ajouter hyperliens juridiques (applyTextStyle linkUrl) + vérifier avec MCP Légifrance
8. Vérifier (readDocument)
9. **Générer version réelle** : si le document doit exister en version réelle, le créer dans `⚖️ Actes/🔑 Token/{dossier}/` puis lancer `python3` [`.dev/app/generate_real_versions.py`](.dev/app/generate_real_versions.py)
10. **Mettre à jour README.md** si nouveau fichier notable ajouté

## Workflow maintien du dossier

1. Avant toute action : lire [🧠 Memory/VACCIN.md](%F0%9F%A7%A0%20Memory/VACCIN.md) + [`AGENTS.md`](AGENTS.md) + [🧠 Memory/STATUS.md](%F0%9F%A7%A0%20Memory/STATUS.md)
2. Après toute modification de structure : **mettre à jour README.md**
3. Après toute création de document tokenisé : **générer version réelle** si nécessaire
4. Token GitHub indisponible ? Vérifier dans Secret Manager avant d'utiliser le fallback `~/.git-credentials`
5. **INTERDICTION FORMELLE des liens absolus en interne** : tout lien pointant vers un fichier du dépôt DOIT être un chemin relatif. Seuls les liens externes (Légifrance, Judilibre, sites web) peuvent être des URL absolues `https://...`. Voir [🧠 Memory/RULES.md](%F0%9F%A7%A0%20Memory/RULES.md) #15.
6. **LIENS OBLIGATOIRES SUR TOUTE CITATION INTERNE** : toute citation d'un dossier ou fichier du dépôt (`⚖️ Actes/...`, `📜 Lois/...`, `🧠 Memory/...`, `📊 Rapports/...`) DOIT être un lien relatif cliquable (Markdown `[texte](chemin)`), jamais un simple texte entre backticks sans lien. Dossier cité → lien vers son `README.md` ; fichier cité → lien vers le fichier. Voir [🧠 Memory/RULES.md](%F0%9F%A7%A0%20Memory/RULES.md) #17. Scripts de vérification : [`.dev/app/linkify_citations.py`](.dev/app/linkify_citations.py) (corrige, dry-run par défaut) et [`.dev/app/audit_citation_links.py`](.dev/app/audit_citation_links.py) (signale les citations non liées).