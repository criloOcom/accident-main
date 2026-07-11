<!-- Breadcrumb -->
[🏠](../../../README.md)
<!-- /Breadcrumb -->

---
title: "Rapport de vérification PIECES MAP"
description: "Date de l'audit :** 2026-07-07"
type: rapport
---

# Rapport de vérification PIECES MAP

**Date de l'audit :** 2026-07-07

## 1. Toute pièce citée dans les conclusions ou actes existe-t-elle bien dans le bordereau ?

**Résultat :** OUI.
Toutes les pièces citées dans les actes de la procédure (Assignations, Constitution de partie civile, dossiers de plaidoirie, etc.) sont bien listées dans les bordereaux.

Les pièces explicitement citées dans le corps des actes sont les **Pièces n°1 à n°10**. Ces 10 pièces figurent toutes dans les deux bordereaux disponibles dans le projet (`04 📑 Bordereau de pieces.md` et `04 📑 Bordereau Audience.md`).

## 2. Y a-t-il des pièces listées mais jamais citées ?

**Résultat :** OUI.
Un grand nombre de pièces listées dans les bordereaux ne sont jamais citées dans le corps des actes.

- Dans le bordereau exhaustif (`04 📑 Bordereau de pieces.md` qui liste 31 pièces), **21 pièces (de la 11 à la 31)** ne sont jamais citées dans le texte des assignations ou conclusions.
- Dans le bordereau d'audience (`04 📑 Bordereau Audience.md` qui liste 25 pièces), **15 pièces (de la 11 à la 25)** ne sont jamais citées.

## 3. Y a-t-il des pièces citées par un numéro qui pointe vers deux documents différents ?

**Résultat :** OUI. PROBLÈME MAJEUR DÉTECTÉ.

Il existe **deux bordereaux distincts** dans le dossier qui possèdent des numérotations asynchrones et conflictuelles.

- `⚖️_Actes/🔑_Token/01_⚖️_Actes_proceduraux/04 📑 Bordereau de pieces.md`
- `⚖️_Actes/🔑_Token/01_⚖️_Actes_proceduraux/04 📑 Bordereau Audience.md`

Dès la Pièce n°1 et de manière flagrante à partir de la Pièce n°6, la correspondance entre le numéro et le document est brisée.

| N° Pièce | Document selon `Bordereau de pieces.md` | Document selon `Bordereau Audience.md` |
|:---:|:---|:---|
| **1** | Paiement Wero | Procès-verbal de police |
| **2** | Certificat médical d'urgence | Certificat médical initial |
| **3** | Compte-rendu opératoire | Compte-rendu opératoire |
| **4** | Certificats d'arrêts de travail | Arrêts de travail |
| **5** | Plainte pénale et PV police | Réquisition judiciaire |
| **6** | Dossier RCT CPAM | Paiement Wero |
| **7** | LRAR mise en demeure à la SAS | Facture de pharmacie |
| **8** | LRAR mise en demeure au Président | Facture de chirurgie |
| **9** | LRAR mise en demeure à la DG | Dossier RCT CPAM |
| **10**| LRAR au Propriétaire des Murs | LRAR mise en demeure à la SAS |

**Conséquence :** Les actes procéduraux se basent sur la numérotation du `Bordereau de pieces.md`. Si un juge se réfère au `Bordereau Audience.md`, les références pointeront vers le mauvais document.

## Recommandation
Il est impératif d'unifier la numérotation des pièces. Soit :
1. Aligner le `Bordereau Audience.md` sur la numérotation chronologique du `Bordereau de pieces.md`.
2. Mettre à jour l'ensemble des Assignations et actes pour qu'ils reflètent la numérotation thématique du `Bordereau Audience.md`.
