---
title: "📁 Actes / reel — Version Réelle"
breadcrumb: "👤 Réel"
description: "Ce dossier contient les versions réelles de tous les actes."
type: readme
---











<!-- Breadcrumb -->
[🏠](../../README.md) › [📁 Actes](../README.md) › 👤 Reel
<!-- /Breadcrumb -->

# 📁 Actes / reel — Version Réelle

---

**Ce dossier contient les versions réelles de tous les actes.**  
Les tokens anonymisés (`**[La Victime]**`, `**[L'Exploitant du Commerce (La SAS)]**`) y sont résolus en identités réelles.

## ⚠️ Règle

> **Ne jamais modifier les fichiers dans `reel/` directement.**  
> Toute modification doit être faite dans [⚖️ Actes/🔑 Token](../🔑%20Token/README.md), puis regénérée via :
> ```bash
> python3 app/generate_real_versions.py
> ```

## 📂 Contenu

- **[⚖️ Actes proceduraux](⚖️%20Actes%20proceduraux/README.md)** — *6* — Assignations, conclusions, requêtes (versions réelles)
- **[✉️ Courriers](✉️%20Courriers/README.md)** — *20* — Courriers et signalements (versions réelles)
- **[📚 Analyses juridiques](📚%20Analyses%20juridiques/README.md)** — *4* — Plaidoiries, FAQ (versions réelles)
- **[💰 Etudes indemnisation](💰%20Etudes%20indemnisation/README.md)** — *1* — Étude d'indemnisation (version réelle)
- **[🗂️ Organisation](🗂️%20Organisation/README.md)** — *3* — Index, plan, calendrier (versions réelles)
- **[🗄️ Archives](🗄️%20Archives/README.md)** — *7* — Archives (versions réelles)

## 🔗 Source

Tous ces fichiers sont générés depuis :
> [⚖️ Actes/🔑 Token](../🔑%20Token/README.md) → `python3 app/generate_real_versions.py` → [⚖️ Actes/👤 Reel](../👤%20Reel/README.md)