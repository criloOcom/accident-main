# Accident de la Main — Dossier Juridique

**Contentieux civil et pénal** suite à un accident corporel survenu le **29 mai 2026** dans un commerce de Foix (section nerveuse/tendineuse de la main droite, défaut d'assurance RC, préjudices estimés à 59 600 €).

**Échéances clés :**

| Date | Événement | Statut |
|------|-----------|--------|
| 14 juillet 2026 | Fin phase amiable (mises en demeure du 29/06) | ✅ Échu |
| Date non fixée | Audience référé-provision (Art. 835 CPC) | ❌ À planifier |
| Date non fixée | Audience Art. 145 CPC (assurance) | ❌ À planifier |
| **12 novembre 2026** | **Rendez-vous UMJ Purpan 13h45 (réquisition police ITT)** | ✅ Fixé |

---

## Arborescence

📁 **[actes/](./actes/)** — Actes juridiques et documents de travail

├── 📁 **[token/](./actes/token/)** — Versions anonymisées (travail courant)
│   ├── 📁 **[00_Preuves_officielles/](./actes/token/00_Preuves_officielles/)** — Inventaire et preuves physiques
│   ├── 📁 **[01_Actes_proceduraux/](./actes/token/01_Actes_proceduraux/)** — Assignations, conclusions, requêtes
│   ├── 📁 **[02_Courriers/](./actes/token/02_Courriers/)** — Mises en demeure, courriers administratifs
│   ├── 📁 **[03_Analyses_juridiques/](./actes/token/03_Analyses_juridiques/)** — Plaidoiries, FAQ, analyses
│   ├── 📁 **[04_Etudes_indemnisation/](./actes/token/04_Etudes_indemnisation/)** — Évaluations Dintilhac
│   ├── 📁 **[05_Organisation/](./actes/token/05_Organisation/)** — Index, calendrier, statistiques
│   └── 📁 **[06_Archives/](./actes/token/06_Archives/)** — Annexes (lois, lexique, pièces)
│
└── 📁 **[reel/](./actes/reel/)** — Versions réelles (identités réelles résolues)

📁 **[memory/](./memory/)** — Mémoire persistante pour les agents IA

📁 **[app/](./app/)** — Scripts Python

📁 **[pieces/](./pieces/)** — Pièces originales extraites des PDFs

---

### Principe token / reel

Le dossier repose sur une **double strate de documents** générée par [generate_real_versions.py](./app/generate_real_versions.py) :

| Dossier | Contenu | Usage |
|---------|---------|-------|
| 📁 [token/](./actes/token/) | **Versions tokenisées** — identités remplacées par `**[La Victime]**` | Travail courant, révision, partage |
| 📁 [reel/](./actes/reel/) | **Versions réelles** — tokens résolus → noms, adresses, email | Impression, envoi, audience |

---

## Documents principaux

### Actes procéduraux ([01_Actes_proceduraux/](./actes/token/01_Actes_proceduraux/))

| # | Document | Description |
|---|----------|-------------|
| 01 | [01_Assignation - V1.md](./actes/token/01_Actes_proceduraux/01_Assignation%20-%20V1.md) | Assignation référé-provision 5 000 € (Art. 835 CPC) |
| 02 | [02_Plainte - V1.md](./actes/token/01_Actes_proceduraux/02_Plainte%20-%20V1.md) | Plainte complémentaire défaut assurance RC |
| 03 | [03_Assignation Article 145 - V1.md](./actes/token/01_Actes_proceduraux/03_Assignation%20Article%20145%20-%20V1.md) | Communication forcée police d'assurance (Art. 145 CPC) |
| 04 | [04_Bordereau de pieces - V1.md](./actes/token/01_Actes_proceduraux/04_Bordereau%20de%20pieces%20-%20V1.md) | Bordereau général (archive) |
| 04b | [04_Bordereau_Audience - V1.md](./actes/token/01_Actes_proceduraux/04_Bordereau_Audience%20-%20V1.md) | Bordereau séquentiel propre (25 pièces) |
| 05 | [05_Conclusions Refere - V1.md](./actes/token/01_Actes_proceduraux/05_Conclusions%20Refere%20-%20V1.md) | Conclusions référé (date à fixer) |
| 06 | [06_Requete Constat Huissier - V1.md](./actes/token/01_Actes_proceduraux/06_Requete%20Constat%20Huissier%20-%20V1.md) | Requête constat d'huissier (Art. 145 CPC) |

### Courriers et gabarits ([02_Courriers/](./actes/token/02_Courriers/))

| N° | Document | Type | Statut |
|----|----------|------|--------|
| 03 | [Courrier SAS - V1.md](./actes/token/02_Courriers/03_Courrier%20SAS%20-%20V1.md) | Mise en demeure SAS | ✅ Envoyé |
| 04 | [Courrier Assureur - V1.md](./actes/token/02_Courriers/04_Courrier%20Assureur%20-%20V1.md) | Action directe assureur | ✅ Envoyé |
| 05 | [Courrier Proprietaire - V1.md](./actes/token/02_Courriers/05_Courrier%20Proprietaire%20-%20V1.md) | Mise en demeure bailleur | ✅ Envoyé |
| 06 | [Courrier President DG - V1.md](./actes/token/02_Courriers/06_Courrier%20President%20DG%20-%20V1.md) | Mise en demeure dirigeants | ✅ Envoyé |
| 07 | [Courrier Consolidation - V1.md](./actes/token/02_Courriers/07_Courrier%20Consolidation%20-%20V1.md) | Demande certificat consolidation | ✅ Envoyé |
| 08 | [Courrier Suivi TAVELLA - V1.md](./actes/token/02_Courriers/08_Courrier%20Suivi%20TAVELLA%20-%20V1.md) | Suivi mairie | ✅ Envoyé |
| 09 | [Courrier Inspection Travail - V1.md](./actes/token/02_Courriers/09_Courrier%20Inspection%20Travail%20-%20V1.md) | Signalement DDETS/DREETS | ✅ Envoyé |
| 11-21 | [11_INPI](./actes/token/02_Courriers/11_Courrier%20INPI%20-%20V1.md) à [21_CPAM](./actes/token/02_Courriers/21_Relance%20CPAM%20-%20V1.md) | Courriers administratifs | ✅ Envoyés |
| 22 | [Gabarit Attestation Témoin Client - V1.md](./actes/token/02_Courriers/22_Gabarit%20Attestation%20T%C3%A9moin%20Client%20-%20V1.md) | Attestation Cerfa | ❌ À transmettre |
| 23 | [Gabarit Attestation Pompier SAMU - V1.md](./actes/token/02_Courriers/23_Gabarit%20Attestation%20Pompier%20SAMU%20-%20V1.md) | Attestation Cerfa | ❌ À transmettre |
| 24 | [Gabarit Attestation Employé - V1.md](./actes/token/02_Courriers/24_Gabarit%20Attestation%20Employ%C3%A9%20-%20V1.md) | Attestation Cerfa | ❌ À transmettre |
| 25 | [Email Relance Dr DJERBI - V1.md](./actes/token/02_Courriers/25_Email%20Relance%20Dr%20DJERBI%20-%20V1.md) | Relance consolidation | ❌ À envoyer |
| 26 | [Email Attestation Temoin Client - V1.md](./actes/token/02_Courriers/26_Email%20Attestation%20Temoin%20Client%20-%20V1.md) | Email transmission témoin | ❌ À envoyer |
| 27 | [Email Attestation Pompier SAMU - V1.md](./actes/token/02_Courriers/27_Email%20Attestation%20Pompier%20SAMU%20-%20V1.md) | Email transmission pompier | ❌ À envoyer |
| 28 | [Email Attestation Employe - V1.md](./actes/token/02_Courriers/28_Email%20Attestation%20Employe%20-%20V1.md) | Email transmission employé | ❌ À envoyer |

### Analyses juridiques ([03_Analyses_juridiques/](./actes/token/03_Analyses_juridiques/))

| Document | Description |
|----------|-------------|
| [07_Plaidoirie dirigeants - V1.md](./actes/token/03_Analyses_juridiques/07_Plaidoirie%20dirigeants%20-%20V1.md) | Plaidoirie Arrêt SATI, Art. L.124-3 |
| [09_FAQ - V1.md](./actes/token/03_Analyses_juridiques/09_FAQ%20-%20V1.md) | FAQ juridique |
| [12_Dossier Plaidoirie - V1.md](./actes/token/03_Analyses_juridiques/12_Dossier%20Plaidoirie%20-%20V1.md) | Dossier de plaidoirie (date à fixer) |
| [13_Responsabilites legales - V1.md](./actes/token/03_Analyses_juridiques/13_Responsabilites%20legales%20-%20V1.md) | Responsabilités légales dirigeants |

### Études indemnisation ([04_Etudes_indemnisation/](./actes/token/04_Etudes_indemnisation/))

| Document | Description |
|----------|-------------|
| [11_Etude indemnisation - V1.md](./actes/token/04_Etudes_indemnisation/11_Etude%20indemnisation%20-%20V1.md) | Évaluation Dintilhac 59 600 € |

### Organisation ([05_Organisation/](./actes/token/05_Organisation/))

| Document | Description |
|----------|-------------|
| [00_Index.md](./actes/token/05_Organisation/00_Index.md) | Index des documents |
| [10_Plan action - V1.md](./actes/token/05_Organisation/10_Plan%20action%20-%20V1.md) | Plan d'action |
| [11_Calendrier procedural - V1.md](./actes/token/05_Organisation/11_Calendrier%20procedural%20-%20V1.md) | Calendrier procédural |

---

## Mémoire persistante ([memory/](./memory/))

Fichiers essentiels pour les agents IA (lire [AGENTS.md](./AGENTS.md) avant toute action) :

| Fichier | Rôle |
|---------|------|
| [VACCIN.md](./memory/VACCIN.md) | 🔴 Protocole obligatoire avant chaque action |
| [STATUS.md](./memory/STATUS.md) | État d'avancement détaillé |
| [TODO.md](./memory/TODO.md) | Plans restants et priorités + tableau de bord dates |
| [STRICT VARIABLES.md](./memory/STRICT%20VARIABLES.md) | Source unique de vérité (dates, montants, faits) |
| [TOKEN MAP.md](./memory/TOKEN%20MAP.md) | Correspondance jeton ↔ identité réelle |
| [PIECES MAP.md](./memory/PIECES%20MAP.md) | Correspondance document → pièces citées |
| [DECISIONS.md](./memory/DECISIONS.md) | Décisions d'architecture et règles |
| [RULES.md](./memory/RULES.md) | Règles permanentes et interdictions |
| [JUSTIFICATION_PROVISION_5000.md](./memory/JUSTIFICATION_PROVISION_5000.md) | Justification provision 5 000 € |
| [EVALUATION_CRITIQUE.md](./EVALUATION_CRITIQUE.md) | Évaluation critique du dossier |
| [RECOMMANDATIONS_DOSSIER.md](./RECOMMANDATIONS_DOSSIER.md) | Recommandations et éléments manquants |
| [RAPPORT_PLAN_H.md](./memory/RAPPORT_PLAN_H.md) | Uniformisation assignations / bordereaux |

---

## Pour les agents IA

1. **Lire [AGENTS.md](./AGENTS.md)** en premier — point d'entrée
2. **Lire [VACCIN.md](./memory/VACCIN.md)** avant toute action — protocole obligatoire
3. **Lire [memory/](./memory/)** pour le contexte complet
4. **Respecter la logique token/reel** : les fichiers dans [token/](./actes/token/) restent tokenisés ; [reel/](./actes/reel/) via [generate_real_versions.py](./app/generate_real_versions.py)
5. **GitHub Token** : Google Secret Manager (`projects/crilo-prod-automation/secrets/GITHUB_TOKEN`) + fallback `~/.git-credentials`

## Conventions

| Règle | Description |
|-------|-------------|
| `<hr><hr>` | Marqueur de saut de page dans les actes |
| `**[Token]**` | Identité anonymisée (ex: `**[La Victime]**`) |
| YAML front matter | Métadonnées sur tous les fichiers .md dans actes/ |
| Format | `Arial JUSTIFIED` pour tous les documents juridiques |
| Identifiant pièce | Triplet `(date, émetteur, objet)` |

## Scripts disponibles ([app/](./app/))

| Script | Rôle |
|--------|------|
| [check_consistency.py](./app/check_consistency.py) | Vérification transversale du dossier |
| [batch_link_legifrance.py](./app/batch_link_legifrance.py) | Insertion de liens Légifrance/Judilibre |
| [generate_real_versions.py](./app/generate_real_versions.py) | Génération des versions réelles (token → réel) |
| [batch_anonymize.py](./app/batch_anonymize.py) | Anonymisation de documents |
| [drive_client.py](./app/drive_client.py) | Client Google Drive |
| [injection.py](./app/injection.py) | Injection de documents dans Google Docs |
| [consolidate_sheet.py](./app/consolidate_sheet.py) | Consolidation de Google Sheets |

Voir [app/README.md](./app/README.md) pour le détail.

## Dépendances techniques

Python 3.13+, uv, Google ADK, Tesseract OCR français, Poppler-utils.
