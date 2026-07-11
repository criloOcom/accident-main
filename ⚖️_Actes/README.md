<!-- Breadcrumb -->
[🏠](../README.md)
<!-- /Breadcrumb -->

---
title: "📁 Actes — Dossier Contentieux"
description: "Bienvenue dans le dossier central du contentieux. Ce dossier repose sur une **double strate** : des versions anonymisées pour le travail courant, et des versions réelles pour l'impression et l'envoi."
type: readme
---

# 📁 Actes — Dossier Contentieux

---

Bienvenue dans le dossier central du contentieux. Ce dossier repose sur une **double strate** : des versions anonymisées pour le travail courant, et des versions réelles pour l'impression et l'envoi.

## 🗂️ Structure

| Dossier | Contenu |
|---------|---------|
| **[`🔑_Token/`](🔑_Token/README.md)** | **Versions tokenisées** — Identités remplacées par `**[La Victime]**`, etc. C'est la strate de travail. |
| **[`👤_Reel/`](👤_Reel/README.md)** | **Versions réelles** — Tokens résolus (noms, adresses, email réels). Version imprimable et envoyable. |

## 🔄 Workflow

1. On travaille exclusivement dans `🔑_Token/` (création, modification, révision)
2. On génère `👤_Reel/` via `python3 app/generate_real_versions.py`
3. On imprime/envoie depuis `👤_Reel/`

## 📋 Sous-dossiers 🔑_Token/ (miroir identique dans 👤_Reel/)

| N° | Dossier | Description |
|----|---------|-------------|
| `00` | **[Preuves officielles](🔑_Token/00_📂_Preuves_officielles/README.md)** | Documents physiques, CR opératoire, PV police |
| `01` | **[Actes procéduraux](🔑_Token/01_⚖️_Actes_proceduraux/README.md)** | Assignations, conclusions, requêtes |
| `02` | **[Courriers](🔑_Token/02_✉️_Courriers/README.md)** | Mises en demeure, signalements, relances |
| `03` | **[Analyses juridiques](🔑_Token/03_📚_Analyses_juridiques/README.md)** | Plaidoiries, FAQ, mémorandums |
| `04` | **[Études d'indemnisation](🔑_Token/04_💰_Etudes_indemnisation/README.md)** | Évaluation Dintilhac (59 600 €) |
| `05` | **[Organisation](🔑_Token/05_🗂️_Organisation/README.md)** | Index, plan d'action, calendrier |
| `06` | **[Archives](🔑_Token/06_🗄️_Archives/README.md)** | Anciens documents de travail, annexes |
