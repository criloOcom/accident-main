---
uid: gzHGbNxRw
title: RAPPORT D'AUDIT DE STRUCTURE
date: FIXME
description: "Date :** 10 juillet 2026"
type: rapport
subtitle: RAPPORT D'AUDIT DE STRUCTURE
objective: Auditer et vérifier la conformité de RAPPORT D'AUDIT DE STRUCTURE
summary: "Date :** 10 juillet 2026"
key_points:
  - I — Arborescence complète
  - II — Vérification Token → Reel
  - III — Conformité AGENTS.md
  - IV — Conformité README.md
  - V — Fichiers orphelins / non documentés
  - VI — README.md manquants
tags:
  - audit
  - conformite
  - qualite
  - preuve
  - token
---
<!-- Breadcrumb -->
*[🏠](../../README.md) › [Rapports](../README.md) › [60 Audits Qualite](./README.md) › RAPPORT AUDIT STRUCTURE*
<hr>
<!-- /Breadcrumb -->

# RAPPORT D'AUDIT DE STRUCTURE

**Date :** 10 juillet 2026
**Projet :** accident-main
**Objet :** Vérification complète de l'arborescence, correspondance 🔑/👤, conformité AGENTS.md

---

## I — Arborescence complète

```
📁 /home/crilocom/accident-main/
├── AGENTS.md
├── README.md
├── .gitignore
├── setup.sh
│
├── Actes/
│   ├── README.md
│   ├── Preuves officielles/         ← Pièces brutes source (11 fichiers)
│   ├── Token/                        ← Versions anonymisées
│   │   ├── README.md
│   │   ├── Preuves_officielles/   (1 fichier + .gitkeep)
│   │   ├── Actes_proceduraux/    (11 fichiers)
│   │   ├── Courriers/            (33 fichiers)
│   │   ├── Analyses_juridiques/   (12 fichiers)
│   │   ├── Etudes_indemnisation/  (4 fichiers)
│   │   ├── Organisation/          (11 fichiers)
│   │   └── Archives/             (9 fichiers + annexes/)
│   │       └── annexes/                 (2 fichiers)
│   └── Reel/                         ← Versions réelles
│       ├── README.md
│       ├── Preuves_officielles/   (1 fichier)
│       ├── Actes_proceduraux/    (13 fichiers)
│       ├── Courriers/            (33 fichiers)
│       ├── Analyses_juridiques/   (12 fichiers)
│       ├── Etudes_indemnisation/  (4 fichiers)
│       ├── Organisation/          (11 fichiers)
│       └── Archives/             (7 fichiers — sans annexes/)
│
├── Lois/
│   ├── README.md
│   ├── 24 fiches jurisprudence + articles .md
│   └── pdfs/                           (24 PDFs + 1 supplémentaire)
│
├── Memory/                          (20 fichiers, pas de README.md)
│
├── Rapports/
│   ├── 3 rapports racine
│   ├── audit/                          (2 fichiers)
│   └── Archives/                    (58 fichiers dans 8 sous-dossiers)
│
├── reports/                            ← NON DOCUMENTÉ
│   ├── audit/                          (11 fichiers)
│   ├── expertise/                      (2 fichiers)
│   └── jurisprudence/                  (3 fichiers)
│
├── app/                                ← NON DOCUMENTÉ (≠ .dev/app/)
│   └── 3 fichiers Python
│
├── .dev/
│   ├── app/                            (28 fichiers Python)
│   ├── tests/
│   ├── deployment/
│   └── ...
│
└── .github/workflows/
```

---

## II — Vérification Token → Reel

### II.1 — Preuves_officielles
| Token | Reel | Statut |
|----------|---------|--------|
| `01 Dossier UMJ Preparation.md` | ✅ Présent | OK |
| `.gitkeep` | ❌ Absent | OK (place technique) |
| `README.md` | ✅ Présent | OK |

### II.2 — Actes_proceduraux
| Token | Reel | Statut |
|----------|---------|--------|
| `TJ Foix - TJ Foix - Référé Provision - Assignation.md` | ✅ Présent | OK |
| `02 🚔 Plainte.md` | ✅ Présent | OK |
| `DJI Foix - DJI Foix - Partie Civile - Constitution.md` | ✅ Présent | OK |
| `03 🔍 Assignation Article 145.md` | ✅ Présent | OK |
| `04 📑 Bordereau.md` | ✅ Présent | OK |
| `05 🎯 Conclusions Refere.md` | ✅ Présent | OK |
| `06 Constat Huissier - Requête.md` | ✅ Présent | OK |
| `07 TJ Foix - Référé Provision - Ordonnance Projet.md` | ✅ Présent | OK |
| `15 ⚖️ Réquisitoire introductif.md` | ✅ Présent | OK |
| `Parquet Foix - Signalement Fraude.md` | ✅ Présent | OK |
| `TC Foix - TC Foix - Mandataire Ad Hoc - Requête.md` | ✅ Présent | OK |
| — | ❌ `04 📑 Bordereau Audience.md` | **EXCÉDENT** 👤 |
| — | ❌ `04 📑 Bordereau de pieces.md` | **EXCÉDENT** 👤 |

### II.3 — Courriers
✅ **Correspondance parfaite** (33 fichiers identiques, hors .gitkeep)

### II.4 — Analyses_juridiques
✅ **Correspondance parfaite** (12 fichiers)

### II.5 — Etudes_indemnisation
✅ **Correspondance parfaite** (4 fichiers)

### II.6 — Organisation
✅ **Correspondance parfaite** (11 fichiers)

### II.7 — Archives
| Token | Reel | Statut |
|----------|---------|--------|
| `Archive - Fiche Réflexe 48h Victime.md` | ✅ Présent | OK |
| `Archive - Action Directe Assureur RC.md` | ✅ Présent | OK |
| `Archive - Dossier Présentation.md` | ✅ Présent | OK |
| `Archive - Analyse Jurisprudence.md` | ✅ Présent | OK |
| `Archive - Analyse Correction Juridique.md` | ✅ Présent | OK |
| `DJI Foix - DJI Foix - Partie Civile - Constitution.md` | ✅ Présent | OK |
| `Archive - Stratégie Contentieux Civil.md` | ✅ Présent | OK |
| `Archive - Stratégie Contentieux Pénal.md` | ✅ Présent | OK |
| `annexes/ANNEXE_B_Lois_Jurisprudence.md` | ❌ Absent | **MANQUANT** |
| `annexes/ANNEXE_C_Pieces.md` | ❌ Absent | **MANQUANT** |
| `README.md` | ✅ Présent | OK |

---

## III — Conformité AGENTS.md

| Référence AGENTS.md | Réalité | Conforme ? |
|---------------------|---------|------------|
| `token/` | `Token/` | ❌ Nom différent |
| `reel/` | `Reel/` | ❌ Nom différent |
| `.dev/app/generate_real_versions.py` | ✅ Existe | OK |
| `.dev/app/sync_notebooklm.py` | ✅ Existe | OK |
| `.dev/app/check_consistency.py` | ✅ Existe | OK |
| `.dev/app/batch_anonymize.py` | ✅ Existe | OK |
| `.dev/app/tools.py` | ✅ Existe | OK |
| `.dev/app/agent.py` | ✅ Existe | OK |
| `Preuves_officielles/` (root Actes) | ✅ Existe | OK |
| Structure 00-06 sous `token/` et `reel/` | ✅ Présente | OK |

## IV — Conformité README.md

| Référence README.md | Réalité | Conforme ? |
|---------------------|---------|------------|
| `📦_pieces/` | ❌ **N'EXISTE PAS** | **MANQUANT** |
| `.dev/app/generate_real_versions.py` | ✅ Existe | OK |
| `.dev/app/sync_notebooklm.py` | ✅ Existe | OK |
| `.dev/app/check_consistency.py` | ✅ Existe | OK |
| `.dev/app/drive_client.py` | ✅ Existe | OK |
| `.dev/app/batch_anonymize.py` | ✅ Existe | OK |
| `.dev/app/batch_link_legifrance.py` | ✅ Existe | OK |

---

## V — Fichiers orphelins / non documentés

### V.1 — `reports/` (racine)
Non mentionné dans AGENTS.md ni README.md. Contient 16 rapports qui complètent (et parfois doublonnent) ceux dans [Rapports](../../Actes/Token/README.md).

| Fichier | Aussi présent dans Rapports ? |
|---------|-------------------------------|
| `reports/audit/audit_email_34.md` | ❌ Non |
| `reports/audit/audit_legiarti_actes.md` | ❌ Non |
| `reports/audit/audit_legiarti_courriers.md` | ❌ Non |
| ... (13 autres) | ❌ Non |

### V.2 — `app/` (racine)
Non mentionné dans AGENTS.md ni README.md.

| Fichier | Aussi présent dans .dev/app/ ? |
|---------|-------------------------------|
| `app/__init__.py` | ❌ Non (vide) |
| `app/enhance_markdown.py` | ⚠️ OUI (doublon de `.dev/app/enhance_markdown.py`) |
| `app/add_yaml_actes.py` | ❌ Non |

---

## VI — README.md manquants

| Dossier | README ? |
|---------|----------|
| [Rapports](../../Actes/Token/README.md) | ❌ Absent |
| [Rapports/audit](../../Actes/Token/README.md) | ❌ Absent |
| [Rapports/Archives](../../Actes/Token/README.md) | ❌ Absent |
| [Memory](../../Actes/Token/README.md) | ❌ Absent |
| `reports/` | ❌ Absent |
| `reports/audit/` | ❌ Absent |
| `reports/expertise/` | ❌ Absent |
| `reports/jurisprudence/` | ❌ Absent |
| `app/` | ❌ Absent |
| [Lois/pdfs](../../Actes/Token/README.md) | ❌ Absent |

---

## VII — Synthèse des anomalies

| # | Gravité | Anomalie |
|---|---------|----------|
| 1 | 🔴 **Critique** | `📦_pieces/` mentionné dans README.md (ligne 31) n'existe pas |
| 2 | 🔴 **Critique** | `reports/` en doublon avec [Rapports](../../Actes/Token/README.md) — source de confusion, non documenté |
| 3 | 🟠 **Moyen** | `app/` (racine) non documenté, avec un doublon de `enhance_markdown.py` |
| 4 | 🟠 **Moyen** | Reel/01 a 2 fichiers excédentaires vs Token/01 : `Bordereau Audience.md` et `Bordereau de pieces.md` |
| 5 | 🟠 **Moyen** | Reel/06 manque le dossier `annexes/` (2 fichiers) présent dans Token/06 |
| 6 | 🟡 **Faible** | AGENTS.md écrit `token/` et `reel/` au lieu de `Token/` et `Reel/` |
| 7 | 🟡 **Faible** | 9 dossiers sans README.md (non bloquant mais réduction de la navigabilité) |

---

## VIII — Recommandations

1. **Créer `📦_pieces/`** ou **supprimer la ligne** du README.md — incohérence documentaire bloquante

2. **Fusionner ou clarifier** la dualité `reports/` ↔ [Rapports](../../Actes/Token/README.md) : soit déplacer `reports/` dans [Rapports](../../Actes/Token/README.md), soit documenter officiellement les deux répertoires avec des rôles distincts

3. **Supprimer ou fusionner** `app/` (racine) dans `.dev/app/` — le doublon `enhance_markdown.py` est source d'erreurs

4. **Générer les annexes** dans Reel/06 (lancer `generate_real_versions.py` après avoir vérifié que le script couvre bien `annexes/`)

5. **Vérifier** si les 2 bordereaux excédentaires 👤 sont des résidus ou des documents légitimes — si légitimes, les ajouter aussi dans Token

6. **Mettre à jour AGENTS.md** avec les vrais noms de dossiers `Token/` et `Reel/`

7. **Ajouter README.md** dans [Rapports](../../Actes/Token/README.md) et [Memory](../../Actes/Token/README.md) pour améliorer la navigation