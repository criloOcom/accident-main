<!-- Breadcrumb -->
[🏠](../../../README.md)
<!-- /Breadcrumb -->

---
title: "Rapport d'Audit — LEGIARTI des courriers 03 à 34"
description: "Mission M4** | **Date :** 10/07/2026 | **Auditeur :** Agent ADK"
type: rapport
---

# Rapport d'Audit — LEGIARTI des courriers 03 à 34

**Mission M4** | **Date :** 10/07/2026 | **Auditeur :** Agent ADK

---

## Résumé des constats

- **Articles vérifiés :** 17 LEGIARTI sur 8 codes
- **Conformes :** 11
- **Anomalies :** **5 anomalies graves dont 2 erreurs de fond**
- **Non vérifiables :** 1 (API Légifrance indisponible pour certaines consultations directes)

---

## 1. Vérifications conformes (✅)

| Article | LEGIARTI | Code | Statut | Source |
|---|---|---|---|---|
| Art. 1719 | LEGIARTI000020459127 | Code civil | VIGUEUR | Courrier 03 |
| Art. 1720 | LEGIARTI000006442784 | Code civil | VIGUEUR | Courrier 03 |
| Art. 145 | LEGIARTI000051869339 | CPC | VIGUEUR | Courrier 03 |
| L.124-3 | LEGIARTI000017735449 | Code des assurances | VIGUEUR | Courriers 05/06 |
| L.225-251 | LEGIARTI000006226329 | Code de commerce | VIGUEUR | Courrier 03 |
| L.2212-4 | LEGIARTI000006390155 | CGCT | VIGUEUR | Courrier 06 |
| L.252 | LEGIARTI000006316012 | LPF | VIGUEUR | Courrier 06 |
| L.274 | LEGIARTI000042914471 | LPF | VIGUEUR | Courrier 06 |
| R.123-128 | LEGIARTI000039278214 | Code de commerce | VIGUEUR | Courrier 30 |
| L.113-2 | LEGIARTI000035731302 | Code des assurances | VIGUEUR | Courriers 05/06* |
| L.227-1 | LEGIARTI000048535177 | Code de commerce | VIGUEUR | Courrier 06* |

> *Ces articles sont cités sans LEGIARTI dans les courriers — le LEGIARTI ci-dessus correspond à la version VIGUEUR constatée par la recherche Légifrance.

---

## 2. Anomalies constatées (🔴)

### ANOMALIE 1 — Courrier 03 (et 06) : Texte erroné pour L.227-8 C.com.

**Citation dans le courrier :**
> « Les administrateurs et le directeur général sont responsables individuellement ou solidairement selon le cas, envers la société ou envers les tiers, soit des infractions aux dispositions législatives ou réglementaires applicables aux sociétés anonymes, soit des violations des statuts, soit des fautes commises dans leur gestion. »

**LEGIARTI cité :** LEGIARTI000006227036 ✅ (correct pour L.227-8)

**Texte réel de L.227-8 (VIGUEUR) :**
> « Les règles fixant la responsabilité des membres du conseil d'administration et du directoire des sociétés anonymes sont applicables au président et aux dirigeants de la société par actions simplifiée. »

**Conclusion :** Le texte cité est celui de **L.225-251** (responsabilité des administrateurs de SA), pas de L.227-8 (SAS). Le LEGIARTI est correct mais **le texte ne correspond pas à l'article**. Erreur de fond.

**Gravité :** 🟠 Élevée — le texte cité change le sens juridique (L.227-8 est un article de renvoi, L.225-251 est un article de fond).

---

### ANOMALIE 2 — Courriers 05 et 06 : Chemin complet erroné pour L.124-3 C.assur.

**Chemin complet cité dans le courrier :**
> Code des assurances > Partie législative > Livre Ier : Le contrat > Titre Ier : Règles communes aux assurances de dommages et aux assurances de personnes > **Chapitre II : Le fonds de garantie des victimes des actes de terrorisme et d'autres infractions** > Section 1 : Dispositions générales

**Chemin complet réel (LEGIARTI000017735449) :**
> Partie législative > Livre Ier : Le contrat > **TITRE II : Les assurances de dommages non maritimes > CHAPITRE IV : Les assurances de responsabilité**

**Conclusion :** Le chemin complet place L.124-3 dans le mauvais chapitre (Fonds de garantie au lieu d'Assurances de responsabilité). L'article lui-même est correct, mais la localisation dans le plan du code est erronée.

**Gravité :** 🟡 Modérée — n'affecte pas le contenu juridique mais rend la navigation confuse.

---

### ANOMALIE 3 — Courrier 31 : L.123-5-1 — Texte et LEGIARTI ne correspondent pas

**Citation dans le courrier :**
> « Le ministère public peut, dans un délai de deux mois à compter de la publication de l'immatriculation, former opposition à celle-ci par exploit d'huissier de justice lorsque l'immatriculation a été indûment obtenue par des moyens frauduleux. »

**LEGIARTI cité :** LEGIARTI000039278086 (consulter_article retourne erreur 500 API)

**Texte réel de L.123-5-1 VIGUEUR (LEGIARTI000006219291) :**
> « A la demande de tout intéressé ou du ministère public, le président du tribunal, statuant en référé, peut enjoindre sous astreinte au dirigeant de toute personne morale de procéder au dépôt des pièces et actes au registre du commerce et des sociétés auquel celle-ci est tenue par des dispositions législatives ou réglementaires. »

**Conclusion :** Le texte cité ne correspond **absolument pas** au contenu de L.123-5-1. Le texte cité (opposition du ministère public à l'immatriculation) semble provenir d'un article différent (possiblement d'un article du même chapitre ou d'un texte aujourd'hui abrogé). LEGIARTI000039278086 n'est pas le LEGIARTI VIGUEUR.

**Gravité :** 🔴 Critique — l'article et le texte sont totalement déconnectés.

---

### ANOMALIE 4 — Courrier 31 : R.123-143 — Texte et LEGIARTI ne correspondent pas

**Citation dans le courrier :**
> « Tout déposant au greffe peut, sur justification d'un intérêt légitime et après en avoir informé le ministère public, former opposition à une inscription ou à un dépôt. »

**LEGIARTI cité :** LEGIARTI000039868542 (consulter_article retourne erreur 500 API)

**Texte réel de R.123-143 VIGUEUR (LEGIARTI000006257574) :**
> « La décision de refus d'immatriculation ou d'enregistrement de modifications statutaires prise par le greffier en application du deuxième alinéa de l'article R. 123-95 peut être contestée dans le délai de quinze jours à compter de sa notification. »

**Conclusion :** Le texte cité ne correspond absolument pas au contenu de R.123-143. Le LEGIARTI du courrier semble pointer soit vers un article abrogé, soit vers un article différent.

**Gravité :** 🔴 Critique — l'article et le texte sont totalement déconnectés.

---

### ANOMALIE 5 — Courrier 06 : L.227-1 — LEGIARTI version antérieure

**LEGIARTI cité :** LEGIARTI000006227041

**LEGIARTI VIGUEUR :** LEGIARTI000048535177 (version 9.0, en vigueur depuis le 01/01/2025)

**Conclusion :** LEGIARTI000006227041 est une version antérieure de l'article L.227-1. L'article a été modifié en dernier lieu par l'ordonnance n°2023-1142 du 6 décembre 2023, entrée en vigueur le 1er janvier 2025. Selon la date de rédaction du courrier, cela peut être normal ou constituer une absence de mise à jour.

**Gravité :** 🟡 Faible si courrier rédigé avant 2025 ; 🟠 Modérée si postérieur.

---

## 3. Observations complémentaires

### Articles cités sans LEGIARTI

Les articles suivants sont mentionnés dans les courriers sans référence LEGIARTI :

| Article | Code | Courrier |
|---|---|---|
| Art. 222-19 | Code pénal | 05 |
| Art. 222-20 | Code pénal | 05 |
| Art. 40 | Code procédure pénale | 05, 33 |
| Art. 85 | Code procédure pénale | 05, 33 |
| Art. 88 | Code procédure pénale | 05 |
| Art. 706-3 | Code procédure pénale | 33 |
| Art. 56-1 | Code procédure pénale | 33 |
| Art. 202 | Code procédure civile | 03 |
| Art. 835 | Code procédure civile | 33 |
| L.311-1 | CRPA | 05 |
| L.4321-1 | Code du travail | 05 |
| L.4121-1 | Code du travail | 05 |
| L.8221-1 | Code du travail | 06 |
| L.8221-5 | Code du travail | 06 |
| L.8271-1-2 | Code du travail | 06 |
| R.4121-1 | Code du travail | 06 |
| R.4323-58 | Code du travail | 05 |
| L.310-1-1-2 | Code des assurances | 05 |
| L.123-1 | Code construction/habitation | 33 |
| L.376-1 | Code sécurité sociale | 33 |
| L.252-5 | Code de la santé publique | 33 |

### R.123-128 (Courrier 30) — Conforme

Texte cité et article réel sont en concordance parfaite. ✅

### API Legifrance

L'API `consulter_article` (consultation directe par LEGIARTI) a retourné une erreur 500 persistante pour plusieurs identifiants. Les vérifications ont été effectuées via `rechercher_code` (par numéro d'article + nom du code) qui fonctionne correctement.

---

## 4. Recommandations

1. **ANOMALIES 3 et 4 (critiques)** : Corriger immédiatement les textes de L.123-5-1 et R.123-143 dans le courrier 31. Identifier les articles réels correspondant aux textes cités (probablement des articles différents du même code).

2. **ANOMALIE 1 (élevée)** : Remplacer le texte de L.227-8 par le texte correct (article de renvoi vers les règles de la SA).

3. **ANOMALIE 2 (modérée)** : Corriger le chemin complet de L.124-3 dans les courriers 05 et 06.

4. **ANOMALIE 5 (modérée)** : Vérifier si le courrier 06 a été rédigé avant le 01/01/2025. Si oui, mettre à jour le LEGIARTI.

5. **Renvois sans LEGIARTI** : Ajouter les LEGIARTI pour tous les articles cités afin de garantir la traçabilité et la pérennité des références juridiques.

---

*Rapport généré par l'agent ADK — Mission M4*
