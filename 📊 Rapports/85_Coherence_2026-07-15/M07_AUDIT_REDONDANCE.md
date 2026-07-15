---
title: "M07 — Audit des Redondances et Contradictions"
description: "Rapport d'audit de la cohérence documentaire : montants Dintilhac, dates, PIECES MAP, tokens."
type: rapport
---

<!-- Breadcrumb -->
*[🏠](../../README.md) › [📊 Rapports](../README.md) › [85 Coherence 2026-07-15](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) › M07 AUDIT REDONDANCE*
<hr>
<!-- /Breadcrumb -->

# M07 — Audit des Redondances et Contradictions

## I — OBJECTIF DE L'AUDIT

Ce rapport identifie les redondances, contradictions et données obsolètes dans les répertoires et actes du projet. Il s'assure que la Source Unique de Vérité (notamment `🧠 Memory/STRICT VARIABLES.md`) est respectée et que les anciens éléments ne polluent pas la cohérence juridique.

<hr><hr>

## II — ANALYSE PAR DOMAINE

### A. Montants Dintilhac et Évaluations Financières

L'évaluation des préjudices a évolué à plusieurs reprises, entraînant des contradictions majeures entre les actes historiques et la Source Unique de Vérité.

* **La Vérité Factuelle** : `🧠 Memory/STRICT VARIABLES.md` (lignes 51 et 226) fixe `TOTAL_ESTIMATIF_GLOBAL_CANONIQUE` à **120 000 – 160 000 €**.
* **Contradiction 1 (Évaluation Initiale 59 600 €)** : L'ancienne évaluation est explicitement déclarée comme obsolète dans `STRICT VARIABLES.md` et dans `⚖️ Actes/🔑 Token/✉️ Courriers/🚨 Signalements/✉️🚨 INPI.md` (ligne 98). Cependant, elle est encore présentée comme l'évaluation de référence ("estimés à 59 600 €") dans :
  * `⚖️ Actes/🔑 Token/🗄️ Archives/🧠 STRATEGIE Contentieux Civil.md`
  * `⚖️ Actes/🔑 Token/🗄️ Archives/🔧 ANALYSE correction juridique.md`
  * `⚖️ Actes/🔑 Token/🗄️ Archives/📚 ANALYSE Jurisprudence.md`
  * `🧠 Memory/STATUS.md` et `🧠 Memory/TODO.md` y font également référence.
* **Contradiction 2 (Évaluation Intermédiaire 109 500 €)** : Cette valeur obsolète persiste dans `⚖️ Actes/🔑 Token/✉️ Courriers/⚖️ Contentieux/✉️ Saisine FGTI.md` (ligne 88) ("s'élève à ~109 500 €") et dans `🧠 Memory/STRICT VARIABLES.md` sous la variable `MONTANT_TOTAL_ESTIME` (ligne 72, notée SUPERSEDED).
* **Contradiction 3 (Évaluation 126 000 € - 161 500 €)** : Plusieurs actes de Référé Provision utilisent un rapport Dintilhac intermédiaire du 13/07/2026 :
  * `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/⚖️ Assignation Refere Provision.md` (ligne 229)
  * `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/🎯 Conclusions Refere Provision.md` (ligne 153)
  * `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/⚖️ Projet Ordonnance Refere.md` (lignes 103, 192)
  * `📊 Rapports/40_Indemnisation_Dintilhac/RAPPORT_AVOCAT_DINTILHAC_20260713.md` (lignes 109, 153)

### B. Dates et Délais (ITT, Procédures)

* **ITT Initiale vs ITT Totale** : La durée de l'Incapacité Totale de Travail (ITT) a été uniformisée à **56 jours** (du 29/05/2026 au 23/07/2026). Ce chiffre est correct et omniprésent.
* **Incohérence documentaire expliquée** : Le document `🧠 Memory/🗂️ Tokens/token-j-55-fin-d-itt.md` (ligne 32) explique de manière claire que le certificat médical initial mentionnait "1 jour" par erreur matérielle et que cela a été rectifié à 56 jours. Ce point est géré.
* **Redondance d'échéanciers** : Les listes d'actions et les échéances calendaires se chevauchent entre `🧠 Memory/TODO.md` et `🧠 Memory/STATUS.md` (ex: les actions du 15 juillet 2026), avec de nombreuses duplications sur l'état du "Plan A" ou des "Preuves MATÉRIELLES".

### C. Vérification des Tokens (🔑 Token vs TOKEN MAP.md)

L'audit des tokens via le script a révélé 60 tokens formellement définis dans la `TOKEN MAP.md`. Aucune fuite d'identité réelle n'a été détectée dans le dossier Token lors de cette vérification.
* **Cohérence globale** : Les actes dans `⚖️ Actes/🔑 Token/` utilisent la nomenclature standardisée `**[Nom du Token]**` avec des liens vers les fiches du dossier `🧠 Memory/🗂️ Tokens/`.
* **Information Orpheline** : De vieux tokens obsolètes, tels que `[Finance Evaluation Initiale]`, demeurent mappés dans `TOKEN MAP.md` et dans `STRICT VARIABLES.md` (ligne 227) pour assurer la rétrocompatibilité (marqués "Obsolète").

### D. Organisation PIECES MAP vs Bordereau

* **Système de Numérotation Oboslète** : L'utilisation de "Pièce n°X" est explicitement interdite par la règle 2026-07-02 (`🧠 Memory/DECISIONS.md`). L'identifiant officiel d'une pièce est son triplet `(date, émetteur, objet)`.
* **Contradiction** : Le fichier `🧠 Memory/PIECES MAP.md` alerte bien sur cette règle, mais `📊 Rapports/40_Indemnisation_Dintilhac/RAPPORT_AUDIT_FGTI_DINTILHAC.md` et plusieurs autres anciens actes et READMEs utilisent encore les numéros de pièces statiques du tableur source (ex: Pièce 4, Pièce 10).

<hr><hr>

## III — PLAN DE CORRECTION (TODO)

- [ ] **[CRITIQUE]** Mettre à jour les assignations de référé (`J+32`, `J+39`, `J+63`) pour qu'elles reflètent l'estimation canonique `120 000 - 160 000 €` au lieu de `126 000 - 161 500 €` (Avis du 13/07/2026).
- [ ] **[MAJEUR]** Retirer les mentions de l'ancienne évaluation à 59 600 € dans `STATUS.md`, `TODO.md` et dans les documents du dossier `🗄️ Archives/` (ou insérer une note d'obsolescence en en-tête des archives).
- [ ] **[MAJEUR]** Aligner l'estimation de la Saisine FGTI (`✉️ Saisine FGTI.md`) sur le montant canonique.
- [ ] **[MINEUR]** Purger les doublons de calendrier entre `TODO.md` et `STATUS.md`.
- [ ] **[INFO]** Supprimer ou remplacer les références textuelles de type "Pièce n°X" dans les rapports plus anciens pour suivre la nomenclature en triplet.
