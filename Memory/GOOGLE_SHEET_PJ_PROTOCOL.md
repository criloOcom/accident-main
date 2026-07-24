---
uid: GSDOCRECON2026
title: "PROTOCOLE GOOGLE SHEET PJ — Restauration et Enrichissement par Liens GitHub"
description: "Règles strictes de gestion et de complétion du Google Sheet PJ sans dénaturation du travail utilisateur."
type: memory
date: "2026-07-23"
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Memory](./README.md) › GOOGLE SHEET PJ PROTOCOL*
<hr>
<!-- /Breadcrumb -->

<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Memory](./README.md)*
<hr>

# PROTOCOLE GOOGLE SHEET PJ<br>Restauration et Complétion des Liens GitHub

> **Règle d'or pour tout agent ou intervenant** : Le Google Sheet `PJ` (feuille `@`) est l'outil de travail vivant de l'utilisateur. Aucun agent ne doit chercher à deviner ou remplir artificiellement des UIDs dans des colonnes où l'utilisateur ne les a pas saisis. L'intervention d'un agent se limite strictement à **enrichir le tableau existant** par la résolution des UIDs en URLs GitHub valides.

---

## 1. COMPRÉHENSION EXACTE DE LA LIGNE 2 (EN-TÊTES MAÎTRES)

Chaque bloc de colonnes répond à un rôle précis défini en ligne 2 :

| Colonnes | Libellé Ligne 2 | Description / Contenu attendu |
|---|---|---|
| **A** | `uid` | **UID de la Preuve Officielle (Pièce brute)** brute originale |
| **B** | `uid Url .md` | **URL GitHub** pointant vers le fichier `.md` sous `Actes/Preuves_officielles/` |
| **C** | `📄Fichier 🔑ID Drive` | **SOUVERAINETÉ UTILISATEUR ABSOLUE**. Identifiant Google Drive saisi par l'utilisateur. **NE JAMAIS TOUCHER OU EFFACER.** |
| **G** | `uid TOKEN` | **UID du document TOKEN (Anonymisé)**. Présent UNIQUEMENT si l'utilisateur l'a saisi (acte/courrier formalisé). |
| **H** | `uid TOKEN Url` | **URL GitHub** pointant vers l'acte sous `Actes/Token/` |
| **I** | `Titre TOKEN` | Titre du document Token extrait du YAML front-matter |
| **J** | `uid REEL` | **UID du document RÉEL (Non-anonymisé)**. Présent UNIQUEMENT si l'utilisateur l'a saisi. |
| **K** | `uid REEL Url` | **URL GitHub** pointant vers la version réelle sous `Actes/Reel/` |
| **L** | `Titre REEL` | Titre du document Réel extrait du YAML front-matter |

---

## 2. INTERDICTIONS ET RÈGLES STRICTES POUR LES AGENTS

1. **INTERDISION DE COPIER LES UIDs D'UNE COLONNE À L'AUTRE** :

   - Si la colonne `G` ou `J` est vide dans le travail d'origine (`@ Backup AvantInterventionAgent IA`), **LAISSER VIDE**.
   - Ne JAMAIS recopier l'UID de la colonne `A` vers la colonne `G` ou `J` automatiquement.

2. **PROTECTION ABSOLUE DE LA COLONNE C** :

   - La colonne `C` contient les identifiants Google Drive saisis manuellement.
   - Ne JAMAIS modifier, tronquer ou supprimer ces valeurs.

3. **MISSION EXCLUSIVE DE L'AGENT** :

   - Prendre la structure et les UIDs **exacts** du tableau d'origine.
   - Si un UID existe en colonne `A` mais que la colonne `B` est vide ➔ Résoudre l'URL GitHub dans `Actes/Preuves_officielles/` et la mettre en `B`.
   - Si un UID existe en colonne `G` mais que la colonne `H` est vide ➔ Résoudre l'URL GitHub sous `Actes/Token/` et la mettre en `H` (et le titre en `I`).
   - Si un UID existe en colonne `J` mais que la colonne `K` est vide ➔ Résoudre l'URL GitHub sous `Actes/Reel/` et la mettre en `K` (et le titre en `L`).

---

## 3. WORKFLOW ET OUTILS TECHNIQUE

- **Lecture préalable obligatoire** : Lire la feuille `@ Backup AvantInterventionAgent IA` pour obtenir le baseline exact.

- **Indexation locale** : Scanner les fichiers `.md` du dépôt pour associer chaque `uid` à son chemin GitHub exact (`https://github.com/criloOcom/accident-main/blob/main/Actes/...`).

- **Écriture par API Google Sheets MCP** : Utiliser l'outil `writeSpreadsheet` par tranches/chunks (e.g. `A3:C52`, `G3:L52`) pour éviter tout problème de quota ou de timeout.

---

*Protocole officiel mis à jour le 23 juillet 2026.*
