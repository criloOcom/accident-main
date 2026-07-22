---
title: Synthèse des 16 Simulations et Arbre Décisionnel
description: Synthèse stratégique multi-angles des 16 simulations du dossier Accident Main et modélisation de l'arbre de décision global (Plans A, B, C).
type: rapport
date: 2026-07-21
subtitle: Synthèse des 16 Simulations et Arbre Décisionnel
objective: Synthétiser et présenter une vue d'ensemble de Synthèse des 16 Simulations et Arbre Décisionnel
summary: Synthèse stratégique multi-angles des 16 simulations du dossier Accident Main et modélisation de l'arbre de décision global (Plans A, B, C).
key_points:
  - A. MATRICE ACTEUR × POSITION
  - B. ARBRE DE DÉCISION GLOBAL
  - C. PLAN A / PLAN B / PLAN C
  - D. RECOMMANDATIONS
recipient: Avocat
tags:
  - synthese
  - global
  - responsabilite
  - penal
  - preuve
  - avocat
  - token
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [Rapports](./README.md) › Synthèse Simulations*
<hr>
<!-- /Breadcrumb -->

# Synthèse des 16 Simulations et Arbre Décisionnel

Ce document présente la synthèse stratégique issue des 16 simulations réalisées par les différents acteurs professionnels (juges, experts, forces de l'ordre, avocats) concernant l'accident corporel de [**[La Victime]**](../Memory/Tokens/token-victime-nom-complet.md) survenu le 29 mai 2026 au sein du salon de coiffure de [**[L'Exploitant du Commerce (La SAS)]**](../Memory/Tokens/token-exploitation-raison-sociale.md).

<hr><hr>

## A. MATRICE ACTEUR × POSITION

| Acteur | Position/Stratégie recommandée | Notre contre-argument | Risque associé |
|---|---|---|---|
| [Commissaire Police](../Simulations/01_Commissaire_Police.md) | Transmission au Parquet pour suites pénales | Inutile, preuves déjà accablantes (vasque dégradée) | Enquête trop longue, lenteur de la procédure |
| [Juge d'Instruction](../Simulations/02_Juge_Instruction.md) | Information judiciaire, interrogatoires | Les faits sont simples, pas besoin de juge d'instruction | Enlisement du dossier pendant 2-3 ans |
| [Juge des Référés](../Simulations/03_Juge_Referes.md) | Accueil favorable, provision 15k€ et expertise | Le quantum demandé est un strict minimum incontestable | Contestation adverse du montant, refus de provision |
| [Juge Civil](../Simulations/04_Juge_Civil.md) | Condamnation de l'exploitant (art 1242) | La responsabilité est de plein droit, aucune faute de la victime | Insolvabilité de la SAS, condamnation sur coquille vide |
| [Procureur](../Simulations/05_Procureur.md) | Opportunité de poursuites, citation directe | S'assurer que les dirigeants personnes physiques sont visés | Classement sans suite ou absence de peine significative |
| [Gendarme (OPJ)](../Simulations/06_Gendarme_OPJ.md) | Audition des dirigeants et recueil de preuves | Inutile d'attendre leurs aveux, les preuves existent | Garde à vue infructueuse ou fuite des responsabilités |
| [Avocat Conseil](../Simulations/07_Avocat_Conseil.md) | Attaque simultanée au civil, pénal et CIVI | (Pas de contre-argument, c'est notre stratégie) | Dispersion des ressources, coût des procédures multiples |
| [Expert Judiciaire](../Simulations/08_Expert_Judiciaire.md) | Expertise médicale stricte Dintilhac | Ne pas sous-estimer l'Incidence Professionnelle de l'informaticien | Consolidation tardive (mi-2027), sous-évaluation du préjudice |
| [Préfet](../Simulations/09_Prefet.md) | Sanction ERP et contrôle de sécurité | Concentrer sur les indemnités, la sanction admin ne paie pas | Lenteur administrative et impact nul sur l'indemnisation civile |
| [Inspecteur Travail](../Simulations/10_Inspecteur_Travail.md) | Protection des préposés de la SAS | Le focus doit rester sur la victime client, pas les salariés | Complexité juridique avec le droit du travail interférent |
| [Expert Assurances](../Simulations/11_Expert_Assurances.md) | Analyse de la couverture RC professionnelle | L'absence d'assurance probable, préparer la voie CIVI | L'assureur invoque une exclusion de garantie ou un plafond bas |
| [Médecin Légiste](../Simulations/12_Medecin_Legiste.md) | Consolidation et évaluation des séquelles | Anticiper l'aggravation possible (section tendineuse sévère) | Conflit d'experts sur le taux de Déficit Fonctionnel Permanent |
| [Notaire](../Simulations/13_Notaire.md) | Recherche patrimoine et hypothèque | Le capital de 200€ masque les responsabilités personnelles | Insolvabilité organisée par les dirigeants, aucun bien saisissable |
| [Juge Enfants / JAF](../Simulations/14_Juge_Enfants.md) | Pas de mesure d'assistance requise | (L'accident n'affecte pas directement la structure éducative) | (Aucun risque direct lié à ce volet pour la victime) |
| [Médiateur](../Simulations/15_Mediateur.md) | Résolution amiable et provision immédiate | Les dirigeants fuient, la médiation est une perte de temps | Blocage des gérants et abandon de la voie répressive |
| (Synthèse / Plan) | Activer la CIVI en dernier recours si échec total | La FGTI plafonnera, maximiser le référé d'abord | Délais CIVI très longs, montants souvent révisés à la baisse |

<hr><hr>

## B. ARBRE DE DÉCISION GLOBAL

```
SI AJ accordée → avocat commis → référé provision
  ├── SI provision accordée (Probabilité: 85%) → expertise médicale (Probabilité: 95%) → fond (Probabilité: 80%)
  ├── SI provision refusée (Probabilité: 15%) → appel (Probabilité: 50%) → expertise (Probabilité: 60%)
SINON → CIVI (Commission d'Indemnisation des Victimes d'Infractions)
  ├── SI CIVI acceptée (Probabilité: 70%) → indemnisation plafonnée / selon barème FGTI (Probabilité: 90%)
  └── SI CIVI refusée (Probabilité: 30%) → appel CIVI (Probabilité: 40%)
```

<hr><hr>

## C. PLAN A / PLAN B / PLAN C

### Plan A : Voie Pénale et Constitution de Partie Civile

- **Conditions de déclenchement :** Plainte avec constitution de partie civile (CITC) ou citation directe suite au classement ou à la lenteur de l'enquête préliminaire.

- **Probabilité de succès :** Élevée (75%) concernant la condamnation pour blessures involontaires vu le manquement délibéré à la sécurité.

- **Timeline estimée :** 12 à 24 mois.

- **Avantages / Inconvénients :** Permet de mettre en cause personnellement les dirigeants, outrepassant le faible capital de la SAS. Indispensable pour ouvrir la voie FGTI/CIVI. Procédure potentiellement longue.

### Plan B : Voie Civile Prioritaire

- **Conditions de déclenchement :** Référé 145 CPC pour expertise in futurum, et Référé provision (art. 835 CPC).

- **Probabilité de succès :** Très élevée (90%) sur la désignation de l'expert et la provision si l'assurance est présente. Modérée (40%) si la SAS est non assurée et insolvable.

- **Timeline estimée :** 3 à 6 mois pour le référé ; 12 à 18 mois pour le fond post-consolidation.

- **Avantages / Inconvénients :** Rapide pour obtenir une provision (si l'assurance est solvable). Fort risque d'inexécution si la SAS est une coquille vide et sans assurance RC pro valide.

### Plan C : CIVI (Commission d'Indemnisation des Victimes d'Infractions)

- **Conditions de déclenchement :** Preuve de l'infraction pénale et insolvabilité/absence d'assurance du tiers responsable.

- **Probabilité de succès :** Élevée (80%) vu la nature des blessures (ITT > 1 mois) et l'infraction caractérisée.

- **Timeline estimée :** 8 à 12 mois après décision pénale ou justificatif d'insolvabilité.

- **Avantages / Inconvénients :** Sécurité de paiement par le FGTI. L'indemnisation peut cependant être plus strictement évaluée (barèmes) par rapport à une juridiction civile classique.

<hr><hr>

## D. RECOMMANDATIONS

- **Agir en Référé-Provision immédiatement :** Sécuriser 15 000 € de provision et acter la désignation de l'expert judiciaire de façon contradictoire.

- **Maintenir la pression pénale :** La plainte pénale est indispensable pour contourner le risque d'insolvabilité de la SAS (capital 200 €) et engager la responsabilité personnelle de [**[Le Président de l'Exploitation]**](../Memory/Tokens/token-exploitation-president-nom.md).

- **Vérification Assurantielle :** Priorité absolue à la vérification de la police d'assurance RC de la SAS, à défaut, préparer le dossier pour la CIVI/FGTI.

- **Préparation du Dossier Médical et Professionnel :** Documenter minutieusement l'incidence professionnelle de la blessure à la main dominante pour un informaticien, afin de préparer l'expertise de consolidation prévue pour mi-2027.
