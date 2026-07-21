---
title: "RAPPORT D'AUDIT FGTI / DINTILHAC"
date: FIXME
description: "Date :** 10 juillet 2026"
type: rapport
---
<!-- Breadcrumb -->
*[🏠](../../README.md) › [Rapports et Analyses](../README.md) › [40_Indemnisation_Dintilhac — Indemnisation et barèmes](./README.md) › RAPPORT AUDIT FGTI DINTILHAC*
<hr>
<!-- /Breadcrumb -->

# RAPPORT D'AUDIT FGTI / DINTILHAC

**Date :** 10 juillet 2026
**Objet :** Vérification de cohérence des montants Dintilhac et du courrier FGTI
**Périmètre :** 8 fichiers audités (4 token + 4 reel) + 2 fichiers Memory + rapports existants

---

## I — SYNTHÈSE DES INCOHÉRENCES DÉTECTÉES

| # | Gravité | Description | Impact |
|---|---------|-------------|--------|
| 1 | **ALERTE** | Le courrier FGTI utilise les valeurs **optimistes** (~105k€) alors que le compromis interne est ~85-92k€ | Risque de sur-promesse au FGTI |
| 2 | **ALERTE** | Erreur terminologique : "Pretium doloris (PEP)" dans le courrier FGTI — Pretium doloris = Souffrances Endurées (SE), pas PEP | Confusion entre postes |
| 3 | **MOYEN** | Addition des postes du courrier FGTI = ~107 500 € (ou 104 500 € sans DEP), mais le total annoncé est ~105 000 € | Approximation comptable |
| 4 | **MOYEN** | PGPA = 1 900 € dans le courrier FGTI vs 1 380 € dans le compromis | Incohérence de montant |
| 5 | **MOYEN** | DFP = 31 200 € dans le courrier FGTI vs 25 000 € dans le compromis | Incohérence de montant |
| 6 | **MOYEN** | SE = 24 000 € dans le courrier FGTI vs 15 000 € dans le compromis | Incohérence de montant |
| 7 | **MOYEN** | Agrément = 8 000 € dans le courrier FGTI vs 5 000 € dans le compromis | Incohérence de montant |
| 8 | **LÉGER** | Frais divers = 2 000 € dans le courrier FGTI vs 3 000 € dans le compromis | Incohérence de montant |
| 9 | **LÉGER** | ATP (2 000 €) absent du courrier FGTI | Poste manquant |
| 10 | **INFO** | README du dossier 04 obsolète (mentionne 59 600 € seulement) | Documentation non à jour |

---

## II — AUDIT POSTE PAR POSTE — TABLEAU DE CONCORDANCE

| Poste Dintilhac | Doc 11 (Optimiste) | Doc 12 (Optimiste) | Doc 11+12 (Compromis) | Courrier FGTI (19) | FINANCIAL_VARIABLES_DEPRECATED.md | STRICT_VARIABLES.md | Rapport barémique | **Statut** |
|----------------|-------------------|-------------------|----------------------|-------------------|----------------------|-------------------|------------------|-----------|
| PGPA | 1 900 € | 1 900 € | **1 380 €** | **1 900 €** | 1 380 € | 1 900 € | 1 380 € | **INCOHÉRENT** (FGTI utilise l'optimiste) |
| DFT | 1 400 € | 1 400 € | 1 400 € | 1 400 € | (absent) | 1 400 € | 1 400 € | ✅ Cohérent |
| DFP | 31 200 € | 31 200 € | **25 000 €** | **31 200 €** | 25 000 € | 31 200 € | 25 000 € | **INCOHÉRENT** (FGTI utilise l'optimiste) |
| SE (4/7) | 24 000 € | 24 000 € | **15 000 €** | **24 000 €** | 15 000 € | 24 000 € | 15 000 € | **INCOHÉRENT** (FGTI utilise l'optimiste) |
| IP | 30 000 € | 30 000 € | 30 000 € | 30 000 € | 30 000 € | 30 000 € | 30 000 € | ✅ Cohérent |
| Agrément | 8 000 € | 8 000 € | **5 000 €** | **8 000 €** | 5 000 € | 8 000 € | 5 000 € | **INCOHÉRENT** (FGTI utilise l'optimiste) |
| PEP | 3 000 € | 3 000 € | 3 000 € | 3 000 € | 3 000 € | 3 000 € | 3 000 € | ✅ Cohérent |
| DEP | *(absent)* | *(absent)* | 3 000 € | 3 000 € | 3 000 € | 3 000 € | 3 000 € | ✅ Cohérent |
| ATP | *(absent)* | *(absent)* | 2 000 € | **ABSENT** | (absent) | (absent) | (absent) | **MANQUANT** dans courrier FGTI |
| Frais divers | 2 000 € | 2 000 € | **3 000 €** | **2 000 €** | 3 000 € | 2 000 € | 3 000 € | **INCOHÉRENT** (FGTI utilise valeur basse) |
| Art. 700 CPC | 4 000 € | 4 000 € | **3 000 €** | 3 000 € | 3 000 € | 3 000 € | 3 000 € | ✅ Cohérent (FGTI utilise compromis) |
| **TOTAL** | **~105 000 €** | **~105 000 €** | **~92 000 €** | **~105 000 €** | **~85 000 €** | **~105 000 €** | **~85-90 000 €** | **INCOHÉRENT** |

---

## III — ANALYSE DÉTAILLÉE

### III.1 — 3.1 Incohérence structurelle : optimiste vs compromis

Le dossier contient **3 niveaux d'évaluation** qui ne sont pas clairement départagés :

| Niveau | Total | Source |
|--------|-------|--------|
| **Optimiste** (Doc 11, Doc 12) | ~105 000 € | Première analyse, max Dintilhac |
| **Compromis** (Doc 11+12, Rapport barémique) | ~92 000 € | Après intégration analyse Glose |
| **FINANCIAL_VARIABLES** | ~85 000 € | Source unique de vérité financière |

Le courrier FGTI utilise le niveau **optimiste** (~105 000 €) mais avec des valeurs qui ne correspondent exactement ni à l'optimiste ni au compromis.

### III.2 — 3.2 Erreur terminologique critique dans le courrier FGTI

**Section III — INDEMNITES SOLLICITEES :**
```
- Pretium doloris (PEP) : 3 000 €
```

**Problème :** *Pretium doloris* est le terme latin désignant les **Souffrances Endurées (SE)**, pas le Préjudice Esthétique Permanent (PEP). La ligne aurait dû être :
```
- Préjudice Esthétique Permanent (PEP) : 3 000 €
```

Le PEP (cicatrice palmaire 8,5 cm) et les SE (4/7, douleurs neuropathiques, stress post-traumatique) sont DEUX postes distincts. Les confondre dans la nomenclature crée un risque de rejet partiel par le FGTI.

### III.3 — 3.3 Problème d'addition : total annoncé vs total réel

**Courrier FGTI — addition des postes listés :**
1 900 + 1 400 + 30 000 + 31 200 + 24 000 + 8 000 + 3 000 + 2 000 + 3 000 + 3 000 = **107 500 €**

Le total annoncé est **~105 000 €** — un écart de 2 500 €. Si le DEP (3 000 €) est exclu du total : 107 500 - 3 000 = 104 500 €, arrondi à ~105 000 € (acceptable mais imprécis).

### III.4 — 3.4 ITT : 55 ou 55 jours ?

- Tous les documents internes mentionnent **55 jours** (29 mai → 23 juillet 2026) — confirmé par STRICT VARIABLES.md

- La consigne utilisateur mentionne "ITT 55 jours à date"

- **Conclusion :** La valeur interne (55 jours) est cohérente entre tous les documents. Le "55" de l'utilisateur est soit une date de début de mission (J-1), soit une erreur.

### III.5 — 3.5 Incidence professionnelle — vérification

| Critère | Évaluation |
|---------|-----------|
| Méthode BIBAL | ✅ Justifiée (jurisprudence Cass. 2e civ., 2 avril 2026, n° 24-20.972) |
| Calcul : 9 000 × 12% × 27,5 = 29 700 € | ✅ Arithmétiquement correct |
| Arrondi à 30 000 € | ✅ Acceptable |
| Taux de 12% utilisé | ⚠ Même taux que DFP — risque de double compte |
| CA de 9 000 €/an | ⚠ Capitalisation sur 27,5 ans d'un revenu modeste peut être contestée |
| **Conclusion** | **Justifié mais perfectible** — mieux vaudrait documenter que le taux IP est distinct du taux DFP |

### III.6 — 3.6 Comparaison des trois évaluations — écart Glose

Écart entre l'optimiste (105 000 €) et Glose (45 000 €) : **60 000 € (133 %)**.
C'est un écart considérable qui affaiblit la crédibilité de la demande s'il est opposé par le FGTI.

- L'IP est le poste le plus divergent : 30 000 € (BIBAL) vs 2 250 € (Glose) — **×13**

- Un dossier d'expertise médicale solide sera crucial pour justifier l'IP

- Recommandation : préparer une argumentation détaillée sur la méthode BIBAL avec devis d'équipement ergonomique

---

## IV — VÉRIFICATIONS SPÉCIFIQUES

### IV.1 — 4.1 Conditions FGTI (Art. 706-3 CPP)

| Condition | Statut | Preuve |
|-----------|--------|--------|
| Infraction pénale | ✅ | Blessures involontaires (art. 222-19 CP) |
| ITT ≥ 1 mois | ✅ | 55 jours |
| Auteur insolvable | ✅ | Capital 200 € |
| Victime personne physique | ✅ | OK |
| Nationalité française | ✅ | OK |
| Hors Badinter/ONIAM | ✅ | Dans le champ |
| **Conclusion** | **Toutes conditions remplies** | Voie FGTI pleinement ouverte |

### IV.2 — 4.2 Provision référé

| Source | Montant | Détail |
|--------|---------|--------|
| Recommandation interne | 15 000 € | PGPA + frais + SE + IP |
| Glose | 8 000 € | PGPA 1 380 + frais 3 000 + SE 3 000 + art. 700 2 000 |
| Compromis | 15 000 € | Confirmé par rapport barémique |
| **Constat** | **Cohérent** | 15 000 € bien justifié face au capital de 200 € |

### IV.3 — 4.3 FIR (Frais d'Intervention et de Recouvrement) du FGTI

Le FGTI applique un barème de frais pour l'ouverture et la gestion du dossier. Aucun document ne mentionne ce point. À ajouter pour anticiper les déductions éventuelles.

---

## V — RECOMMANDATIONS

### V.1 — 5.1 Priorité haute — corriger le courrier FGTI

1. **Remplacer** la ligne erronée `Pretium doloris (PEP)` par `Préjudice Esthétique Permanent (PEP)`

2. **Ajouter** l'ATP (Assistance Tierce Personne) : 2 000 €

3. **Ajouter** le DFT explicitement listé (déjà présent mais à vérifier)

4. **Corriger** le total additionné pour qu'il corresponde exactement à la somme des postes

5. **Décider** d'un niveau d'évaluation unique (optimiste ou compromis) — recommandation : garder l'optimiste pour le FGTI (stratégie de demande) mais le documenter explicitement comme "estimation haute"

### V.2 — 5.2 Priorité moyenne — harmoniser les sources

6. **Mettre à jour** STRICT VARIABLES.md pour ajouter explicitement les valeurs "compromis" pour tous les postes (comme FINANCIAL_VARIABLES_DEPRECATED.md)

7. **Mettre à jour** le README du dossier 04 pour refléter les 3 niveaux d'évaluation

8. **Ajouter** une mention dans le courrier FGTI précisant "estimation haute sous réserve d'expertise" pour prévenir toute contestation

### V.3 — 5.3 Points de vigilance

9. **Méthode BIBAL** : préparer une note justificative détaillée (devis équipement, jurisprudence, calcul du coefficient 27,5) pour répondre à une éventuelle contestation du FGTI

10. **Double compte IP/DFP** : documenter la distinction entre les deux postes dans la note stratégique

11. **Plafond FGTI** : vérifier si le décret d'application du nouveau plafond FGTI (L.422-7 CA) est applicable (mentionné à 3 000 € dans STRICT VARIABLES.md)

---

## VI — CONCLUSION GLOBALE

| Critère | Note | Commentaire |
|---------|------|-------------|
| Cohérence interne des études Dintilhac | **6/10** | Trois versions (optimiste/compromis/Variables) sans hiérarchie claire |
| Cohérence du courrier FGTI avec les études | **4/10** | Mélange d'optimiste et de compromis + erreur terminologique |
| Justification de l'IP à 30 000 € | **7/10** | Méthode BIBAL solide mais risque de double compte DFP |
| Justification du total ~105 000 € | **6/10** | Addition imprécise (107 500 ≠ 105 000) |
| PGPA pour 55 jours d'ITT | **8/10** | Calcul cohérent (1 380-1 900 €) |
| Conditions FGTI/CIVI | **10/10** | Toutes remplies |
| Provision référé 15 000 € | **9/10** | Bien justifiée |

**L'architecture Dintilhac est solide dans son principe mais souffre d'un manque d'harmonisation entre les fichiers.** La divergence entre les 3 niveaux d'évaluation (optimiste 105k€, compromis 92k€, variables 85k€) doit être tranchée et documentée pour éviter toute contradiction devant le FGTI.