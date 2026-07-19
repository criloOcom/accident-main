---
title: "TODO ACTION — Synthèse exécutable des 15 rapports Jules (nuit 14/07)"
date: 2026-07-14
description: "Todo-list exécutable extraite des 15 rapports de la nuit Jules 2026-07-14. Actions réalisables par l'agent vs actions nécessitant l'avocat/la victime."
type: rapport
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [📊 Rapports](./README.md) › TODO ACTION 2026-07-14*
<hr>
<!-- /Breadcrumb -->

# TODO ACTION — 15 rapports Jules (14/07/2026)

Todo-list exécutable issue de la synthèse croisée des 15 rapports `RAPPORT_*_2026-07-14.md`.
Légende statuts : ✅ fait | 🔧 en cours | ⏳ à faire (agent) | 👤 à faire par l'avocat/la victime | 🚫 bloqué

<hr><hr>

## I — PRIORITÉ CRITIQUE — SÉCURITÉ / RGPD (R1-R5, reportées : validation séparée)
- ⏳ R1 Corriger `.gitignore` (exclure 👤 Reel/, TOKEN MAP, STRICT VARIABLES)

- ⏳ R2 Purger historique Git (187 fuites résiduelles en clair)

- ⏳ R3 Chiffrer TOKEN MAP.md (GPG/Git-crypt)

- ⏳ R4 Hook pre-commit surveillance identités réelles

- ⏳ R5 Marquer versions 👤 Reel « CONFIDENTIEL / NE PAS DIFFUSER »

<hr><hr>

## II — PRIORITÉ HAUTE — EXACTITUDE DES FAITS (STRICT VARIABLES)
- ✅ R6 Vérifié : aucune date d'accident 29/06 dans les fichiers actuels (les 29/06 sont des dates de LRAR/mises en demeure réelles ; STRICT VARIABLES l.111 note l'erreur de certificat 29/06 déjà connue)

- ✅ R7 Vérifié : `870014140507947` = n° de LR de l'arrêt de travail Dr OXYBEL (réel, vérifié La Poste) — pas « invalide ». Pas de modif.

- ✅ R8 Remplacer 59 600 € par ~126 000 € (avis Dintilhac 13/07) dans INPI J+37

- ✅ R9 Déjà satisfaite : STRICT VARIABLES contient avis Dintilhac 13/07 (126-161k€), 59 600 € marqué obsolète (l.194)

<hr><hr>

## III — PRIORITÉ HAUTE — STRATÉGIE DE RECOURS (immédiat)
- 👤 R10 Assignation référé Art. 145 CPC : forcer communication assurance RC Pro + vidéosurveillance — *acte à déposer par l'avocat*

- 👤 R11 Saisies-conservatoires (Art. L.511-1 CPCE) sur comptes/biens personnels dirigeants — *acte à déposer par l'avocat*

- 👤 R12 Opposition à radiation amiable SAS (Greffe TC, Art. R.123-128) — *acte à déposer par l'avocat*

- 👤 R13 Action IN SOLIDUM systématique (SAS + Président + Directrice Générale, jurispr. SATI) — *à intégrer dans les actes par l'avocat*

<hr><hr>

## IV — PRIORITÉ MOYENNE — RÉDACTION DES ACTES
- 👤 R14 Assignation référé-provision : in solidum dirigeants lisible dans dispositif ; lier chaque préjudice à sa pièce — *recommandation M05 à transmettre à l'avocat (acte non versionné dans le dépôt)*

- 👤 R15 Plainte complémentaire : requalifier sur mise en danger délibérée ; citer L.124-3 C. assur. — *recommandation M05 à transmettre à l'avocat*

- 👤 R16 Réquisitoire : formulation incisive, chefs de mise en examen précis (art. 121-2/121-3 CP) — *recommandation M05 à transmettre à l'avocat*

- 👤 R17 Clarifier distinction faute SAS vs faute personnelle dirigeants (art. L.227-8 C. com.) — *recommandation M05 à transmettre à l'avocat*

<hr><hr>

## V — PRIORITÉ CALENDAIRE — À NE PAS RATER
- 👤 R18 Avant 03/09/2026 : surseoir constitution partie civile (délai 3 mois art. 85 CPP)

- 👤 R19 15/07 : dépôt Aide Juridictionnelle (CERFA 16146*03)

- 👤 R20 Dès assureur : référé-provision art. 835 CPC + expertise art. 232 CPC

- 👤 R21 12/11/2026 13h45 : RdV UMJ CHU Purpan (présence physique victime)

- 👤 R22 Certificat consolidation final (Dr DJERBI)

- 👤 R23 Si AJ refusée : basculer voie pénale

<hr><hr>

## VI — PRIORITÉ MOYENNE — ORGANISATION DÉPÔT
- ✅ R24 Supprimer dossier doublon `status/` (migré vers 🚦 Status/ — aucune perte, vérifié)

- ✅ R25 Nettoyer racine : carnet RDV déplacé vers 🧠 Memory/ (fait cette nuit)

- ⏳ R26 Breadcrumbs manquants dans 📊 Rapports/audit/ et AUDIT_YAML_HEADERS.md — *passe de formatage large, à faire*

- ⏳ R27 `<hr><hr>` manquants avant ## dans 🗂️ Organisation/ — *passe de formatage large, à faire*

<hr><hr>

## VII — PRIORITÉ BASSE — HYGIÈNE TECHNIQUE
- ✅ R28 batch_anonymize.py : correction tokens `**` manquants (conformité double strate, signalé M13) + var.

- ✅ R29 Tests pytest/anonymisation : `.dev/tests/unit/app/test_anonymize.py` (4 tests, 4 OK)

- ✅ R30 I/O de batch_anonymize.py enveloppés dans try/except + message ligne

<hr><hr>

*Généré le 2026-07-14 à partir des 15 rapports Jules. Statuts mis à jour au fil de l'exécution.*
