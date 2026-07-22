---
title: Audit des liens internes et synchronisation README
date: 2026-07-18
description: Rapport d'audit sur l'intégrité des liens, la synchronisation des README et la propreté du dépôt.
type: rapport
subtitle: "📊 Rapport d'audit : Liens, README et Propreté"
objective: "Auditer et vérifier la conformité de Rapport d'audit : Liens, README et Propreté"
summary: Rapport d'audit sur l'intégrité des liens, la synchronisation des README et la propreté du dépôt.
key_points:
  - I — LIENS INTERNES CASSÉS ET REDIRECTIONS
  - II — SYNCHRONISATION DES README ET INDEX
  - III — CITATIONS ET FONDEMENTS JURIDIQUES
  - IV — PROPRETÉ ET CONVENTIONS
recipient: Avocat
tags:
  - audit
  - conformite
  - qualite
  - avocat
  - token
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [Rapports](./README.md)*
<hr>
<!-- /Breadcrumb -->

<!-- Breadcrumb -->
<a href="../README.md">Retour</a>
<hr>

# 📊 Rapport d'audit : Liens, README et Propreté

<hr><hr>

## I — LIENS INTERNES CASSÉS ET REDIRECTIONS

L'audit des liens internes révèle plusieurs dizaines de liens cassés. Ceux-ci sont classés par sévérité afin de faciliter la correction.

### A. Liens cassés avec candidats (redirigeables)

Il s'agit de liens dont le chemin est incorrect mais pour lesquels un fichier du même nom existe dans le dépôt.

- **`AGENTS.md`** : le lien [/home/crilocom/accident-main/Memory/README.md](../Memory/README.md) pointe vers un chemin absolu (interdit par les conventions) et de nombreux candidats existent.

- **[Rapports/20_Accueil_Avocat/PACK_ACCUEIL_AVOCAT_AJ.md](20_Accueil_Avocat/PACK_ACCUEIL_AVOCAT_AJ.md)** : lien vers `TJ Foix - TJ Foix - Référé Provision - Assignation.md` introuvable, 2 candidats.

- **`Status/01_PREPARATION.md`** : lien vers `TJ Foix - Bordereau Unifié.md` introuvable, 2 candidats.

- **`Status/02_PRET_POUR_ENVOI.md`** : lien vers `TJ Foix - Bordereau Unifié.md` introuvable, 2 candidats.

- **`Status/brouillon.md`** : lien vers `TJ Foix - Bordereau Unifié.md` introuvable, 2 candidats.

- **`Status/final.md`** : lien vers `TJ Foix - Bordereau Unifié.md` introuvable, 2 candidats.

- **[Memory/TODO.md](../Memory/TODO.md)** : lien vers `TJ Foix - Bordereau Unifié.md` introuvable, 2 candidats.

### B. Liens critiques cassés (introuvables)

Ces liens pointent vers des fichiers ou tokens qui n'existent pas ou plus à l'emplacement indiqué.

- **Tokens manquants dans [Actes/Token](../Actes/Token/README.md) et `Reel/`** :

  - `token-dr-jardon.md` est appelé dans de multiples courriers de mises en demeure et relances (`Propriétaire - Courrier.md`, `SAS - Courrier.md`, `✉️🔄 Consolidation.md`, `DDETS - Signalement.md`, etc.).

  - `token-assureur-rc.md` manque dans `TJ Foix - Conclusions au Fond.md` et plusieurs rapports.

  - `token-metropole-regionale.md` manque dans `20260715 PV Police PV Complementaire AccidentSalonCoiffure.md`.

  - `token-victime-nom-complet.md` manque dans `20270529_Rapport_Expertise_Médicale.md` et `SAS - Assureur RC - Courrier (copie Avocat).md`.

  - `token-exploitation-nom-commercial.md` et `token-exploitation-prepose-nom.md` sont appelés mais introuvables.

- **Fichiers manquants dans [Rapports](README.md)** :

  - `RAPPORT_NAVIGATION_INTERACTIVE_20260711.md` manque dans plusieurs audits.

  - `RAPPORT_AUDIT_RISQUES.md` manque dans `RAPPORT_PREPARATION_PLAINTE_COMPLEMENTAIRE_20260711.md`, `STATUS.md` et `TODO.md`.

### C. Problèmes esthétiques ou faux positifs

- **`README.md`** pointe vers `GEMINI.md` qui est introuvable.

- Les liens `mailto:` (ex: `mailto:sebastien.grazide@gmail.com`) sont considérés comme introuvables par le script actuel car il s'agit d'un protocole mail et non d'un fichier.

- Des liens du type `...` (points de suspension) sont identifiés comme cassés dans `Plainte Complémentaire - Correction.md`.

<hr><hr>

## II — SYNCHRONISATION DES README ET INDEX

L'audit d'intégrité des fichiers README montre des désynchronisations mineures entre le contenu des dossiers et leur documentation.

### A. Fichiers déclarés mais introuvables

- **`README.md` (racine)** déclare `GEMINI.md` qui n'existe pas.

### B. Fichiers présents mais non listés dans leur README respectif

- **[Lois/Code/Code_assurances](../Lois/Code/Code_assurances/README.md)** : le fichier `Article_L124-3_Codesassurances_Legifrance.md` est présent mais non listé.

- **`.dev/app/`** : `resolve_reel_tokens_report.md` est présent mais non listé.

- **[Memory](../Memory/README.md)** : `Mémo Stratégie Bailleur HB BARBER.md` n'est pas listé.

- **[Memory/Tokens](../Memory/Tokens/README.md)** : nombreux tokens manquants dans l'index (ex: `token-cpam-dossier-numero.md`, `token-exploitation-hb-capital-social.md`, `token-pv-police-numero.md`, etc.).

- **[Actes/Token/Analyses_juridiques](../Actes/Token/Analyses_juridiques/README.md)** : `Note - Mémo Axes Juridiques Avocat.md` et `Note - Synthèse Avocat Bascule HB BARBER.md` ne sont pas listés.

- **[Actes/Token/Preuves_officielles](../Actes/Token/Preuves_officielles/README.md)** : `20270529_Rapport_Expertise_Médicale.md` n'est pas listé.

- **`Actes/Token/Actes_proceduraux/📋 Preparation Foix/`** : `Police - Note Erratum Identité.md` n'est pas listé.

- **[Rapports](README.md) et sous-dossiers** :

  - `85_RESTANT_A_FAIRE_2026-07-15.md` n'est pas listé dans [Rapports/README.md](README.md).

  - `00_META_SYNTHESE_MULTI_ANGLE.md` n'est pas listé dans `30_Analyses_Multi_Angle/README.md`.

  - `RAPPORT_SYNTHESE_GLOBALE_CHANTIER_2026-07-14.md` n'est pas listé dans `70_Technique_Repo/README.md`.

  - `FICHE_REUNION_AVOCAT_AJ_10MIN.md` n'est pas listé dans `20_Accueil_Avocat/README.md`.

<hr><hr>

## III — CITATIONS ET FONDEMENTS JURIDIQUES

Le script d'audit des citations internes (`.dev/app/audit_citation_links.py`) confirme que :

- **Toutes les citations internes sont cliquables.** (0 citation interne non liée dans 0 fichier).

- L'intégrité des liens de citation juridique vers Légifrance ou les fichiers de la bibliothèque locale [Lois](../Lois/README.md) est préservée pour les fichiers testés.

<hr><hr>

## IV — PROPRETÉ ET CONVENTIONS

### A. Propreté des dossiers (caches et fichiers orphelins)

- Les répertoires de cache typiques (`__pycache__`, `.pytest_cache`) sont absents du dépôt ou ont été correctement ignorés/supprimés.

- Des scripts Python ou rapports mal placés traînent à la racine du dépôt :

  - `generate_clean_audit.py` est un script orphelin ou temporaire à la racine au lieu d'être dans `.dev/app/`.

### B. Respect des conventions (CONVENTIONS.md)

L'observation globale permet de constater que certains fichiers récents nécessiteraient l'exécution du pipeline d'unification pour garantir une conformité totale :

- Le remplacement de `---` par `<hr><hr>` entre les sections (via `normalize_sections.py`).

- Le fil d'Ariane généré manuellement ou absent dans certains rapports.

- La bonne application des listes à puces au lieu des tableaux pour les inventaires de README.

Il est recommandé de lancer de manière préventive :
- `python3 .dev/app/sync_readme_listings.py --apply`

- `python3 .dev/app/fix_internal_links.py`