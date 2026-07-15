---
title: "Audit de stabilité technique et robustesse des scripts"
description: "Rapport évaluant la robustesse technique du dépôt, les risques de régression et les fuites de données potentielles."
type: rapport
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [📊 Rapports](./README.md) › RAPPORT STABILITE TECHNIQUE*
<hr>
<!-- /Breadcrumb -->

# RAPPORT DE STABILITÉ TECHNIQUE ET DE ROBUSTESSE
> **Date** : 14 juillet 2026
> **Auteur** : Assistant Juridique (Agent IA)
> **Objectif** : Évaluer la robustesse des scripts Python du dépôt pour prévenir toute régression ou fuite de données réelles.

<hr><hr>

## I — PIPELINE D'ANONYMISATION (`batch_anonymize.py`)

L'analyse du script d'anonymisation révèle des limitations techniques majeures dues à l'utilisation de remplacements statiques (`str.replace`).

- **Limites liées à la casse** : Le script utilise une liste de 103 remplacements exacts (79 variantes en casse mixte, 24 variantes standard). Si un nom est écrit avec une casse non prévue (ex: "Prénom Nom" ou "prénom nom"), il ne sera pas remplacé.
- **Risque sur les prénoms ou noms isolés** : Le dictionnaire contient 28 variantes de mots uniques (prénoms ou noms). Toutefois, cette approche par mots exacts n'empêche pas les variations typographiques ou les fautes de frappe de passer au travers des mailles du filet.
- **Risque de fuite (Data Leak)** : En l'état, la probabilité qu'une identité réelle se retrouve dans la strate `🔑 Token` est élevée si le document source contient une variante orthographique ou de casse inattendue.

**Recommandations** :
- Abandonner les remplacements basés sur `str.replace`.
- Implémenter une approche basée sur des expressions régulières (Regex) avec le flag insensible à la casse (`re.IGNORECASE`).
- Appliquer des patterns de détection plus globaux pour capturer les adresses emails et numéros de sécurité sociale / SIRET de manière générique.

<hr><hr>

## II — GÉNÉRATION DES VERSIONS RÉELLES (`generate_real_versions.py`)

Ce script est responsable de la transformation des fichiers tokenisés vers la strate `👤 Reel`.

- **Déconnexion de la Source de Vérité** : Le script utilise un dictionnaire de remplacement `REVERSE_MAP` codé en dur contenant 92 entrées, au lieu de parser dynamiquement `🧠 Memory/TOKEN MAP.md`. Toute mise à jour de la table des tokens oblige à modifier manuellement ce script, violant le principe de la Source Unique de Vérité (SSOT).
- **Risque de perte d'informations** : Étant donné que `batch_anonymize.py` possède 103 remplacements et `REVERSE_MAP` seulement 92, il existe une désynchronisation évidente. Certains tokens récemment ajoutés risquent de ne pas être reconvertis.
- **Robustesse de l'itération** : Le script parcourt correctement les sous-dossiers et écrit dans le dossier cible, mais ne supprime pas les anciens fichiers réels qui auraient été renommés ou supprimés dans la strate `🔑 Token`.

**Recommandations** :
- Refactoriser le script pour qu'il parse et charge `TOKEN MAP.md` dynamiquement à chaque exécution.
- Nettoyer le dossier de destination `👤 Reel` avant génération pour éviter les fichiers fantômes.

<hr><hr>

## III — VERIFICATION CROSS-DOCUMENT (`check_consistency.py`)

Ce script est la clé de voûte de la vérification de l'intégrité du projet, mais il présente des angles morts (faux négatifs).

- **Couverture des vérifications existantes** : Le script vérifie efficacement les liens internes brisés, la présence de tokens non résolus, et l'existence des citations LEGIARTI.
- **Angles morts (Faux négatifs)** :
  - La vérification du "frontmatter" YAML est superficielle. Elle cherche uniquement le pattern "date" et vérifie qu'elle n'est pas antérieure à la date de l'accident. Elle ne valide pas la structure complète du YAML (ex: clés obligatoires comme `titre`, `description`, `type`).
  - Le script ne vérifie pas si les versions générées dans `👤 Reel` sont exemptes de tokens (un oubli de traduction laisserait des `**[...]**`).

**Recommandations** :
- Implémenter une validation formelle du schéma YAML (ex: utilisation de la librairie `pyyaml`).
- Ajouter une étape vérifiant l'absence absolue de balises `**[...]**` dans la strate `👤 Reel`.

<hr><hr>

## IV — SCRIPTS DE CONFORMITE ET NORMALISATION

L'audit des scripts `normalize_sections.py`, `linkify_citations.py` et `audit_citation_links.py` révèle une bonne conception globale.

- **Conformité aux conventions** : Ils respectent les règles édictées dans `CONVENTIONS.md` (séparateurs `<hr><hr>`, citations en liens relatifs).
- **Risques de corruption** : `normalize_sections.py` gère le YAML et les blocs de code, mais reste basé sur des heuristiques (regex). Une mauvaise formatation du YAML initial pourrait entraîner l'injection de séparateurs HTML dans les métadonnées.

**Recommandations** :
- Séparer strictement l'extraction du bloc YAML du reste du contenu avant toute opération de remplacement regex.

<hr><hr>

## V — GESTION DES ERREURS

L'ensemble des scripts de la base de code souffre d'un manque de robustesse face aux exceptions.

- **Fichiers manquants ou mal formés** : La lecture et l'écriture des fichiers s'effectuent sans bloc `try...except`. Un fichier corrompu, verrouillé, ou une erreur d'encodage fera crasher le script en cours de route.
- **Parsing silencieux** : Les erreurs de syntaxe dans les documents (YAML invalide, liens markdown mal construits) ne sont souvent ni interceptées ni remontées de manière explicite.

**Recommandations** :
- Envelopper les opérations I/O et le parsing regex dans des blocs de gestion d'erreur.
- Fournir des logs clairs pointant vers le numéro de ligne du fichier problématique.

<hr><hr>

## VI — SÉCURITÉ ET RISQUE DE FUITE DE DONNÉES (DATA LEAK)

L'aspect le plus critique du dépôt concerne la gestion des données réelles (PII - Personally Identifiable Information).

- **Fichiers contenant des identités réelles** : Le fichier `🧠 Memory/TOKEN MAP.md` et le script `.dev/app/generate_real_versions.py` (via son dictionnaire en dur) contiennent en clair les identités de toutes les parties.
- **Répertoire Reel** : Le répertoire `⚖️ Actes/👤 Reel/` contient les documents en clair, prêts à être imprimés ou envoyés.
- **Configuration Git** : Le fichier `.gitignore` **ne filtre aucun de ces éléments**. Seuls les fichiers cache, `.env` et les PDFs (sauf lois) sont exclus.

En conséquence, **toutes les données réelles sont actuellement suivies par Git**, constituant une violation de sécurité majeure pour un dépôt qui se veut anonymisé (double strate).

**Recommandations Urgentes** :
- Ajouter immédiatement au `.gitignore` les répertoires et fichiers suivants :
  - `⚖️ Actes/👤 Reel/`
  - `🧠 Memory/TOKEN MAP.md`
  - `🧠 Memory/STRICT VARIABLES.md` (si des données sensibles s'y trouvent)
- Nettoyer l'historique Git (via `git filter-repo` ou `BFG Repo-Cleaner`) pour purger les commits contenant des informations réelles.
- Extraire la table des correspondances vers un fichier chiffré ou local non versionné.

<hr><hr>

## VII — CHECKLIST DES TESTS À AJOUTER

Afin de sécuriser le dépôt contre les régressions, les tests unitaires / d'intégration suivants doivent être ajoutés à la suite `pytest` :

- Test unitaire : Le script d'anonymisation capture correctement les casses mixtes, accents, et erreurs typographiques légères.
- Test unitaire : Le parseur YAML valide la présence des champs requis (`title`, `description`, `type`).
- Test d'intégration : La génération `Reel` produit un nombre de fichiers exact à la source `Token`, et aucun fichier `Reel` ne contient la chaîne de caractères `**[`.
- Test de sécurité : Un hook pre-commit (ou CI) vérifiant qu'aucun nom réel issu de `TOKEN MAP` ne se trouve dans les fichiers du dossier `🔑 Token`.
