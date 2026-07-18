---
title: "RAPPORT D'AUDIT — Courriers (✉️ Courriers)"
description: "Date :** 10 juillet 2026"
type: rapport
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [📊 Rapports et Analyses](./README.md) › RAPPORT AUDIT COURRIERS*
<hr>
<!-- /Breadcrumb -->

# RAPPORT D'AUDIT<br>Courriers (✉️ Courriers)

**Date :** 10 juillet 2026  
**Périmètre :** [⚖️ Actes/🔑 Token/✉️ Courriers](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) (fichiers 03 à 35)  
**Objet :** Vérification structurelle, YAML, tokens non résolus, cohérence inter-courriers, existence des versions réelles

---

## I — TABLEAU SYNTHÉTIQUE

| N° | Titre court | Statut | Source | Token non résolu | Problèmes |
|----|------------|--------|--------|------------------|-----------|
| 03 | Courrier SAS | final | drive | `Finance Provision Référé` | 1 token non résolu |
| 04 | Courrier Assureur | final | drive | `[Adresse à compléter]` | 1 adresse non résolue |
| 05 | Courrier Propriétaire | final | drive | `[Adresse à compléter]` | 1 adresse non résolue |
| 06 | Courrier Président DG | final | drive | `Finance Provision Référé` | 1 token non résolu + titre section sans `#` |
| 06 V2 | Relance Dirigeants | **projet** | local | `DATE RELANCE V2`, `N° LRAR Exploitant`, `N° LRAR Directrice`, `N° LRAR Président`, `DATE REOUVERTURE BOUTIQUE` | **5 tokens non résolus** |
| 07 | Courrier Consolidation | final | drive | `[Adresse à compléter]` | 1 adresse non résolue + accents incohérents |
| 08 | Suivi Adjoint Maire | final | drive | Aucun | OK |
| 09 | Inspection Travail | final | drive | `[Adresse à compléter]`, `[Adresse du Commerce]` | 2 adresses non résolues |
| 10 | Doyen Juges Instruction | final | drive | `[Adresse Tribunal Judiciaire]` | 1 adresse non résolue + `[ ... ]` placeholders |
| 11 | INPI | final | drive | `[Adresse à compléter]` | 1 adresse + doublon token YAML (accentué/non accentuée) |
| 12 | URSSAF | final | drive | Aucun | `[Le Prepose]` en simple crochet (incohérent) |
| 13 | Préfecture | final | drive | `[Adresse à compléter]`, `[Adresse du Commerce]` | 2 adresses non résolues |
| 14 | CODAF | final | drive | Aucun | OK |
| 15 | SIE | final | drive | `[Adresse à compléter]` | 1 adresse + `[La Ville]` simple crochet dans YAML |
| 16 | Conseil Départemental | final | drive | `[Adresse à compléter]`, `[Adresse du Commerce]` | 2 adresses non résolues |
| 17 | CPAM | final | drive | `[Adresse à compléter]` | 1 adresse non résolue |
| 18 | SDIS | final | drive | `[Adresse à compléter]` | 1 adresse non résolue |
| 19 | FGTI | final | drive | Aucun | OK |
| 20 | Relance Police | final | drive | `[Adresse à compléter]` | 1 adresse + simple crochet dans titre |
| 21 | Relance CPAM | final | drive | `[Adresse à compléter]` | 1 adresse non résolue |
| J+32 | Attestation Temoin Client | final | drive | `[À compléter]` (x5) | **Intentionnel** (gabarit) — `destinataire: null` |
| 23 | Attestation Pompier SAMU | final | drive | `[À compléter]` (x5) | **Intentionnel** (gabarit) — `destinataire: null` |
| J+32 | Attestation Employe | final | drive | `[À compléter]` (x5) | **Intentionnel** (gabarit) — `destinataire: null` |
| 25 | Relance Dr DJERBI | **brouillon** | local | Aucun | `[La Métropole Régionale]` en simple crochet + `statut: brouillon` |
| 26 | Email Attestation Témoin | **brouillon** | local | Aucun | `source: local`, single bracket tokens |
| 27 | Email Attestation Pompier | **brouillon** | local | Aucun | `source: local`, single bracket tokens |
| 28 | Email Attestation Employé | **brouillon** | local | Aucun | `source: local`, single bracket tokens |
| 29 | Courrier Maire Foix | final | — | Aucun | **Absence de `source` et `drive_id`** dans YAML |
| 30 | Courrier President TC | final | — | Aucun | **Absence de `source` et `drive_id`** + `[Avocat]` simple crochet |
| 31 | Courrier INPI Opposition | final | — | Aucun | **Absence de `source` et `drive_id`** + `[Avocat]` simple crochet |
| 32 | SIE URSSAF Mutualisation | **projet** | local | `[Adresse à compléter]` | **Fautes YAML** (`La Président`, `Le Directrice`) + 1 adresse |
| 33 | Requête Constat 145 CPC | **projet** | local | `[Adresse du TJ à compléter]` | 1 adresse non résolue + `statut: projet` |
| 34 | EMAIL Maire / Police ERP | **brouillon** | — | Aucun | **Emails réels** `btavella@...` et `secretariat@...` dans fichier token |
| 35 | Courrier President TJ Foix | final | — | Aucun | **Absence de `source` et `drive_id`** |

---

## II — DÉTAIL PAR COURRIER

### II.1 — Courrier SAS (Mise en Demeure)
- **YAML :** Complet. `statut: final`, `source: drive`, `drive_id` présent.

- **Structure :** Objet, introduction, rappel des obligations légales, faits, transparence, formule de politesse. Présent.

- **Token non résolu :** `**[Finance Provision Référé]**` (l. 99) — montant de provision non défini.

- **Observation :** Très bon document de référence.

### II.2 — Courrier Assureur (Action Directe)
- **YAML :** Complet.

- **Structure :** Complète.

- **Token non résolu :** `**[Adresse à compléter]**` (l. 35) — adresse de la compagnie d'assurance manquante.

- **Observation :** Montants chiffrés explicites (59 600 € / 15 000 €). Références jurisprudentielles citées.

### II.3 — Courrier Propriétaire
- **YAML :** Complet. Indentation YAML des `personnes` avec espaces (style différent des autres fichiers).

- **Structure :** Complète.

- **Token non résolu :** `**[Adresse à compléter]**` (l. 28) — adresse du propriétaire.

### II.4 — Courrier Président DG
- **YAML :** Complet.

- **Structure :** Complète mais **titre de section manquant** (l. 135) : `Transparence sur la suite donnée au dossier` — pas de préfixe `##` contrairement aux autres sections.

- **Token non résolu :** `**[Finance Provision Référé]**` (l. 151).

- **Observation :** Même token non résolu que 03 — devrait être harmonisé.

### II.5 — 06 V2 — Relance Dirigeants
- **YAML :** `statut: projet`, `source: local`. Pas de `drive_id`.

- **Structure :** Complète (inclut annexes juridiques).

- **Tokens non résolus (5) :**

  - `**[DATE RELANCE V2]**` (l. 37)
  - `**[N° LRAR Exploitant]**` (l. 50)
  - `**[N° LRAR Directrice]**` (l. 51)
  - `**[N° LRAR Président]**` (l. 52)
  - `**[DATE REOUVERTURE BOUTIQUE]**` (l. 60)
- **Observation :** Nécessite finalisation et passage en `statut: final`.

### II.6 — Courrier Consolidation
- **YAML :** Complet.

- **Token non résolu :** `**[Adresse à compléter]**` (l. 37).

- **Observation :** Incohérence d'accents — le titre dit `Certificat Medical` (sans accent) mais `Médical` ailleurs. 1ère occurrence des tokens `J+37` et `J+55`.

### II.7 — Suivi Adjoint Maire
- **YAML :** Complet. Utilise `Le Commerce de l'Exploitation` comme token de l'enseigne.

- **Structure :** Complète.

- **Token non résolu :** Aucun.

- **Observation :** Référence `Article L. 311-1 CRPA`. Modèle de propreté.

### II.8 — Inspection Travail
- **YAML :** Complet.

- **Tokens non résolus (2) :**

  - `**[Adresse à compléter]**` (l. 32)
  - `**[Adresse du Commerce]**` (l. 43)
- **Observation :** Utilise `[Adresse du Commerce]` sans préfixe `L'`. Cohérent avec 13, 16, 18.

### II.9 — Doyen Juges Instruction
- **YAML :** Complet.

- **Token non résolu :** `**[Adresse Tribunal Judiciaire]**` (l. 38).

- **Observation :** Contient `[ ... ]` (l. 47 et 56) comme placeholders pour numéro de PV — à remplacer par `**[N° PV Police]**`.

### II.10 — INPI
- **YAML :** Doublon dans `personnes` : `La Directrice Generale` (sans accent) ET `La Directrice Générale` (avec accent). Idem pour `Le President` / `Le Président`.

- **Token non résolu :** `**[Adresse à compléter]**` (l. 34).

- **Observation :** Nettoyer les doublons YAML.

### II.11 — URSSAF
- **YAML :** Complet.

- **Token non résolu :** Aucun.

- **Observation :** `[Le Prepose de l'Exploitation]` (l. 43) en **simple crochet** au lieu de `**[...]**` — incohérence de format.

### II.12 — Préfecture
- **YAML :** Complet.

- **Tokens non résolus (2) :**

  - `**[Adresse à compléter]**` (l. 33)
  - `**[Adresse du Commerce]**` (l. 44)
- **Observation :** Bonne structure, sections numérotées claires.

### II.13 — CODAF
- **YAML :** Complet.

- **Token non résolu :** Aucun.

- **Observation :** Adresse réelle de la Préfecture déjà renseignée. Bon document.

### II.14 — SIE
- **YAML :** `[La Ville de l'Accident]` en simple crochet dans la valeur `destinataire` (l. 7 du YAML).

- **Token non résolu :** `**[Adresse à compléter]**` (l. 30).

- **Observation :** Simple crochet dans le YAML (l. 28 du texte aussi : `[La Ville de l'Accident]`).

### II.15 — Conseil Départemental
- **YAML :** Complet.

- **Tokens non résolus (2) :**

  - `**[Adresse à compléter]**` (l. 30)
  - `**[Adresse du Commerce]**` (l. 43)
- **Observation :** Structure claire avec sections numérotées I, II, III.

### II.16 — CPAM
- **YAML :** Complet.

- **Token non résolu :** `**[Adresse à compléter]**` (l. 34).

- **Observation :** Intègre un tableau bordereau bien structuré avec pièces numérotées. Document le plus volumineux.

### II.17 — SDIS
- **YAML :** Complet.

- **Token non résolu :** `**[Adresse à compléter]**` (l. 35).

- **Observation :** Structure simple, sections concises. Utilise `[Adresse du Commerce]`.

### II.18 — FGTI
- **YAML :** Complet.

- **Token non résolu :** Aucun.

- **Observation :** Barème Dintilhac détaillé (105 000 €). Bon document.

### II.19 — Relance Police
- **YAML :** Complet.

- **Token non résolu :** `**[Adresse à compléter]**` (l. 31).

- **Observation :** `[La Ville de l'Accident]` en simple crochet dans la ligne de titre (l. 29).

### II.20 — Relance CPAM
- **YAML :** Complet.

- **Token non résolu :** `**[Adresse à compléter]**` (l. 29).

- **Observation :** Court et concis.

### II.21 — 22, 23, 24 — Gabarits d'Attestations
- **YAML :** `destinataire: null` (statut intentionnel pour gabarits). `statut: final`.

- **Tokens `[À compléter]` :** Intentionnels — le document est un gabarit CERFA.

- **Observation :** Les tokens `**[L'Exploitant du Commerce (La SAS)]**` apparaissent en simple crochet dans les textes d'exemple (l. 36-38).

### II.22 — Relance Dr DJERBI
- **YAML :** `statut: brouillon`, `source: local`.

- **Token non résolu :** Aucun de critique.

- **Observation :** `[La Métropole Régionale]` en simple crochet. Mention `Fichier tokenisé — À envoyer en version réelle`.

### II.23 — 26, 27, 28 — Emails Attestations
- **YAML :** `statut: brouillon`, `source: local`.

- **Observation :** Tokens en simple crochet `[L'Adresse de l'Exploitation]` (l. 18) et `[L'Exploitant du Commerce]` (l. 24).

- **Note :** Chacun mentionne `Joindre le PDF du Cerfa n° 11527*03` — dépendance externe.

### II.24 — Courrier Maire Foix
- **YAML :** `statut: final` mais **absence de `source` et `drive_id`**.

- **Token non résolu :** Aucun.

- **Observation :** Document finalisé mais non versé dans le Drive ? À régulariser.

### II.25 — Courrier President TC
- **YAML :** `statut: final`, `auteur: Nom de l'Avocat de la Victime` (pas `La Victime`). **Absence de `source` et `drive_id`**.

- **Observation :** `[Nom de l'Avocat de la Victime]` en simple crochet. `[La Ville de l'Accident]` en simple crochet dans en-tête.

### II.26 — Courrier INPI Opposition
- **YAML :** Même configuration que 30. **Absence de `source` et `drive_id`**.

- **Observation :** `[Nom de l'Avocat de la Victime]` en simple crochet. Fait référence à `La Victime` comme créancière.

### II.27 — SIE URSSAF Mutualisation
- **YAML :** `statut: projet`, `source: local`.

  - **Fautes :** `Le President de l'Exploitation` (sans accent) + `La Président de l'Exploitation` **(faute d'accord : « La » + « Président »)** + `Le Directrice Generale de l'Exploitation` **(faute d'accord : « Le » + « Directrice »)**.
- **Token non résolu :** `**[Adresse à compléter]**` (l. 36).

- **Observation :** Nécessite correction des genres dans YAML.

### II.28 — Requête Constat 145 CPC
- **YAML :** `statut: projet`, `source: local`.

- **Token non résolu :** `**[Adresse du TJ à compléter]**` (l. 39).

- **Observation :** `[La Ville de l'Accident]` en simple crochet dans en-tête (l. 35). `**[L'Etablissement SOS Main]**` sans accent (incohérent).

### II.29 — EMAIL Maire / Police Municipale ERP
- **YAML :** `statut: brouillon`. `type: email` (catégorisation différente). Pas de `source`.

- **🔴 Alerte :** `btavella@mairie-foix.fr` (l. 13) et `secretariat@mairie-foix.fr` (l. 14) — adresses email réelles dans un fichier tokenisé. Même s'il s'agit d'adresses publiques, leur présence dans la strate token constitue une **anomalie** (le fichier aurait dû rester en strate réelle).

- **Observation :** Chronologie complète des échanges retracée.

### II.30 — Courrier President TJ Foix
- **YAML :** `statut: final` mais **absence de `source` et `drive_id`**.

- **Token non résolu :** Aucun.

- **Observation :** Document de transmission de preuves complémentaires. Mentionne explicitement `PV n°2026/015967` (non tokenisé, acceptable comme n° de procédure).

---

## III — CORRESPONDANCE VERSIONS RÉELLES

Tous les fichiers token (03 à 35) ont leur équivalent réel dans [⚖️ Actes/👤 Reel/✉️ Courriers](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md). ✅

**Fichier manquant côté reel :** `.gitkeep` présent côté token uniquement (normal).

---

## IV — PROBLÈMES TRANSVERSAUX

### IV.1 — `**[Adresse à compléter]**` — 12 occurrences dans 12 fichiers
| Fichier | Ligne |
|---------|-------|
| 04 | 35 |
| 05 | 28 |
| 07 | 37 |
| 09 | 32 |
| 11 | 34 |
| 13 | 33 |
| 15 | 30 |
| 16 | 30 |
| 17 | 34 |
| 18 | 35 |
| 20 | 31 |
| 21 | 29 |
| 32 | 36 |

### IV.2 — `**[Finance Provision Référé]**` — 2 occurrences
- 03 (l. 99) et 06 (l. 151)

### IV.3 — Tokens date/LRAR non résolus dans 06 V2
- 5 tokens créés pour cette version de relance

### IV.4 — Absence de `source`/`drive_id` pour 4 fichiers `statut: final`
- 29, 30, 31, 35

### IV.5 — Incohérence de format `[Token]` vs `**[Token]**`
Observé dans : 12, 15, 20, 22, 25, 26, 27, 28, 30, 31, 33, 34 (plus de 12 fichiers)

### IV.6 — Fautes dans YAML `personnes` — [fichier 32](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9A%96%EF%B8%8F%20Actes%20proceduraux/%F0%9F%93%9C%20Contentieux%20civil/%F0%9F%93%91%20Bordereau%20Unifie.md)
- `La Président de l'Exploitation` (faute d'accord)

- `Le Directrice Generale de l'Exploitation` (faute d'accord)

### IV.7 — 5 fichiers en `statut: projet` ou `brouillon` avec `source: local`
- 06 V2 (projet), 25 (brouillon), 26 (brouillon), 27 (brouillon), 28 (brouillon), 32 (projet), 33 (projet), 34 (brouillon)

### IV.8 — Adresse email réelle dans strate token — [fichier 34](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9A%96%EF%B8%8F%20Actes%20proceduraux/%F0%9F%93%9C%20Contentieux%20civil/%F0%9F%93%91%20Bordereau%20Unifie.md)

---

## V — RECOMMANDATIONS

### V.1 — Prioritaires
1. **Résoudre les `[Adresse à compléter]`** dans les 12 fichiers concernés avec les adresses réelles des destinataires.

2. **Définir et résoudre `[Finance Provision Référé]`** dans la TOKEN MAP, ou le remplacer par un montant fixe comme dans 04 et 19.

3. **Corriger les fautes YAML** dans 32 (`La Président` → `Le Président`, `Le Directrice` → `La Directrice Générale`).

4. **Supprimer les emails réels** de 34 ou déplacer ce fichier en strate réelle uniquement.

5. **Compléter les YAML** de 29, 30, 31, 35 avec `source:` et `drive_id:`.

### V.2 — Structurelles
6. **Harmoniser le format des tokens** : remplacer tous les `[Token]` simples par `**[Token]**` dans le corps des documents.

7. **Nettoyer les doublons YAML** dans 11 (`personnes` avec et sans accents).

8. **Ajouter le `#` manquant** dans 06 (l. 135) pour la section "Transparence".

9. **Remplacer les placeholders `[ ... ]`** dans 10 par `**[N° PV Police]**`.

10. **Finaliser les 6 fichiers en statut projet/brouillon** et les pousser vers le Drive.

### V.3 — Process
11. **Vérifier l'existence des courriers 01 et 02** — la numérotation commence à 03, ce qui suggère des documents manquants ou une numérotation différente dans un autre dossier.

12. **Uniformiser la syntaxe YAML** pour `personnes` (certains fichiers utilisent des listes avec tiret `-`, d'autres des listes indentées).

13. **Ajouter une vérification automatique** dans le pipeline de génération pour détecter les `[À compléter]` résiduels avant passage en `statut: final`.

14. **Créer un token `[Adresse du TJ]`** standardisé dans la TOKEN MAP pour remplacer les variations (`Adresse Tribunal Judiciaire`, `Adresse du TJ à compléter`, etc.).

---

Rapport généré le 10 juillet 2026 — Audit manuel des 33 fichiers de courriers.