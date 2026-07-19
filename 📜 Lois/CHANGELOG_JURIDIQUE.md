---
title: "CHANGELOG JURIDIQUE"
date: FIXME
description: "Suivi des modifications apportées aux fiches juridiques (articles et jurisprudence)."
type: loi
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [⚖️ Bibliothèque Juridique](./README.md) › CHANGELOG JURIDIQUE*
<hr>
<!-- /Breadcrumb -->

# CHANGELOG JURIDIQUE

## 2026-07-13 — Correction et mise à jour extensive

### Articles de loi — Corrections

| Fichier | Modification | Raison |
|---|---|---|
| `📒 Code penal/Article_434-4_CodePenal_Legifrance.md` | **Réécriture complète.** Texte + contexte + jurisprudence remplacés. Ancien texte erroné : "refus de remettre un acte" (2 ans, 30k€) → texte officiel : "obstacle à la manifestation de la vérité" (3 ans, 45k€) | Le fichier contenait le texte d'un article complètement différent. LEGIARTI `006418608` était correct dans le YAML mais le corps ne correspondait pas. |
| `📒 Code penal/Article_434-15_CodePenal_Legifrance.md` | **Réécriture complète.** Texte + contexte + jurisprudence remplacés. Ancien texte erroné : "destruction/dégradation de biens" (2 ans, 30k€) → texte officiel : "subornation de témoin" (3 ans, 45k€). Footnote `LEGIARTI000006417900` supprimée (ID inexistant). | Double erreur : corps faux + footnote pointant vers un LEGIARTI introuvable. |
| `📒 Code penal/Article_434-15-1_CodePenal_Legifrance.md` | YAML + text vérifiés | OK — aucune modification nécessaire |
| `📒 Code procedure penale/Article_706-3_CodeProcedurePenale_Legifrance.md` | YAML + corps : `LEGIARTI000006577625` → `LEGIARTI000048442345` | Mise à jour vers version en vigueur depuis nov. 2023 |
| `📒 Code commerce/Article_L227-1_Code_Legifrance.md` | YAML : `LEGIARTI000047591332` → `LEGIARTI000048535177` | Mise à jour vers version en vigueur |
| `📒 Autres codes/Article_223-1_Code_Legifrance.md` | **Remplissage du placeholder.** Texte officiel + contexte + jurisprudence ajoutés | Fichier en "À VÉRIFIER" ; LEGIARTI `LEGIARTI000024042637` vérifié OK |
| `📒 Autres codes/Article_L611-3_Code_Legifrance.md` | **Remplissage du placeholder.** Texte officiel + contexte ajoutés | Fichier en "À VÉRIFIER" ; LEGIARTI `LEGIARTI000044052542` vérifié OK |
| `📒 Autres codes/Article_L123-2_Code_Legifrance.md` | **Remplissage du placeholder.** Texte officiel + contexte ajoutés | Fichier en "À VÉRIFIER" ; LEGIARTI `LEGIARTI000051752672` vérifié OK |

### Jurisprudence — Corrections

| Fichier | Modification | Raison |
|---|---|---|
| `📜 Jurisprudence/🏛️ Action directe et obligation d'assurance/19-15.659_CourCassation.md` | YAML + README : signalé comme RNSM non publié (pas de JURITEXT). Avertissement ajouté dans le corps. Date corrigée (14 mai → 28 mai 2020) et description | Arrêt classé sous mauvais thème (URSSAF, pas action directe). Non publié (ECLI:FR:CCASS:2020:C210277). Usage indicatif seulement. |
| `📜 Jurisprudence/17-26.282_CourCassation.md` | Marquée NON TROUVÉ — pourvoi inexistant dans Judilibre | 0 résultats, même en recherche relaxée, toutes chambres confondues |

### README — Corrections

| Fichier | Modification |
|---|---|
| `📜 Lois/README.md` | LEGIARTI mis à jour pour 434-15-1 (L76), 706-3 (L86), L227-1 (L97). Mermaid J2 : "Arrêt 17-26.282" → "17-26.282 ⚠️ non trouvé". Description 19-15.659 corrigée. Footnote `[^1]` de vérification ajoutée. |
| `📜 Jurisprudence/README.md` | 19-15.659 documenté (RNSM). 17-26.282 marqué non trouvé. Footnote `[^1]` de vérification ajoutée. |
| `📜 Jurisprudence/🏛️ Action directe et obligation d'assurance/README.md` | Date 19-15.659 corrigée (14 mai → 28 mai 2020). Description corrigée ("Action directe contre l'assureur" → "Rejet RNSM URSSAF") |

### Méthode

- **Outils utilisés :** MCP Légifrance-prod, OpenLegi, Judilibre

- **Vérifications croisées :** LEGIARTI/JURITEXT contrôlés sur Légifrance via API

- **Articles non vérifiables au moment de l'audit :** Aucun (l'API Litige est revenue entre-temps)

---

## 2026-07-11 — Création initiale de l'inventaire juridique

- Inventaire complet des 27 articles et 27 arrêts dans `📜 Lois/`

- Compilation des anomalies (10 signalées)

- Soumission à l'agent "chargé de doc" pour revue