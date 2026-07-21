---
title: "M06 — Audit de la Contre-Expertise Médicale"
date: FIXME
description: "Vérification de la cohérence de la stratégie de contre-expertise médicale au sein du dossier (demande, contestation, honoraires, localisation)."
type: rapport
---
<!-- Breadcrumb -->
*[🏠](../../README.md) › [📊 Rapports et Analyses](../README.md) › [🎯 Audits de Cohérence et Conformité](./README.md) › M06 AUDIT CONTRE EXPERTISE*
<hr>
<!-- /Breadcrumb -->

# M06 — Audit de la Contre-Expertise Médicale

## I — Demande de contre-expertise dans l'assignation
- [x] **Vérification :** La demande de contre-expertise est-elle formulée dans l'assignation ?

- **Statut :** **CRITIQUE**

- **Constat :** FICHIER `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/📜 Contentieux civil/Refere Assignation Provision.md` (et autres fichiers de l'assignation) ne mentionne aucune demande de contre-expertise. L'assignation sollicite uniquement une **expertise médicale** judiciaire initiale (sur le fondement de l'article 145 du CPC) mais ne formule pas de demande de *contre-expertise*.

- **Note :** La mention d'une éventuelle contre-expertise apparaît uniquement de manière anticipée dans l'évaluation des Frais Divers (`⚖️ Actes/🔑 Token/💰 Etudes indemnisation/📊 Evaluation Dintilhac Consolidee.md`, ligne 114 et `📊 Rapports/40_Indemnisation_Dintilhac/20260708_Rapport_Baremique_Dintilhac.md`, ligne 44) pour un montant provisionné dans la demande globale, mais pas formellement sollicitée dans l'assignation.

<hr><hr>

## II — Motifs de contestation et conclusions de l'expertise UMJ
- [x] **Vérification :** Les motifs de contestation sont-ils cohérents avec les conclusions de l'expertise UMJ ?

- **Statut :** **MINEUR**

- **Constat :** Dans `🧠 Memory/🗂️ Tokens/token-j-167-expertise-umj.md`, il est indiqué qu'une contre-expertise "peut être sollicitée si les conclusions sont contestées". Cependant, l'expertise UMJ n'a lieu que le 12 novembre 2026, et l'expertise judiciaire civile n'a lieu que le 29 mai 2027 (`⚖️ Actes/🔑 Token/📂 Preuves officielles/20270529 ⚖️ Rapport Expertise Médicale.md`). Aucune contestation n'est formellement documentée dans les actes actuels puisque les expertises sont soit futures (par rapport à la date de référence juillet 2026), soit simulées comme favorables (le rapport de mai 2027 conclut à 12% DFP et une IP majeure, ce qui correspond aux attentes prudentes/médianes de la victime).

<hr><hr>

## III — Honoraires de l'expert
- [x] **Vérification :** Les honoraires mentionnés sont-ils cohérents avec les barèmes en vigueur ?

- **Statut :** **INFO**

- **Constat :** Les honoraires d'expertise médicale sont mentionnés dans les conclusions au fond (`⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/📜 Contentieux civil/Conclusions au Fond TJ Foix.md`, ligne 257) pour un montant de **1 000 €**. Ce montant est réaliste pour une expertise médicale judiciaire classique en nomenclature Dintilhac, bien qu'il s'agisse de frais de l'expertise initiale et non spécifiquement d'une contre-expertise. Dans `📊 Evaluation Dintilhac Consolidee.md`, une enveloppe globale de 3 000 € de Frais Divers est demandée pour couvrir "kinésithérapie 3x/semaine, déplacements, frais dossier, contre-expertise éventuelle".

<hr><hr>

## IV — Choix du cabinet expert (CHUM TOULOUSE)
- [x] **Vérification :** Le cabinet expert choisi (CHUM TOULOUSE) est-il cohérent avec la localisation géographique ?

- **Statut :** **MAJEUR**

- **Constat :** L'entité "CHUM TOULOUSE" **N'EXISTE PAS** dans la documentation. Toulouse possède un CHU (Centre Hospitalier Universitaire), pas un CHUM (Centre Hospitalier de l'Université de Montréal). De plus, aucune recherche dans l'ensemble des fichiers ne retourne de mention de "CHUM TOULOUSE" ou "CHUM".
Cependant, l'expertise UMJ est bien prévue à **Toulouse** (`⚖️ Actes/🔑 Token/📂 Preuves officielles/📁 Preparation Expertise UMJ.md`), ce qui est cohérent avec la localisation de la victime (`⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/👮 Contentieux penal/PV Audition Plainte Complementaire Foix.md`). L'expert judiciaire désigné (Dr X) est inscrit près la Cour d'appel de Toulouse (`20270529 ⚖️ Rapport Expertise Médicale.md`), également cohérent. L'acronyme "CHUM TOULOUSE" fourni dans la demande est une hallucination.

<hr><hr>

## V — Délais et calendrier de procédure
- [x] **Vérification :** La contre-expertise a-t-elle un impact sur le calendrier de procédure ?

- **Statut :** **INFO**

- **Constat :** Inconnu en l'état. Aucune contre-expertise n'ayant été formellement demandée ni ordonnée à ce stade, il n'y a pas d'impact documenté sur le calendrier de procédure existant (`⚖️ Actes/🔑 Token/🗂️ Organisation/📅 Calendrier Procedure.md`).

<hr><hr>

## VI — TODO Actions Correctives
- [ ] Mettre à jour l'assignation en référé si une provision spécifique pour frais de médecin-conseil (assistance à expertise/contre-expertise) doit y figurer expressément.

- [ ] Supprimer ou corriger toute référence externe à "CHUM TOULOUSE" (hallucination) pour la remplacer par "CHU de Toulouse" ou "UMJ de Toulouse" selon le contexte approprié.