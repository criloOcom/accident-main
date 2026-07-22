---
uid: pd9GxJ5vQ
title: CHANGELOG JURIDIQUE
date: 2026-07-21
description: Suivi des modifications apportées aux fiches juridiques (articles et jurisprudence).
type: loi
subtitle: CHANGELOG JURIDIQUE
objective: Analyser CHANGELOG JURIDIQUE
summary: Suivi des modifications apportées aux fiches juridiques (articles et jurisprudence).
key_points:
  - 2026-07-21 — Enrichissement jurisprudence (11 décisions + 2 docs stratégiques)
  - 2026-07-20 — Création des 3 derniers articles manquants (Phase 4)
  - 2026-07-13 — Correction et mise à jour extensive
  - 2026-07-11 — Création initiale de l'inventaire juridique
tags:
  - rapport
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [⚖️ Lois](./README.md)*
<hr>
<!-- /Breadcrumb -->

# CHANGELOG JURIDIQUE

## 2026-07-21 — Enrichissement jurisprudence (11 décisions + 2 docs stratégiques)

### Arrêts Cour de cassation (4)

| RG | Chambre | Date | Thème | Source |
|----|---------|------|-------|--------|
| 80-16.679 | Civ. 1re | 10 mars 1982 | Prescription action directe (L.124-3) | Légifrance ✅ |
| 20-23.462 | Civ. 2e | 24 nov. 2022 | Action directe subrogatoire CPAM | Légifrance ✅ |
| 20-22.100 | Civ. 2e | 24 nov. 2022 | Champ FGAO | Légifrance ✅ |
| 20-19.288 | Civ. 2e | 24 nov. 2022 | Exclusion FGAO accidents corporels | Légifrance ✅ |

**Dossier** : `Action_directe_et_obligation_d'assurance/` (4→8 arrêts)

### Décisions CA/TJ (7)

| RG | Juridiction | Date | Thème | Source |
|----|-------------|------|-------|--------|
| 11/03512 | CA Toulouse | 18 juin 2013 | Lien causal ERP | Doctrine.fr (pas Légifrance) |
| 15/01748 | CA Chambéry | 3 mai 2016 | Obligation de sécurité ERP | Doctrine.fr |
| 19/08999 | TJ Nanterre | 7 janv. 2025 | Transaction sans aggravation | Doctrine.fr |
| 20/05541 | TJ Rennes | 20 janv. 2026 | Incidence professionnelle | Doctrine.fr |
| 21/04988 | TJ Versailles | 23 mai 2024 | Réserve d'aggravation | Doctrine.fr |
| 22/02447 | TJ Nanterre | 18 sept. 2024 | Devoir d'information | Doctrine.fr |
| 22/01019 | CA Versailles | 14 mai 2025 | Prescription action directe | Doctrine.fr |

**Dossier** : `Jurisprudence_du_fond_(CA-TJ)/` (nouveau dossier — 7 décisions)

### Documents stratégiques (2)

- `Mémoire_de_synthèse_—_Recours_assurances_ERP.md` (277 lignes, 6 sections) — Synthèse transversale

- `Note_—_Procédure_Action_Directe_Assureur_L124-3.md` (358 lignes, 9 sections) — Feuille de route procédurale

**Dossier** : `Analyses_juridiques/` — versions Reel générées

### Limitations

- RG des décisions CA/TJ non indexés dans l'API Légifrance → textes intégraux indisponibles via MCP

- 4 arrêts Cass. vérifiés via legifrance-prod ✅

- Mention `À VÉRIFIER` dans fichiers CA/TJ

---

## 2026-07-20 — Création des 3 derniers articles manquants (Phase 4)

| Fichier | Action | LEGIARTI vérifié |
|---|---|---|
| `Code_commerce/Article_L123-5-1_Codecommerce.md` | Création — Art. L.123-5-1 C.com (injonction dépôt RCS) | LEGIARTI000006219291 ✅ VIGUEUR |
| `Code_commerce/Article_L123-3_Codecommerce.md` | Création — Art. L.123-3 C.com (injonction immatriculation/radiation RCS) | LEGIARTI000025559422 ✅ VIGUEUR |
| `Code_du_travail/Article_L8221-1_CodeTravail.md` | Création — Art. L.8221-1 C.trav (interdiction travail dissimulé) | LEGIARTI000006904815 ✅ VIGUEUR |

### README — Mises à jour

| Fichier | Modification |
|---|---|
| `Code_commerce/README.md` | L.123-3 corrigé (lien vers fichier correct) + L.123-5-1 ajouté |
| `Code_du_travail/README.md` | L.8221-1 ajouté |
| [Lois/README.md](README.md) | Code du travail ajouté à la structure + listing (6 articles). Code commerce : 8→13 articles. L.123-3, L.123-5-1 ajoutés. |

### Méthode

- Vérification via OpenLegi (Légifrance-prod API 500). Tous VIGUEUR.

- Les 15 articles manquants de l'audit complet (2026-07-11) sont désormais tous créés. ✅

---

## 2026-07-13 — Correction et mise à jour extensive

### Articles de loi — Corrections

| Fichier | Modification | Raison |
|---|---|---|
| `Code penal/Article_434-4_CodePenal_Legifrance.md` | **Réécriture complète.** Texte + contexte + jurisprudence remplacés. Ancien texte erroné : "refus de remettre un acte" (2 ans, 30k€) → texte officiel : "obstacle à la manifestation de la vérité" (3 ans, 45k€) | Le fichier contenait le texte d'un article complètement différent. LEGIARTI `006418608` était correct dans le YAML mais le corps ne correspondait pas. |
| `Code penal/Article_434-15_CodePenal_Legifrance.md` | **Réécriture complète.** Texte + contexte + jurisprudence remplacés. Ancien texte erroné : "destruction/dégradation de biens" (2 ans, 30k€) → texte officiel : "subornation de témoin" (3 ans, 45k€). Footnote `LEGIARTI000006417900` supprimée (ID inexistant). | Double erreur : corps faux + footnote pointant vers un LEGIARTI introuvable. |
| `Code penal/Article_434-15-1_CodePenal_Legifrance.md` | YAML + text vérifiés | OK — aucune modification nécessaire |
| `Code procedure penale/Article_706-3_CodeProcedurePenale_Legifrance.md` | YAML + corps : `LEGIARTI000006577625` → `LEGIARTI000048442345` | Mise à jour vers version en vigueur depuis nov. 2023 |
| `Code_commerce/Article_L227-1_Code_Legifrance.md` | YAML : `LEGIARTI000047591332` → `LEGIARTI000048535177` | Mise à jour vers version en vigueur |
| `Autres_codes/Article_223-1_Code_Legifrance.md` | **Remplissage du placeholder.** Texte officiel + contexte + jurisprudence ajoutés | Fichier en "À VÉRIFIER" ; LEGIARTI `LEGIARTI000024042637` vérifié OK |
| `Autres_codes/Article_L611-3_Code_Legifrance.md` | **Remplissage du placeholder.** Texte officiel + contexte ajoutés | Fichier en "À VÉRIFIER" ; LEGIARTI `LEGIARTI000044052542` vérifié OK |
| `Autres_codes/Article_L123-2_Code_Legifrance.md` | **Remplissage du placeholder.** Texte officiel + contexte ajoutés | Fichier en "À VÉRIFIER" ; LEGIARTI `LEGIARTI000051752672` vérifié OK |

### Jurisprudence — Corrections

| Fichier | Modification | Raison |
|---|---|---|
| `Jurisprudence/Action_directe_et_obligation_d'assurance/19-15.659_CourCassation.md` | YAML + README : signalé comme RNSM non publié (pas de JURITEXT). Avertissement ajouté dans le corps. Date corrigée (14 mai → 28 mai 2020) et description | Arrêt classé sous mauvais thème (URSSAF, pas action directe). Non publié (ECLI:FR:CCASS:2020:C210277). Usage indicatif seulement. |
| `Jurisprudence/17-26.282_CourCassation.md` | Marquée NON TROUVÉ — pourvoi inexistant dans Judilibre | 0 résultats, même en recherche relaxée, toutes chambres confondues |

### README — Corrections

| Fichier | Modification |
|---|---|
| [Lois/README.md](README.md) | LEGIARTI mis à jour pour 434-15-1 (L76), 706-3 (L86), L227-1 (L97). Mermaid J2 : "Arrêt 17-26.282" → "17-26.282 ⚠️ non trouvé". Description 19-15.659 corrigée. Footnote `[^1]` de vérification ajoutée. |
| `Jurisprudence/README.md` | 19-15.659 documenté (RNSM). 17-26.282 marqué non trouvé. Footnote `[^1]` de vérification ajoutée. |
| `Jurisprudence/Action_directe_et_obligation_d'assurance/README.md` | Date 19-15.659 corrigée (14 mai → 28 mai 2020). Description corrigée ("Action directe contre l'assureur" → "Rejet RNSM URSSAF") |

### Méthode

- **Outils utilisés :** MCP Légifrance-prod, OpenLegi, Judilibre

- **Vérifications croisées :** LEGIARTI/JURITEXT contrôlés sur Légifrance via API

- **Articles non vérifiables au moment de l'audit :** Aucun (l'API Litige est revenue entre-temps)

---

## 2026-07-11 — Création initiale de l'inventaire juridique

- Inventaire complet des 27 articles et 27 arrêts dans [Lois](README.md)

- Compilation des anomalies (10 signalées)

- Soumission à l'agent "chargé de doc" pour revue