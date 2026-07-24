---
uid: JiqFPsXXR
title: "NOTIFICATION — Application immédiate de l'Avenant Nomenclature"
description: "Date** : 10 juillet 2026"
type: memory
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Memory](./README.md) › RECADRAGE NOMENCLATURE*
<hr>
<!-- /Breadcrumb -->

# NOTIFICATION<br>Application immédiate de l'Avenant Nomenclature

**Date** : 10 juillet 2026
**Destinataires** : Tous les agents (opencode, Jules, NotebookLM, Google Gemini, tiers)
**Objet** : Fiabilisation de la nomenclature des statuts d'envoi — Rectification des erreurs d'audit

---

## 1. Contexte

L'audit interne du 10 juillet 2026 a mis en évidence une **confusion technique grave et récurrente** entre la rédaction d'un document sur Google Drive et son expédition juridique réelle.

Plusieurs agents ont qualifié à tort des documents de « Envoyés » alors qu'ils sont encore au statut de projet ou brouillon, entraînant des erreurs d'appréciation qui faussent la stratégie contentieuse.

## 2. Erreurs factuelles commises par les agents (à corriger immédiatement)

| Affirmation erronée | Vérité du dossier | Agent responsable |
|---------------------|-------------------|-------------------|
| « N°04 (Assureur) a été envoyé le 29/06/2026 » | **FAUX** — Le fichier contient `[Adresse à compléter]`. L'assureur n'est pas identifié. Aucun envoi matériel n'a pu avoir lieu. | opencode |
| « N°07 (Consolidation) envoyé le 31/05/2026 » | **FAUX** — Hallucination temporelle. L'opération a eu lieu le 30/05/2026. La consolidation requiert un suivi d'1 an minimum. | opencode |
| « N°09 (Inspection Travail) envoyé » | **FAUX** — Le fichier indique « Je me réserve le droit de procéder à des signalements » (conditionnel). Document en réserve stratégique. | opencode |
| « N°11-16 (INPI, URSSAF…) envoyés » | **FAUX** — Absence de bordereaux LRAR ou de récépissés. Présents sur Drive uniquement. La Phase 6d STATUS.md est une « Injection Drive », pas une expédition postale. | opencode |
| « N°17-21 (CPAM, SDIS…) envoyés » | **FAUX** — Même absence de preuve d'expédition. | opencode |

## 3. Règle impérative (Avenant n°15 intégré dans RULES.md)

Un document ne peut être qualifié de **« ENVOYÉ »** que si une **preuve matérielle externe** est annexée au dossier :

| Preuve | Exemple concret dans le dossier |
|--------|------------------------------|
| Numéro LRAR | 87001424863012T (N°03 SAS) |
| AR signé | Bailleur M. Romain Delrieu (N°05) |
| Preuve dépôt greffe | TJ Foix (N°10 CPC) |
| Récépissé postal | 870014282662911 (N°06 V2) |
| Facture LRAR en ligne | Z0132713629 (N°06 V2) |

**Tout document sans preuve matérielle = PROJET ou BROUILLON, même si `statut: final` et `source: drive`.**

## 4. Tableau des statuts réels (corrigé)

### ✅ ENVOYÉS (preuve matérielle dans le dossier)

| N° | Document | Preuve |
|:--:|----------|--------|
| 03 | [Mise en demeure SAS](../Actes/Reel/Courriers/SAS_&_Salon/SAS%20-%20Courrier.md) | LRAR 87001424863012T |
| 05 | [Mise en demeure bailleur](../Actes/Reel/Courriers/Propriétaire/Propri%C3%A9taire%20-%20Courrier.md) | AR signé M. Delrieu |
| 06 | [Mise en demeure dirigeants](../Actes/Reel/Courriers/SAS_&_Salon/SAS%20-%20Pr%C3%A9sident%20-%20Courrier.md) | LRAR 87001424721856G + 87001424862879J |
| 06 V2 | [Relance dirigeants](../Actes/Reel/Courriers/SAS_&_Salon/SAS%20-%20Dirigeants%20-%20Courrier%20-%20Relance.md) | Dépôt 870014282662911 + facture Z0132713629 |
| 10 | [CPC Doyen TJ Foix](../Actes/Reel/Actes_proceduraux/Contentieux_civil/TJ%20Foix%20-%20CPC%20145%20-%20Requ%C3%AAte.md) | Dépôt greffe |

### 🟠 PRÊTS POUR ENVOI

| N° | Document | Blocage |
|:--:|----------|---------|
| 34 | [Email Maire Foix Police ERP](../Actes/Reel/Courriers/Mairie/Mairie%20-%20ERP%20Tavella%20-%20Courrier.md) | **🚀 ENVOI PRÉVU DEMAIN 11/07 8H00** |

### 🟡 PROJETS / BROUILLONS

| N° | Document | Raison |
|:--:|----------|--------|
| 04 | [Action directe assureur](../Actes/Reel/Courriers/SAS_&_Salon/SAS%20-%20Assureur%20RC%20-%20Courrier.md) | `[Adresse à compléter]` — assureur non identifié |
| 07 | [Demande consolidation](../Actes/Reel/Courriers/Médical/M%C3%A9decin%20Traitant%20-%20Consolidation%20-%20Demande.md) | État non consolidé, suivi ~1 an |
| 09 | [Inspection Travail](../Actes/Reel/Courriers/Administrations/DDETS%20-%20Signalement.md) | En réserve stratégique (conditionnel) |
| 11 | [INPI signalement](../Actes/Reel/Courriers/Administrations/INPI%20-%20Signalement.md) | Aucune preuve d'expédition |
| 12 | [URSSAF travail dissimulé](../Actes/Reel/Courriers/Administrations/URSSAF%20-%20Signalement.md) | Aucune preuve d'expédition |
| 13 | [Préfecture confirmation](../Actes/Reel/Courriers/Administrations/Pr%C3%A9fecture%20-%20Signalement.md) | Aucune preuve d'expédition |
| 14 | [CODAF signalement](../Actes/Reel/Courriers/Administrations/CODAF%20-%20Signalement.md) | Aucune preuve d'expédition |
| 15 | [SIE information litige](../Actes/Reel/Courriers/Administrations/SIE%20-%20Signalement.md) | Aucune preuve d'expédition |
| 16 | [Conseil Départemental ERP](../Actes/Reel/Courriers/Administrations/Conseil%20D%C3%A9partemental%20-%20Signalement.md) | Aucune preuve d'expédition |
| 17 | [CPAM recours tiers](../Actes/Reel/Courriers/CPAM/CPAM%20-%20Recours%20Tiers%20-%20Saisine.md) | Aucune preuve d'expédition |
| 18 | [SDIS sécurité ERP](../Actes/Reel/Courriers/Administrations/SDIS%20-%20Signalement.md) | Aucune preuve d'expédition |
| 19 | [FGTI saisine conservatoire](../Actes/Reel/Courriers/Justice/FGTI%20-%20Saisine.md) | Aucune preuve d'expédition |
| 20 | [Relance Police](../Actes/Reel/Courriers/Police/Police%20-%20Vid%C3%A9os%20-%20Relance.md) | Aucune preuve d'expédition |
| 21 | [Relance CPAM](../Actes/Reel/Courriers/CPAM/CPAM%20-%20Relance.md) | Aucune preuve d'expédition |

### 🔴 GABARITS NON TRANSMIS

| N° | Document | Blocage |
|:--:|----------|---------|
| 22 | [Attestation témoin client](../Actes/Reel/Attestations/T%C3%A9moin%20Client%20-%20Attestation.md) | Pas de témoin identifié |
| 23 | [Attestation pompier SAMU](../Actes/Reel/Courriers/Témoins/Pompier%20SAMU%20-%20Attestation.md) | Coordonnées pompier inconnues |
| 24 | [Attestation employé](../Actes/Reel/Attestations/Employ%C3%A9%20-%20Attestation.md) | Pas d'employé SAS identifié |

## 5. Sanction

Toute nouvelle erreur de qualification (PROJET qualifié ENVOYÉ sans preuve matérielle) constitue une **faute professionnelle** au sens de la Règle n°14 (vérification sur pièces source) et de la Règle n°15 (avenant nomenclature).

L'agent concerné devra :
1. Identifier et lister tous les fichiers impactés par l'erreur

2. Corriger le statut dans le fichier et dans STATUS.md

3. Signaler la correction dans le prochain commit

---

**Application immédiate** : 10 juillet 2026, 23h00

**Signature** : Rédacteur en chef du dossier Accident de la Main