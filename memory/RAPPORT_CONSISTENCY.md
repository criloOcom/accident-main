# Rapport de Consistency

## État Initial
L'exécution de `python3 app/check_consistency.py` a généré les avertissements suivants :

```
=== VÉRIFICATION CROSS-DOCUMENT ===

  WARN    09_Courrier Inspection Travail - V1.md → token potentiel non documenté : [Adresse a completer]
  WARN    11_Courrier INPI - V1.md → token potentiel non documenté : [Adresse a completer]
  WARN    12_Courrier URSSAF - V1.md → token potentiel non documenté : [Adresse a completer]
  WARN    13_Courrier Prefecture - V1.md → token potentiel non documenté : [Adresse a completer]
  WARN    14_Courrier CODAF - V1.md → token potentiel non documenté : [Adresse a completer]
  WARN    15_Courrier SIE - V1.md → token potentiel non documenté : [Adresse a completer]
  WARN    16_Courrier Conseil Departemental - V1.md → token potentiel non documenté : [Adresse a completer]
  WARN    18_Courrier SDIS - V1.md → token potentiel non documenté : [Adresse a completer]
  WARN    19_Courrier FGTI - V1.md → token potentiel non documenté : [Adresse a completer]
  WARN    20_Relance Police - V1.md → token potentiel non documenté : [Adresse a completer]
  WARN    21_Relance CPAM - V1.md → token potentiel non documenté : [Adresse a completer]

0 erreur(s), 11 avertissement(s)
```

## Corrections Apportées
Remplacement de la chaîne `[Adresse a completer]` par `[Adresse à compléter]` dans tous les fichiers Markdown du dossier `actes/02_Courriers/`. L'écriture `[Adresse à compléter]` fait partie de la liste des tokens acceptés.

## État Final
L'exécution de `python3 app/check_consistency.py` ne renvoie désormais aucune erreur ni avertissement :

```
=== VÉRIFICATION CROSS-DOCUMENT ===

Rien à signaler — tout est cohérent.
```
