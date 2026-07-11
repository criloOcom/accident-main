<!-- [🏠](../README.md) > 📁 [ 📊_Rapports ](....../README.md) > 📁 [ 🗄️_Archives ](..../README.md) > 📁 [ audit ](../README.md) > 📄 [ RAPPORT_AUDIT_RGPD.md ](.RAPPORT_AUDIT_RGPD.md) -->
---
title: "Audit RGPD et Anonymisation — Dossier Accident de la Main"
description: "Le dossier juridique manipule des données à caractère personnel (DCP) hautement sensibles, notamment des données de santé (dossiers médicaux, préjudices corporels, etc.) soumises à l'article 9 du RGPD. Le risque principal réside dans la compromission"
type: rapport
---

# Audit RGPD et Anonymisation — Dossier Accident de la Main

## 1. Bilan des risques

Le dossier juridique manipule des données à caractère personnel (DCP) hautement sensibles, notamment des données de santé (dossiers médicaux, préjudices corporels, etc.) soumises à l'article 9 du RGPD. Le risque principal réside dans la compromission de ces données en cas d'accès non autorisé au dépôt GitHub, qui est par nature un environnement moins sécurisé qu'un coffre-fort numérique qualifié.

L'architecture à double strate (fichiers "token" contenant des pseudonymes et fichiers "réels" générés localement) est une excellente initiative de _Privacy by Design_. Toutefois, l'audit a révélé des failles significatives dans sa mise en œuvre, exposant les identités réelles des parties prenantes. La publication ou le partage de ce dépôt en l'état constituerait une violation de données au sens de l'article 33 du RGPD.

## 2. Fuites de données détectées

L'analyse des fichiers du répertoire `⚖️_Actes/🔑_Token/` a mis en évidence plusieurs fuites de données où les identités réelles ou des informations directement identifiantes ont échappé au processus d'anonymisation :

**Fichier : `⚖️_Actes/🔑_Token/06_🗄️_Archives/annexes/📚 ANNEXE A Lexique Tokens.md`**
Ce fichier centralise l'ensemble de la correspondance entre les tokens et les données réelles. Sa présence même dans le répertoire "token" annule l'intérêt de la double strate, car il permet la ré-identification immédiate de l'ensemble des acteurs.
*   **Fuites :** Sébastien GRAZIDE, Sabir MOUNTASSER, Catherine ANDISSAC, Ayoub BENNOURINE, Romain DELRIEU, Dr Iskander DJERBI, Dr Julie JARDON, Dr Yogan OXYBEL, Sigrid DESBOIS, SAS LES MAUVAIS GARÇONS.
*   **Données identifiantes :** adresses (10 Avenue de Purpan, 22 Rue Lafaurie, 108 Avenue Paul Bert), SIREN/SIRET (938 033 222, 938 033 222 00010, 500 474 457), N° Dossier CPAM (31727387), N° PV Police (2026/015967), email (sebastien.grazide@gmail.com).

**Fichier : `⚖️_Actes/🔑_Token/05_🗂️_Organisation/00 📇 Index.md`**
*   Ligne 101 : `2026-07-05 - 25 📧 Relance Dr DJERBI - V1 ✓ Vérifié` (Nom du médecin). — **⏳ ⏳ À FAIRE PAR SÉBASTIEN (Envoyer le courrier de relance pour certificat de consolidation)**

**Fichier : `⚖️_Actes/🔑_Token/01_⚖️_Actes_proceduraux/05 🎯 Conclusions Refere.md`**
*   Lignes 58 et 80 : Mention en clair du numéro de PV de police `2026/015967`.

**Fichier : `⚖️_Actes/🔑_Token/03_📚_Analyses_juridiques/14 Stratégie jurisprudentielle.md`**
*   Ligne 141 : Mention en clair du numéro de PV de police `n°2026/015967`.

## 3. Évaluation technique : `batch_anonymize.py` et `generate_real_versions.py`

**`batch_anonymize.py` (Script d'anonymisation)**
*   **Méthodologie :** Le script utilise une approche basique de remplacement de chaînes de caractères (`str.replace()`) basée sur un dictionnaire statique.
*   **Vulnérabilités :**
    *   **Sensibilité à la casse et à la syntaxe :** Il ne capture pas les variations de casse (ex: "Grazide" vs "GRAZIDE") non prévues, les fautes de frappe ou les formats inattendus (ex: "Monsieur S. Grazide").
    *   **Prénoms isolés :** Les remplacements portent souvent sur les noms complets. Si un document utilise uniquement le prénom ("Sébastien a déclaré..."), il ne sera pas anonymisé.
    *   **Données indirectement identifiantes :** Les numéros de téléphone, IBAN ou plaques d'immatriculation non explicitement listés passeraient au travers.

**`generate_real_versions.py` (Génération des fichiers réels)**
*   **Sécurité :** Ce script ne pose pas de problème en soi, à condition que le répertoire de sortie (`⚖️_Actes/👤_Reel/`) soit strictement exclu du contrôle de version via `.gitignore` pour éviter tout commit accidentel des données en clair. C'est le cas actuellement.

## 4. Conformité CNIL et Juridique

Le traitement actuel des données personnelles dans ce projet pose plusieurs problèmes de conformité vis-à-vis du RGPD et des recommandations de la CNIL :

*   **Pseudonymisation vs. Anonymisation :** Le processus mis en place est de la **pseudonymisation** et non de l'anonymisation. La CNIL définit l'anonymisation comme un processus irréversible. Or, la présence de `TOKEN MAP.md` et de `ANNEXE A Lexique Tokens.md` permet de ré-identifier les personnes. Les données pseudonymisées restent des données personnelles soumises au RGPD.
*   **Sécurité des données de santé :** Les données médicales exigent un niveau de sécurité accru. Stocker des données de santé, même pseudonymisées si la clé de ré-identification est facilement accessible dans le même environnement, est un risque majeur.
*   **Registre des activités de traitement :** En tant qu'avocat ou professionnel du droit, le responsable du traitement doit tenir un registre des activités de traitement (Article 30 du RGPD).
*   **Information des personnes concernées :** Les personnes (clients, parties adverses) doivent être informées du traitement de leurs données (Articles 13 et 14 du RGPD).

## 5. Recommandations techniques et juridiques

### Recommandations Techniques

1.  **Suppression immédiate de `ANNEXE A Lexique Tokens.md` du répertoire `token` :** La clé de ré-identification (`TOKEN MAP.md` ou autre) ne doit **jamais** être stockée dans les mêmes répertoires de travail que les documents pseudonymisés. Elle devrait idéalement être stockée hors du dépôt, par exemple dans un gestionnaire de secrets ou un fichier local chiffré, et injectée lors de la génération.
2.  **Amélioration de `batch_anonymize.py` :**
    *   Remplacer `str.replace()` par des expressions régulières (`re.sub()`) pour gérer la casse (`re.IGNORECASE`) et les variations syntaxiques.
    *   Ajouter des règles regex génériques pour capter les formats standards de données sensibles (emails, numéros de sécurité sociale, numéros de téléphone, numéros de dossier CPAM/Police) même s'ils ne sont pas dans la liste statique.
3.  **Correction des fuites identifiées :** Remplacer les occurrences restantes de "DJERBI" et "2026/015967" dans les fichiers markdown mentionnés.
4.  **Vérification automatisée continue :** Intégrer le script `audit_rgpd.py` dans le pipeline d'intégration continue (ex: hooks pre-commit) pour bloquer tout commit contenant des motifs identifiants.

### Recommandations Juridiques

1.  **Chiffrement au repos :** Chiffrer le dépôt entier si possible, ou au moins les répertoires contenant les clés de ré-identification (`🧠_Memory/TOKEN MAP.md` et `🧠_Memory/STRICT VARIABLES.md`), en utilisant des outils comme `git-crypt` ou `SOPS`.
2.  **Hébergement :** S'assurer que le service d'hébergement Git utilisé (ex: GitHub) présente les garanties nécessaires (DPA - Data Processing Agreement). Éviter à tout prix les dépôts publics.
3.  **Minimisation des données :** Ne conserver dans `STRICT VARIABLES.md` que les données strictement nécessaires au traitement du dossier.
4.  **Délai de conservation :** Définir et appliquer une politique de purge des données une fois le dossier juridique clos et les délais de prescription échus.

### Annexe : Google Drive

Concernant la synchronisation Google Drive mentionnée dans les directives du projet, il est impératif que **seules les versions token** soient stockées sur Google Drive, dans la mesure où le Drive est utilisé comme espace de travail collaboratif potentiellement exposé. Si des documents du répertoire `⚖️_Actes/👤_Reel/` sont synchronisés, cela constitue une violation de la politique de sécurité du projet et du RGPD.
