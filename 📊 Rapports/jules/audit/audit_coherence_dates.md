---
title: "Audit de Cohérence Documentaire : Dates (Courriers 09 à 34)"
description: "Objectif** : Vérification de la cohérence des dates dans les courriers prêts à envoyer (actes 09 à 34) conformément au référentiel `STRICT VARIABLES.md`."
type: rapport
---





<!-- Breadcrumb -->
[🏠](../../../README.md) › [📊 Rapports et Analyses](../../README.md) › [🤖 Jules](../README.md) › [📁 audit](./README.md) › audit coherence dates
<!-- /Breadcrumb -->

# Audit de Cohérence Documentaire : Dates (Courriers 09 à 34)

**Objectif** : Vérification de la cohérence des dates dans les courriers prêts à envoyer (actes 09 à 34) conformément au référentiel `STRICT VARIABLES.md`.

## Résultats de l'audit

| Fichier | Pages | Dates vérifiées | Problèmes détectés (⚠️) ou OK (✓) |
|---|---|---|---|
| 09 ✉️ Courrier Inspection Travail.md | 2 | 2026-07-05, 22 avril 2024, 29 juin 2026, 29 mai 2026, 5 juillet 2026 | ✓ OK |
| 10 ✉️ Courrier Doyen Juges Instruction.md | 1 | 2 juin 2026, 2026-07-06, 29 mai 2026, 6 juillet 2026 | ✓ OK |
| 11 ✉️ Courrier INPI.md | 1 | 2026-07-05, 29 juin 2026, 29 mai 2026, 5 juillet 2026 | ✓ OK |
| 12 ✉️ Courrier URSSAF.md | 1 | 2026-07-05, 29 mai 2026, 5 juillet 2026 | ✓ OK |
| 13 ✉️ Courrier Prefecture.md | 2 | 2026-07-05, 29 juin 2026, 29 mai 2026, 5 juillet 2026 | ✓ OK |
| 14 ✉️ Courrier CODAF.md | 1 | 2026-07-05, 22 avril 2024, 29 mai 2026, 5 juillet 2026 | ✓ OK |
| 15 ✉️ Courrier SIE.md | 1 | 2026-07-05, 29 juin 2026, 29 mai 2026, 5 juillet 2026 | ✓ OK |
| 16 ✉️ Courrier Conseil Departemental.md | 1 | 2026-07-05, 25 juin 1980, 29 mai 2026, 5 juillet 2026 | ✓ OK |
| 17 ✉️ Courrier CPAM.md | 2 | 10 juin 2026, 2026-07-06, 23 juillet 2026, 29 juin 2026, 29 mai 2026, 3 juin 2026, 30 juin 2026, 30 mai 2026, 31 mai 2026, 5 juillet 2026, 6 juillet 2026 | ✓ OK (J+3, J+21, J+4, J+32 sont des tokens textuels corrects pour les tableaux de pièces jointes) |
| 18 ✉️ Courrier SDIS.md | 1 | 2026-07-05, 29 mai 2026, 5 juillet 2026 | ✓ OK |
| 19 ✉️ Courrier FGTI.md | 2 | 2026-07-06, 23 juillet 2026, 29 juin 2026, 29 mai 2026, 30 juin 2026, 5 juillet 2026, 6 juillet 2026 | ✓ OK |
| 20 🔄 Relance Police.md | 1 | 2 juin 2026, 2026-07-05, 29 mai 2026, 5 juillet 2026 | ✓ OK |
| 21 🔄 Relance CPAM.md | 1 | 2026-07-05, 29 mai 2026, 3 juin 2026, 5 juillet 2026 | ✓ OK |
| 22 📋 Attestation Témoin Client.md | 1 | 2026-06-30, 29 mai 2026 | ✓ OK |
| 23 📋 Attestation Pompier SAMU.md | 1 | 2026-06-30, 29 mai 2026 | ✓ OK |
| 24 📋 Attestation Employé.md | 1 | 2026-06-30, 29 mai 2026 | ✓ OK |
| 25 📧 Relance Dr DJERBI.md | 1 | 12 novembre 2026, 2026-07-06, 29 mai 2026, 30 mai 2026, 5 juillet 2026 | ✓ OK |
| 26 📧 Attestation Temoin Client.md | 1 | 2026-07-06, 29 mai 2026 | ✓ OK |
| 27 📧 Attestation Pompier SAMU.md | 1 | 2026-07-06, 29 mai 2026 | ✓ OK |
| 28 📧 Attestation Employe.md | 1 | 2026-07-06, 29 mai 2026 | ✓ OK |
| 29 ✉️ Courrier Maire Foix.md | 1 | 2026-07-09, 29 mai 2026, 9 juillet 2026 | ✓ OK |
| 30 ✉️ Courrier President TC.md | 2 | 2026-07-09, 9 juillet 2026 | ✓ OK |
| 31 ✉️ Courrier INPI Opposition.md | 1 | 2026-07-09, 29 mai 2026, 9 juillet 2026 | ✓ OK |
| 32 ✉️ Courrier SIE URSSAF Mutualisation.md | 2 | 2026-07-09, 29 mai 2026, 3 avril 1955 | ⚠️ Token `[J+41]` non résolu dans l'en-tête (devrait être: 9 juillet 2026) |
| 33 ✉️ Requete Constat Huissier 145 CPC.md | 2 | 18 janvier 1982, 2026-07-09, 29 juin 2026, 29 mai 2026, 30 mai 2026, 6 juillet 2026 | ⚠️ Token `[J+41]` non résolu dans l'en-tête (devrait être: 9 juillet 2026) |
| 34 ✉️ EMAIL Maire Foix - Police Municipale ERP.md | 1 | 2 juin 2026, 2026-07-10, 23 juin 2026, 29 juin 2026, 29 mai 2026, 5 juillet 2026, 6 juillet 2026 | ✓ OK |

## Observations générales

- Les dates de naissance (`18 janvier 1982`), les dates d'accident (`29 mai 2026`) et les dates de chirurgie (`30 mai 2026`) mentionnées dans le corps du texte sont cohérentes sur l'ensemble des documents vérifiés et conformes à `STRICT VARIABLES.md`.
- Les jetons `[J+3]`, `[J+4]`, `[J+21]`, `[J+32]` dans le fichier 17 (CPAM) sont utilisés comme références textuelles pour les annexes et non comme champs de publipostage à convertir en date, leur usage est donc correct.
- Les seules exceptions concernent les documents 32 et 33, qui comportent toujours le jeton `[J+41]` dans l'en-tête, lequel n'a pas été traduit par sa valeur finale (`9 juillet 2026`).

---
Audit généré par Jules (Auditeur de Cohérence Documentaire)