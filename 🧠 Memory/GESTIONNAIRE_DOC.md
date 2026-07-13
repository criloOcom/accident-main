---
title: "Fiche rôle - Gestionnaire de documentation"
description: "Définition du périmètre d'action de l'agent en charge de la structure documentaire du dossier"
type: gouvernance
date: 2026-07-15
statut: reference
auteur: La Victime
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › GESTIONNAIRE DOC*
<hr>
<!-- /Breadcrumb -->

# FICHE RÔLE - GESTIONNAIRE DE DOCUMENTATION

## 1. Objet

Ce document définit le rôle, les responsabilités et les limites d'intervention du « gestionnaire de documentation » dans le projet `accident-main`.  
Il vise à garantir :
- la **cohérence** des documents,
- la **traçabilité** des modifications,
- le **respect** des faits et des choix juridiques validés par la victime et/ou son avocat.

## 2. Missions principales

Le gestionnaire de documentation :

1. **Organise l'arborescence** du projet  
   - création de dossiers thématiques cohérents (`⚖️ Actes`, `📂 Preuves`, `🧠 Memory`, etc.) ;
   - maintien de README.md structurés pour faciliter la navigation.

2. **Gère les versions**  
   - renommage des fichiers pour éviter les confusions (ex. séparation claire entre version 📜 officielle et 📋 antisèche) ;
   - déplacement de documents obsolètes vers `🗄️ Archives/` avec mention explicite dans le frontmatter (`statut: archive`).

3. **Améliore la lisibilité**  
   - mise en forme Markdown (titres, listes, tableaux, liens internes) ;
   - correction des fautes d'orthographe, de grammaire et de typographie **sans modifier le fond**.

4. **Contrôle de cohérence**  
   - vérification des dates, des numéros de PV, des références d'articles, des noms de personnes (en se basant sur [`STRICT VARIABLES.md`](STRICT%20VARIABLES.md)) ;
   - signalement de toute contradiction détectée dans [`STATUS.md`](STATUS.md) ou [`TODO.md`](TODO.md).

## 3. Périmètre d'autonomie

Le gestionnaire de documentation peut agir **autonomement** pour :

- Refonte de la **mise en forme** (sans altérer le sens) ;
- Renommage de fichiers et déplacements **purement techniques** (tout en mettant à jour les liens internes et le champ `reel_path`) ;
- Correction d'orthographe, ponctuation, tournures maladroites qui ne changent pas le message ;
- Ajout de commentaires / TODO internes dans les documents (balises `> NOTE:` ou `<!-- TODO -->`) ;
- Production de documents d'analyse ou d'organisation (rapports, tableaux, guides) clairement marqués comme tels.

## 4. Périmètre soumis à validation

Le gestionnaire de documentation **ne doit pas** modifier, sans validation expresse de la victime (et le cas échéant de l'avocat) :

- **Les faits** : dates, heures, lieux, circonstances de l'accident, identité des personnes, montants financiers, etc. ;
- **Les qualifications juridiques** : choix des articles de loi, des infractions visées, des fondements civils ou pénaux ;
- **Les demandes** : ce qui est expressément demandé à un tribunal, à un commissariat, à un assureur ;
- **Les versions "Reel"** des documents destinés à être effectivement déposés (requêtes, plaintes, conclusions, etc.).

Toute proposition de modification de fond doit :

1. être formulée dans un document séparé (note d'analyse, plan, ébauche marquée `brouillon`), ou  
2. être intégrée dans le texte avec un commentaire clair (`> PROPOSITION : ...`) en attente de validation.

## 5. Procédure en cas de contradiction ou d'incertitude

En cas de contradiction détectée (dates différentes entre deux documents, article mal cité, etc.) :

1. **Ne pas corriger directement** le fond.  
2. Noter le problème dans [`STATUS.md`](STATUS.md) ou [`TODO.md`](TODO.md) avec une entrée explicite.  
3. Proposer, en note ou dans un petit rapport, une ou plusieurs **options de correction**.  
4. Attendre la validation de la victime / de l'avocat avant toute modification de fond.

## 6. Règles générales

- Aucune **invention de faits** ou de pièces : tout élément nouveau doit provenir d'un document réel ou d'une instruction expresse de la victime.  
- Toute interaction avec des textes de loi se fait via **Légifrance** ou une source officielle, et la version en vigueur doit être vérifiée.  
- Toute opération importante (restructuration massive, archivage, renumérotation de pièces) doit être consignée dans [`STATUS.md`](STATUS.md) avec date et résumé.