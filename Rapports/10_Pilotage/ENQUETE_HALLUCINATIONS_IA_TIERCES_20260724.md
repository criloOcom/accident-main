---
uid: EnqGem24X
title: "Enquête — Hallucinations et erreurs factuelles des IA tierces (Gemini) — 24/07/2026"
description: "Diagnostic des causes des erreurs factuelles commises par les agents IA tiers (Gemini, Gems, conseil), questionnaire d'audit à leur soumettre, et protocole de vaccination pour empêcher la récidive"
type: rapport
date: "2026-07-24"
tags:
- audit

- IA tierces

- hallucinations

- vaccination
---
<!-- Breadcrumb -->
*[🏠](../../README.md) › [Rapports](../README.md) › [10 Pilotage](./README.md) › ENQUETE HALLUCINATIONS IA TIERCES 20260724*
<hr>
<!-- /Breadcrumb -->

# ENQUÊTE<br>Hallucinations des IA tierces (Gemini) — Diagnostic, Questionnaire, Vaccination

## I — INVENTAIRE DES ERREURS FACTUELLES CONSTATÉES (corpus daté)

| # | Date | Erreur commise par l'IA tierce | Vérité du dépôt (source) |
|---|------|-------------------------------|--------------------------|
| E1 | 23/07 | « Statuts LRAR récupérés » présentés avant confirmation officielle | Relevé La Poste = seule source ([Memory/STRICT VARIABLES.md](../../Memory/STRICT%20VARIABLES.md)) |
| E2 | 23/07 | « PV complémentaire mentionne déjà le TPT » | Faux au moment dit — mis à jour seulement au commit 83606aad |
| E3 | 23/07 | « Bordereau inclut déjà les pièces 53-55 » | Faux au moment dit — fait au commit 83606aad |
| E4 | 23/07 | LRAR SORROCHE présentée comme distribuée | Toujours « en cours de transport » (relevé La Poste 23/07) |
| E5 | 24/07 | « gérance M. [L'Ancien Président de l'Exploitation] et M. [Le Président de l'Exploitation] » ([L'Exploitant du Commerce (La SAS)]) | [L'Ancien Président de l'Exploitation] = ancien président de LES MAUVAIS GARÇONS, aucun lien avec [L'Exploitant du Commerce (La SAS)] |
| E6 | 24/07 | ~~« [L'Exploitant du Commerce (La SAS)] immatriculée le 19 mai 2026 »~~ **RETIRÉE 24/07 : Gemini avait raison.** L'attestation RNE (pièce du 17/07) porte bien « Date d'immatriculation au RNE : 19/05/2026 » ET « Début d'activité : 22/04/2026 ». Notre STRICT VARIABLES confondait les deux dates — corrigé. | Attestation RNE/INPI ([pièce HB Barber](../../Actes/Preuves_officielles/20260716_💈_HB_Barber/20260717_Export_Portail_Data_HB_BARBERpdf.md)) |
| E7 | 24/07 | « WhatsApp distribué/lu sans réponse » | Ligne validée : « distribué à 16h01, sans réponse » — AUCUNE spéculation sur la lecture |
| E8 | 24/07 | ~~« accident à 15h20 »~~ **RETIRÉE 24/07 : Gemini avait raison sur la source.** Le PV de police n° 2026/015967 mentionne « Le 29/05/2026 à 15:20 » comme horodatage officiel du fait ; la déclaration établit paiement Wero 15h20 → retour < 5 min → accident (~15h25). Le « 15h00 » de STRICT VARIABLES était l'approximation — corrigé. | PV n° 2026/015967 ([pièce Police](../../Actes/Preuves_officielles/20260602_Police_PV/20260602_PV_Police_PV_n°2026-015967_AccidentSalonCoiffure.md)) |
| E9 | 24/07 | Conseil d'envoyer « les yeux fermés » la Relance 3 au bailleur | Courrier DÉJÀ ENVOYÉ le 19/07 (LRAR 87500152910287Q), DISTRIBUÉ le 23/07 |
| E10 | 24/07 | « aucun lien mort dans ses références » (Relance 3) | 3 notes de bas de page recyclent le même LEGIARTI pour 3 articles différents |

## II — DIAGNOSTIC : LES 6 CAUSES PROBABLES

1. **Absence d'accès au dépôt en temps réel (cause n° 1).** Gemini ne lit pas GitHub à chaque réponse : il raisonne sur des extraits collés dans la conversation, souvent périmés de plusieurs commits. E2, E3, E9 sont des erreurs de FRAÎCHEUR : il décrit un état passé (ou souhaité) comme actuel. Symptôme typique : il « valide » des choses qu'il n'a pas pu lire.

2. **Confusion d'entités proches (cause n° 2).** Deux SAS successives au même endroit, deux dirigeantes au nom composé proche ([La Directrice Générale de l'Exploitation] / [La Directrice Générale de l'Exploitation]), deux présidents. Sans fiche d'identité par entité sous les yeux, le modèle fusionne les entités (E5). C'est l'hallucination la plus dangereuse pour les documents transmis aux autorités.

3. **Complaisance de validation (cause n° 3).** Les IA conversationnelles tendent à confirmer et embellir (« tout est impeccablement synchronisé », « prêt à l'envoi », « aucun lien mort ») plutôt qu'à vérifier. Une « validation » sans preuve d'accès à la source est une décoration, pas un audit (E3, E10).

4. **Reconstruction plausible des chiffres et dates (cause n° 4).** Quand une date/heure précise manque du contexte fourni, le modèle en génère une plausible (19 mai ≈ proche du 29 mai ; 15h20 = heure Wero vue ailleurs). E6, E8.

5. **Glissement sémantique cumulatif (cause n° 5).** « Distribué » devient « distribué/lu » (E7), « récupéré » (E1) : à chaque reformulation, le modèle intensifie légèrement. Sur un dossier juridique, chaque glissement est une faille exploitable par la partie adverse.

6. **Absence de notion de statut de cycle de vie des documents (cause n° 6).** Le modèle ne distingue pas projet / envoyé / distribué (E9) s'il ne lit pas le champ YAML `statut:` et le registre LRAR. Il évalue un texte « dans l'absolu » comme s'il était encore à envoyer.

## III — QUESTIONNAIRE D'AUDIT À SOUMETTRE À GEMINI

À coller tel quel. Exiger des réponses précises, sans flatterie, question par question.

1. Quand tu affirmes qu'un fichier du dépôt contient X, as-tu réellement LU le contenu du fichier au moment de ta réponse, ou déduis-tu son contenu de notre conversation ? Réponds pour chacune de tes 3 dernières validations.

2. Quel est le hash du dernier commit que tu as réellement consulté ? Quelle est la date de ta dernière lecture effective du dépôt ?

3. D'où as-tu tiré l'affirmation « [L'Exploitant du Commerce (La SAS)] immatriculée le 19 mai 2026 » ? Cite ta source exacte (fichier + ligne, ou pièce). Si tu ne peux pas la citer, explique comment ce chiffre est apparu dans ta réponse.

4. D'où as-tu tiré « gérance M. [L'Ancien Président de l'Exploitation] » pour [L'Exploitant du Commerce (La SAS)] ? Quelle pièce du dossier relie [L'Ancien Président de l'Exploitation] à [L'Exploitant du Commerce (La SAS)] ? (Réponse attendue : aucune.) Pourquoi as-tu fusionné deux sociétés distinctes ?

5. Avant de me conseiller d'envoyer la Relance 3 au bailleur, as-tu vérifié le champ `statut:` de son YAML frontmatter et le registre LRAR de STRICT VARIABLES ? Si non, pourquoi as-tu émis un conseil d'action sans vérifier l'état du document ?

6. Quand tu écris « aucun lien mort dans ses références », quel contrôle as-tu effectué concrètement ? Peux-tu me lister les 10 URL de bas de page de ce courrier ? (S'il ne peut pas : la « validation » était inventée.)

7. Pourquoi as-tu écrit « distribué/lu » alors que la ligne actée du dossier est « distribué, sans spéculation sur la lecture » ? Où as-tu vu « lu » ?

8. Quelle est, selon toi, l'heure exacte de l'accident, et quelle est ta source ? (Test : STRICT VARIABLES dit 15h00 ; 15h20 = Wero.)

9. Sur une échelle explicite, quel est ton niveau de certitude pour chaque affirmation factuelle de ta dernière réponse ? Es-tu capable de marquer « NON VÉRIFIÉ » quand tu n'as pas la source ?

10. Que proposes-tu comme protocole personnel pour ne plus jamais : (a) valider un fichier non lu, (b) fusionner deux entités, (c) intensifier un statut (distribué→lu), (d) conseiller une action sur un document déjà envoyé ?

## IV — PROTOCOLE DE VACCINATION (mesures côté dépôt et côté échanges)

**V1 — En-tête de contexte daté obligatoire.** Tout message envoyé à une IA tierce commence par un bloc : `ÉTAT DU DÉPÔT : commit <hash> du <date> — toute connaissance antérieure est périmée`. L'IA doit répéter ce hash dans sa réponse.

**V2 — Fiche d'identité des entités (anti-E5/E6).** Coller systématiquement le bloc « FAITS IMMUABLES » (section V ci-dessous) dans chaque nouvelle conversation tierce. Ne jamais laisser l'IA reconstruire les dirigeants de mémoire.

**V3 — Règle « source ou silence ».** Exiger de l'IA tierce : toute affirmation factuelle (date, statut, contenu de fichier) doit citer sa source (fichier, pièce, message daté) ou être marquée `[NON VÉRIFIÉ]`. Une réponse sans marquage est réputée non fiable.

**V4 — Interdiction de valider sans lecture.** Les formules « tout est à jour », « conforme », « prêt » sont interdites à une IA qui n'a pas lu les fichiers dans le tour courant. Elle doit dire : « je ne peux pas le vérifier, demande à Hermès ».

**V5 — Statut de cycle de vie en tête de courrier (anti-E9).** Avant tout conseil d'envoi, l'IA doit citer le champ `statut:` du YAML et la ligne LRAR correspondante de STRICT VARIABLES.

**V6 — Vocabulaire postal verrouillé (anti-E1/E7).** Seuls termes admis : « pris en charge », « en cours de transport », « avis de réception numérique disponible / distribué le JJ/MM », « en instance », « sans réponse à ce jour ». Les mots « lu », « récupéré », « réceptionné et accepté » sont interdits sauf preuve dédiée.

**V7 — Contre-audit systématique par Hermès.** Toute réponse d'IA tierce contenant des faits est vérifiée contre le dépôt AVANT intégration ou action (règle déjà appliquée — la maintenir). L'utilisateur ne déclenche aucune action matérielle (envoi, impression, déplacement) sur seul avis d'une IA sans accès au dépôt.

## V — BLOC « FAITS IMMUABLES » À COLLER AUX IA TIERCES

```
FAITS IMMUABLES (source : Memory/STRICT VARIABLES.md — interdiction de les reconstruire de mémoire) :
- Accident : 29/05/2026 vers 15h20-15h30 (PV police : « à 15:20 » ; paiement Wero 15h20 puis retour < 5 min), 22 Rue Lafaurie, 09000 Foix.
- Victime : informaticien indépendant (SIREN 500 474 457). AUCUNE autre profession.
- Exploitant au 29/05/2026 : [L'Exploitant du Commerce (La SAS)], SIREN 104 103 262 — début d'activité 22/04/2026, immatriculation RNE 19/05/2026 (deux dates distinctes, ne pas confondre).
  Président : [Le Président de l'Exploitation]. DG : [La Directrice Générale de l'Exploitation] (ép. [La Directrice Générale de l'Exploitation]).
- Ancien exploitant (parti le 10/03/2026) : SAS LES MAUVAIS GARÇONS, SIREN 938 033 222.
  Président : [L'Ancien Président de l'Exploitation]. [L'Ancien Président de l'Exploitation] n'a AUCUN rôle chez [L'Exploitant du Commerce (La SAS)].
- ITT totale : 55 jours (29/05 → 23/07/2026). TPT : 24/07 → 23/08/2026 (Dr Prisca AKUÉ).
- CPAM RCT : n° 31727387. PV police : n° 2026/015967.
- WhatsApp témoin : distribué le 18/07/2026 à 16h01, SANS réponse. Ne jamais écrire « lu ».
- Relance 3 bailleur : DÉJÀ ENVOYÉE (LRAR 87500152910287Q, 19/07), DISTRIBUÉE le 23/07. Ne pas conseiller son envoi.
```
