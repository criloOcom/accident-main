---
title: RAPPORT DE CONFORMITÉ RGPD ET INFORMATIQUE ET LIBERTÉS
date: 2026-07-14
description: Audit de conformité RGPD / Loi Informatique et Libertés du dossier accident-main.
type: rapport
subtitle: RAPPORT DE CONFORMITÉ RGPD ET INFORMATIQUE ET LIBERTÉS — Dossier Accident de la Main — 29 mai 2026
objective: Analyser RAPPORT DE CONFORMITÉ RGPD ET INFORMATIQUE ET LIBERTÉS Dossier Accident de la Main 29 mai 2026
summary: Audit de conformité RGPD / Loi Informatique et Libertés du dossier accident-main.
key_points:
  - I — DOUBLE STRATE 🔑 TOKEN / 👤 REEL : MINIMISATION ET PRIVACY BY DESIGN
  - II — RISQUES DE FUITES DE DONNÉES RÉELLES
  - III — DURÉE DE CONSERVATION DES DONNÉES
  - IV — EXERCICE DES DROITS DES PERSONNES
  - V — SÉCURITÉ DU TRAITEMENT ET DES DONNÉES
  - VI — BASE LÉGALE DU TRAITEMENT
tags:
  - rapport
  - token
  - legifrance
---
<!-- Breadcrumb -->
*[🏠](../../README.md) › [Rapports](../README.md) › [30 Analyses Multi Angle](./README.md)*
<hr>
<!-- /Breadcrumb -->

# RAPPORT DE CONFORMITÉ RGPD ET INFORMATIQUE ET LIBERTÉS<br>Dossier Accident de la Main — 29 mai 2026

<hr><hr>

## I — DOUBLE STRATE 🔑 TOKEN / 👤 REEL : MINIMISATION ET PRIVACY BY DESIGN

### I.1 — Mécanisme actuel
Le dépôt Git utilise une architecture en double strate. Les documents de travail (assignations, plaintes, analyses) sont stockés dans un sous-répertoire `Token/` et sont anonymisés via un système de tokens (ex. [**[La Victime]**](../../Memory/Tokens/token-victime-nom-complet.md), [**[L'Exploitant du Commerce (La SAS)]**](../../Memory/Tokens/token-exploitation-raison-sociale.md)). Les versions contenant les données réelles sont générées dans un sous-répertoire `Reel/` par le script `generate_real_versions.py`.

### I.2 — Analyse de conformité
- Ce mécanisme est conforme au principe de « minimisation des données » énoncé à l'[article 5, paragraphe 1, point c), du règlement (UE) 2016/679 (RGPD)](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000032961803/). En effet, les données à caractère personnel (noms, adresses, coordonnées) ne sont affichées en clair que lorsque cela est strictement nécessaire pour l'édition des actes définitifs.

- Ce système répond pleinement à l'obligation de protection des données dès la conception et par défaut (« Privacy by design ») prévue par l'[article 25 du RGPD](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000032961803/).

### I.3 — Recommandations
- Veiller à ce que les fichiers constituant la table de correspondance (`STRICT VARIABLES.md` et `TOKEN MAP.md`) soient protégés avec le même niveau de sécurité que les données réelles, puisqu'ils permettent la ré-identification directe.

<hr><hr>

## II — RISQUES DE FUITES DE DONNÉES RÉELLES

### II.1 — Emplacements à risque
D'après l'analyse du fonctionnement du dépôt, des données personnelles en clair pourraient subsister ou fuiter dans les emplacements suivants :

- **L'historique Git** : Risque d'avoir commité par inadvertance des versions réelles ou des données personnelles non tokenisées par le passé.

- **Les fichiers de cache** : Tels que `__pycache__/` ou `.pytest_cache/`, générés lors de l'exécution des scripts Python de traitement.

- **Les fichiers temporaires locaux** : Fichiers potentiellement laissés dans le dossier `/tmp/` par les agents lors de la conversion des documents (comme indiqué dans la documentation).

- **Les branches non purgées** : Branches Git parallèles contenant des tests ou des ébauches avec des données réelles.

### II.2 — Plan d'action priorisé
- **Sévérité Haute** : Configurer strictement le fichier `.gitignore` pour s'assurer que le répertoire `Reel/` et tous les fichiers de cache (`__pycache__`) soient ignorés de manière permanente.

- **Sévérité Haute** : Nettoyer l'historique Git (ex. via `git filter-repo`) pour s'assurer qu'aucune donnée de `Reel/` n'ait été versionnée par le passé.

- **Sévérité Moyenne** : Mettre en place un script de nettoyage automatique (hook de pre-commit) supprimant les fichiers temporaires et les caches liés à l'anonymisation.

<hr><hr>

## III — DURÉE DE CONSERVATION DES DONNÉES

### III.1 — Principes applicables
- L'[article 5, paragraphe 1, point e), du RGPD](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000032961803/) impose que les données soient conservées sous une forme permettant l'identification pendant une durée n'excédant pas celle nécessaire au regard des finalités du traitement.

- En matière de contentieux (responsabilité civile et pénale pour l'accident du 29 mai 2026), la durée de conservation est dictée par la procédure et la prescription des actions judiciaires.

### III.2 — Durée recommandée
- Les données peuvent être conservées en base active pendant toute la durée des procédures juridiques (voies de recours incluses).

- À la clôture définitive, les données du dossier client doivent basculer en archivage intermédiaire pendant une durée de 5 ans, délai de prescription de l'action en responsabilité dirigée contre l'avocat ([article 2225 du code civil](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000019017110/)).

- Les règles spécifiques aux archives publiques ([article L. 213-1](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033712721/) et [article L. 213-2](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051835859/) du code du patrimoine) encadrent la communicabilité et l'accès à long terme des décisions rendues et des pièces de procédure remises aux greffes.

<hr><hr>

## IV — EXERCICE DES DROITS DES PERSONNES

### IV.1 — Droits applicables
- Toute personne concernée (la victime, le dirigeant [**[Le Président de l'Exploitation]**](../../Memory/Tokens/token-exploitation-president-nom.md), l'employé [**[Le Préposé de l'Exploitation]**](../../Memory/Tokens/token-exploitation-prepose-nom.md)) dispose des droits d'accès, de rectification et d'effacement sur ses données personnelles ([articles 15, 16 et 17 du RGPD](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000032961803/)).

### IV.2 — Limites dans le cadre contentieux
- **Le droit à l'effacement** ne s'applique pas lorsque le traitement est nécessaire à « la constatation, à l'exercice ou à la défense de droits en justice », conformément à l'[article 17, paragraphe 3, point e), du RGPD](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000032961803/).

- **Le secret professionnel** protège les communications. Conformément à l'[article 226-13](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006335294/) et l'[article 226-14](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000034592480/) du code pénal, les éléments couverts par le secret de l'avocat ne peuvent être divulgués à des tiers (ex. un codéfendeur) s'exerçant un droit d'accès. La communication des pièces entre parties obéit strictement au principe du contradictoire et à l'obligation pour chaque partie de prouver les faits ([article 9 du code de procédure civile](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000024496743/)).

<hr><hr>

## V — SÉCURITÉ DU TRAITEMENT ET DES DONNÉES

### V.1 — Risques actuels
- **Dépôt distant** : Stocker des données médicales ou d'identité sur GitHub (même en dépôt privé) expose à des risques d'accès non autorisés en cas de compromission du compte.

- **Accès locaux** : Le token d'accès GitHub et les identifiants présents en local (`~/.git-credentials`) constituent une faille potentielle si le poste informatique de développement est compromis.

### V.2 — Mesures recommandées
- Appliquer rigoureusement l'[article 32 du RGPD](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000032961803/) (sécurité du traitement) en s'assurant du chiffrement systématique des postes de travail.

- Interdire strictement la synchronisation ou le commit du répertoire `Reel/` vers un cloud non certifié HDS (Hébergement de Données de Santé) si ce dossier contient des informations médicales sans tokenisation.

<hr><hr>

## VI — BASE LÉGALE DU TRAITEMENT

### VI.1 — Fondement juridique principal
- Le traitement des données d'identité et de contact des différentes parties (victime, auteurs présumés, témoins) est licite puisqu'il est nécessaire aux fins des **intérêts légitimes** poursuivis par la victime pour préparer sa défense et faire valoir ses droits ([article 6, paragraphe 1, point f), du RGPD](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000032961803/)).

### VI.2 — Cas des données de santé
- Le dossier comporte d'importantes données médicales concernant [**[La Victime]**](../../Memory/Tokens/token-victime-nom-complet.md) (certificats de [**[Le Médecin Généraliste]**](../../Memory/Tokens/token-victime-medecin-generaliste.md) et de [**[Le Chirurgien SOS Main]**](../../Memory/Tokens/token-hopital-sosmain-chirurgien.md), séquelles).

- Ce traitement est autorisé par l'exception prévue à l'[article 9, paragraphe 2, point f), du RGPD](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000032961803/), qui dispose que l'interdiction de traiter des données sensibles est levée si « le traitement est nécessaire à la constatation, à l'exercice ou à la défense d'un droit en justice ».

<hr><hr>

## VII — MODÈLE DE MENTION DE CONFIDENTIALITÉ

Il est recommandé d'apposer la mention suivante sur tout document non tokenisé extrait de `Reel/` et transmis à un tiers non soumis au secret professionnel :

> « Les informations contenues dans ce document sont strictement confidentielles. Elles comportent des données à caractère personnel, dont d'éventuelles données de santé, protégées par le règlement (UE) 2016/679 (RGPD) et la loi n° 78-17 du 6 janvier 1978. Leur traitement est strictement limité à l'exercice et la défense des droits en justice (art. 6 §1 f) et art. 9 §2 f) du RGPD). Toute reproduction, diffusion ou utilisation non autorisée est interdite. Les personnes concernées disposent de droits sur leurs données, dans les limites prévues par le RGPD concernant l'exercice de droits en justice. »