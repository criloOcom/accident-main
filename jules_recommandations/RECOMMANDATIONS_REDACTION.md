# Recommandations pour la Rédaction des Actes Juridiques

## Introduction
Ce document compile les recommandations issues de recherches web et de l'analyse du dossier `actes/` afin d'améliorer la qualité, le professionnalisme et la clarté des actes juridiques produits (assignations, constitutions de partie civile, etc.).

## 1. Principes Fondamentaux de la Rédaction Juridique
- **Clarté, Précision et Rigueur :** Les actes doivent être rédigés dans un langage clair, sans ambiguïté. Chaque terme juridique doit être utilisé à bon escient.
- **Structure Cohérente :** Respecter une architecture logique (exposé des faits, discussion juridique/moyens, demandes/par dispositif). L'utilisation de titres et sous-titres numérotés facilite la lecture.
- **Neutralité et Objectivité :** Le ton doit rester professionnel, factuel et mesuré, en évitant les tournures purement émotionnelles.

## 2. Recommandations Spécifiques par Type d'Acte

### 2.1 Assignation (ex: Assignation Référé Provision)
- **Le Dispositif :** C'est la partie la plus importante. Il doit récapituler précisément les prétentions, car le juge ne statue que sur ce qui est demandé dans le dispositif.
- **Les Fondements Juridiques :** Citer de manière exacte les articles de loi et la jurisprudence applicable (ex: art. 835 CPC pour le référé-provision).
- **Motivation des demandes :** L'urgence (si applicable), l'absence de contestation sérieuse ou le trouble manifestement illicite doivent être démontrés point par point.
- **L'état des pièces :** Un bordereau des pièces visées dans l'acte doit être systématiquement annexé à l'assignation.

### 2.2 Constitution de Partie Civile
- **Exposé clair du préjudice :** Démontrer le lien de causalité direct et certain entre l'infraction pénale et le préjudice subi (ex: blessure à la main suite à la négligence).
- **Chiffrage des demandes :** Prévoir une évaluation (même provisionnelle) des préjudices en s'appuyant sur des nomenclatures reconnues (ex: nomenclature Dintilhac).
- **Demande d'expertise :** Si l'évaluation finale n'est pas possible, formuler explicitement une demande d'expertise médicale judiciaire.

## 3. Amélioration Formelle des Documents du Dossier `actes/`
- **Uniformisation :** S'assurer que tous les actes (civils et pénaux) respectent la même charte de présentation (polices, marges, alignement justifié).
- **Gestion des Pièces :** S'assurer que les références aux pièces (ex: `🔒 PIÈCE ORIGINALE`) sont correctement insérées et listées dans les actes.
- **Anonymisation / Tokens :** Continuer d'appliquer rigoureusement la logique de tokens (`[La Victime]`, `[L'Exploitant du Commerce]`) et vérifier systématiquement qu'aucune donnée personnelle n'est laissée en clair, conformément au `TOKEN MAP.md`.
- **Sauts de page :** Respecter strictement la consigne d'utiliser `=== PAGE BREAK ===` avant les sections majeures pour un rendu professionnel sous Google Docs.

## 4. Prochaines Étapes pour l'Agent de Demain
- Réviser les fichiers dans `actes/contentieux-civil/` et `actes/contentieux-penal/` pour vérifier l'alignement avec ces recommandations (notamment la présence du dispositif clair et le bordereau de pièces).
- Appliquer ces standards de présentation lors de la prochaine étape d'injection dans Google Docs.
