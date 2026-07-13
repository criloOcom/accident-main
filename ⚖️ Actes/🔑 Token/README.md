---
title: "🎭 Actes / token — Version Anonymisée"
breadcrumb: "🎭 Token"
description: "Ce dossier contient la version de travail de tous les actes."
type: readme
---
<!-- Breadcrumb -->
*[🏠](../../README.md) › [📁 Actes](../README.md) › 🔑 Token*
<hr>
<!-- /Breadcrumb -->

# 🎭 Actes / token<br>Version Anonymisée

---

**Ce dossier contient la version de travail de tous les actes.**  
Les identités réelles (noms, adresses, email, immatriculations) y sont remplacées par des tokens entre crochets et en **gras** : `**[La Victime]**`, `**[L'Exploitant du Commerce (La SAS)]**`, etc.

## ✅ Règles

- **Toute modification se fait ici.** Ne jamais modifier les fichiers dans `reel/`.
- Un fichier créé ou modifié dans `token/` doit être propagé dans `reel/` via le script.
- Les tokens sont définis dans [🧠 Memory/TOKEN MAP.md](../../%F0%9F%A7%A0%20Memory/TOKEN%20MAP.md) et [🧠 Memory/STRICT VARIABLES.md](../../%F0%9F%A7%A0%20Memory/STRICT%20VARIABLES.md).

## 📂 Contenu

- **[00 — Preuves officielles](%F0%9F%93%82%20Preuves%20officielles/README.md)** — 0 fichier · Documents physiques (en attente d'insertion)
- **[01 — Actes procéduraux](%E2%9A%96%EF%B8%8F%20Actes%20proceduraux/README.md)** — 6 fichiers · Pièces juridiques principales (assignations, conclusions)
- **[02 — Courriers](%E2%9C%89%EF%B8%8F%20Courriers/README.md)** — 20 fichiers · Correspondance avec tiers (administrations, assurances)
- **[03 — Analyses juridiques](%F0%9F%93%9A%20Analyses%20juridiques/README.md)** — 4 fichiers · Plaidoiries, FAQ, analyses de fond
- **[04 — Études d'indemnisation](%F0%9F%92%B0%20Etudes%20indemnisation/README.md)** — 1 fichier · Évaluation financière des préjudices
- **[05 — Organisation](%F0%9F%97%82%EF%B8%8F%20Organisation/README.md)** — 3 fichiers · Index, plan d'action, calendrier
- **[06 — Archives](%F0%9F%97%84%EF%B8%8F%20Archives/README.md)** — 7 fichiers · Anciennes versions, annexes, lexique

## 🗺️ Cartographie du dossier (interactif)

```mermaid
graph TD
    A[🎭 Actes / token] --> B[00 Preuves officielles]
    A --> C[01 Actes procéduraux]
    A --> D[02 Courriers]
    A --> E[03 Analyses juridiques]
    A --> F[04 Études indemnisation]
    A --> G[05 Organisation]
    A --> H[06 Archives]
    C --> C1[01 Assignation]
    C --> C2[02 Plainte]
    C --> C3[07 Constitution partie civile]
    C --> C4[08 Projet ordonnance]
    C --> C5[09 Réquisitoire]
    C --> C6[10 Signalement parquet]
    C --> C7[11 Requête mandataire ad hoc]
    D --> D1[20 courriers tiers]
    E --> E1[04 analyses de fond]
```