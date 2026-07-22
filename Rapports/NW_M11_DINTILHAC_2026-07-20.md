---
title: "NW_M11_DINTILHAC_2026-07-20"
type: preuve
date: "2026-07-20"
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [Rapports](./README.md)*
<hr>
<!-- /Breadcrumb -->

# RAPPORT D'ÉVALUATION FINANCIÈRE DINTILHAC — MISSION NIGHT WATCH M11

**Date :** 2026-07-20
**Objet :** Vérification du calcul Dintilhac, croisement avec STRICT VARIABLES et audit de cohérence

## 1. Chargement de la skill
✅ **Skill `accident-main-dintilhac-eval`** : Les règles d'évaluation Dintilhac ont été intégrées (Méthode BIBAL pour l'IP, points Mornet pour le DFP, barème indicatif pour SE).

## 2. Référentiel Canonique (`Memory/STRICT VARIABLES.md`)
Conformément au §1 (Rapport d'expertise 2027-05-29), les valeurs de référence absolues sont :
- **DFP (12%) :** 25 200 €

- **SE (4/7) :** 14 000 €

- **IP :** 28 000 €

## 3. Audit des fichiers dans `Etudes_indemnisation/`

### 3.1. `Note - Évaluation Dintilhac Consolidée.md`
- **Statut :** **INCOHÉRENCES MAJEURES DÉTECTÉES**

- **DFP :** Le document mentionne de multiples scénarios historiques (31 200 € à 12%, 25 000 € à 8%, et un compromis retenu à 25 000 € pour 10%). Ces montants sont **SUPERSEDED** par le rapport d'expertise (25 200 €).

- **SE :** Le document mentionne des fourchettes allant de 15 000 € à 30 000 € (et une évaluation à 24 000 € ou 15 000 €) au lieu du montant canonique de 14 000 €.

- **IP :** Le document mentionne 30 000 € (méthode BIBAL 27.5) et d'autres scénarios (16 200 €), alors que le montant canonique est 28 000 €.

### 3.2. `Protocole%20-%20Transactionnel%20Dintilhac%2013-07-2026.md`
- Ce document cite le "Rapport d'Évaluation Indemnitaire du 13 juillet 2026", qui précède l'expertise. Il utilise des montants provisionnels et fait référence à des scénarios prudents/médians, ce qui est normal pour un document pré-expertise, mais doit être lu à l'aune des variables strictes si une mise à jour est requise.

## 4. Audit des Conclusions au Fond (`TJ Foix - Conclusions au Fond.md`)
- **Statut :** **COHÉRENT**

- **DFP :** Mentionne correctement "25 200 €" (12 %).

- **SE :** Mentionne correctement "14 000 €" (4/7).

- **IP :** Mentionne correctement "28 000 €" (méthode BIBAL : 9 000 × 12 % × coeff 25 = 27 000 €, retenu à 28 000 €).

- Les conclusions sont alignées avec `STRICT VARIABLES.md`.

## 5. Audit des Conclusions Référé Provision (`TJ Foix - TJ Foix - Référé Provision - Conclusions.md`)
- **Statut :** **COHÉRENT (Phase provisoire)**

- Le document demande une provision de 15 000 €, ce qui est justifié et cohérent avec `STRICT VARIABLES.md` (MONTANT_PROVISION_AMIABLE: 15 000 €).

## 6. Synthèse et Recommandations
- Les **Conclusions au fond** et les **Preuves (Rapport d'expertise)** sont parfaitement alignées avec le référentiel.

- Les documents dans `Etudes_indemnisation/` reflètent les évaluations *pré-expertise*. Bien que ces documents aient une valeur historique, il convient de s'assurer qu'aucun nouveau calcul ne se base sur ces scénarios "SUPERSEDED".

### Actions correctives recommandées
- Mettre à jour l'en-tête de `Note - Évaluation Dintilhac Consolidée.md` (Token et Reel) pour indiquer clairement que les montants sont caducs et renvoyer vers le rapport d'expertise de 2027 et `STRICT VARIABLES.md` (§1).

- Maintenir la vigilance sur les copies de ces évaluations (rapports d'avocats, rapports internes) qui pourraient encore citer 31 200 € (DFP) ou 30 000 € (IP).
