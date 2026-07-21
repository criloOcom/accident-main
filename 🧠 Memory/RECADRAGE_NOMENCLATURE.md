---
title: "NOTIFICATION — Application immédiate de l'Avenant Nomenclature"
description: "Date** : 10 juillet 2026"
type: memory
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › RECADRAGE NOMENCLATURE*
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
| 03 | [Mise en demeure SAS](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%A2%20SAS%20%26%20Salon/%E2%9C%89%EF%B8%8F%20SAS%20-%20Courrier.md) | LRAR 87001424863012T |
| 05 | [Mise en demeure bailleur](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%A0%20Propri%C3%A9taire/%E2%9C%89%EF%B8%8F%20Propri%C3%A9taire%20-%20Courrier.md) | AR signé M. Delrieu |
| 06 | [Mise en demeure dirigeants](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%A2%20SAS%20%26%20Salon/%E2%9C%89%EF%B8%8F%20SAS%20-%20Pr%C3%A9sident%20-%20Courrier.md) | LRAR 87001424721856G + 87001424862879J |
| 06 V2 | [Relance dirigeants](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%A2%20SAS%20%26%20Salon/%E2%9C%89%EF%B8%8F%20SAS%20-%20Dirigeants%20-%20Courrier%20-%20Relance.md) | Dépôt 870014282662911 + facture Z0132713629 |
| 10 | [CPC Doyen TJ Foix](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9A%96%EF%B8%8F%20Actes%20proceduraux/%F0%9F%93%9C%20Contentieux%20civil/Requete%20Art.145%20CPC.md) | Dépôt greffe |

### 🟠 PRÊTS POUR ENVOI

| N° | Document | Blocage |
|:--:|----------|---------|
| 34 | [Email Maire Foix Police ERP](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%9B%EF%B8%8F%20Mairie/%E2%9C%89%EF%B8%8F%20Mairie%20-%20ERP%20Tavella%20-%20Courrier.md) | **🚀 ENVOI PRÉVU DEMAIN 11/07 8H00** |

### 🟡 PROJETS / BROUILLONS

| N° | Document | Raison |
|:--:|----------|--------|
| 04 | [Action directe assureur](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%A2%20SAS%20%26%20Salon/%E2%9C%89%EF%B8%8F%20SAS%20-%20Assureur%20RC%20-%20Courrier.md) | `[Adresse à compléter]` — assureur non identifié |
| 07 | [Demande consolidation](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%E2%9A%95%EF%B8%8F%20M%C3%A9dical/%E2%9C%89%EF%B8%8F%20Courrier%20-%20Demande%20Consolidation.md) | État non consolidé, suivi ~1 an |
| 09 | [Inspection Travail](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%9B%EF%B8%8F%20Administrations/%E2%9C%89%EF%B8%8F%20Inspection%20du%20Travail%20-%20Signalement.md) | En réserve stratégique (conditionnel) |
| 11 | [INPI signalement](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%9B%EF%B8%8F%20Administrations/%E2%9C%89%EF%B8%8F%20INPI%20-%20Signalement.md) | Aucune preuve d'expédition |
| 12 | [URSSAF travail dissimulé](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%9B%EF%B8%8F%20Administrations/%E2%9C%89%EF%B8%8F%20URSSAF%20-%20Signalement.md) | Aucune preuve d'expédition |
| 13 | [Préfecture confirmation](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%9B%EF%B8%8F%20Administrations/%E2%9C%89%EF%B8%8F%20Pr%C3%A9fecture%20-%20Signalement.md) | Aucune preuve d'expédition |
| 14 | [CODAF signalement](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%9B%EF%B8%8F%20Administrations/%E2%9C%89%EF%B8%8F%20CODAF%20-%20Signalement.md) | Aucune preuve d'expédition |
| 15 | [SIE information litige](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%9B%EF%B8%8F%20Administrations/%E2%9C%89%EF%B8%8F%20SIE%20-%20Signalement.md) | Aucune preuve d'expédition |
| 16 | [Conseil Départemental ERP](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%9B%EF%B8%8F%20Administrations/%E2%9C%89%EF%B8%8F%20Conseil%20D%C3%A9partemental%20-%20Signalement.md) | Aucune preuve d'expédition |
| 17 | [CPAM recours tiers](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%A5%20CPAM/%E2%9C%89%EF%B8%8F%20CPAM%20-%20Recours%20Tiers%20-%20Saisine.md) | Aucune preuve d'expédition |
| 18 | [SDIS sécurité ERP](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%9B%EF%B8%8F%20Administrations/%E2%9C%89%EF%B8%8F%20SDIS%20-%20Signalement.md) | Aucune preuve d'expédition |
| 19 | [FGTI saisine conservatoire](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%9B%EF%B8%8F%20Justice/%E2%9C%89%EF%B8%8F%20Saisine%20-%20FGTI.md) | Aucune preuve d'expédition |
| 20 | [Relance Police](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%91%AE%20Police/%E2%9C%89%EF%B8%8F%20Police%20-%20Vid%C3%A9os%20-%20Relance.md) | Aucune preuve d'expédition |
| 21 | [Relance CPAM](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%8F%A5%20CPAM/%E2%9C%89%EF%B8%8F%20CPAM%20-%20Relance.md) | Aucune preuve d'expédition |

### 🔴 GABARITS NON TRANSMIS

| N° | Document | Blocage |
|:--:|----------|---------|
| 22 | [Attestation témoin client](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%91%A5%20T%C3%A9moins/%E2%9C%89%EF%B8%8F%20Attestation%20-%20T%C3%A9moin%20Client.md) | Pas de témoin identifié |
| 23 | [Attestation pompier SAMU](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%91%A5%20T%C3%A9moins/%E2%9C%89%EF%B8%8F%20Attestation%20-%20Pompier%20SAMU.md) | Coordonnées pompier inconnues |
| 24 | [Attestation employé](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/%E2%9C%89%EF%B8%8F%20Courriers/%F0%9F%91%A5%20T%C3%A9moins/%E2%9C%89%EF%B8%8F%20Attestation%20-%20Employ%C3%A9.md) | Pas d'employé SAS identifié |

## 5. Sanction

Toute nouvelle erreur de qualification (PROJET qualifié ENVOYÉ sans preuve matérielle) constitue une **faute professionnelle** au sens de la Règle n°14 (vérification sur pièces source) et de la Règle n°15 (avenant nomenclature).

L'agent concerné devra :
1. Identifier et lister tous les fichiers impactés par l'erreur

2. Corriger le statut dans le fichier et dans STATUS.md

3. Signaler la correction dans le prochain commit

---

**Application immédiate** : 10 juillet 2026, 23h00

**Signature** : Rédacteur en chef du dossier Accident de la Main