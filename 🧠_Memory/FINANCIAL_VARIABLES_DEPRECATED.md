---
title: "⚠ DÉPRÉCIÉ — VARIABLES FINANCIÈRES (voir STRICT VARIABLES.md)"
description: "Ce fichier regroupe l'ensemble des montants financiers (provisions, préjudices Dintilhac, astreintes et dépens) pour le dossier de **[La Victime]**. Ces valeurs sont la référence unique du projet pour toutes les substitutions."
type: memory
---


<!-- Breadcrumb -->
[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › FINANCIAL VARIABLES DEPRECATED
<!-- /Breadcrumb -->

# ⚠ DÉPRÉCIÉ — VARIABLES FINANCIÈRES

**Ce fichier est déprécié.** La Source Unique de Vérité est désormais `STRICT VARIABLES.md`, qui contient une section "Correspondance tokens financiers alternatifs `[Finance ...]`" reprenant l'intégralité de ce contenu.

Conserver pour archive uniquement — ne plus utiliser.

---

## 1. PROVISIONS ET DÉPENS DE RÉFÉRÉ

| Variable financière | Jeton associé | Montant | Description |
| :--- | :--- | :--- | :--- |
| **MONTANT_PROVISION_REFERE** | `[Finance Provision Référé]` | **15 000 €** | Provision réclamée au juge des référés |
| **MONTANT_ARTICLE_700** | `[Finance Article 700]` | **3 000 €** | Indemnité réclamée au titre de l'article 700 du CPC |
| **MONTANT_ASTREINTE_145** | `[Finance Astreinte 145]` | **150 €** | Astreinte journalière pour la production de l'assurance |
| **MONTANT_ARTICLE_700_145** | `[Finance Article 700 Référé 145]` | **1 500 €** | Indemnité réclamée pour la procédure article 145 CPC |
| **MONTANT_ARTICLE_475_1** | `[Finance Article 475-1]` | **3 000 €** | Indemnité réclamée au tribunal correctionnel (pénal) |

---

## 2. POSTES DE PRÉJUDICE (NOMENCLATURE DINTILHAC - COMPROMIS RECOMMANDÉ)

Ces valeurs correspondent aux estimations raisonnables de réparation du préjudice corporel de la victime (totalisant **85 000 €**).

| Poste de préjudice (Dintilhac) | Jeton associé | Montant | Détails |
| :--- | :--- | :--- | :--- |
| **(PGPA) Pertes de gains pros actuels** | `[Finance PGPA]` | **1 380 €** | Basé sur 56 jours d'ITT et 750 €/mois de CA |
| **(DFP) Déficit fonctionnel permanent** | `[Finance DFP]` | **25 000 €** | Taux estimé à 10% avant consolidation définitive |
| **(SE) Souffrances endurées** | `[Finance Souffrances Endurées]` | **15 000 €** | Niveau évalué à 4/7 |
| **(IP) Incidence professionnelle** | `[Finance Incidence Professionnelle]` | **30 000 €** | Dévalorisation et aménagement ergonomique |
| **Préjudice d'Agrément** | `[Finance Préjudice Agrément]` | **5 000 €** | Privation de guitare et codage de loisirs |
| **(PEP) Préjudice esthétique permanent** | `[Finance Préjudice Esthétique]` | **3 000 €** | Cicatrice palmaire visible de 8,5 cm |
| **(DEP) Dévalorisation professionnelle** | `[Finance Dévalorisation Pro]` | **3 000 €** | Perte de compétitivité sur le marché |
| **Frais Divers / Médicaux** | `[Finance Frais Divers]` | **3 000 €** | Déplacements, kinésithérapie, médecin-conseil |

---

## 3. FACTURES ET CRÉANCES DIVERSES

| Variable financière | Jeton associé | Montant | Émetteur |
| :--- | :--- | :--- | :--- |
| **FACTURE_CHIRURGIE** | `[Finance Facture Chirurgie]` | **790,23 €** | Clinique de l'Union (Chirurgien SOS Main) |
| **WERO_PRESTATION** | `[Finance Prestation Salon]` | **15,00 €** | Paiement initial (remboursé par le salon) |