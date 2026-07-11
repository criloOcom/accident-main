<!-- [🏠](../README.md) > 📁 [ 📊_Rapports ](..../README.md) > 📁 [ audit ](../README.md) > 📄 [ audit_juritext.md ](.audit_juritext.md) -->

# Rapport d'Audit JURITEXT — Mission M6

**Date :** 10 juillet 2026  
**Périmètre :** `⚖️_Actes/🔑_Token/` (dossiers 01 à 06)  
**Méthode :** Extraction par grep + vérification API `openlegi_get_decision_judiciaire`  
**Protocole :** JURITEXT_PROTOCOL.md

---

## Résumé

- **22 identifiants JURITEXT uniques** extraits et vérifiés
- **20 ✅ valides** (correspondance JURITEXT ↔ numéro pourvoi ↔ contenu)
- **2 ❌ anomalies** dans `05 🎯 Conclusions Refere.md` (numéros de pourvoi erronés)
- **0** JURITEXT introuvable

---

## Tableau de Synthèse

| # | JURITEXT | Pourvoi réel | Chambre | Date | Cité comme | Fichiers | Statut |
|---|----------|-------------|---------|------|-----------|----------|--------|
| 1 | 0007047369 | 99-17.092 | Com. | 20/05/2003 | SATI — 99-17.092 | 9 fichiers (actes, courriers, analyses, études, org.) | ✅ |
| 2 | 0007043704 | 97-17.378 | Ass. Plén. | 25/02/2000 | Costedoat — 97-17.378 | 5 fichiers | ✅ |
| 3 | 0007071351 | 00-82.066 | Ass. Plén. | 14/12/2001 | Cousin — 00-82.066 | 3 fichiers | ✅ |
| 4 | 0007028156 | 90-14.261 | Civ. 2e | 15/05/1992 | 90-14.261 | `01 Assignation.md` | ✅ |
| 5 | 0007037753 | 96-16.128 | Civ. 2e | 19/11/1998 | 96-16.128 | `01 Assignation.md` | ✅ |
| 6 | 0007030228 | 91-11.285 | Com. | 26/01/1993 | 91-11.285 | `04 Bordereau pieces.md` | ✅ |
| 7 | 0007047223 | 02-14.783 | Ass. Plén. | 19/12/2003 | 02-14.783 | `12 Évaluation Dintilhac.md`, `11+12 Éval consolidee.md` | ✅ |
| 8 | 0029014493 | 13-80.849 | Crim. | 27/05/2014 | 13-80.849 | `📚 ANALYSE Jurisprudence.md`, `00 Index.md` | ✅ |
| 9 | 0044482848 | 20-16.463 | Civ. 1re | 08/12/2021 | 20-16.463 | 8 fichiers | ✅ |
| 10 | 0043782126 | 20-15.106 | Civ. 2e | 08/07/2021 | 20-15.106 | 7 fichiers | ✅ |
| 11 | 0049418278 | 22-19.307 | Civ. 2e | 04/04/2024 | 22-19.307 | 8 fichiers | ✅ |
| 12 | 0043489943 | 19-23.173 | Civ. 2e | 06/05/2021 | 19-23.173 | 5 fichiers | ✅ |
| 13 | 0046282365 | 20-20.404 | Com. | 07/09/2022 | 20-20.404 | `01 Assignation.md` | ✅ |
| 14 | 0026432928 | 11-14.339 | Soc. | 26/09/2012 | 11-14.339 | `01 Assignation.md`, `03 Assignation Art 145.md` | ✅ |
| 15 | 0032312857 | 15-15.306 | Civ. 2e | 24/03/2016 | 15-15.306 | `01 Assignation.md` | ✅ |
| 16 | 0036780068 | 17-14.499 | Civ. 2e | 29/03/2018 | 17-14.499 | `12 Évaluation Dintilhac.md`, `11+12 Éval consolidee.md` | ✅ |
| 17 | 0049857400 | 23-15.345 | Civ. 1re | 26/06/2024 | 23-15.345 | `12 Évaluation Dintilhac.md`, `11+12 Éval consolidee.md` | ✅ |
| 18 | 0044105739 | 20-17.263 | Civ. 2e | 09/09/2021 | 20-17.263 | `12 Évaluation Dintilhac.md` | ✅ |
| 19 | 0045822770 | 21-12.478 | Civ. 3e | 11/05/2022 | 21-12.478 | `12 Évaluation Dintilhac.md`, `11+12 Éval consolidee.md`, `15 Note Droit Assurances.md`, `13 Responsabilites legales.md` | ✅ |
| 20 | 0039122827 | 18-13.791 | Civ. 2e | 12/09/2019 | 18-13.791 | `11+12 Éval consolidee.md` | ✅ |
| 21 | 0053859671 | 24-20.972 | Civ. 2e | 02/04/2026 | 24-20.972 | `12 Évaluation Dintilhac.md`, `11+12 Éval consolidee.md` | ✅ |
| 22 | 0021271786 | 08-17.959 | Civ. 2e | 10/11/2009 | 08-17.959 | `12 Évaluation Dintilhac.md`, `11+12 Éval consolidee.md` | ✅ |
| 23 | 0043302280 | 19-25.198 | Com. | 17/03/2021 | 19-25.198 | `Note Conservation Preuves Numeriques.md` | ✅ |
| 24 | 0031988483 | 10-23.378 | Civ. 2e | 04/02/2016 | 10-23.378 | (audit Dintilhac) | ✅ |
| **25** | **0007012425** | **82-13.234** | **Civ. 1re** | **12/07/1983** | **89-18.422** | **`05 Conclusions Refere.md`** | **❌** |
| **26** | **0007006621** | **78-12.440** | **Civ. 1re** | **02/10/1980** | **74-10.466** | **`05 Conclusions Refere.md`** | **❌** |

---

## Anomalies Détectées

### ANOMALIE 1 — `05 🎯 Conclusions Refere.md` (ligne 85)

**Cité comme :** Arrêt n° 89-18.422, Cour de cassation, 2e chambre civile, 13 février 1991  
**Lien :** `JURITEXT000007012425`  
**Réalité API :** Pourvoi **82-13.234**, Cour de cassation, **Chambre civile 1**, **12 juillet 1983** — REJET (coopérative agricole, obligation de résultat)

**Problème :** L'URL JURITEXT ne pointe pas vers l'arrêt 89-18.422 attendu mais vers un arrêt sans rapport de 1983.  
**Risque :** La citation juridique sur la responsabilité du fait des choses (échelle qui bascule) n'est pas étayée par la décision réelle pointée.

### ANOMALIE 2 — `05 🎯 Conclusions Refere.md` (ligne 93)

**Cité comme :** Arrêt n° 74-10.466, Cour de cassation, 2e chambre civile, 5 mai 1975  
**Lien :** `JURITEXT000007006621`  
**Réalité API :** Pourvoi **78-12.440**, Cour de cassation, **Chambre civile 1**, **2 octobre 1980** — REJET (mandat immobilier, nullité vente)

**Problème :** L'URL JURITEXT ne pointe pas vers l'arrêt 74-10.466 attendu mais vers un arrêt sans rapport de 1980.  
**Risque :** La citation sur le vice inhérent non exonératoire n'est pas étayée par la décision réelle pointée.

---

## Anomalies Historiques (déjà corrigées)

Les anomalies suivantes, identifiées dans des audits précédents, sont **déjà corrigées** dans les fichiers `🔑_Token` actuels :

| Ancien JURITEXT (faux) | Nouveau JURITEXT (correct) | Pourvoi | Source |
|---|---|---|---|
| 000044515079 | 000044105739 | 20-17.263 | `jurisprudence_hallucinations_report.md` |
| 000036835776 | 000036780068 | 17-14.499 | `jurisprudence_hallucinations_report.md` |
| 000049914357 | 000049857400 | 23-15.345 | `jurisprudence_hallucinations_report.md` |
| 000045683755 | 000045822770 | 21-12.478 | `jurisprudence_hallucinations_report.md` |
| 000046284523 | 000046282365 | 20-20.404 | `jurisprudence_hallucinations_report.md` |
| 000028994017 | 000029014493 | 13-80.849 | `jurisprudence_hallucinations_report.md` |
| 000007152625 | 000007047369 | 99-17.092 (SATI) | `jurisprudence_hallucinations_report.md` |
| 000043514489 | 000044482848 | 20-16.463 | `jurisprudence_hallucinations_report.md` |
| 000006485532 | 000007047223 | 02-14.783 | `jurisprudence_hallucinations_report.md` |
| 000007043322 | 000007071351 | 00-82.066 (Cousin) | `jurisprudence_hallucinations_report.md` |
| 000007043831 | 000007043704 | 97-17.378 (Costedoat) | `jurisprudence_hallucinations_report.md` |
| 000050460532 | 000049418278 | 22-19.307 | `jurisprudence_hallucinations_report.md` |
| 000033127860 | 000039122827 | 18-13.791 | `jurisprudence_hallucinations_report.md` |

---

## Statistiques par Dossier

| Dossier | Nb occurrences | Toutes vérifiées ? |
|---------|:------------:|:------------------:|
| `01_⚖️_Actes_proceduraux/` | 14 | ❌ (2 anomalies dans `05 Conclusions Refere.md`) |
| `02_✉️_Courriers/` | 8 | ✅ |
| `03_📚_Analyses_juridiques/` | 11 | ✅ |
| `04_💰_Etudes_indemnisation/` | 16 | ✅ |
| `05_🗂️_Organisation/` | 8 | ✅ |
| `06_🗄️_Archives/` | 12 | ✅ |

---

## Recommandations

1. **Correction prioritaire** : Remplacer les JURITEXT dans `05 🎯 Conclusions Refere.md` :
   - Ligne 85 : Remplacer `JURITEXT000007012425` par le JURITEXT correct correspondant à **89-18.422** (Civ. 2e, 13 février 1991)
   - Ligne 93 : Remplacer `JURITEXT000007006621` par le JURITEXT correct correspondant à **74-10.466** (Civ. 2e, 5 mai 1975)
2. **Recherche complémentaire** : Utiliser Judilibre ou la recherche Légifrance pour trouver les JURITEXT corrects des deux arrêts manquants, qui traitent de la responsabilité du fait des choses.
3. **Vérification post-correction** : Re-exécuter le script `check_consistency.py` après correction.
