---
title: "Guide de l'Avocat : Utilisation de l'Écosystème du Projet"
date: FIXME
description: "Guide pédagogique expliquant la navigation et l'utilisation de l'écosystème Git, l'architecture Token/Reel, et la contribution au projet."
type: rapport
---
<!-- Breadcrumb -->
*[🏠](../../README.md) › [Rapports](../README.md) › [20 Accueil Avocat](./README.md)*
<hr>
<!-- /Breadcrumb -->

<hr>

# Guide de l'Avocat : Utilisation de l'Écosystème du Projet

Bienvenue dans l'espace de travail collaboratif du dossier. Ce guide a été spécialement conçu pour vous aider à naviguer efficacement au sein de notre environnement. Bien que reposant sur des technologies modernes comme Git, cet espace est pensé pour structurer, sécuriser et tracer la construction de notre dossier juridique.

<hr><hr>

## I — L'Arborescence : La Règle de la "Double Strate"

Notre dossier est structuré selon un principe fondamental de "Double Strate", conçu pour protéger les données personnelles tout en permettant la génération automatique de documents prêts à être signés.

*   **La strate "Token" (Source de Vérité) :**
    Située dans le dossier [Actes/Token](../../Actes/Token/README.md) (ou `actes/token/`), cette strate est le cœur du projet. Tous les actes, conclusions, et courriers y sont rédigés sous une forme anonymisée. C'est ici que le travail de rédaction et de réflexion s'opère. **C'est la seule version qui doit être modifiée.**

*   **La strate "Reel" (Version Générée) :**
    Située dans le dossier [Actes/Reel](../../Actes/Reel/README.md) (ou `actes/reel/`), cette strate contient les documents finaux, où toutes les données anonymisées ont été automatiquement remplacées par les véritables identités. **Ces fichiers ne doivent jamais être modifiés manuellement**, car ils sont regénérés automatiquement à partir de la strate Token.

<hr><hr>

## II — Comment Lire un Fichier "Token"

Lorsque vous consultez un document de la strate Token, il diffère légèrement d'un document Word classique. Voici les éléments clés pour le lire confortablement :

*   **L'En-tête (Frontmatter) :**
    Tout en haut du document, entre des lignes de tirets `---`, se trouve le bloc de métadonnées (le *Frontmatter*). Il indique le titre, la date, le type d'acte, et les parties concernées. Ce bloc sert au système informatique pour trier et générer les documents finaux, il n'apparaîtra pas dans la version imprimée.

*   **Les Identifiants (Tokens) :**
    Pour préserver la confidentialité et garantir l'exactitude des informations, les identités, montants ou dates clés sont remplacés par des balises spécifiques, souvent encadrées par des doubles crochets `[[ ]]` ou mises en gras sous la forme `**[Nom du Token]**` (par exemple : `[**[La Victime]**](../../Memory/Tokens/token-victime-nom-complet.md)`). Le système informatique se charge de les remplacer par les vrais noms lors de la génération.

*   **Les Liens Relatifs :**
    Vous croiserez parfois des textes bleus soulignés qui renvoient vers d'autres fichiers du projet (par exemple, vers une pièce ou une preuve). Ce sont des "liens relatifs". Ils vous permettent de naviguer facilement de l'argumentaire à la pièce justificative correspondante d'un simple clic.

<hr><hr>

## III — La Correspondance entre Fichiers Token et Documents Juridiques

La structure de nos fichiers reflète la logique procédurale. Chaque fichier `.md` (Markdown) de la strate Token correspond directement à un futur document juridique :

*   Un fichier nommé `assignation.md` dans la strate Token a vocation à devenir votre projet d'assignation finalisé dans la strate Reel.

*   Les titres à l'intérieur de ces fichiers (précédés par des `#` ou des `##`) se transformeront automatiquement en titres hiérarchiques propres dans la version finale (PDF ou Word).

*   La rédaction s'effectue dans ces fichiers `.md`. La mise en page définitive (police, marges) est appliquée automatiquement en aval, vous garantissant de pouvoir vous concentrer exclusivement sur le fond juridique.

<hr><hr>

## IV — Comment Proposer des Modifications (Pull Requests)

Nous utilisons le système de révision "Git" pour tracer chaque évolution du dossier. Plutôt que de vous envoyer des versions "V1", "V2_finale", "V3_vraiment_finale" par email, voici comment nous procédons :

*   **La Branche (Votre espace de travail) :**
    Lorsque des modifications sont nécessaires, un espace dédié (une "branche") est créé. C'est un brouillon isolé qui n'affecte pas le dossier principal.

*   **La "Pull Request" (PR) ou Demande d'Intégration :**
    Une fois votre rédaction ou vos corrections terminées dans votre branche, une "Pull Request" est ouverte. C'est une page de discussion qui montre très exactement (en vert et rouge) ce qui a été ajouté ou supprimé par rapport à la version précédente.

*   **La Validation :**
    Sur cette page de Pull Request, vous pouvez laisser des commentaires ciblés sur des paragraphes précis, valider les choix stratégiques, et enfin approuver l'intégration. Une fois validées, les modifications rejoignent le dossier principal (la branche `main`).

<hr><hr>

## V — La Convention de Nommage "J+XX"

Pour situer chaque événement dans la chronologie de l'affaire sans dépendre de dates absolues (qui peuvent changer en cours de procédure), nous utilisons la convention `J+XX` :

*   **J0** représente le jour de l'événement initial (l'accident).

*   Les fichiers ou répertoires sont souvent préfixés ou étiquetés par `J+` suivi du nombre de jours écoulés depuis l'événement. Par exemple, un acte médical ou une démarche réalisée 30 jours après l'accident portera la mention `J+30`.

*   Cette méthode permet de vérifier d'un coup d'œil la cohérence des délais légaux, de prescription, et l'enchaînement logique des préjudices, indépendamment de la date de création informatique du fichier.