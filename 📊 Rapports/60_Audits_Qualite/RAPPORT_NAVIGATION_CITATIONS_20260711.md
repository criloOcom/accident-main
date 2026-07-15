---
title: "RAPPORT — Liens obligatoires sur les citations internes (Règle #17)"
description: "Mise en conformité de la navigation : toute citation de dossier/fichier interne doit être un lien cliquable. Règle #17, scripts, état des lieux."
type: rapport
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [📊 Rapports et Analyses](./README.md) › RAPPORT NAVIGATION CITATIONS 20260711*
<hr>
<!-- /Breadcrumb -->

# RAPPORT<br>Liens obligatoires sur les citations internes

## Objectif
Garantir que **toute citation d'un dossier ou d'un fichier interne au dépôt** soit un **lien relatif cliquable** (Markdown `[texte](chemin)`), jamais un simple texte entre backticks sans lien. Objectif : navigation totale entre tous les fichiers, sans régression qualité par les agents futurs.

## Règle instituée
- **Règle #17** ajoutée dans `🧠 Memory/RULES.md` : liens obligatoires sur toute citation interne (dossier → `README.md` du dossier ; fichier → fichier).
- Inscrite dans `AGENTS.md` (point 6 du workflow) pour que **tout agent** la respecte dès sa prise de poste.

## Scripts créés (.dev/app)
1. `linkify_citations.py` — transforme automatiquement les citations backtick internes non liées en liens (dossier→README, fichier→fichier ; résolution de la convention historique `{token,reel}`). Dry-run par défaut, `--apply` pour écrire.
2. `audit_citation_links.py` — vérifie qu'aucune citation interne n'est laissée en texte brut non lié (signale les cibles introuvables). À lancer en pré-commit pour éviter les régressions.

## Action réalisée (commit associé)
- **485 liens créés** sur 78 fichiers (citations pointant vers des cibles existantes : dossiers → leur README, fichiers → les fichiers).
- **2 hubs de gouvernance corrigés** (lus par tous les agents) :
  - `🧠 Memory/WORKFLOW.md` : citations `⚖️ Actes/archives/STRATEGIE_...` (dossier renommé) → `⚖️ Actes/🔑 Token/🗄️ Archives/🧠 STRATEGIE Contentieux Civil.md` (+ Pénal), liées.
  - `🧠 Memory/RULES.md` : même correction.
- Aucune régression : `check_consistency.py` (« Rien à signaler »), `audit_readme_integrity.py` (0 erreur), audit YAML (0 invalide).

## Restant à traiter (non bloquant)
Environ 290 citations résiduelles pointent vers des **cibles inexistantes** ou sont des **conventions illustratives**. Répartition :
- **Conventions illustratives** (à ignorer) : `🧠 Memory/RULES.md #12`, `⚖️ Actes/...` (listage de dossiers dans AGENTS.md), `*.md`, `{00-06}`, `XXX.md`.
- **Docs d'archive / journaux historiques** (`📊 Rapports/🗄️ Archives/...`, `🧠 Memory/STATUS.md`) : chemins historiques morts (fichiers renommés/supprimés, ex. `📊 Rapports/expertise/20260707 Mémoire juridique Glose.md` jamais importé, docs fantômes `RAPPORT_JURISPRUDENCES.md`).
- **Quelques docs fantômes connus** déjà signalés dans l'audit Hermès (ex. `🧠 Memory/RAPPORT_JURISPRUDENCES.md`).

Ces citations résiduelles sont dans des documents de **reporting/archivage**, pas dans la documentation de navigation active. Leur correction manuelle est à faire par un agent disposant du contexte (pour décider : corriger vers le nouvel emplacement, ou supprimer la référence historique). La règle #17 empêchera toute NOUVELLE citation non liée.

## Recommandation
- Ajouter `python3 .dev/app/audit_citation_links.py` au pre-commit (avec `check_consistency.py` et `audit_readme_integrity.py`) pour bloquer toute régression de navigation.
- Traiter les docs d'archive `📊 Rapports/🗄️ Archives/` et `STATUS.md` dans une passe dédiée (corriger les chemins morts ou marquer les sections comme historiques).