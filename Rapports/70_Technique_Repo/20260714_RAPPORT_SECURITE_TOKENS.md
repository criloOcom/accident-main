---
uid: 8Q23rKA3R
title: Audit de sécurité juridique des tokens et de la double strate
date: 2026-07-14
description: Rapport d'analyse sur la résistance du système d'anonymisation et sa conformité avec le secret de l'instruction (Art. 11 CPP).
type: rapport
subtitle: AUDIT DE SÉCURITÉ JURIDIQUE DES TOKENS ET DE LA DOUBLE STRATE
objective: Analyser AUDIT DE SÉCURITÉ JURIDIQUE DES TOKENS ET DE LA DOUBLE STRATE
summary: Rapport d'analyse sur la résistance du système d'anonymisation et sa conformité avec le secret de l'instruction (Art. 11 CPP).
key_points:
  - I — RÉVERSIBILITÉ DU MAPPING
  - II — COHÉRENCE DES TOKENS
  - III — FUITES RÉSIDUELLES ET COMMANDE DE SURVEILLANCE
  - IV — CONFORMITÉ DES VERSIONS RÉELLES
  - V — SECRET DE L'INSTRUCTION ET CONFIDENTIALITÉ
tags:
  - rapport
  - token
---
<!-- Breadcrumb -->
*[🏠](../../README.md) › [Rapports](../README.md) › [70 Technique Repo](./README.md)*
<hr>
<!-- /Breadcrumb -->

# AUDIT DE SÉCURITÉ JURIDIQUE DES TOKENS ET DE LA DOUBLE STRATE
> Rapport du 14 juillet 2026 sur la robustesse du système d'anonymisation 🔑 / 👤 et les risques de réidentification en lien avec l'obligation de confidentialité.

<hr><hr>

## I — RÉVERSIBILITÉ DU MAPPING

L'architecture actuelle centralise la vérité des identités réelles au sein du fichier de configuration `TOKEN MAP.md`. Ce fichier constitue le point de vulnérabilité majeur du système.

- **Point unique de vérité** : `TOKEN MAP.md` est le seul dictionnaire permettant d'associer un token à une identité ou donnée réelle.

- **Risque de fuite** : S'il est actuellement protégé (hors synchronisation Drive), sa présence en clair au sein du dépôt Git public constitue un risque critique de réidentification totale. Si le dépôt et la `TOKEN MAP.md` fuitent conjointement, toutes les identités anonymisées (et donc les documents associés) deviennent immédiatement lisibles et accessibles, compromettant irréversiblement les données de santé et l'anonymat de l'affaire.

- **Recommandation** : Il est impératif de recourir au chiffrement de ce fichier (ex. via GPG ou Git-crypt) afin de garantir que même en cas d'exfiltration du dépôt, le dictionnaire de réversibilité demeure illisible.

<hr><hr>

## II — COHÉRENCE DES TOKENS

L'analyse comparée des scripts d'anonymisation (`batch_anonymize.py`) et de restitution (`generate_real_versions.py`) révèle de graves failles de cohérence qui affectent la stabilité de la double strate.

- **Désynchronisation des scripts** : `batch_anonymize.py` utilise par endroits des syntaxes obsolètes sans la protection par doubles astérisques (ex. `[Le Prepose de l'Exploitation]` au lieu de `[**[Le Préposé de l'Exploitation]**](../../Memory/Tokens/token-exploitation-prepose-nom.md)`), tandis que `generate_real_versions.py` et `TOKEN MAP.md` privilégient la forme stricte.

- **Absence de frontières d'expressions régulières (Regex boundaries)** : Le script `batch_anonymize.py` repose principalement sur un remplacement basique via la méthode `.replace()`. Cela entraîne la non-capture de variantes nominales (casse mixte, erreurs de saisie) qui ne figurent pas strictement dans le dictionnaire.

- **Tokens orphelins et lacunes de mapping** : Des variantes identitaires essentielles, notamment pour l'Adjoint au Maire (TAVELLA) ou les médecins intervenants, ne sont pas capturées de façon uniforme.

- **Recommandation** : Le script d'anonymisation doit être refondu pour exploiter des expressions régulières avec frontières de mots (`\b`), permettant ainsi de limiter les faux positifs tout en attrapant systématiquement les cibles d'anonymisation.

<hr><hr>

## III — FUITES RÉSIDUELLES ET COMMANDE DE SURVEILLANCE

Une investigation approfondie des documents d'ores et déjà traités au sein du répertoire « Token » a révélé un volume significatif d'échecs de la procédure d'anonymisation.

Au total, **187 occurrences de données réelles** (noms, numéros de dossiers) demeurent en clair au sein des actes prétendument tokenisés.

* Le médecin généraliste a été retrouvé en clair : 86 occurrences (Oxybel).

* Le numéro de procès-verbal de police a fuité : 66 occurrences (2026/015967).

* Le numéro de dossier de la Caisse Primaire d'Assurance Maladie : 58 occurrences (31727387).

* L'identité du médecin urgentiste / chirurgien : 57 occurrences (JARDON) et 22 occurrences pour son prénom (Julie), ainsi que 6 occurrences (DJERBI).

* L'identité de l'Adjoint au Maire : 14 occurrences (TAVELLA).

* Des adresses postales : 3 occurrences (22 rue lafaurie).

**Plan de durcissement et surveillance** :
Afin de prévenir toute nouvelle fuite au sein des fichiers `.md` produits dans la strate Token, il convient d'exécuter de façon régulière et automatique (idéalement via un hook de pre-commit) la commande `grep` de surveillance suivante :

```bash
grep -riE "(S[eé]bastien|GRAZIDE|Sabir|MOUNTASSER|Catherine|ANDISSAC|SORROCHE|Ayoub|BENNOURINE|Romain|DELRIEU|Iskander|DJERBI|Julie|JARDON|Oxybel|Sigrid|DESBOIS|TAVELLA|Tavella|sebastien\.grazide|500 474 457|938 033 222|10 Avenue de Purpan|22 Rue Lafaurie|108 Avenue Paul Bert|2026/015967|31727387)" "Actes/Token/"
```

<hr><hr>

## IV — CONFORMITÉ DES VERSIONS RÉELLES

Les documents produits au sein de la strate « Reel » s'appuient sur l'action de substitution opérée par `generate_real_versions.py`.

- **Conformité technique** : Le script de génération fonctionne de façon satisfaisante en appliquant le mapping inverse (de `**[Token]**` vers Identité Réelle).

- **Problématique induite par les fuites résiduelles** : Compte tenu des 187 fuites répertoriées ci-dessus dans la strate Tokenisée, les documents réels incluent une redondance hétérogène (des identités générées par les tokens corrects côtoyant des identités qui avaient échappé au script d'anonymisation).

- **Conséquences sur l'audit** : Ce mécanisme, bien qu'il préserve l'intégrité de la vérité factuelle dans la version réelle, confirme que la strate Token n'assure pas actuellement l'anonymisation requise en cas de partage des documents.

<hr><hr>

## V — SECRET DE L'INSTRUCTION ET CONFIDENTIALITÉ

Les pièces générées dans le dossier concernent en partie une enquête pénale suite au dépôt de plainte, matérialisée par le PV de police n°2026/015967.

Il est fondamental de rappeler le cadre légal strict entourant ces procédures en droit français, fondé sur le principe du secret de l'instruction et de l'enquête.

- **Fondement légal vérifié** :
L'article 11 du Code de procédure pénale (ID Légifrance : LEGIARTI000006574847, en vigueur et modifié) dispose clairement :
> « Sauf dans le cas où la loi en dispose autrement et sans préjudice des droits de la défense, la procédure au cours de l'enquête et de l'instruction est secrète. Toute personne qui concourt à cette procédure est tenue au secret professionnel dans les conditions et sous les peines des articles 226-13 et 226-14 du code pénal. [...] »

- **Application au dossier** :
Les actes constitutifs du dossier (versions réelles) reprenant des extraits ou constats tirés des procédures d'enquête policière sont soumis de facto à ce devoir de discrétion. En tant qu'avocat ou partie prenante agissant dans la défense de la victime, la communication de pièces réelles peut compromettre l'enquête en cours et violer les devoirs déontologiques.

- **Action requise** :
Toute déclinaison non-anonymisée de ces actes, spécifiquement les fichiers de la strate « Reel », DOIT impérativement inclure la mention **« CONFIDENTIEL / NE PAS DIFFUSER »** afin de satisfaire aux dispositions de l'article 11 du Code de procédure pénale et d'éviter un délit pénal par violation du secret professionnel.