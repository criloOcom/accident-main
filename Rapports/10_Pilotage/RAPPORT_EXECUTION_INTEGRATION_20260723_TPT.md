---
uid: zuXnHsLzU
title: "Rapport d'exécution — Intégration des 3 pièces médicales du 23/07/2026 (temps partiel thérapeutique)"
description: "Rapport d'exécution de la mission d'intégration documentaire : note de suivi Dr AKUÉ, avis de temps partiel thérapeutique 24/07→23/08/2026, compte-rendu de kinésithérapie"
type: rapport
date: 2026-07-23
statut: final
auteur: Hermès (agent)
---
<!-- Breadcrumb -->
*[🏠](../../README.md) › [Rapports](../README.md) › [10 Pilotage](./README.md)*
<hr>
<!-- /Breadcrumb -->

# RAPPORT D'EXÉCUTION<br>INTÉGRATION DES PIÈCES MÉDICALES DU 23 JUILLET 2026

## 1 — Confirmation de lecture des 3 documents

- ✅ **Note de suivi clinique — Dr Prisca AKUÉ** (Centre Médical L'Orangerie, Blagnac, 23/07/2026) : cicatrice propre, fermée, indurée ; flexion MCP index ~120° ; flexion IPP presque complète ; douleurs palpation / hyperextension / flexion. (Scan → OCR tesseract fra.)

- ✅ **Avis d'arrêt de travail (CERFA 10170*08) — temps partiel / travail aménagé pour raison médicale du 24/07/2026 au 23/08/2026**, case « accident causé par un tiers » cochée (29/05/2026). (Scan → OCR.)

- ✅ **Compte-rendu de kinésithérapie détaillé** (A. Teissier, remplaçant de J. Milas, Blagnac — bilan du 25/06/2026 transmis le 23/07/2026) : adhérences cicatricielles, extension MP droite 30° vs 80° à gauche, flexion MP 85°/90°, PSFS 5,0/10, appréhension à la reprise d'effort. (Texte natif.)

## 2 — Fichiers créés

- [Actes/Preuves_officielles/20260723-1730_DrPrisca_NoteDeSuivi/](../../Actes/Preuves_officielles/20260723-1730_DrPrisca_NoteDeSuivi/README.md) (fiche pièce + README, drive_id `1-nd07QdUAjUtusTTYoSOCGiRWgCI95kV`)

- [Actes/Preuves_officielles/20260723-1730_DrPrisca_ArretDeTravail_TempsPartiel/](../../Actes/Preuves_officielles/20260723-1730_DrPrisca_ArretDeTravail_TempsPartiel/README.md) (fiche pièce + README, drive_id `1QTGk0dI16Lo09uqq44iF0heUWyWS3NM7`)

- [Actes/Preuves_officielles/20260723-1544_Kine_CompteRendu/](../../Actes/Preuves_officielles/20260723-1544_Kine_CompteRendu/README.md) (fiche pièce + README, drive_id `1c7I1pepe5FVsGnrAQmeoi2UMLPKKG5ew`)

- [Memory/Tokens/token-medecin-de-suivi.md](../../Memory/Tokens/token-medecin-de-suivi.md) — nouveau token `[Le Médecin de Suivi]` = Dr Prisca AKUÉ

- [Actes/Token/Courriers/CPAM/CPAM_Signalement_TempsPartiel_Therapeutique.md](../../Actes/Token/Courriers/CPAM/CPAM_Signalement_TempsPartiel_Therapeutique.md) (projet de courrier) + version Réel générée via `generate_real_versions.py`

## 3 — Fichiers modifiés

- [Memory/PIECES MAP.md](../../Memory/PIECES%20MAP.md) — pièces **53, 54, 55**

- [Memory/EVIDENCE_MATRIX.md](../../Memory/EVIDENCE_MATRIX.md) — lignes **ACQ-19, ACQ-20, ACQ-21** (avec liens Drive)

- [Memory/STRICT VARIABLES.md](../../Memory/STRICT%20VARIABLES.md) — nouvelle variable `TEMPS_PARTIEL_THERAPEUTIQUE : 24/07/2026 → 23/08/2026`

- [Memory/Mini_Calendrier_Procedure.md](../../Memory/Mini_Calendrier_Procedure.md) — consultation 23/07, début TPT 24/07, jalon fin TPT 23/08 (réévaluation)

- [Memory/CALENDAR_MAP.md](../../Memory/CALENDAR_MAP.md) — 3 lignes (23/07, 24/07, 23/08)

- [Memory/CARNET_RDV_UTILISATEUR.md](../../Memory/CARNET_RDV_UTILISATEUR.md) — RDV kiné 15h00 + consultation Dr AKUÉ 16h15

- [Memory/Tokens/token-j-55-fin-d-itt.md](../../Memory/Tokens/token-j-55-fin-d-itt.md) — section « Suite immédiate — temps partiel thérapeutique »

- [Memory/TOKEN MAP.md](../../Memory/TOKEN%20MAP.md) — entrée `[Le Médecin de Suivi]`

- [.dev/app/batch_anonymize.py](../../.dev/app/batch_anonymize.py) + [.dev/app/generate_real_versions.py](../../.dev/app/generate_real_versions.py) — mapping AKUÉ ↔ `[Le Médecin de Suivi]` (dans les DEUX sens, Règle #3)

- [Rapports/10_Pilotage/FRISE_CHRONOLOGIQUE_MULTI_VOLETS.md](FRISE_CHRONOLOGIQUE_MULTI_VOLETS.md) — ligne « Juillet 2026 (J+55/J+56) », volet médical

- [Rapports/50_Medical/MEMO_EXPERTISE_MEDICALE_VICTIME.md](../50_Medical/MEMO_EXPERTISE_MEDICALE_VICTIME.md) — pièces à réunir pour l'expertise enrichies des 3 documents

- [Rapports/40_Indemnisation_Dintilhac/20260714_RAPPORT_EVALUATION_DINTILHAC.md](../40_Indemnisation_Dintilhac/20260714_RAPPORT_EVALUATION_DINTILHAC.md) — nouvelle **section V — Actualisation du 23/07/2026** (DFT partiel, PGPA, IP, absence de consolidation)

- [Actes/Preuves_officielles/README.md](../../Actes/Preuves_officielles/README.md) et [Actes/Token/Courriers/CPAM/README.md](../../Actes/Token/Courriers/CPAM/README.md) — listings synchronisés

## 4 — Impact sur la chronologie

- **29/05 → 23/07/2026** : arrêt de travail **total** — 55 jours d'ITT (inchangé, `ITT_TOTAL`).

- **24/07 → 23/08/2026** : **temps partiel thérapeutique (travail aménagé)** — 31 jours de reprise partielle. La fin d'ITT n'est PAS une reprise complète : bascule DFT total → DFT partiel, PGPA prolongée au prorata de la réduction d'activité (travailleur indépendant), incidence professionnelle objectivée (poste aménagé, dictée vocale), **absence de consolidation confirmée**.

- **23/08/2026** : jalon de réévaluation médicale (prolongation / reprise complète / consolidation) — ajouté aux calendriers.

## 5 — Contrôles de conformité

- ✅ YAML frontmatter en ligne 1 et parsable sur les 15 fichiers créés/modifiés à frontmatter (vérification `yaml.safe_load` : 15/15 OK), drive_id présents dans les 3 fiches de preuve.

- ✅ Liens internes relatifs : 0 lien mort dans les fichiers nouvellement créés (audit script maison ; 1 lien corrigé dans le courrier CPAM après premier passage).

- ✅ `check_consistency.py` : « Rien à signaler — tout est cohérent. »

- ⚠️ Liens morts **préexistants** (hors périmètre de la mission) : FRISE_CHRONOLOGIQUE_MULTI_VOLETS.md (16, cibles Reel/Token planifiées non encore créées), token-j-55-fin-d-itt.md (2), EVIDENCE_MATRIX.md (1), README CPAM (1). Non introduits par cette mission — à traiter séparément.

- ⚠️ **Google Calendar `[AM]` : événements NON créés** — l'API a refusé (403 « insufficient authentication scopes », le jeton actuel n'a pas le scope Calendar en écriture). Les 3 événements (consultation 23/07, début TPT 24/07, fin TPT 23/08) sont marqués « ⚠️ À CRÉER » dans CALENDAR_MAP.md.

- ℹ️ Aucun commit effectué — en attente du feu vert utilisateur.
