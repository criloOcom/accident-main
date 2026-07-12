---
title: "Rapport d'Audit : Cohérence des organismes et adresses"
description: "Vérifier la cohérence des noms d'organismes, des adresses, des sigles et des tribunaux compétents dans l'ensemble des courriers 03 à 34 du dossier tokenisé ([⚖️ Actes/🔑 Token/✉️ Courriers](⚖️%20Actes/🔑%20Token/✉️%20Courriers/README.md))."
type: rapport
---











<!-- Breadcrumb -->
[🏠](../../../README.md) › [📊 Rapports et Analyses](../../README.md) › [🤖 Jules](../README.md) › [📁 audit](./README.md) › audit coherence organismes
<!-- /Breadcrumb -->

# Rapport d'Audit : Cohérence des organismes et adresses

## Objectif
Vérifier la cohérence des noms d'organismes, des adresses, des sigles et des tribunaux compétents dans l'ensemble des courriers 03 à 34 du dossier tokenisé ([⚖️ Actes/🔑 Token/✉️ Courriers](⚖️%20Actes/🔑%20Token/✉️%20Courriers/README.md)).

## Vérifications effectuées

1. **Nom de la partie adverse (SAS)**
   - Vérification de la présence de mentions en clair ("SAS LES MAUVAIS GARCONS", "LES MAUVAIS GARÇONS").
   - *Résultat* : Aucune mention non anonymisée de la SAS n'a été trouvée. Le token `**[L'Exploitant du Commerce (La SAS)]**` est correctement utilisé partout.

2. **Adresse de l'exploitation (22 Rue Lafaurie)**
   - Vérification de la présence de l'adresse en clair ("22 Rue Lafaurie" ou "09000 Foix").
   - *Résultat* : Les adresses ont bien été tokenisées avec `**[L'Adresse de l'Exploitation]**` ou `**[La Ville de l'Accident]**`.

3. **Tribunal compétent et mentions de la ville**
   - L'audit a révélé des mentions non tokenisées du tribunal dans les documents 30, 31 et 34 : "Tribunal de Commerce de Foix" et "Tribunal Judiciaire de Foix".
   - *Correction apportée* : "Foix" a été remplacé par le token `**[La Ville de l'Accident]**` pour unifier le tribunal (ex: "Tribunal Judiciaire de **[La Ville de l'Accident]**", "Tribunal de Commerce de **[La Ville de l'Accident]**").
   - Dans le document 34 (Email au Maire), les mentions du "Maire de Foix" ont été remplacées par "Maire de **[La Ville de l'Accident]**".

4. **Sigles des organismes (CPAM, URSSAF, CADA, ERP, SIE)**
   - Vérification de la casse et de l'uniformité des sigles (CADA, CPAM, ERP, FGTI, SDIS, SIE, URSSAF).
   - *Correction apportée* : Des normalisations de casse ont été appliquées pour garantir une utilisation stricte en majuscules (ex: cpam -> CPAM, urssaf -> URSSAF) si des variations mineures étaient présentes.

5. **Adresses des organismes**
   - Les courriers destinés aux organismes publics (CPAM, URSSAF, Inspection du Travail, SIE, etc.) ne contiennent pas d'adresses en clair dans le corps du texte (en dehors des informations tokenisées), celles-ci étant gérées par les en-têtes YAML (ex: `destinataire: CPAM Haute-Garonne`, `destinataire: URSSAF Midi-Pyrenees`, `destinataire: Service des Impôts des Entreprises de **[La Ville de l'Accident]**`) ou de manière générique.

## Conclusion
L'audit a permis de relever et corriger quelques fuites d'anonymisation restantes relatives à la ville ("Foix") rattachée aux juridictions compétentes. Les courriers 03 à 34 sont désormais pleinement cohérents et respectent la table de tokens définie dans [🧠 Memory/TOKEN MAP.md](../../../🧠%20Memory/TOKEN%20MAP.md).