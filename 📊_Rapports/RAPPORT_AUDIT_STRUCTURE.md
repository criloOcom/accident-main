# RAPPORT D'AUDIT DE STRUCTURE


```
🏠 [Accueil](../README.md) > 📁 [ 📊_Rapports ](../README.md) > 📄 [ RAPPORT_AUDIT_STRUCTURE.md ](.RAPPORT_AUDIT_STRUCTURE.md)
```


```
🏠 [Accueil](../README.md) > 📁 [ 📊_Rapports ](../README.md) > 📄 [ RAPPORT_AUDIT_STRUCTURE.md ](.RAPPORT_AUDIT_STRUCTURE.md)
```

**Date :** 10 juillet 2026
**Projet :** accident-main
**Objet :** Vérification complète de l'arborescence, correspondance 🔑/👤, conformité AGENTS.md

---

## 1. Arborescence complète

```
📁 /home/crilocom/accident-main/
├── AGENTS.md
├── README.md
├── .gitignore
├── setup.sh
│
├── ⚖️_Actes/
│   ├── README.md
│   ├── 00_Preuves_officielles/         ← Pièces brutes source (11 fichiers)
│   ├── 🔑_Token/                        ← Versions anonymisées
│   │   ├── README.md
│   │   ├── 00_📂_Preuves_officielles/   (1 fichier + .gitkeep)
│   │   ├── 01_⚖️_Actes_proceduraux/    (11 fichiers)
│   │   ├── 02_✉️_Courriers/            (33 fichiers)
│   │   ├── 03_📚_Analyses_juridiques/   (12 fichiers)
│   │   ├── 04_💰_Etudes_indemnisation/  (4 fichiers)
│   │   ├── 05_🗂️_Organisation/          (11 fichiers)
│   │   └── 06_🗄️_Archives/             (9 fichiers + annexes/)
│   │       └── annexes/                 (2 fichiers)
│   └── 👤_Reel/                         ← Versions réelles
│       ├── README.md
│       ├── 00_📂_Preuves_officielles/   (1 fichier)
│       ├── 01_⚖️_Actes_proceduraux/    (13 fichiers)
│       ├── 02_✉️_Courriers/            (33 fichiers)
│       ├── 03_📚_Analyses_juridiques/   (12 fichiers)
│       ├── 04_💰_Etudes_indemnisation/  (4 fichiers)
│       ├── 05_🗂️_Organisation/          (11 fichiers)
│       └── 06_🗄️_Archives/             (7 fichiers — sans annexes/)
│
├── 📜_Lois/
│   ├── README.md
│   ├── 24 fiches jurisprudence + articles .md
│   └── pdfs/                           (24 PDFs + 1 supplémentaire)
│
├── 🧠_Memory/                          (20 fichiers, pas de README.md)
│
├── 📊_Rapports/
│   ├── 3 rapports racine
│   ├── audit/                          (2 fichiers)
│   └── 🗄️_Archives/                    (58 fichiers dans 8 sous-dossiers)
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

## 2. Vérification 🔑_Token → 👤_Reel

### 00_📂_Preuves_officielles
| 🔑 Token | 👤 Reel | Statut |
|----------|---------|--------|
| `01 Dossier UMJ Preparation.md` | ✅ Présent | OK |
| `.gitkeep` | ❌ Absent | OK (place technique) |
| `README.md` | ✅ Présent | OK |

### 01_⚖️_Actes_proceduraux
| 🔑 Token | 👤 Reel | Statut |
|----------|---------|--------|
| `01 ⚖️ Assignation.md` | ✅ Présent | OK |
| `02 🚔 Plainte.md` | ✅ Présent | OK |
| `02b 🛡️ Constitution Partie Civile.md` | ✅ Présent | OK |
| `03 🔍 Assignation Article 145.md` | ✅ Présent | OK |
| `04 📑 Bordereau.md` | ✅ Présent | OK |
| `05 🎯 Conclusions Refere.md` | ✅ Présent | OK |
| `06 📸 Requete Constat Huissier.md` | ✅ Présent | OK |
| `07 ⚖️ Projet Ordonnance Refere.md` | ✅ Présent | OK |
| `15 ⚖️ Réquisitoire introductif.md` | ✅ Présent | OK |
| `16 ⚠️ Signalement Parquet Fraud.md` | ✅ Présent | OK |
| `17 ⚖️ Requete Mandataire Ad Hoc.md` | ✅ Présent | OK |
| — | ❌ `04 📑 Bordereau Audience.md` | **EXCÉDENT** 👤 |
| — | ❌ `04 📑 Bordereau de pieces.md` | **EXCÉDENT** 👤 |

### 02_✉️_Courriers
✅ **Correspondance parfaite** (33 fichiers identiques, hors .gitkeep)

### 03_📚_Analyses_juridiques
✅ **Correspondance parfaite** (12 fichiers)

### 04_💰_Etudes_indemnisation
✅ **Correspondance parfaite** (4 fichiers)

### 05_🗂️_Organisation
✅ **Correspondance parfaite** (11 fichiers)

### 06_🗄️_Archives
| 🔑 Token | 👤 Reel | Statut |
|----------|---------|--------|
| `11 Fiche Reflexe 48h Victime.md` | ✅ Présent | OK |
| `⚡ ActionDirecte AssureurRC.md` | ✅ Présent | OK |
| `📁 Dossier Presentation.md` | ✅ Présent | OK |
| `📚 ANALYSE Jurisprudence.md` | ✅ Présent | OK |
| `🔧 ANALYSE correction juridique.md` | ✅ Présent | OK |
| `🛡️ Constitution Partie Civile.md` | ✅ Présent | OK |
| `🧠 STRATEGIE Contentieux Civil.md` | ✅ Présent | OK |
| `🧠 STRATEGIE Contentieux Penal.md` | ✅ Présent | OK |
| `annexes/⚖️ ANNEXE B Lois Jurisprudence.md` | ❌ Absent | **MANQUANT** |
| `annexes/📑 ANNEXE C Pieces.md` | ❌ Absent | **MANQUANT** |
| `README.md` | ✅ Présent | OK |

---

## 3. Conformité AGENTS.md

| Référence AGENTS.md | Réalité | Conforme ? |
|---------------------|---------|------------|
| `token/` | `🔑_Token/` | ❌ Nom différent |
| `reel/` | `👤_Reel/` | ❌ Nom différent |
| `.dev/app/generate_real_versions.py` | ✅ Existe | OK |
| `.dev/app/sync_notebooklm.py` | ✅ Existe | OK |
| `.dev/app/check_consistency.py` | ✅ Existe | OK |
| `.dev/app/batch_anonymize.py` | ✅ Existe | OK |
| `.dev/app/tools.py` | ✅ Existe | OK |
| `.dev/app/agent.py` | ✅ Existe | OK |
| `00_📂_Preuves_officielles/` (root ⚖️_Actes) | ✅ Existe | OK |
| Structure 00-06 sous `token/` et `reel/` | ✅ Présente | OK |

## 4. Conformité README.md

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

## 5. Fichiers orphelins / non documentés

### `reports/` (racine)
Non mentionné dans AGENTS.md ni README.md. Contient 16 rapports qui complètent (et parfois doublonnent) ceux dans `📊_Rapports/`.

| Fichier | Aussi présent dans 📊_Rapports ? |
|---------|-------------------------------|
| `reports/audit/audit_email_34.md` | ❌ Non |
| `reports/audit/audit_legiarti_actes.md` | ❌ Non |
| `reports/audit/audit_legiarti_courriers.md` | ❌ Non |
| ... (13 autres) | ❌ Non |

### `app/` (racine)
Non mentionné dans AGENTS.md ni README.md.

| Fichier | Aussi présent dans .dev/app/ ? |
|---------|-------------------------------|
| `app/__init__.py` | ❌ Non (vide) |
| `app/enhance_markdown.py` | ⚠️ OUI (doublon de `.dev/app/enhance_markdown.py`) |
| `app/add_yaml_actes.py` | ❌ Non |

---

## 6. README.md manquants

| Dossier | README ? |
|---------|----------|
| `📊_Rapports/` | ❌ Absent |
| `📊_Rapports/audit/` | ❌ Absent |
| `📊_Rapports/🗄️_Archives/` | ❌ Absent |
| `🧠_Memory/` | ❌ Absent |
| `reports/` | ❌ Absent |
| `reports/audit/` | ❌ Absent |
| `reports/expertise/` | ❌ Absent |
| `reports/jurisprudence/` | ❌ Absent |
| `app/` | ❌ Absent |
| `📜_Lois/pdfs/` | ❌ Absent |

---

## 7. Synthèse des anomalies

| # | Gravité | Anomalie |
|---|---------|----------|
| 1 | 🔴 **Critique** | `📦_pieces/` mentionné dans README.md (ligne 31) n'existe pas |
| 2 | 🔴 **Critique** | `reports/` en doublon avec `📊_Rapports/` — source de confusion, non documenté |
| 3 | 🟠 **Moyen** | `app/` (racine) non documenté, avec un doublon de `enhance_markdown.py` |
| 4 | 🟠 **Moyen** | 👤_Reel/01 a 2 fichiers excédentaires vs 🔑_Token/01 : `Bordereau Audience.md` et `Bordereau de pieces.md` |
| 5 | 🟠 **Moyen** | 👤_Reel/06 manque le dossier `annexes/` (2 fichiers) présent dans 🔑_Token/06 |
| 6 | 🟡 **Faible** | AGENTS.md écrit `token/` et `reel/` au lieu de `🔑_Token/` et `👤_Reel/` |
| 7 | 🟡 **Faible** | 9 dossiers sans README.md (non bloquant mais réduction de la navigabilité) |

---

## 8. Recommandations

1. **Créer `📦_pieces/`** ou **supprimer la ligne** du README.md — incohérence documentaire bloquante
2. **Fusionner ou clarifier** la dualité `reports/` ↔ `📊_Rapports/` : soit déplacer `reports/` dans `📊_Rapports/`, soit documenter officiellement les deux répertoires avec des rôles distincts
3. **Supprimer ou fusionner** `app/` (racine) dans `.dev/app/` — le doublon `enhance_markdown.py` est source d'erreurs
4. **Générer les annexes** dans 👤_Reel/06 (lancer `generate_real_versions.py` après avoir vérifié que le script couvre bien `annexes/`)
5. **Vérifier** si les 2 bordereaux excédentaires 👤 sont des résidus ou des documents légitimes — si légitimes, les ajouter aussi dans 🔑_Token
6. **Mettre à jour AGENTS.md** avec les vrais noms de dossiers `🔑_Token/` et `👤_Reel/`
7. **Ajouter README.md** dans `📊_Rapports/` et `🧠_Memory/` pour améliorer la navigation
