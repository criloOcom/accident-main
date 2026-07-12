---
title: "RAPPORT D'ANONYMISATION — DOSSIER ACTES/TOKEN/"
description: "L'objectif de cet audit est de s'assurer de l'intégrité absolue de l'anonymisation des documents contenus dans le répertoire [⚖️ Actes/🔑 Token](⚖️%20Actes/🔑%20Token/README.md) conformément à la table de correspondance définie dans [TOKEN MAP.md](file:///home/crilocom/accident-main"
type: rapport
---











<!-- Breadcrumb -->
[🏠](../../../README.md) › [📊 Rapports et Analyses](../../README.md) › [📁 🗄️ Archives](../README.md) › [📁 audit](./README.md) › AGENT-08 anonymisation
<!-- /Breadcrumb -->

# RAPPORT D'ANONYMISATION — DOSSIER ACTES/TOKEN/

## 1. Objectif et Contexte
L'objectif de cet audit est de s'assurer de l'intégrité absolue de l'anonymisation des documents contenus dans le répertoire [⚖️ Actes/🔑 Token](⚖️%20Actes/🔑%20Token/README.md) conformément à la table de correspondance définie dans [TOKEN MAP.md](../../../🧠%20Memory/TOKEN%20MAP.md). Aucun nom réel, prénom, adresse, adresse courriel ou donnée localisante/identifiante ne doit subsister dans ces fichiers de diffusion.

---

## 2. Synthèse des Résultats
Bien que la majorité des documents de travail et courriers principaux respectent les consignes d'anonymisation, **plusieurs fuites de données sensibles substantielles** ont été détectées au sein du répertoire [⚖️ Actes/🔑 Token](⚖️%20Actes/🔑%20Token/README.md).

Les fuites identifiées se répartissent en 5 catégories :
1. **Noms de personnes physiques** : Persistance des noms de praticiens médicaux (Dr DJERBI, Dr JARDON, Dr OXYBEL). — **⏳ ⏳ À FAIRE PAR SÉBASTIEN (Envoyer le courrier de relance pour certificat de consolidation)**
2. **Données localisantes (géographie et adresses)** : Présence en clair de la ville de "Foix", du quartier/hôpital "Purpan", et de la métropole "Toulouse".
3. **Noms de personnes morales** : Persistance de la mention de "SAS Les Mauvais Garçons".
4. **Identifiants techniques** : Numéro SIRET de la victime en clair, numéro de dossier CPAM.
5. **Lexique complet de correspondance** : Présence de l'Annexe A contenant la totalité des correspondances entre tokens et données réelles au sein même de l'arborescence des actes anonymisés.

---

## 3. Détail des Fuites de Données Identifiées

| Fichier | Ligne(s) | Contenu trouvé | Type de fuite | Token de remplacement ou Correction suggérée |
| :--- | :--- | :--- | :--- | :--- |
| [01_Dossier_UMJ_Preparation.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/📂 Preuves officielles/01_Dossier_UMJ_Preparation.md) | 4 | `**Lieu :** UMJ Purpan` | Donnée géographique | `**Lieu :** UMJ de **[La Métropole Régionale]**` |
| [01_Dossier_UMJ_Preparation.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/📂 Preuves officielles/01_Dossier_UMJ_Preparation.md) | 17, 20, 29, 47, 48 | `Dr DJERBI` | Nom médecin | `**[Le Chirurgien SOS Main]**` | — **⏳ ⏳ À FAIRE PAR SÉBASTIEN (Envoyer le courrier de relance pour certificat de consolidation)**
| [01_Dossier_UMJ_Preparation.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/📂 Preuves officielles/01_Dossier_UMJ_Preparation.md) | 18, 19, 49, 50 | `Dr JARDON` | Nom médecin | `**[Le Médecin en Urgence]**` |
| [01_Dossier_UMJ_Preparation.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/📂 Preuves officielles/01_Dossier_UMJ_Preparation.md) | 23, 51 | `Dr OXYBEL` | Nom médecin | `**[Le Médecin Généraliste]**` |
| [01_Dossier_UMJ_Preparation.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/📂 Preuves officielles/01_Dossier_UMJ_Preparation.md) | 40 | `(RCT 31727387)` | Identifiant CPAM | `(RCT **[N° Dossier CPAM]**)` |
| [04_Bordereau_Audience.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/04_Bordereau_Audience.md) | 55, 56 | `UMJ de Purpan` / `Purpan` | Donnée géographique | `UMJ de **[La Métropole Régionale]**` |
| [08_Courrier Suivi TAVELLA.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/✉️ Courriers/08_Courrier%20Suivi%20TAVELLA.md) | Nom du fichier | `TAVELLA` | Nom de famille | Renommer le fichier en `08_Courrier Suivi Adjoint Maire.md` |
| [README.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/✉️ Courriers/README.md) | 22 | `Dr DJERBI` | Nom médecin | `**[Le Chirurgien SOS Main]**` | — **⏳ ⏳ À FAIRE PAR SÉBASTIEN (Envoyer le courrier de relance pour certificat de consolidation)**
| [README.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/✉️ Courriers/README.md) | 28 | `TAVELLA` (dans [Suivi TAVELLA]) | Nom de famille | Modifier en `[Suivi Adjoint Maire]` |
| [14_Courrier CODAF.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/✉️ Courriers/14_Courrier%20CODAF.md) | 92 | `Foix` et `Toulouse` | Données géographiques | `**[La Ville de l'Accident]**` et `**[La Métropole Régionale]**` |
| [15_Courrier SIE.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/✉️ Courriers/15_Courrier%20SIE.md) | 7, 29 | `Foix` | Donnée géographique | `**[La Ville de l'Accident]**` |
| [20_Relance Police.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/✉️ Courriers/20_Relance%20Police.md) | 7, 30 | `Foix` | Donnée géographique | `**[La Ville de l'Accident]**` |
| [25_Email Relance Dr DJERBI.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/✉️ Courriers/25_Email%20Relance%20Dr%20DJERBI.md) | 2 | `Dr DJERBI` | Nom médecin | `**[Le Chirurgien SOS Main]**` | — **⏳ ⏳ À FAIRE PAR SÉBASTIEN (Envoyer le courrier de relance pour certificat de consolidation)**
| [25_Email Relance Dr DJERBI.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/✉️ Courriers/25_Email%20Relance%20Dr%20DJERBI.md) | 32 | `Purpan` | Donnée géographique | `**[La Métropole Régionale]**` | — **⏳ ⏳ À FAIRE PAR SÉBASTIEN (Envoyer le courrier de relance pour certificat de consolidation)**
| [FAQ.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/📚 Analyses juridiques/09_FAQ.md) | 146 | `Purpan` | Donnée géographique | `**[La Métropole Régionale]**` |
| [00_Index.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/🗂️ Organisation/00_Index.md) | 87 | `Dr DJERBI` | Nom médecin | `**[Le Chirurgien SOS Main]**` | — **⏳ ⏳ À FAIRE PAR SÉBASTIEN (Envoyer le courrier de relance pour certificat de consolidation)**
| [00_Index.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/🗂️ Organisation/00_Index.md) | 88, 237 | `TAVELLA` | Nom de famille | `l'Adjoint au Maire` ou `l'Adjoint` |
| [Plan action.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/🗂️ Organisation/10_Plan%20action.md) | 70 | `Purpan` | Donnée géographique | `**[La Métropole Régionale]**` |
| [Plan action.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/🗂️ Organisation/10_Plan%20action.md) | 122 | `Purpan` | Donnée géographique | `**[La Métropole Régionale]**` |
| [ANALYSE_correction_juridique.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/🗄️ Archives/ANALYSE_correction_juridique.md) | 69 | `SAS Les Mauvais Garçons` | Personne morale | `**[L'Exploitant du Commerce (La SAS)]**` |
| [STRATEGIE_Contentieux_Civil.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/🗄️ Archives/STRATEGIE_Contentieux_Civil.md) | 127 | `500 474 457` | Identifiant victime | `**[L'Identifiant Professionnel de la Victime]**` |
| [STRATEGIE_Contentieux_Penal.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/🗄️ Archives/STRATEGIE_Contentieux_Penal.md) | 87 | `btavella@mairie-foix.fr` | Email & nom/ville | `**[L'Email de l'Adjoint au Maire]**` |
| [ANNEXE C Pieces.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/🗄️ Archives/annexes/ANNEXE%20C%20Pieces.md) | 7 | `Pharmacie Foix` | Donnée géographique | `Pharmacie de **[La Ville de l'Accident]**` |

---

## 4. Analyse de l'Substitution (ANNEXE A)
Le fichier [ANNEXE A Lexique Tokens.md](file:///home/crilocom/accident-main/⚖️ Actes/🔑 Token/🗄️ Archives/annexes/ANNEXE%20A%20Lexique%20Tokens.md) contient l'ensemble des clés en clair associées aux jetons génériques :
- Sébastien GRAZIDE
- Sabir MOUNTASSER
- Catherine ANDISSAC / SORROCHE
- Ayoub BENNOURINE
- Romain DELRIEU
- Dr Iskander DJERBI
- Dr Julie JARDON
- Dr Yogan OXYBEL
- Sigrid DESBOIS
- SAS LES MAUVAIS GARÇONS
- Clinique de l'Union
- Adresses réelles complètes, emails, SIRET, SIREN, etc.

> [!IMPORTANT]
> Pour que le dossier [⚖️ Actes/🔑 Token](⚖️%20Actes/🔑%20Token/README.md) soit considéré comme **strictement anonymisé**, l'intégralité du fichier `ANNEXE A Lexique Tokens.md` doit être retiré de ce sous-dossier ou ses correspondances réelles doivent être vidées. La table de correspondance légitime doit résider uniquement dans le dossier de gestion sécurisé [/home/crilocom/accident-main/🧠 Memory/TOKEN MAP.md](../../../🧠%20Memory/TOKEN%20MAP.md).

---

## 5. Recommandations et Plan d'Action
1. **Exécution d'une phase de correction manuelle ou scriptée** : Remplacer l'ensemble des occurrences relevées dans le tableau de la section 3 par leurs tokens respectifs.
2. **Renommage du fichier courrier** : Renommer le fichier `08_Courrier Suivi TAVELLA.md` en `08_Courrier Suivi Adjoint Maire.md` et mettre à jour les liens de navigation dans `🗂️ Organisation/00_Index.md` et `✉️ Courriers/README.md`.
3. **Déplacement / Suppression de l'ANNEXE A** : Supprimer le fichier `⚖️ Actes/🔑 Token/🗄️ Archives/annexes/ANNEXE A Lexique Tokens.md` ou le remplacer par un fichier explicatif listant uniquement les tokens disponibles mais sans leur valeur de décryptage en clair.