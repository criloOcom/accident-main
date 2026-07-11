---
title: "📁 Actes — Dossier Contentieux"
breadcrumb: "📁 Actes"
description: "Bienvenue dans le dossier central du contentieux. Ce dossier repose sur une **double strate** : des versions anonymisées pour le travail courant, et des versions réelles pour l'impression et l'envoi."
type: readme
---








<!-- Breadcrumb -->
[🏠](../README.md) › ⚖️ Actes
<!-- /Breadcrumb -->

# 📁 Actes — Dossier Contentieux

---

Bienvenue dans le dossier central du contentieux. Ce dossier repose sur une **double strate** : des versions anonymisées pour le travail courant, et des versions réelles pour l'impression et l'envoi.

## 🗺️ Cartographie interactive (Mermaid)

```mermaid
graph TD
    A[📁 Actes — Dossier Contentieux] --> T[🔑 Token — travail]
    A --> R[👤 Reel — envoi]
    T --> T0[00 Preuves]
    T --> T1[01 Actes procéduraux]
    T --> T2[02 Courriers]
    T --> T3[03 Analyses]
    T --> T4[04 Indemnisation]
    T --> T5[05 Organisation]
    T --> T6[06 Archives]
    R --> R0[00 Preuves]
    R --> R1[01 Actes procéduraux]
    R --> R2[02 Courriers]
    R --> R3[03 Analyses]
    R --> R4[04 Indemnisation]
    R --> R5[05 Organisation]
    R --> R6[06 Archives]
    T1 -->|assignations, conclusions| A1[11 actes]
    T2 -->|courriers tiers| A2[20 courriers]
    T4 -->|Dintilhac| A4[59 600 €]
```

## 🔄 Workflow

1. On travaille exclusivement dans `🔑 Token/` (création, modification, révision)
2. On génère `👤 Reel/` via `python3 app/generate_real_versions.py`
3. On imprime/envoie depuis `👤 Reel/`

## 📋 Sous-dossiers 🔑 Token/ (miroir identique dans 👤 Reel/)

- **[📂 Preuves officielles](🔑%20Token/📂%20Preuves%20officielles/README.md)** — Documents physiques, CR opératoire, PV police
- **[⚖️ Actes procéduraux](🔑%20Token/⚖️%20Actes%20proceduraux/README.md)** — Assignations, conclusions, requêtes
- **[✉️ Courriers](🔑%20Token/✉️%20Courriers/README.md)** — Mises en demeure, signalements, relances
- **[📚 Analyses juridiques](🔑%20Token/📚%20Analyses%20juridiques/README.md)** — Plaidoiries, FAQ, mémorandums
- **[💰 Études d'indemnisation](🔑%20Token/💰%20Etudes%20indemnisation/README.md)** — Évaluation Dintilhac (59 600 €)
- **[🗂️ Organisation](🔑%20Token/🗂️%20Organisation/README.md)** — Index, plan d'action, calendrier
- **[🗄️ Archives](🔑%20Token/🗄️%20Archives/README.md)** — Anciens documents de travail, annexes