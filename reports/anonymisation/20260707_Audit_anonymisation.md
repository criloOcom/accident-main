# Audit d'Anonymisation

**Date :** 2026-07-07
**Périmètre :** `actes/token/` (récursif)

Ce rapport liste toutes les occurrences de données nominatives, adresses, numéros de téléphone, emails et noms d'entreprises réelles identifiées lors de l'audit et qui ont été remplacées par des tokens d'anonymisation.

## Fichier : `actes/token/01_Actes_proceduraux/02 🚔 Plainte.md`
- Détection(s) : Adresse
  > `14 Boulevard du Sud — BP 50078` remplacé par `**[Adresse Tribunal Judiciaire]**`

## Fichier : `actes/token/02_Courriers/08 ✉️ Courrier Suivi Adjoint Maire.md`
- Détection(s) : Code postal et Adresse
  > `09000` remplacé par `**[Code Postal de l'Accident]**`
  > `45, cours Gabriel Fauré` remplacé par `**[Adresse de la Mairie]**`

## Fichier : `actes/token/02_Courriers/10 ✉️ Courrier Doyen Juges Instruction.md`
- Détection(s) : Ville et Adresse
  > `Foix` remplacé par `**[La Ville de l'Accident]**`
  > `14 Boulevard du Sud — BP 50078` remplacé par `**[Adresse Tribunal Judiciaire]**`

## Fichier : `actes/token/03_Analyses_juridiques/13 📜 Responsabilites legales.md`
- Détection(s) : Noms d'entreprise et Villes
  > `SAS LES MAUVAIS GARÇONS` remplacé par `**[L'Exploitant du Commerce (La SAS)]**`
  > `Foix` remplacé par `**[La Ville de l'Accident]**`
  > `Toulouse` remplacé par `**[La Métropole Régionale]**`

## Fichier : `actes/token/04_Etudes_indemnisation/12 Évaluation Dintilhac détaillée.md`
- Détection(s) : Villes
  > `Toulouse` remplacé par `**[La Métropole Régionale]**`
  > `Foix` remplacé par `**[La Ville de l'Accident]**`

## Fichier : `actes/token/05_Organisation/10 🗂️ Plan action.md`
- Détection(s) : Téléphones et Adresses
  > `05 61 65 75 00` remplacé par `**[Téléphone Tribunal Judiciaire]**`
  > `05 61 65 73 00` remplacé par `**[Téléphone Commissariat]**`
  > `05 61 65 70 70` remplacé par `**[Téléphone Huissier]**`
  > `05 61 65 00 10` remplacé par `**[Téléphone Ordre Avocats]**`
  > `2 Rue des Déportés` remplacé par `**[Adresse Tribunal Judiciaire]**`
  > `8 Avenue du 19 Mars 1962` remplacé par `**[Adresse Commissariat]**`

## Fichier : `actes/token/05_Organisation/20 📦 Bon envoi physique.md`
- Détection(s) : Adresse
  > `14 Boulevard du Sud — BP 50078` remplacé par `**[Adresse Tribunal Judiciaire]**`

## Fichier : `actes/token/06_Archives/🛡️ Constitution Partie Civile.md`
- Détection(s) : Code postal et Adresse
  > `09000` remplacé par `**[Code Postal de l'Accident]**`
  > `10 Rue du Palais` remplacé par `**[Adresse Tribunal Judiciaire]**`
