---
title: "Rapport d'Audit — Structuration des En-têtes YAML"
description: "État des lieux, structure canonique et feuille de route corrective pour la standardisation des front matter YAML dans le dépôt accident-main."
type: rapport
date: 2026-07-13
tags:
  - audit
  - YAML
  - standardisation
  - métadonnées
statut: final
---

# 📋 RAPPORT D'AUDIT SUR LA STRUCTURATION DES EN-TÊTES YAML

**Projet :** accident-main

**Date :** 13 juillet 2026

---

## I — ⚠️ ÉTAT DES LIEUX & FAIBLESSES DÉTECTÉES

L'analyse croisée des scripts de standardisation (`yaml_schema.py`) et des règles de gouvernance du projet (`RULES.md`) met en évidence trois faiblesses majeures :

1. **Hétérogénéité des métadonnées :** Certains fichiers (comme les index de documentation ou les notes) possèdent un en-tête minimaliste (`title`, `description`, `type`), alors que les courriers et actes procéduraux nécessitent des couples clé/valeur beaucoup plus spécifiques (`date`, `statut`, `auteur`, `destinataire`) pour garantir leur valeur probante.

2. **Erreurs de qualification de statuts :** Plusieurs fichiers portent abusivement la mention `statut: final` dans leur YAML alors qu'ils contiennent encore des crochets de texte non résolus (`[À compléter]`, `[Adresse]`) ou qu'ils ne disposent d'aucune preuve matérielle de dépôt ou d'envoi postal (numéro LRAR).

3. **Absence de traçabilité temporelle & procédurale :** Il manque actuellement de manière systématique des champs permettant de connaître la chronologie de modification et la position exacte du document dans l'arbre d'ordonnancement de la procédure (ex: jalons d'envoi théoriques type `J+31`, `J+37`).

### I.1 — Chiffres clés

| Métrique | Valeur |
|----------|--------|
| Fichiers `.md` totaux | 658 |
| Fichiers avec YAML | 427 |
| Fichiers sans YAML | 231 (ignorés — pièces brutes) |
| Types distincts utilisés | 22 (13 canoniques, 9 non-canoniques) |
| Valeurs de `statut` distinctes | 8 |
| Fichiers avec `statut: final` mais placeholders non résolus | 11 |
| Fichiers sans `proof_delivery` (sur 50 `final`) | 50 (100 %) |
| Fichiers `source: drive` sans `drive_id` | 4 |

---

## II — 🎯 STRUCTURE CANONIQUE UNIFIÉE

Désormais, tout fichier `.md` du dépôt doit respecter l'ordre canonique strict en **Ligne 1** (pour assurer le rendu correct sur l'interface GitHub).

Voici le gabarit complet et exhaustif qui sert de modèle de référence :

```yaml
---
title: "Titre explicite et lisible du document"
description: "Résumé succinct mais complet du contenu (pas de mention 'null' ou 'None')"
type: "loi|jurisprudence|courrier|assignation|plainte|analyse_juridique|etude_indemnisation|rapport|readme|memory|status|preuve|archive|fiche|document|directory"
statut: "final|projet|brouillon|preparation|envoye|archive|fusionne"

# Métadonnées Temporelles & Évolution
date: YYYY-MM-DD
date_creation: YYYY-MM-DD        # Optionnel — injecté sélectivement
date_modification: YYYY-MM-DD    # Optionnel — injecté sélectivement
jalon_procedure: "J+XX"          # Alias: jx (conservé)

# Acteurs concernés (Obligatoire pour courriers/actes)
auteur: "[Token de l'auteur]"
destinataire: "[Token du destinataire]"

# Liens croisés & Traçabilité (Obligatoire pour les dossiers synchronisés)
reel_path: "../../👤 Reel/chemin_relatif_vers_fichier_reel.md"
token_path: "../../🔑 Token/chemin_relatif_vers_fichier_token.md"

# Traçabilité des Preuves & Sources
drive_id: "ID_GOOGLE_DRIVE_EXCLUSIF"
proof_delivery: "870014XXXXXXXXX"   # Optionnel — numéro de suivi LRAR/AR
source: "Légifrance|Judilibre|Pièce brute|drive|local"
last_verified: YYYY-MM-DD          # Optionnel

# Variables d'extraction d'Audits (Selon le type)
tags:
  - "Nomenclature Dintilhac"
  - "RNE"
---
```

### II.1 — Types canoniques

| Type | Description | Utilisation |
|------|-------------|-------------|
| `loi` | Article de code juridique | `📜 Lois/` |
| `jurisprudence` | Décision de justice (arrêt) | `📜 Lois/📜 Jurisprudence/` |
| `courrier` | Courrier / correspondance | `✉️ Courriers/` |
| `assignation` | Acte d'assignation en justice | `⚖️ Actes proceduraux/` |
| `plainte` | Plainte pénale | Procédure pénale |
| `analyse_juridique` | Analyse ou mémorandum juridique | `📚 Analyses juridiques/` |
| `etude_indemnisation` | Étude d'indemnisation (Dintilhac) | `💰 Etudes indemnisation/` |
| `rapport` | Rapport d'audit ou d'expertise | `📊 Rapports/` |
| `readme` | Fichier d'index / porte d'entrée | README.md, `🗂️ Organisation/` |
| `memory` | Fichier mémoire du projet | `🧠 Memory/` |
| `status` | Suivi d'état d'envoi | `🚦 Status/` |
| `preuve` | Pièce de preuve brute | `📂 Preuves officielles/` |
| `archive` | Document archivé | `🗄️ Archives/` |
| `fiche` | Fiche réflexe / note | Guides, checklists |
| `document` | Document général | Fichiers divers |
| `directory` | Index de répertoire | README d'index de sous-dossiers |

### II.2 — Statuts canoniques

| Statut | Signification |
|--------|---------------|
| `final` | Document finalisé, envoyé ou prêt à l'emploi |
| `projet` | Version projet, en attente de relecture/validation |
| `brouillon` | En cours de rédaction ou d'édition |
| `preparation` | En préparation (checklists, plannings) |
| `envoye` | Document envoyé (LRAR, email, dépôt) |
| `archive` | Document historique conservé pour référence |
| `fusionne` | Fusionné dans un autre document |

---

## III — CARTE DES CORRECTIONS

### III.1 — 3.1 Types non-canoniques à normaliser (9 types, 36 fichiers)

| Ancien type | Nouveau type | Fichiers concernés |
|-------------|--------------|-------------------|
| `analyse` (4) | `analyse_juridique` | Mémoires / tableaux de défense |
| `requete` (2) | `assignation` | Requête Article 145 CPC |
| `organisation` (2) | `readme` | Bordereau pièces |
| `guide_personnel` (2) | `readme` | Guide dialogue police |
| `guide` (2) | `readme` | Guide demande AJ |
| `checklist_personnelle` (2) | `readme` | Checklist déplacement |
| `antisèche` (2) | `readme` | Antisèche orale |
| `gouvernance` (1) | `memory` | GESTIONNAIRE_DOC.md |
| `directory` (20) | _Conservé — ajouté aux types canoniques_ | README d'index |

### III.2 — 3.2 Statuts non-canoniques à normaliser

| Ancien statut | Nouveau statut | Fichiers |
|---------------|---------------|----------|
| `obsolète_ne_pas_relancer` (2) | `archive` | Saisine FGTI + Opposition Radiation TC |

### III.3 — 3.3 Faux `statut: final` à rétrograder en `projet` (11 fichiers)

| Fichier | Raison |
|---------|--------|
| `🔄 CPAM.md` | `[Adresse à compléter]` |
| `🔄 Police Videos.md` | `[Adresse à compléter]` |
| `✉️🔄 Consolidation.md` | `[Adresse à compléter]` |
| `✉️🔄 Inspection Travail.md` | `[Date d'envoi — À compléter]` |
| `✉️🔄 Préfecture CODAF.md` | `[Date d'envoi — À compléter]` |
| `✉️🚨 INPI.md` | `[Adresse à compléter]` |
| `✉️🚨 Prefecture.md` | `[Adresse à compléter]` |
| `✉️🚨 SDIS.md` | `[Adresse à compléter]` |
| `✉️🚨 SIE.md` | `[Adresse à compléter]` |
| `✉️⚖️ CPAM Recours Tiers.md` | `[Adresse à compléter]` |
| `⚡ ActionDirecte AssureurRC.md` | `[Adresse à compléter]` |

### III.4 — 3.4 `drive_id` manquants (4 fichiers avec `source: drive`)

| Fichier |
|---------|
| `📑 Bordereau Unifie.md` |
| `📅 Calendrier Procedure.md` |
| `🧠 STRATEGIE Contentieux Civil.md` |
| `🧠 STRATEGIE Contentieux Penal.md` |

---

## IV — 🛠️ FEUILLE DE ROUTE CORRECTIVE

### IV.1 — Étape 1 — Mise à jour du schéma (`yaml_schema.py`)

- Ajouter `directory` aux types canoniques
- Ajouter la validation stricte des `statut` et `type`
- Ajouter les champs optionnels : `date_creation`, `date_modification`, `proof_delivery`
- Ajouter les mappings de normalisation des types non-canoniques

### IV.2 — Étape 2 — Injection sélective (`inject_optional_yaml_fields.py`)

Script dédié pour ajouter les champs optionnels (`date_creation`, `date_modification`, `proof_delivery`, `last_verified`) uniquement aux fichiers qui en ont besoin (courriers, actes, analyses juridiques).

### IV.3 — Étape 3 — Corrections manuelles automatisées

- Rétrograder 11 faux `statut: final` en `projet`
- Normaliser 8 types non-canoniques
- Normaliser 1 statut non-canonique (`obsolète_ne_pas_relancer` → `archive`)

### IV.4 — Étape 4 — Pipeline d'exécution

```bash
python3 .dev/app/update_status_system.py
python3 .dev/app/add_drive_links.py --apply
python3 .dev/app/check_consistency.py
python3 .dev/app/generate_real_versions.py
```

---

## V — SCRIPTS EXISTANTS AUDITÉS

| Script | Rôle | Statut |
|--------|------|--------|
| `yaml_schema.py` | Schéma YAML canonique + normalisation | À enrichir |
| `update_status_system.py` | Liens croisés Token/Reel + index des statuts | Opérationnel |
| `add_drive_links.py` | Ajout liens Drive cliquables dans le corps | Opérationnel |
| `check_consistency.py` | Validation globale du dépôt | Opérationnel |
| `generate_real_versions.py` | Génération versions réelles depuis tokens | Opérationnel |
