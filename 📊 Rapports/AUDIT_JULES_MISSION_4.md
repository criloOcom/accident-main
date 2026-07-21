---
title: "Rapport d'Audit : Bascule vers la SAS HB BARBER"
description: "Audit des dates et identifiants de la SAS HB BARBER (SIRET, SIREN, date de début d'activité au 22 avril 2026, capital, associés) dans tout le dépôt pour valider la bascule."
type: report
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [📊 Rapports](./README.md) › AUDIT_JULES_MISSION_4*
<hr>
<!-- /Breadcrumb -->

# Rapport d'Audit : Bascule vers la SAS HB BARBER

Ce rapport présente les résultats de l'audit complet du dépôt concernant la bascule des identifiants et dates de l'ancienne entité (SAS LES MAUVAIS GARCONS) vers la nouvelle (SAS HB BARBER).

## 1. Analyse des occurrences de la SAS HB BARBER (Cible)

L'audit révèle que les nouveaux identifiants ont été correctement intégrés dans les générateurs, dictionnaires de tokens et de nombreuses pièces du dossier :

- **SIREN (104 103 262)** : Présent dans `.dev/app/generate_real_versions.py`, `.dev/app/batch_anonymize.py`, `🧠 Memory/TOKEN MAP.md`, et les fiches de tokens (`token-exploitation-hb-siren.md`, etc.).

- **SIRET (104 103 262 00010)** : Présent dans les mêmes fichiers de configuration, ainsi que dans des actes clés comme `⚖️ Assignation Refere Provision.md`, `⚖️ Requete Mandataire Ad Hoc.md` et `✉️ Police Plainte Complementaire ⚖️Contentieux.md`.

- **Capital (1 000 €)** : Correctement paramétré et retrouvé dans les actes civils (référé) et la stratégie du bailleur (`🧠 Memory/Mémo Stratégie Bailleur HB BARBER.md`).

- **Date de début d'activité (22 avril 2026)** : Bien documentée dans `🧠 Memory/STATUS.md`, `🧠 Memory/USER_DOC_SYNTHESE.md`, les fiches tokens et la plainte complémentaire.

- **Dirigeants (Hamza BERGUIGA / Catherine SORROCHE)** : Correctement tokenisés et mentionnés dans les assignations.

## 2. Incohérences et Reliquats de l'ancienne SAS (Les Mauvais Garçons)

Malgré la création des tokens HB BARBER, le système présente d'importants reliquats de l'ancienne entité, particulièrement dans les fichiers de configuration de base et la mémoire canonique :

- **STRICT VARIABLES.md** : Conserve les mentions de l'ancienne entité comme référence principale (capital: 200 €) sans basculer l'ensemble des variables canoniques sur HB BARBER, bien que la plainte complémentaire et le statut précisent l'inactivité de LMG au jour de l'accident.

- **Scripts de génération (.dev/app/)** : Les scripts `anonymize_doc.py`, `consolidate_sheet.py`, `generate_token_files.py` et `batch_anonymize.py` maintiennent des mappings natifs vers l'ancien SIREN `938 033 222` et l'ancien capital `200 €`. L'ancienne SAS est toujours configurée comme « L'Exploitant du Commerce » par défaut.

- **KNOWLEDGE_GRAPH.json et CARNET_RDV_UTILISATEUR.md** : Contiennent toujours l'ancien SIRET `938 033 222 00010` comme référence pour l'accident.

- **Pièces officielles** : Les anciens Kbis, factures et avis INSEE sont évidemment historiques, ce qui est normal, mais les documents de procédure civile et pénale (hormis les compléments récents) visent encore potentiellement l'ancien SIRET par défaut si les tokens `[L'Identifiant de l'Exploitation]` sont utilisés plutôt que les variantes `-hb-`.

## 3. Analyse du risque et Recommandations

L'architecture actuelle maintient une "double vérité" dangereuse :
1. Les anciens tokens (`[L'Exploitant du Commerce (La SAS)]`, `[SIRET de l'Exploitation]`) pointent vers la SAS Les Mauvais Garçons.

2. Les nouveaux tokens (`[Le Nouvel Exploitant (HB BARBER)]`, `[Identifiant du Nouvel Exploitant]`) pointent vers HB BARBER.

**Recommandations pour achever la bascule :**

- [ ] **Mise à jour des scripts de génération** : Remplacer l'ancien SIREN (938 033 222) par le nouveau (104 103 262) et le capital de 200 € par 1 000 € dans `.dev/app/generate_real_versions.py`, `anonymize_doc.py`, et `generate_token_files.py` en tant que valeurs par défaut si le pivot total est décidé.

- [ ] **Mise à jour de STRICT VARIABLES.md** : Modifier la section `Dates clés` et `Personnes morales` pour indiquer formellement que l'Établissement au jour de l'accident était la SAS HB BARBER (Capital 1 000 €), en passant la SAS LMG au rang d'entité historique.

- [ ] **Audit des Actes** : S'assurer que tous les actes ciblant l'exploitant au 29 mai 2026 utilisent désormais exclusivement les tokens `-hb-` ou que les tokens génériques sont re-mappés vers HB BARBER dans le Dictionnaire.
