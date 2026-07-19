---
title: "Rapport d'Audit Tokens et Cohérence"
date: 2026-07-18
description: "Vérification de la cohérence de l'ensemble des tokens d'anonymisation, avec un focus sur le nouveau token **[Le Téléphone du Préposé]**."
type: rapport
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [📊 Rapports](./README.md) › RAPPORT_AUDIT_TOKENS_2026-07-18*
<hr>

# Rapport d'Audit Tokens et Cohérence

Ce rapport présente l'audit du système de tokens d'anonymisation du dossier, réalisé le 18 juillet 2026, suite à l'introduction du nouveau token `**[Le Téléphone du Préposé]**`. Il évalue la complétude du mapping, l'implémentation de la double strate (Token/Réel), le déploiement du nouveau token et les éventuelles fuites de données réelles.

<hr><hr>

## 1. Matrice de complétude `TOKEN MAP.md` et fiches individuelles

L'analyse comparative entre `🧠 Memory/TOKEN MAP.md` et les fiches individuelles du dossier `🧠 Memory/🗂️ Tokens/` révèle une architecture globalement structurée, mais avec des désynchronisations.

- **Tokens répertoriés dans la MAP :** 69 tokens (identifiés sous la forme `[**[Token]**]`).

- **Nouveau token :** Le token `**[Le Téléphone du Préposé]**` est bien listé et correctement déclaré.

- **Fiches existantes :** 85 fiches MD ont été trouvées, incluant `token-exploitation-prepose-telephone.md` et la mise à jour de `token-exploitation-prepose-nom.md`.

- **Incohérences dans l'index :** Le fichier `🧠 Memory/🗂️ Tokens/README.md` liste manuellement les fiches et n'est pas à jour vis-à-vis de la carte principale. Les 9 tokens suivants (issus de la MAP) n'y figurent pas :

  - `**[SIREN du Nouvel Exploitant]**`
  - `**[Le Nouvel Exploitant (HB BARBER)]**`
  - `**[Capital du Nouvel Exploitant]**`
  - `**[N° Dossier CPAM]**`
  - `**[SIRET de l'Exploitation]**`
  - `**[Le Président du Nouvel Exploitant]**`
  - `**[J+54]**`
  - `**[N° PV Police]**`
  - `**[Identifiant du Nouvel Exploitant]**`

<hr><hr>

## 2. Validation de la Double Strate (Scripts)

L'anonymisation et la génération des versions réelles reposent sur deux scripts clés. L'audit révèle que ces scripts ne prennent pas en charge l'ensemble des 69 tokens documentés.

### Script `generate_real_versions.py`
Le script contient bien le nouveau token `**[Le Téléphone du Préposé]**`, mais **11 tokens documentés dans la MAP sont absents** de sa table de conversion :
- `**[Capital Social de l'Exploitation]**`

- `**[Code Postal de l'Accident]**`

- `**[Date de naissance de la victime]**`

- `**[J+27 Confirmation kiné]**`

- `**[J+36 Lettre consolidation]**`

- `**[J+38 Mise à jour]**`

- `**[J+41 Courrier SIE URSSAF]**`

- `**[J+41 Requête Constat 145]**`

- `**[J+54]**`

- `**[Prénom de la Victime]**`

- `**[Âge de la Victime]**`

### Script `batch_anonymize.py`
Le script omet **38 tokens** présents dans la MAP. Parmi les absences notables, on retrouve la majorité des dates événementielles (ex: `J+0 Accident`, `J+31 Mises en demeure`) ainsi que des tokens structurels (`Code Postal de l'Accident`, `Le Téléphone de la Victime`, `SIREN de l'Exploitation`).

<hr><hr>

## 3. Déploiement du nouveau token

Le nouveau token `**[Le Téléphone du Préposé]**` a été intégré dans le dossier de manière étendue.

- **Nombre d'insertions :** Le token est présent dans **22 fichiers** distincts au sein du répertoire `⚖️ Actes/🔑 Token/`.

- L'objectif mentionnait 26 fichiers, il y a donc potentiellement 4 fichiers où le token devrait figurer et où il est absent ou remplacé par une autre expression, mais son utilisation reste massive dans les courriers, mémos stratégiques et notes de synthèse.

<hr><hr>

## 4. Fuites détectées (Données réelles)

Une recherche ciblée sur les données réelles du préposé (Ayoub Bennourine, ainsi que ses numéros de téléphone) dans le sous-dossier sécurisé `⚖️ Actes/🔑 Token/` a révélé **3 fichiers non expurgés**, constituant un échec critique d'anonymisation.

Les fuites d'identités réelles ont été détectées dans les fichiers suivants :
- `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/📋 Preparation Foix/📋 Note Personnelle Commissariat Foix.md` (Fuite du prénom "AYOUB")

- `⚖️ Actes/🔑 Token/📚 Analyses juridiques/📜 Note Synthese Avocat Bascule HB BARBER.md` (Fuite du prénom/nom "Ayoub B.")

- `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/📋 Preparation Foix/📋 Projet Declaration PV Foix.md` (Fuite du prénom "AYOUB B" et du téléphone réel "+33 7 58 40 12 87")

<hr><hr>

## 5. Faux envois (TODOs identifiés)

Conformément aux directives générales : plusieurs documents dans le dossier peuvent comporter des mentions de type « ✅ Déposé », « Transmis », ou « Envoyé ». Il convient de noter que ces mentions sont factices dans l'état actuel de l'affaire et correspondent à des actions non accomplies (notamment la demande d'Aide Juridictionnelle).

<hr><hr>

## 6. Plan d'action recommandé

Pour sécuriser définitivement l'architecture d'anonymisation, les actions suivantes sont requises :

- **Étape 1 :** Assainir immédiatement les 3 fichiers présentant des fuites en y remplaçant "Ayoub", "AYOUB B" et le numéro "+33 7 58 40 12 87" par les tokens officiels.

- **Étape 2 :** Mettre à jour `generate_real_versions.py` pour y inclure les 11 tokens manquants.

- **Étape 3 :** Mettre à jour `batch_anonymize.py` pour y intégrer l'ensemble des 38 tokens manquants.

- **Étape 4 :** Régulariser le `README.md` du dossier Tokens pour qu'il s'aligne fidèlement sur `TOKEN MAP.md`.
