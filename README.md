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

├── 📁 **[token/](./actes/token/)** — Versions anonymisées (travail courant) <br>
│   ├── 📁 **[00_Preuves_officielles/](./actes/token/00_Preuves_officielles/)** — Inventaire et preuves physiques <br>
│   ├── 📁 **[01_Actes_proceduraux/](./actes/token/01_Actes_proceduraux/)** — Assignations, conclusions, requêtes <br>
│   ├── 📁 **[02_Courriers/](./actes/token/02_Courriers/)** — Mises en demeure, courriers administratifs <br>
│   ├── 📁 **[03_Analyses_juridiques/](./actes/token/03_Analyses_juridiques/)** — Plaidoiries, FAQ, analyses <br>
│   ├── 📁 **[04_Etudes_indemnisation/](./actes/token/04_Etudes_indemnisation/)** — Évaluations Dintilhac <br>
│   ├── 📁 **[05_Organisation/](./actes/token/05_Organisation/)** — Index, calendrier, statistiques <br>
│   └── 📁 **[06_Archives/](./actes/token/06_Archives/)** — Annexes (lois, lexique, pièces) <br>
│
└── 📁 **[reel/](./actes/reel/)** — Versions réelles (identités réelles résolues)

📁 **[memory/](./memory/)** — Mémoire persistante pour les agents IA

📁 **[app/](./app/)** — Scripts Python

📁 **[reports/](./reports/)** — Rapports d'analyse et de validation <br>
├── 📁 **[audit/](./reports/audit/)** — Rapports d'audit et vérifications <br>
├── 📁 **[expertise/](./reports/expertise/)** — Rapports d'analyse et mémoires juridiques <br>
└── 📁 **[ordalie/](./reports/ordalie/)** — Validation juridique

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
| 01 | [01 ⚖️ Assignation.md](./actes/token/01_Actes_proceduraux/01 ⚖️ Assignation.md) | Assignation référé-provision 5 000 € (Art. 835 CPC) |
| 02 | [02 🚔 Plainte.md](./actes/token/01_Actes_proceduraux/02 🚔 Plainte.md) | Plainte complémentaire défaut assurance RC |
| 02b | [02b 🛡️ Constitution Partie Civile.md](./actes/token/01_Actes_proceduraux/02b%20%F0%9F%9B%A1%EF%B8%8F%20Constitution%20Partie%20Civile.md) | Constitution de partie civile (Art. 222-19/222-20 CP + L.227-8 C.com.) |
| 03 | [03 🔍 Assignation Article 145.md](./actes/token/01_Actes_proceduraux/03%20%F0%9F%94%8D%20Assignation%20Article%20145.md) | Communication forcée police d'assurance (Art. 145 CPC) |
| 04 | [04 📑 Bordereau unifié.md](./actes/token/01_Actes_proceduraux/04%20%F0%9F%93%91%20Bordereau.md) | Bordereau unifié 43 pièces (groupes A-G) |
| 05 | [05 🎯 Conclusions Refere.md](./actes/token/01_Actes_proceduraux/05%20%F0%9F%8E%AF%20Conclusions%20Refere.md) | Conclusions référé (date à fixer) |
| 06 | [06 📸 Requete Constat Huissier.md](./actes/token/01_Actes_proceduraux/06%20%F0%9F%93%B8%20Requete%20Constat%20Huissier.md) | Requête constat d'huissier (Art. 145 CPC) |
| 15 | [15 ⚖️ Réquisitoire introductif.md](./actes/token/01_Actes_proceduraux/15%20%E2%9A%96%EF%B8%8F%20R%C3%A9quisitoire%20introductif.md) | Réquisitoire introductif enquête pénale |

### Courriers et gabarits ([02_Courriers/](./actes/token/02_Courriers/))

| N° | Document | Type | Statut |
|----|----------|------|--------|
| 03 | [Courrier SAS.md](./actes/token/02_Courriers/03%20%E2%9C%89%EF%B8%8F%20Courrier%20SAS.md) | Mise en demeure SAS | ✅ Envoyé |
| 04 | [Courrier Assureur.md](./actes/token/02_Courriers/04%20%E2%9C%89%EF%B8%8F%20Courrier%20Assureur.md) | Action directe assureur | ✅ Envoyé |
| 05 | [Courrier Proprietaire.md](./actes/token/02_Courriers/05%20%E2%9C%89%EF%B8%8F%20Courrier%20Proprietaire.md) | Mise en demeure bailleur | ✅ Envoyé |
| 06 | [Courrier President DG.md](./actes/token/02_Courriers/06%20%E2%9C%89%EF%B8%8F%20Courrier%20President%20DG.md) | Mise en demeure dirigeants | ✅ Envoyé |
| 07 | [Courrier Consolidation.md](./actes/token/02_Courriers/07%20%E2%9C%89%EF%B8%8F%20Courrier%20Consolidation.md) | Demande certificat consolidation | ✅ Envoyé |
| 08 | [Courrier Suivi TAVELLA.md](./actes/token/02_Courriers/08%20%E2%9C%89%EF%B8%8F%20Courrier%20Suivi%20Adjoint%20Maire.md) | Suivi mairie | ✅ Envoyé |
| 09 | [Courrier Inspection Travail.md](./actes/token/02_Courriers/09%20%E2%9C%89%EF%B8%8F%20Courrier%20Inspection%20Travail.md) | Signalement DDETS/DREETS | ✅ Envoyé |
| 10 | [Courrier Doyen Juges Instruction.md](./actes/token/02_Courriers/10%20%E2%9C%89%EF%B8%8F%20Courrier%20Doyen%20Juges%20Instruction.md) | Envoi CPC au Doyen | ✅ Drive |
| 11-16, 18 | [INPI](./actes/token/02_Courriers/11%20%E2%9C%89%EF%B8%8F%20Courrier%20INPI.md) à [SDIS](./actes/token/02_Courriers/18%20%E2%9C%89%EF%B8%8F%20Courrier%20SDIS.md) | Courriers administratifs | ✅ Envoyés |
| 17 | [Courrier CPAM.md](./actes/token/02_Courriers/17%20%E2%9C%89%EF%B8%8F%20Courrier%20CPAM.md) | Transmission + bordereau récapitulatif CPAM | ✅ Drive |
| 19 | [Courrier FGTI.md](./actes/token/02_Courriers/19%20%E2%9C%89%EF%B8%8F%20Courrier%20FGTI.md) | Saisine conservatoire FGTI | ✅ Drive |
| 20 | [Relance Police.md](./actes/token/02_Courriers/20%20%F0%9F%94%84%20Relance%20Police.md) | Relance police | ✅ Envoyé |
| 21 | [Relance CPAM.md](./actes/token/02_Courriers/21%20%F0%9F%94%84%20Relance%20CPAM.md) | Relance CPAM | ✅ Envoyé |
| 22 | [Gabarit Attestation Témoin Client.md](./actes/token/02_Courriers/22%20%F0%9F%93%8B%20Attestation%20T%C3%A9moin%20Client.md) | Attestation Cerfa | ❌ À transmettre |
| 23 | [Gabarit Attestation Pompier SAMU.md](./actes/token/02_Courriers/23%20%F0%9F%93%8B%20Attestation%20Pompier%20SAMU.md) | Attestation Cerfa | ❌ À transmettre |
| 24 | [Gabarit Attestation Employé.md](./actes/token/02_Courriers/24%20%F0%9F%93%8B%20Attestation%20Employ%C3%A9.md) | Attestation Cerfa | ❌ À transmettre |
| 25 | [Email Relance Dr DJERBI.md](./actes/token/02_Courriers/25%20%F0%9F%93%A7%20Relance%20Dr%20DJERBI.md) | Relance consolidation | ❌ À envoyer |
| 26 | [Email Attestation Temoin Client.md](./actes/token/02_Courriers/26%20%F0%9F%93%A7%20Attestation%20Temoin%20Client.md) | Email transmission témoin | ❌ À envoyer |
| 27 | [Email Attestation Pompier SAMU.md](./actes/token/02_Courriers/27%20%F0%9F%93%A7%20Attestation%20Pompier%20SAMU.md) | Email transmission pompier | ❌ À envoyer |
| 28 | [Email Attestation Employe.md](./actes/token/02_Courriers/28%20%F0%9F%93%A7%20Attestation%20Employe.md) | Email transmission employé | ❌ À envoyer |

### Analyses juridiques ([03_Analyses_juridiques/](./actes/token/03_Analyses_juridiques/))

| Document | Description |
|----------|-------------|
| [07 🎤 Plaidoirie dirigeants.md](./actes/token/03_Analyses_juridiques/07%20%F0%9F%8E%A4%20Plaidoirie%20dirigeants.md) | Plaidoirie Arrêt SATI, Art. L.124-3 |
| [09 ❓ FAQ.md](./actes/token/03_Analyses_juridiques/09 ❓ FAQ.md) | FAQ juridique |
| [12 📁 Dossier Plaidoirie.md](./actes/token/03_Analyses_juridiques/12%20%F0%9F%93%81%20Dossier%20Plaidoirie.md) | Dossier de plaidoirie (date à fixer) |
| [13 📜 Responsabilites legales.md](./actes/token/03_Analyses_juridiques/13%20%F0%9F%93%9C%20Responsabilites%20legales.md) | Responsabilités légales dirigeants |
| [14 📐 Stratégie jurisprudentielle.md](./actes/token/03_Analyses_juridiques/14%20Strat%C3%A9gie%20jurisprudentielle.md) | Stratégie jurisprudentielle |
| [15 📝 Note Droit Assurances.md](./actes/token/03_Analyses_juridiques/15%20Note%20Droit%20Assurances.md) | Note sur le droit des assurances |
| [99 🛡️ Memoire en defense adverse.md](./actes/token/03_Analyses_juridiques/99%20%F0%9F%9B%A1%EF%B8%8F%20Memoire%20en%20defense%20adverse.md) | Mémoire en défense adverse anticipé |

### Études indemnisation ([04_Etudes_indemnisation/](./actes/token/04_Etudes_indemnisation/))

| Document | Description |
|----------|-------------|
| [11 💰 Etude indemnisation.md](./actes/token/04_Etudes_indemnisation/11%20%F0%9F%92%B0%20Etude%20indemnisation.md) | Évaluation Dintilhac 59 600 € |
| [11+12 📊 Evaluation Dintilhac consolidee.md](./actes/token/04_Etudes_indemnisation/11+12%20%F0%9F%93%8A%20Evaluation%20Dintilhac%20consolidee.md) | Évaluation consolidée ~92 000 € |
| [13 📋 Note strategique FGTI CIVI.md](./actes/token/04_Etudes_indemnisation/13%20Note%20strategique%20FGTI%20CIVI.md) | Note stratégique FGTI / CIVI |

### Organisation ([05_Organisation/](./actes/token/05_Organisation/))

| Document | Description |
|----------|-------------|
| [00 📇 Index.md](./actes/token/05_Organisation/00 📇 Index.md) | Index des documents |
| [10 🗂️ Plan action.md](./actes/token/05_Organisation/10%20%F0%9F%97%82%EF%B8%8F%20Plan%20action.md) | Plan d'action |
| [11 📅 Calendrier procedural.md](./actes/token/05_Organisation/11%20%F0%9F%93%85%20Calendrier%20procedural.md) | Calendrier procédural |
| [20 📦 Bon envoi physique.md](./actes/token/05_Organisation/20%20%F0%9F%93%A6%20Bon%20envoi%20physique.md) | Bon d'envoi physique — checklist impression/envoi |

---

## Rapports d'expertise et validation ([reports/](./reports/))

| Dossier | Description |
|---------|-------------|
| [audit/](./reports/audit/) | Rapports d'audit, suivi des agents, rapports techniques et d'anonymisation |
| [expertise/](./reports/expertise/) | Mémoires juridiques, analyses approfondies et gloses |
| [jurisprudence/](./reports/jurisprudence/) | Rapports d'audit de jurisprudence |
| [ordalie/](./reports/ordalie/) | Rapports de validation juridique et tests de cohérence ("ordalie") |
| [anonymisation/](./reports/anonymisation/) | Rapports d'audit d'anonymisation |
| [ordonnance_refere.md](./reports/ordonnance_refere.md) | Projet d'ordonnance de référé motivée |

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
