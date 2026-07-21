---
title: "Synthèse — Travaux de cohérence RESTANT à faire (85_Coherence 2026-07-15)"
date: 2026-07-15
description: "Liste agrégée et vérifiée des corrections encore NON appliquées issues des 15 audits de cohérence du 15/07/2026."
type: rapport
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [📊 Rapports et Analyses](./README.md) › 85 RESTANT A FAIRE 2026-07-15*
<hr>
<!-- /Breadcrumb -->

# Synthèse — Ce qui N'A PAS ENCORE ÉTÉ FAIT

> Généré le 15/07/2026 après relecture des 15 rapports de `📊 Rapports/85_Coherence_2026-07-15/` et **vérification dans le dépôt réel**.
>
> **Constat brut :** les 15 rapports détaillés documentent un travail RESTANT, pas un travail déjà effectué.
> Sur 2868 points listés : **2802 sont encore non traités** (cases `[ ]`), seuls 66 sont des étapes de « vérification » ou « conformité constatée » (cases `[x]` dans M06/M14).
>
> **Vérification live effectuée dans le dépôt (preuve que rien n'est corrigé) :**
> - « 29 juin 2026 » (erreur de date, M01/M09) → encore présent dans **47 fichiers**
> - Noms réels dans la strate Token `🔑` (TAVELLA/JARDON/DJERBI/LES MAUVAIS GARÇONS, M05/M08/M09) → encore dans **24 fichiers Token**
> - JURITEXT0000 invalides (M04) → **3** encore présents dans `📜 Lois/EXEMPLES_REQUETES_MCP.md`
> - Hallucination « CHUM TOULOUSE » (M06) → encore dans **2 fichiers**
>
> ⚠️ **Les 15 rapports détaillés (`85_Coherence_2026-07-15/Mxx_*.md`) ne doivent PAS être supprimés tels quels : ils constituent la feuille de route exacte des correctifs.** Cette synthèse les résume ; les listes ligne-par-ligne restent dans chaque Mxx.

<hr><hr>

## I — DATES ERRONÉES (M01 + M09) — 109 points
- M01 : 10 dates à aligner sur la Source Unique de Vérité (`🧠 Memory/STRICT VARIABLES.md`).

- M09 : 99 incohérences (dont « 29 juin » au lieu de « 29 mai », fuites de noms, mécanisme de l'accident).

- **Vérif live :** 47 fichiers contiennent encore « 29 juin 2026 » → non corrigé.

- Détail : `85_Coherence_2026-07-15/M01_AUDIT_DATES.md`, `M09_AUDIT_NARRATIF.md`.

## II — MONTANTS DINTILHAC (M02) — 197 points
- Écarts entre les montants cités (DFP/IP/SE/PEP/Agrément/Total Estimatif…) et les valeurs canoniques de `STRICT VARIABLES.md` (post-expertise 2027).

- Concerne actes procéduraux, courriers, études d'indemnisation, simulations et rapports.

- Détail : `85_Coherence_2026-07-15/M02_AUDIT_MONTANTS.md`.

## III — FONDEMENTS JURIDIQUES / CITATIONS (M03) — 1242 points
- Citations incomplètes (code manquant : « Article 145 du Code de proc »), articles inexistants (ex. 2224 du Code civil), formats d'alinéa.

- Le plus gros lot (1242). Principalement des citations à compléter avec le bon code (CPC / Code civil / Code pénal…).

- Détail : `85_Coherence_2026-07-15/M03_AUDIT_FONDEMENTS_JURIDIQUES.md`.

## IV — JURITEXT INVALIDES (M04) — 444 points
- Identifiants `JURITEXT0000…` inexistants ou mal formatés dans `📜 Lois/` (notamment `EXEMPLES_REQUETES_MCP.md`).

- **Vérif live :** 3 JURITEXT0000 encore présents → non corrigé.

- Règle #11 stricte : ne jamais deviner un JURITEXT, vérifier sur Légifrance.

- Détail : `85_Coherence_2026-07-15/M04_AUDIT_JURITEXT.md`.

## V — DOUBLE STRATE TOKEN/REEL (M05) — 162 points — ✅ VÉRIFIÉ LE 15/07 (pas de fuite dans le TEXTE, noms dans liens/chemins)
- **Vérif live du 15/07 (exécution de la vague 1) :** scan de tous les `.md` de `⚖️ Actes/🔑 Token/`.

  - Les occurrences de JARDON/TAVELLA/DJERBI/LES MAUVAIS GARÇONS/Lafaurie dans le **texte visible** sont inexistantes (déjà tokenisées en visible).
  - Elles apparaissent UNIQUEMENT dans : libellés de lien markdown, métadonnées `reel_path`, breadcrumbs, et noms de fichiers (ex. `🔄 DrDJERBI Consolidation ✉️Mail.md`).
  - **Décision anti-régression :** ne PAS remplacer dans ces zones — renommer un `reel_path` ou un libellé de lien casserait la double strate Token↔Reel (vérifié par accident : un 1er script avait modifié 5 fichiers en cassant les `reel_path` → **annulé via `git checkout`**).
  - `Purpan` dans « Hôpital de Purpan (CHU Toulouse) » = ambigu (hôpital, pas adresse victime) → laissé.
- **Conclusion : M05 ne nécessite AUCUNE correction de texte.** Les « fuites » listées par l'audit sont des faux positifs (comptage naïf incluant URLs/liens/chemins). Zéro régression.

- **Reste à traiter (strate `👤 Reel`) :** tokens non résolus (`**[La Victime]**`, `**[Capital Social de l'Exploitation]**`, dates/J+…) → gérés par `generate_real_versions.py` (ré-générer la strate Reel), PAS par édition manuelle.

- Détail : `85_Coherence_2026-07-15/M05_AUDIT_TOKEN_REEL.md`.

## VI — CONTRE-EXPERTISE MÉDICALE (M06) — 2 actions
- [CRITIQUE] Aucune demande de contre-expertise formulée dans l'assignation.

- [MAJEUR] Hallucination « CHUM TOULOUSE » (inexistant) → remplacer par « CHU de Toulouse » / « UMJ de Toulouse ».

- **Vérif live :** « CHUM TOULOUSE » encore dans 2 fichiers → non corrigé.

- Détail : `85_Coherence_2026-07-15/M06_AUDIT_CONTRE_EXPERTISE.md`.

## VII — REDONDANCES / CONTRADICTIONS (M07) — 5 points
- Évaluations Dintilhac obsolètes (59 600 €, 109 500 €, 126 000–161 500 €) persistant dans actes/archives/rapports au lieu de la canonique 120 000–160 000 €.

- Numérotation « Pièce n°X » interdite (DECISIONS.md) encore utilisée.

- Détail : `85_Coherence_2026-07-15/M07_AUDIT_REDONDANCE.md`.

## VIII — CONSISTANCE INTERNE DES ACTES (M08) — 28 points — ⚠️ PARTIEL (visa corrigé, citations à vérifier)
- **Vérif live + action du 15/07 (Vague 2) :**

  - ✅ **Visa corrigé en toute sûreté** (4 fichiers) : « Vu les articles L. 227-8 **et L. 225-251** du Code de commerce » → « Vu l'article L. 227-8 du Code de commerce ». Pour une **SAS** (Chapitre VII C. com.), le fondement de la responsabilité des dirigeants est **L.227-8**, pas L.225-251 (qui est le régime des SA). Zéro doublon, zéro lien cassé.
    - Fichiers : `Référé - Assignation Provision.md`, `Constitution - Partie Civile.md`, `Requete Art.145 CPC.md`, `✉️ Relance - Dirigeants SAS.md`.
  - ⏸️ **Citations narrative/corps LAISSÉES + FLAGGÉES « À VÉRIFIER »** (5 fichiers, 14 occurrences) : `Référé - Assignation Provision.md` (corps), `Constitution - Partie Civile.md` (corps), `✉️ Courrier - Président SAS.md` (corps), `Note - Plaidoirie Responsabilité Dirigeants.md`, `🗄️ Archives/Archive - Stratégie Contentieux Pénal.md`.
    - **Raison (anti-régression + Règle #11)** : ces occurrences citent le *texte* de l'article ou font un renvoi narratif. Remplacer le numéro seul créerait un mismatch (le texte cité correspond à L.225-251, pas L.227-8). Il faut **vérifier sur Légifrance** que L.227-8 porte le même fondement avant toute modification. Non automatisable → reporté.
- **Fuites Tavella** : voir M05 (vague 1) — aucune fuite visible confirmée, noms seulement dans URLs/noms de fichiers.

- Détail : `85_Coherence_2026-07-15/M08_AUDIT_CONSISTANCE_INTERNE.md`.

## IX — PROCESS / RÈGLES (M10) — 49 points
- Fichiers sans front matter YAML / sans breadcrumb (`🚦 Status/*.md`, `🧠 Memory/CARNET_RDV_UTILISATEUR.md`, plusieurs rapports).

- Séparateurs `<hr><hr>` manquants.

- Détail : `85_Coherence_2026-07-15/M10_AUDIT_PROCESS.md`.

## X — TIMELINE / PROCÉDURE (M11) — 7 points
- [CRITIQUE] Anachronisme : actes datés 07/2026 qui mentionnent consolidation 03/2027 / expertise 05/2027 (Constitution - Partie Civile).

- Détail : `85_Coherence_2026-07-15/M11_AUDIT_PROCEDURE.md`.

## XI — FORMAT / CONVENTIONS (M12) — 520 points
- Dossiers sans emoji, fichiers hors pattern, YAML/breadcrumb manquants (`📜 Jurisprudence/*`, `🚦 Status/*`, rapports…).

- Détail : `85_Coherence_2026-07-15/M12_AUDIT_FORMAT.md`.

## XII — TYPOS / ORTHOGRAPHE (M13) — 22 points (MAJEUR)
- « suite à » → « à la suite de » (26 occurrences MAJEUR listées).

- (Ponctuation/espaces insécables : 1000+ occurrences — normaliser par script, non manuel.)

- Détail : `85_Coherence_2026-07-15/M13_AUDIT_TYPOS.md`.

## XIII — MÉMOIRES / CONCLUSIONS (M14) — 8 points
- [CRITIQUE] Mémoire en défense adverse : montants hallucinés (DFP 31 200 €, IP 30 000 €), URL article 1241 erronée (c'est 1240), dispositif manquant.

- Détail : `85_Coherence_2026-07-15/M14_AUDIT_MEMOIRES.md`.

## XIV — HYPOTHÈSES / SCÉNARIOS DÉFENSE (M15) — 7 points
- Analyse des objections adverses (quantum, causalité, nullité, contradictoire). Travail d'analyse, pas de correction de fichier.

- Détail : `85_Coherence_2026-07-15/M15_AUDIT_HYPOTHESES.md`.

<hr><hr>

## XV — Recommandation

1. **Ne pas supprimer** les 15 rapports détaillés : ils sont la checklist exécutable (2802 items). Les marquer « traités » serait faux — la vérification live prouve le contraire.

2. Traiter par vagues prioritaires : **M05 (fuites PII — CRITIQUE)** → **M01/M09 (dates)** → **M04 (JURITEXT)** → **M08 (L.225-251)** → **M02/M03 (montants + fondements)**.

3. M12/M13/M10 (format/typos) : passer par scripts de normalisation (`.dev/app/normalize_sections.py` existe) plutôt que correction manuelle.

*Ce fichier est vivant : à mettre à jour au fil des correctifs appliqués (cocher les Mxx correspondants).*