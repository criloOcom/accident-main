# STATUT D'AVANCEMENT — 6 juillet 2026

## Phase 6-10 — Corrections audit + scellement (6 juillet 2026) ✅

### Ce qui a été fait
- **Phase 1** : Purge jurisprudence fabriquée `07-83.385` et correction `91-11.207` en `91-11.285` (JURITEXT000007030228).
- **Phase 2** : Correction LEGIARTI Art.1240 et 835 CPC (remplacés par version en VIGUEUR).
- **Phase 3** : Anonymisation noms réels résiduels dans `token/` + renommage du fichier courrier 08 pour éliminer la fuite nominale.
- **Phase 4** : Correction date `ANNEXE A` (29 juin → 29 mai pour l'accident).
- **Phase 5** : Checker amélioré avec vérification API Légifrance en temps réel.
- **Phase 6** : Nettoyage des fichiers orphelins dans `reel/` (suppression de `08_Courrier Suivi TAVELLA.md`).
- **Phase 7** : Vérification sur le Drive des documents `UNIFIE_ANONYME` (Doc 1 et 3 vérifiés avec LEGIARTIs corrects).
- **Phase 8** : Double vérification croisée (liens Légifrance testés + absence de noms réels hors `ANNEXE A` scannée).
- **Phase 9** : Test du checker amélioré concluant (détection et blocage d'un LEGIARTI invalide non listé).

### État final
- `python3 app/check_consistency.py` : 0 erreur
- `token/` : 58 fichiers — aucun nom réel hors `ANNEXE A Lexique Tokens.md`
- `reel/` : 55 fichiers — synchronisé
- Drive : docs `UNIFIE_ANONYME` vérifiés et conformes

## Phase 4 — Injection normalisée et renommage Drive (4-5 juillet 2026) ✅

### Ce qui a été fait
- **14 documents injectés** avec `replaceDocumentWithMarkdown(firstHeadingAsTitle: true)` à partir des fichiers normalisés dans `markdown_normalized/`
- **Normalisation préalable** : script `normalize_markdown.py` corrigeant les `\u000b` → `\n\n`, listes `1. 1. 1.` → `1. 2. 3.`, gras/italique, espaces
- **14 documents renommés** sur Google Drive avec préfixe numérique 01-14 cohérent (avant : préfixes hérités dupliqués, e.g. "04 ANALYSE..." pour le doc 11)
- **Vérification confirmée** : contenu correct pour les 14 docs (titre, date, INTRODUCTION, tokens)

### Drive names actuels (14/14)
| # | Drive name |
|---|-----------|
| 01 | 01 Assignation Reféré Provision FINAL - UNIFIE_ANONYME |
| 02 | 02 Action Directe Assureur RC (Art. L.124-3) - UNIFIE_ANONYME |
| 03 | 03 Plainte Complément Défaut Assurance RC - UNIFIE_ANONYME |
| 04 | 04 Assignation Référé Provision V1 - UNIFIE_ANONYME |
| 05 | 05 Constitution Partie Civile - UNIFIE_ANONYME |
| 06 | 06 Dossier de Présentation - UNIFIE_ANONYME |
| 07 | 07 ETUDE Indemnisation MAX - UNIFIE_ANONYME |
| 08 | 08 Index Etat Final Dossier - UNIFIE_ANONYME |
| 09 | 09 Plan Action Chronologie - UNIFIE_ANONYME |
| 10 | 10 Synthèse FAQ - UNIFIE_ANONYME |
| 11 | 11 ANALYSE correction juridique - UNIFIE_ANONYME |
| 12 | 12 ANALYSE Jurisprudence - UNIFIE_ANONYME |
| 13 | 13 ANALYSE Plaidoirie Dirigeants - UNIFIE_ANONYME |
| 14 | 14 ANALYSE Responsabilités Légales Dirigeants - UNIFIE_ANONYME |

## Phase 3 — Annexe C ajoutée aux 14 documents ✅

### Ce qui a été fait
- PIECES MAP.md créé dans `memory/` avec mapping complet document→pièces
- Annexe C générée sur mesure pour chaque document (listes à puces, liens Drive cliquables)
- Chaque Annexe C liste les pièces spécifiquement citées dans le contenu du document
- Docs 1-4 (procéduraux) → pièces financières, médicales, pénales, CPAM
- Docs 5-6 (bordereau pièces) → pièces 1-10 explicitement listées
- Docs 7-12 (analytiques) → pièces médicales clés + CPAM + URSSAF
- Docs 13-14 (dirigeants) → pièces INSEE/INPI + plainte + CPAM

### Documents désormais complets (Annexes A+B+C)
Tous les 14 documents UNIFIE_ANONYME contiennent :
1. ✅ Contenu principal avec tokens en gras (V2)
2. ✅ Corrections factuelles appliquées
3. ✅ Liens Légifrance/Judilibre cachés (7 docs : 6,7,8,9,10,11,14)
4. ✅ Annexe A — Lexique des jetons
5. ✅ Annexe B — Textes de loi et jurisprudence cités
6. ✅ Annexe C — Liste des pièces citées avec liens Drive

## Correction #2026-07-02 — Mensonges factuels + Date de naissance

### Date de naissance erronée
- Doc 1 (Assignation FINAL) : « né le **12 mars** 1982 » → corrigé en « né le **18 janvier** 1982 »
- Cause racine : contamination par template sans boucle de vérification
- Solution : création de `STRICT VARIABLES.md` + règle Double-Pass dans `RULES.md`

### Correction factuelle (mensonges éradiqués)

**Source de vérité** : Dossier de Presentation original (`1CPMOR23awztNxiJYVoEZkRkKMxuXDfJzFrVB4ioxbGw`) — le coiffeur est monté sur la vasque → basculement → main droite a percuté une cassure préexistante.

### Corrections appliquées

| Doc | Mensonge | Correction |
|-----|----------|------------|
| 1 | « s'est effondrée et brisée / débris de céramique » | ✅ « basculement brutal... cassure majeure préexistante » |
| 1 | « incapacité physique absolue d'utiliser un outil informatique » | ✅ « incapacité d'utiliser sa main droite » |
| 1 | « le paralyse entièrement dans son activité professionnelle » | ✅ « limite gravement son activité professionnelle » |
| 1 | « défaut d'entretien ou d'installation » | ✅ « escalade du préposé... cassure préexistante non signalée » |
| 2 | « incapacité absolue d'exercer son activité professionnelle » | ✅ « incapacité d'utiliser sa main droite » |
| 10 | « totalement paralysée » | ✅ « gravement compromise » |

## Correction #2026-07-03 — Fausse liquidation (hallucination IA)

### Problème
Doc 11 (ANALYSE et correction juridique) affirmait comme un fait certain :
> *"L'Exploitant est actuellement engagé dans un processus de liquidation"*

**C'est une hallucination de l'IA génératrice.** Aucun document source (PJ, KBIS, INPI, etc.) ne contient cette information.

### Correction appliquée
- Doc 11 UNIFIE_ANONYME ✅ → remplacé par constat d'incertitude
- Source 🔬 ANALYSE et correction juridique ✅ → idem
- Anciennes versions contaminées (2 docs) → corbeille

### Nouveau texte
> *"À ce jour, le statut exact de L'Exploitant demeure incertain : les courriers recommandés adressés le 29 juin 2026 à la société et à ses dirigeants sont restés sans réponse ni accusé de réception signé."*

### Règles ajoutées
- **STRICT VARIABLES.md** : ⚠ Statut de la SAS inconnu — ne jamais inventer
- **RULES.md** : INTERDICTION D'INVENTER UN STATUT JURIDIQUE — pas de statut sans source

## Correction #2026-07-03b — Pages d'introduction insérées dans les 13 documents

### Problème
Les 13 documents UNIFIE_ANONYME (hors Doc 14 modèle déjà fait) n'avaient pas de page d'introduction narrative (TITLE + date + « INTRODUCTION » HEADING_1 + prose + saut de page).

### Travail effectué
- **13 introductions rédigées en prose juridique** (phrases complètes, pas de listes à puces)
- Chaque introduction est propre au document : contexte de l'affaire, fondements juridiques, objectif du document
- « INTRODUCTION » stylé en HEADING_1 (vérifié en JSON)
- Saut de page inséré entre l'introduction et le contenu original
- Contenu original préservé (liens, listes, tableaux, gras)

### Réparations effectuées
- **Docs 1-4, 5-7** : introduction insérée sans dommage au contenu
- **Docs 8, 9, 11** : contenu original rogné par deleteRange → réinséré manuellement + page break
- **Docs 10, 12, 13** : contenu rogné → réinséré et vérifié le 3 juillet 2026
- **Doc 14** : untouched (modèle déjà existant)

### État final (3 juillet 2026)
| # | Titre | Introduction | HEADING_1 | Page break |
|---|-------|-------------|-----------|------------|
| 1 | Assignation RÉFÉRÉ PROVISION FINAL | ✅ Prose | ✅ | ✅ |
| 2 | ActionDirecteAssureurRC | ✅ Prose | ✅ | ✅ |
| 3 | Plainte Complément Défaut Assurance RC | ✅ Prose | ✅ | ✅ |
| 4 | Assignation Référé Provision 5000€ V1 | ✅ Prose | ✅ | ✅ |
| 5 | Pièce 11 Constitution Partie Civile | ✅ Prose | ✅ | ✅ |
| 6 | Dossier de Presentation | ✅ Prose | ✅ | ✅ |
| 7 | ETUDE Indemnisation MAX | ✅ Prose | ✅ | ✅ |
| 8 | Index EtatFinalDuDossier | ✅ Prose | ✅ | ✅ |
| 9 | PlanAction ChronologieProcédure | ✅ Prose | ✅ | ✅ |
| 10 | Synthèse FAQ JuridiqueProcédure | ✅ Prose | ✅ | ✅ |
| 11 | ANALYSE correction juridique | ✅ Prose | ✅ | ✅ |
| 12 | ANALYSE Jurisprudence AccidentCorporel | ✅ Prose | ✅ | ✅ |
| 13 | ANALYSE Plaidoirie Responsabilité Dirigeants | ✅ Prose | ✅ | ✅ |
| 14 | ANALYSE ResponsabilitesLegales (modèle) | ✅ (préexistant) | ✅ | ✅ |

## Dossier Drive
- ID dossier de travail : `1LnXAHlLLLHN0quyhiRq4CdVAKHRGolWk`
- Annuaire Lois : `14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ`
- ARCHIVES : `1poohpxlkv79P5QcvVcXoYXj80nKFEDPV`

## Documents traités avec tokens V2 (14/14 — COMPLET)

Tous les 14 documents ont été anonymisés, injectés et **corrigés factuellement** (mensonges #2026-07-02).

| # | Drive name | ID Original | ID UNIFIE_ANONYME (actif) |
|---|-----------|------------|---------------------------|
| 1 | 01 Assignation Reféré Provision FINAL | `1FpD4dc4JlgVutHR1sdY-g5-aedI2jdw6iL6C5C5a2hA` | `1ZIfWjszjl5VoxBxourQiDeRATbkckkWPzbU9tYmg5yg` |
| 2 | 02 Action Directe Assureur RC (Art. L.124-3) | `1-5wPPbmfrpP4UzFCysGMYgaThI4wZfkZOQ7Gg1IQ7Bg` | `1_tNTGHf1VGnx1zD0PvyrdvqHLAyYDBU_7wRibBwWlJY` |
| 3 | 03 Plainte Complément Défaut Assurance RC | `1KXeatBLQ1WvtKdU4APU5PyAdRSVmogApSMNteEybUqc` | `1TVN7SyAWgTLQtOvUzpWqqlfF7fyzT8H8yLziKLQhelc` |
| 4 | 04 Assignation Référé Provision V1 | `1J1bmCek8imtkgJnXniJg-9RXNapGjzTvnxJPgF_HFh4` | `1L3lJuFQ3CmswKlBg8P5YF6whQQ1AV7QTCLQ_arWo39A` |
| 5 | 05 Constitution Partie Civile | `19X-lkkBYiri7DXP5nMgHkKuxgI8DB4M1LQFf6fDDgLQ` | `1tdFbDxNceGVjaABoYiHkUR1jxd8y0OaezWUOoV3ZDGc` |
| 6 | 06 Dossier de Présentation | `1CPMOR23awztNxiJYVoEZkRkKMxuXDfJzFrVB4ioxbGw` | `1DdpbOypghzt9XE09oxtzx46ngPdU4pnc4gayLQEZ_TU` |
| 7 | 07 ETUDE Indemnisation MAX | `1FKb_mrP_JwMd49KRU74LCuHmOtnsYkzxKA1vNxXuCi8` | `1PiBFn1oA1DtkT61N-zvdPmsCYsmR0au9V4BA9IZzrH4` |
| 8 | 08 Index Etat Final Dossier | `1810cAMY1636YPs99QCBojuy9RZzDVAbYTg8qHCf06ps` | `1Zp-JK9kz0V0DTqNbA7QDDfHliWAqv7Ebyw4Yu3Li6lU` |
| 9 | 09 Plan Action Chronologie | `1u0oort0Z2a63GU86Rt2DMVO16mvxw-BrGisEONdI960` | `153cOANMpw-OoxZqq3jgo34NsWHPY_-cRXZntM_Ydf9s` |
| 10 | 10 Synthèse FAQ | `1cO7WKREKbwXKg1M_OTzX3dCf1u01te6Xaf4HDiMAS8s` | `1eoOJ-bcHBNnLsKYo7_mVz7K1w0gFfhZE_NHdUj3CBoM` |
| 11 | 11 ANALYSE correction juridique | `1hipg8_VqZil-iISUKikWEEW8ElMgpgvSoUUx8vp-5cE` | `1Ikk9wlfyLuFlTofsyLiz6836bHM5g4_ejQhGuRdUkes` |
| 12 | 12 ANALYSE Jurisprudence | `1-aZHyfr5DoPsB2dtjpkYM7TSDHJzsOMVguGI3kXKWVs` | `1AO7GLNpbNGa9ChiUVa5rbbhLtmppzMTgOcg9qCIJBRU` |
| 13 | 13 ANALYSE Plaidoirie Dirigeants | `1Dm7bs3MepNwzxZSVgIy3l40tdHTUZYzKDYvTWVVpi0I` | `1uHOesWZrUf16NVs7kC_dr15JtthOfaJnUNo6e3Z7W90` |
| 14 | 14 ANALYSE Responsabilités Légales Dirigeants | `12M7PJyq4F6uCF_TslK48eFCYvHPeZQTqQD4lI_2NXzE` | `1lUKoGE8kozmE3KA4zErv9GYmJZ0yctOk9tn92O8KT34` |

---

## Infrastructure Jules — Drive CLI + Setup (4 juillet 2026)

### Nouveaux fichiers
| Fichier | Rôle |
|---------|------|
| `setup.sh` | Script d'initialisation : `uv sync` + config Drive |
| `app/drive_auth.py` | Module d'authentification Drive (OAuth → env vars ou ADC) |
| `app/drive_client.py` | CLI Drive pour Jules : list, upload, download, export, search, create-folder |

### Authentification Drive
- **Méthode primaire** : OAuth refresh token (même client que `gcp-oauth.keys.json`)
- **Méthode fallback** : Application Default Credentials (ADC)
- **Pas de SA key** : l'org policy `iam.disableServiceAccountKeyCreation` bloque la création de clés
- **Variables d'environnement** : `GOOGLE_DRIVE_CLIENT_ID`, `GOOGLE_DRIVE_CLIENT_SECRET`, `GOOGLE_DRIVE_REFRESH_TOKEN`

### Testé et vérifié
- ✅ `uv run python -m app.drive_client list` → liste les 4 sous-dossiers du dossier Accident Main
- ✅ `uv run python -m app.drive_client upload` → upload fonctionnel
- ✅ `uv run python -m app.drive_client search` → recherche par nom
- ✅ `uv run python -m app.drive_client export --format markdown --print` → export Google Doc vers stdout

### Nouveaux ajouts — 4 juillet 2026 (soir)
| Ajout | Détail |
|-------|--------|
| `lois/` | 16 textes juridiques (PDF→.md) du dossier Drive **00 Lois** + INDEX.md |
| `app/mcp_bridge/` | Clients Judilibre et Légifrance sans FastMCP, utilisables en CLI |
| `app/drive_client.py` | Nouvelle commande `read-sheet` pour Google Sheets |
| `setup.sh` | Mis à jour : support Piste + MCP Bridge |
| `pyproject.toml` | requires-python → >=3.12, dépendances : pylegifrance, requests, pypdf |

### À faire pour toi (Jules Settings → jules.google.com/settings)

| Variable | Source |
|----------|--------|
| `GOOGLE_DRIVE_CLIENT_ID` | `gcp-oauth.keys.json` → `installed.client_id` |
| `GOOGLE_DRIVE_CLIENT_SECRET` | `gcp-oauth.keys.json` → `installed.client_secret` |
| `GOOGLE_DRIVE_REFRESH_TOKEN` | `application_default_credentials.json` → `refresh_token` |
| `PISTE_CREDENTIALS` | JSON complet de `app/tools.py` → `get_secret("PISTE_CREDENTIALS")` |
| Setup script | `./setup.sh` (pas `echo do setup`) |

**Important** : le setup script doit être `./setup.sh` (pas `echo do setup`),
car Jules supprime les env vars après le setup. setup.sh matérialise les
credentials dans `.drive-token.json` et `.piste-credentials.json`, que le
code Python lit ensuite en fallback.

### Credentials déjà configurés (tu les as mis)
- ✅ `GOOGLE_DRIVE_CLIENT_ID`
- ✅ `GOOGLE_DRIVE_CLIENT_SECRET`
- ✅ `GOOGLE_DRIVE_REFRESH_TOKEN`
- ✅ `PISTE_CREDENTIALS`
- ❌ **Setup script** : encore `echo do setup` → à changer en `./setup.sh`

## Phase 5b — Création et anonymisation des courriers 03-06 (5 juillet 2026) ✅

### Ce qui a été fait
- **03_Courrier SAS.md** : créé et anonymisé depuis `pieces/20260629 ✉️ LR MiseEnDemeure SAS LesMauvaisGarcons.md`
- **04_Courrier Assureur.md** : créé depuis `archives/ActionDirecte_AssureurRC.md` + alignement montant global 59 600€
- **05_Courrier Proprietaire.md** : créé et anonymisé depuis `pieces/20260629 ✉️ LR MiseEnDemeure Bailleur MrDELRIEU.md`
- **06_Courrier President DG.md** : créé par fusion des pièces SABIR et ANDISSAC en courrier unique double destinataire
- **Tous les courriers** : YAML frontmatter, liens Légifrance, tokens en **gras**
- **Scripts mis à jour** : `add_yaml_actes.py` (4 entrées), `batch_link_legifrance.py` (chemins corrigés + support JURITEXT)
- **Index mis à jour** : stats (14 docs), mention fichiers à insérer supprimée, travaux restants nettoyés
- `python3 app/check_consistency.py` : 0 erreur, 1 avertissement (bénin)

## Phase 5c — Injection des 4 courriers sur Drive (5 juillet 2026) ✅

### Ce qui a été fait
- **4 Google Docs créés** sur Drive dans le dossier de travail :
  - `03 Courrier SAS Mise en Demeure - UNIFIE_ANONYME` (`1s5_z0l9yti3Ir6yBGH5xlZE-2LMs8uMJGlVcQA_sHKc`)
  - `04 Action Directe Assureur RC - UNIFIE_ANONYME` (`14VIXTJK4n9eH66eVNZ6hJO6gLkiRBqnJpWijsDbkE2k`)
  - `05 Courrier Proprietaire - UNIFIE_ANONYME` (`1W-C6nM5G_GUPzHjnaq56kRzdHwMuwTfaWQE8nNS9hj4`)
  - `06 Courrier President DG - UNIFIE_ANONYME` (`1pheN3_rudxydYS2AQI7a1KGeFRr3PKD5Zett6Ac899I`)
- **Markdown injecté** avec `replaceDocumentWithMarkdown(firstHeadingAsTitle: true)`
- **JUSTIFIED appliqué** sur les 4 documents
- **drive_id mis à jour** dans les fichiers locaux YAML
- **Consistency check : 0 erreur**

### Vérification PV Police (OCR)
- **OCR effectué** sur le scan PDF original du PV (n°2026/015967, 3 pages, 300 DPI)
- **Texte confirmé** : le PV dit bien « monté sur une vasque en céramique » — aucune erreur de transcription
- Cohérence documentaire vérifiée (PV original = transcription = actes juridiques)

## Phase 5 — Correction audit de coherence (5 juillet 2026) ✅

### Corrections appliquees
- Montants 58 100€ → 59 600€ dans 4 fichiers (Plainte, Plaidoirie, FAQ, Responsabilites)
- Contradiction interne 11_Etude indemnisation corrigee (texte aligne sur tableau)
- Frontmatter YAML duplique supprime dans 6 fichiers
- Nesting de liens Legifrance nettoie (5 niveaux → 1 niveau) dans 10 fichiers
- Tokens d'anonymisation corriges : civilite supprimee, "coiffeur" → **[Le Prépose de l'Exploitation]**
- Chemins obsoletes dans RULES.md et WORKFLOW.md mis a jour
- Date STATUS.md corrigee (4→5 juillet), date ANNEXE C corrigee (27/05→29/06)
- `python3 app/check_consistency.py` : 0 erreur, 1 avertissement (benin)

## Phase 5c — Injection des 4 courriers sur Drive (5 juillet 2026) ✅

### Ce qui a été fait
- **4 Google Docs créés** sur Drive dans le dossier de travail :
  - `03 Courrier SAS Mise en Demeure - UNIFIE_ANONYME` (`1s5_z0l9yti3Ir6yBGH5xlZE-2LMs8uMJGlVcQA_sHKc`)
  - `04 Action Directe Assureur RC - UNIFIE_ANONYME` (`14VIXTJK4n9eH66eVNZ6hJO6gLkiRBqnJpWijsDbkE2k`)
  - `05 Courrier Proprietaire - UNIFIE_ANONYME` (`1W-C6nM5G_GUPzHjnaq56kRzdHwMuwTfaWQE8nNS9hj4`)
  - `06 Courrier President DG - UNIFIE_ANONYME` (`1pheN3_rudxydYS2AQI7a1KGeFRr3PKD5Zett6Ac899I`)
- **Markdown injecté** avec `replaceDocumentWithMarkdown(firstHeadingAsTitle: true)`
- **JUSTIFIED appliqué** sur les 4 documents
- **drive_id mis à jour** dans les fichiers locaux YAML
- **Consistency check : 0 erreur**

### Vérification PV Police
- **OCR effectué** sur le scan PDF original du PV (2026/015967, 3 pages)
- **Texte confirmé** : le PV dit bien « monté sur une vasque en céramique » — aucune erreur de transcription
- Cohérence documentaire vérifiée (PV original = transcription = actes juridiques)

## Phase 5d — Courrier Consolidation Dr DJERBI (Plan E) (5 juillet 2026) ✅

### Ce qui a été fait
- **07_Courrier Consolidation.md** : créé et injecté sur Drive
- Contenu : demande de certificat médical de consolidation pour permettre l'évaluation DFP/IP/SE
- Mention : Nomenclature Dintilhac + Cass. Civ. 2e, 4 avril 2024, n° 22-19.307
- **JUSTIFIED appliqué** sur le document
- **drive_id mis à jour** dans le fichier local YAML
- Drive ID : `1PSv6c0YFvLa0WDEbwc3AVxL14z7ARi5ne50ctJgCvWI`
- Dossier : `20269999 xx FUTUR xx`

## Phase 6a — Courriers Suivi TAVELLA + Inspection Travail (Plan B) (5 juillet 2026) ✅

### Ce qui a été fait
- **08_Courrier Suivi TAVELLA.md** : créé et injecté — réponse à l'adjoint au maire pour demande de suivi Inspection du Travail + CODAF + demande de communication des rapports
- **09_Courrier Inspection Travail.md** : créé et injecté — demande directe à la DDETS/DREETS avec liste des manquements présumés (DUERP, assurance RC, équipement, formation, travail dissimulé)
- **JUSTIFIED appliqué** sur les 2 documents
- **drive_id mis à jour** dans les fichiers locaux YAML
- Drive IDs : `1Xj4wf-v-ShCeq44vjb6XulUM_y2WnuLKO68flsuPKNw` (08), `1tStFiBk8gxB6kWk_HQGPSLH2-QCQVxkARBz7SDer2gM` (09)

## Phase 6b — Rédaction des 12 courriers d'alerte preventives (5 juillet 2026) ✅

### Ce qui a été fait
- **Règle permanente ajoutée** dans RULES.md et DECISIONS.md : séparation stricte tokens ↔ dossier de correspondance réelle
- **12 nouveaux courriers créés** dans `actes/02_Courriers/` (nos 10 à 21) :

| # | Fichier | Destinataire | Objet | Type |
|---|---------|-------------|-------|------|
| 10 | `10_Courrier Greffe TC.md` | Greffe TC Foix | Inscription observation RCS | LRAR |
| 11 | `11_Courrier INPI.md` | INPI / RNE | Signalement litige en cours | LRAR |
| 12 | `12_Courrier URSSAF.md` | URSSAF Midi-Pyrénées | Signalement travail dissimulé | LRAR |
| 13 | `13_Courrier Prefecture.md` | Préfecture 09 | Confirmation signalement | LRAR |
| 14 | `14_Courrier CODAF.md` | CODAF 09 | Signalement officiel manquements | LRAR |
| 15 | `15_Courrier SIE.md` | SIE Foix | Information litige | LRAR |
| 16 | `16_Courrier Conseil Departemental.md` | CD 09 | Signalement sécurité ERP | LRAR |
| 17 | `17_Courrier CARSAT.md` | CARSAT Midi-Pyrénées | Signalement risque pro | Email |
| 18 | `18_Courrier SDIS.md` | SDIS 09 | Signalement sécurité ERP | Email |
| 19 | `19_Courrier FGTI.md` | FGTI | Information conservatoire | LRAR + Email |
| 20 | `20_Relance Police.md` | Police Foix | Suivi plainte + demande vidéos | Email |
| 21 | `21_Relance CPAM.md` | CPAM Haute-Garonne | Suivi dossier RCT | Email |

- **Tous rédigés en version longue** (contexte + faits + fondements juridiques), conformément aux courriers 03-06
- **Consistency check** : 0 erreur, 13 avertissements bénins `[Adresse a completer]` (inchangé)
- **Délai respecté** : pas de relance SAS/dirigeants avant le 14 juillet (délai légal 15 jours)

### Règle permanente instaurée
- Les fichiers de travail (actes/, memory/, courriers .md) sont **100% en tokens anonymes**
- Un dossier de correspondance réelle séparé sera créé UNIQUEMENT au moment de l'envoi
- Aucun fichier « mixte » tokens+réel ne doit exister

## Phase 6c — Corrections post-audit (5 juillet 2026) ✅

### Problèmes identifiés par l'audit externe

| Point | Statut |
|-------|--------|
| Greffe TC incompétent pour litige civil individuel | ✅ Supprimé |
| CARSAT incompétente pour client tiers | ✅ Supprimé |
| URSSAF recentré travail dissimulé uniquement | ✅ Reformulé |
| Plainte : victime client, pas salarié | ✅ Requalifié |
| Assureur RC inconnu → Article 145 CPC | ✅ Créé |

### Fichiers supprimés
- `actes/02_Courriers/10_Courrier Greffe TC.md` — Greffe TC incompétent (observation RCS pas pour litige civil individuel)
- `actes/02_Courriers/17_Courrier CARSAT.md` — CARSAT incompétente (pas de pouvoir sur client tiers)

### Fichiers modifiés
- `actes/02_Courriers/12_Courrier URSSAF.md` — Recentré sur travail dissimulé pur (plus de récit accident/victime)
- `actes/01_Actes_proceduraux/02_Plainte.md` — Ajout « en qualité de client » pour requalification
- `actes/05_Organisation/00_Index.md` — Tableau mis à jour (suppressions + Article 145)

### Fichiers créés
- `actes/01_Actes_proceduraux/03_Assignation Article 145.md` — Assignation en référé Article 145 CPC pour communication police d'assurance RC Pro sous astreinte (150€/jour)

### État après corrections
- **17 courriers** (03-09, 11-16, 18-21)
- **3 actes procéduraux** (01 Assignation, 02 Plainte, 03 Article 145)
- **0 erreur** à la consistency check (a vérifier)

## Phase 6d — Injection Drive des 11 documents (5 juillet 2026) ✅

### Documents injectés sur Drive (dossier `1LnXAHlLLLHN0quyhiRq4CdVAKHRGolWk`)

| # | Drive name | ID |
|---|-----------|-----|
| 03 | 03 Assignation Article 145 - UNIFIE_ANONYME | `1R26179ks7vLkzw0hYEHL888i0p1VS9ppa6s8R8kQ_gg` |
| 11 | 11 Courrier INPI - UNIFIE_ANONYME | `1gFhTi6GhD6uDRW_XZcbk13JgpaJOOfGxEXb9ZX0KV4E` |
| 12 | 12 Courrier URSSAF - UNIFIE_ANONYME | `1LdLfCnWLiD2v1N1SMF3FAeh681znM0kXOrAlBXeOe8w` |
| 13 | 13 Courrier Prefecture - UNIFIE_ANONYME | `1sIkiScOSFZyXcfEqyuxEW8q0NC_g4YoAYLmEBsuYXbM` |
| 14 | 14 Courrier CODAF - UNIFIE_ANONYME | `1Lva-hW9g9d6B4TITlttg28HD6y06MxaUtjzSVQyC4EY` |
| 15 | 15 Courrier SIE - UNIFIE_ANONYME | `1yl55r__e8V0Rjnf3DETzaOCuhNX1CedEvcJo8FVIxAA` |
| 16 | 16 Courrier Conseil Departemental - UNIFIE_ANONYME | `1pBi3ofZ86aGKRkL9X367bHZvHj0fU55iMC_Izmz6gHQ` |
| 18 | 18 Courrier SDIS - UNIFIE_ANONYME | `1CCl3bFp_jkYtAF8yEDNtJn5Tic8miKsxLOSGNP2peoE` |
| 19 | 19 Courrier FGTI - UNIFIE_ANONYME | `1rtaTa6scRGc0TmelWNMrX6bN-kqe98b1dhT5OT-qsXc` |
| 20 | 20 Relance Police - UNIFIE_ANONYME | `171CF_LzNopYxIS6Tn4i3t3Ghx3ut14F1gh6-KjHevCA` |
| 21 | 21 Relance CPAM - UNIFIE_ANONYME | `1MHhZf_KN4b3jcym5DRJefVGCEjhHQm6ZHT1hOuJ-W4k` |

### Travail effectué
- **11 Google Docs créés** avec `replaceDocumentWithMarkdown(firstHeadingAsTitle: true)`
- **JUSTIFIED appliqué** sur les 11 documents
- **drive_id mis à jour** dans les fichiers locaux YAML
- **Total Drive** : 18 documents UNIFIE_ANONYME (03-09, 11-16, 18-21 + 03 Article 145 + anciens 01-14)

## Correction #2026-07-05 — Récit erroné 09 Courrier Inspection Travail ✅

### Problème
La version initiale du **09 Courrier Inspection Travail** contenait une erreur factuelle dans la description de l'accident et dans le fondement juridique :

- **Ligne 51** (INTRODUCTION) : « le préposé a escaladé le bac à shampoing **pour effectuer sa tâche** » — c'est faux. Il est monté sur le bac pour **régler le poste de télévision**.
- **Ligne 74** (liste manquements) : le fondement invoqué était la **formation sécurité** (L. 4141-2) — inadapté. Il s'agit d'un défaut d'**équipement d'accès en hauteur** (L. 4121-1 + R. 4323-58 et suivants).

### Correction appliquée
- **INTRODUCTION** : remplacé par « sur lequel il avait dû monter **pour accéder au poste de télévision, faute d'équipement d'accès adapté (escabeau)** »
- **Liste des manquements (puce 4)** : remplacée par **Absence d'équipement d'accès en hauteur** avec articles L. 4121-1 (obligation générale de sécurité) et R. 4323-58 et suivants (travaux en hauteur)
- **Version Drive mise à jour** via `replaceDocumentWithMarkdown` (même ID : `1tStFiBk8gxB6kWk_HQGPSLH2-QCQVxkARBz7SDer2gM`)
- **Fichier local corrigé** : `actes/02_Courriers/09_Courrier Inspection Travail.md`

---

## Phase 7 — Restructuration token/reel + README.md + Checker (6 juillet 2026) ✅

### Ce qui a été fait
- **Restructuration token/reel** : `actes/00-06` → `actes/token/00-06/`, `actes/07_Reel` → `actes/reel/`, script `generate_real_versions.py` réécrit (scan multi-dossiers, génération dans `actes/reel/` avec sous-dossiers miroirs + README.md)
- **17 README.md riches** créées : fil d'Ariane, emoji, table des fichiers, navigation verticale
- **INDEX.md → README.md** : 7 fichiers renommés
- **Règle répertoire souverain érigée** : AGENTS.md règle #10, RULES.md règle #0, DECISIONS.md, VACCIN.md
- **Clone parasite supprimé** (`/tmp/opencode/accident-main/`)
- **check_consistency.py corrigé** : patch URL decode (urllib.parse.unquote) + path ANNEXES `actes/token/06_Archives/annexes` → **0 erreur, 65 avertissements bénins** (`[À compléter]` placeholders)
- **Règle #1 RULES.md** : interdiction de poser des questions au conditionnel (vérifier par soi-même d'abord)
- **Plan H vérifié** : assignations 01 et 03 avec "PAR CES MOTIFS" conformes, visas corrects, bordereaux présents

### Vérification faite
- `check_consistency.py` : 0 erreur ✅
- Plan H : assignation 01 (visas 145+835 CPC / 1240+1242 CC, pièces 1-6, bordereau ✅), assignation 03 (visas 145 CPC / L.124-3 C. Assur, pièces 7-10, bordereau ✅)
- 14 PRs mergées (#28–#41), 0 PR ouverte

## Phase 7b — Bordereau séquentiel + Justification provision + Emails témoins (6 juillet 2026) ✅

### Ce qui a été fait
- **Nouveau bordereau séquentiel** : `04_Bordereau_Audience.md` créé — 25 pièces en 6 groupes thématiques (A-F), numérotation propre, dédoublonnée
- **Assignation 01 enrichie** : nouveau §D *Justification du montant de la provision* (5 arguments : fourchette référentiel, proportionnalité, provision *ad litem*, silence de l'exploitant, jurisprudence Cass.)
- **Email relance Dr DJERBI** : `25_Email Relance Dr DJERBI.md` — relance certificat consolidation
- **3 emails transmission attestations** : `26/27/28_Email Attestation` pour client/pompier/employé
- **Génération versions réelles** : 46 fichiers regénérés dans `actes/reel/` (incl. 5 nouveaux)
- **Document clé identifié** : Réquisition Police UMJ 02/06/2026 (PDF) + retranscription téléphonique — confirme le rendez-vous réel du **12 novembre 2026** à Purpan
- **Compréhension corrigée** : plus de dates fabriquées (31 juillet, expertise médicale civile) — seules dates réelles : 14 juillet (fin amiable), 12 novembre (UMJ ITT)
- **Check consistency** : 0 erreur, 65 avertissements bénins (inchangé)
- **2 commits + push** : phase 7b complète (modifs + generate_real_versions)
