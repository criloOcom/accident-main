---
title: "Rapport de correction — JURITEXT erronés"
description: "Fichier corrigé :** [⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/05 🎯 Conclusions Refere.md](⚖️%20Actes/🔑%20Token/⚖️%20Actes%20proceduraux/05%20🎯%20Conclusions%20Refere.md)"
type: rapport
---








<!-- Breadcrumb -->
[🏠](../../../README.md) › [📊 Rapports et Analyses](../../README.md) › [🤖 Jules](../README.md) › [📁 audit](./README.md) › correction juritext 05
<!-- /Breadcrumb -->

# Rapport de correction — JURITEXT erronés

**Fichier corrigé :** [⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/05 🎯 Conclusions Refere.md](⚖️%20Actes/🔑%20Token/⚖️%20Actes%20proceduraux/05%20🎯%20Conclusions%20Refere.md)
**Date :** 10/07/2026

---

## Anomalie 1 — Ligne 85

| Champ | Avant | Après |
|---|---|---|
| **Numéro pourvoi** | 89-18.422 ✅ | 89-18.422 ✅ *(inchangé)* |
| **JURITEXT** | `JURITEXT000007012425` ❌ *(pointe vers 82-13.234, 1983, coopérative agricole)* | `JURITEXT000007026411` ✅ |
| **Décision** | https://www.legifrance.gouv.fr/juri/id/JURITEXT000007012425 | https://www.legifrance.gouv.fr/juri/id/JURITEXT000007026411 |
| **Contenu réel** | Coopérative agricole, pourvoi 82-13.234 | Échelle qui bascule, blessé mortellement, responsabilité du gardien |
| **Vérifié via** | OpenLegi (recherche 89-18.422) | Civ. 2e, 13 février 1991, Bulletin 1991 II N° 55 p. 29 |

## Anomalie 2 — Ligne 93

| Champ | Avant | Après |
|---|---|---|
| **Numéro pourvoi** | 74-10.466 ✅ | 74-10.466 ✅ *(inchangé)* |
| **JURITEXT** | `JURITEXT000007006621` ❌ *(pointe vers 78-12.440, 1980, mandat immobilier)* | `JURITEXT000006993485` ✅ |
| **Décision** | https://www.legifrance.gouv.fr/juri/id/JURITEXT000007006621 | https://www.legifrance.gouv.fr/juri/id/JURITEXT000006993485 |
| **Contenu réel** | Mandat immobilier, pourvoi 78-12.440 | Vice inhérent à la chose (arbre pourri), force majeure exclue |
| **Vérifié via** | OpenLegi (recherche 74-10.466) | Civ. 2e, 5 mai 1975, Bulletin N. 135 P. 111 |

---

## Sauvegarde

- **Backup :** `/home/crilocom/reports/audit/05_conclusions_refere_BACKUP.md`

## Note annexe

Le fichier miroir [⚖️ Actes/👤 Reel/⚖️ Actes proceduraux/05 🎯 Conclusions Refere.md](⚖️%20Actes/👤%20Reel/⚖️%20Actes%20proceduraux/05%20🎯%20Conclusions%20Refere.md) contient les **mêmes JURITEXT erronés** aux lignes 85 et 93. Il devra être corrigé manuellement ou via regénération (`generate_real_versions.py`).