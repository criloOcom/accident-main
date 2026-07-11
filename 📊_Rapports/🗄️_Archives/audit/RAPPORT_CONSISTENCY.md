<!-- Breadcrumb -->
[🏠](../../../README.md) › [📊 Rapports et Analyses](../../README.md) › [📁 🗄️_Archives](../README.md) › [📁 audit](./README.md) › RAPPORT CONSISTENCY
<!-- /Breadcrumb -->

---
title: "Rapport de Consistency"
description: "L'exécution de `python3 app/check_consistency.py` a généré les avertissements suivants :"
type: rapport
---

# Rapport de Consistency

## État Initial
L'exécution de `python3 app/check_consistency.py` a généré les avertissements suivants :

```
=== VÉRIFICATION CROSS-DOCUMENT ===

  WARN    09_Courrier Inspection Travail.md → token potentiel non documenté : [Adresse a completer]
  WARN    11_Courrier INPI.md → token potentiel non documenté : [Adresse a completer]
  WARN    12_Courrier URSSAF.md → token potentiel non documenté : [Adresse a completer]
  WARN    13_Courrier Prefecture.md → token potentiel non documenté : [Adresse a completer]
  WARN    14_Courrier CODAF.md → token potentiel non documenté : [Adresse a completer]
  WARN    15_Courrier SIE.md → token potentiel non documenté : [Adresse a completer]
  WARN    16_Courrier Conseil Departemental.md → token potentiel non documenté : [Adresse a completer]
  WARN    18_Courrier SDIS.md → token potentiel non documenté : [Adresse a completer]
  WARN    19_Courrier FGTI.md → token potentiel non documenté : [Adresse a completer]
  WARN    20_Relance Police.md → token potentiel non documenté : [Adresse a completer]
  WARN    21_Relance CPAM.md → token potentiel non documenté : [Adresse a completer]

0 erreur(s), 11 avertissement(s)
```

## Corrections Apportées
Remplacement de la chaîne `[Adresse a completer]` par `[Adresse à compléter]` dans tous les fichiers Markdown du dossier `⚖️_Actes/02_✉️_Courriers/`. L'écriture `[Adresse à compléter]` fait partie de la liste des tokens acceptés.

## État Final
L'exécution de `python3 app/check_consistency.py` ne renvoie désormais aucune erreur ni avertissement :

```
=== VÉRIFICATION CROSS-DOCUMENT ===

Rien à signaler — tout est cohérent.
```
