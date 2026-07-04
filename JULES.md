# JULES — Guide pour l'agent Google Jules

Ce fichier documente tout ce que Jules (Google Jules) doit savoir pour travailler sur ce projet.

## Structure du projet

```
accident-main/
├── markdown_normalized/    ← Source de vérité : 14 fichiers .md prêts à injecter
├── memory/                 ← Mémoire persistante partagée
│   ├── PIECES_MAP.md       ← Mapping fichier.md ↔ Google Doc ID (indispensable !)
│   ├── TOKEN_MAP.md        ← Correspondance jetons ↔ identités réelles
│   ├── STRICT_VARIABLES.md ← Dates, montants, faits vérifiés
│   ├── RULES.md            ← Règles permanentes et interdictions
│   ├── DECISIONS.md        ← Décisions d'architecture
│   └── STATUS.md           ← État d'avancement détaillé
├── app/
│   ├── batch_anonymize.py  ← Script d'anonymisation (source officielle des tokens)
│   ├── add_page_breaks.py  ← Script d'ajout des marqueurs === PAGE BREAK ===
│   └── injection.py        ← Script d'injection .md → Google Docs
├── JULES.md                ← Ce fichier
├── .env.example            ← Variables d'environnement requises
└── ...
```

## Liens utiles

- **Dossier Drive de travail** : `1LnXAHlLLLHN0quyhiRq4CdVAKHRGolWk`
- **Annuaire Lois** : `14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ`
- **ARCHIVES** : `1poohpxlkv79P5QcvVcXoYXj80nKFEDPV`

## Convention `=== PAGE BREAK ===`

Les fichiers `.md` dans `markdown_normalized/` utilisent le marqueur `=== PAGE BREAK ===` pour indiquer où insérer des sauts de page lors de l'injection dans Google Docs.

**Emplacements standards** :
- Après l'introduction (avant le corps du document)
- Avant chaque section majeure (`# I.`, `# II.`, `# III.`, etc.)
- Avant chaque Annexe (A, B, C)

**Algorithme d'injection** :
1. Lire le `.md`
2. Splitter sur `=== PAGE BREAK ===`
3. Segment 1 → `replaceDocumentWithMarkdown(firstHeadingAsTitle=true)`
4. Segments 2..N → `appendMarkdown()` + `insertPageBreak()` à la fin du doc

## Mapping fichiers ↔ Google Docs

Le fichier `memory/PIECES_MAP.md` contient le mapping complet :
- Nom du fichier `.md` → ID Google Docs
- Les IDs sont stables (ne changent pas après renommage)

**Exemple** :
```
### Doc 01 — Assignation Reféré Provision FINAL
`1ZIfWjszjl5VoxBxourQiDeRATbkckkWPzbU9tYmg5yg`
```

## Setup initial (Jules)

Dans Jules Settings → Setup script, mettre :

```
./setup.sh
```

Le script **doit être exécuté** pour matérialiser les credentials dans des fichiers
(`.drive-token.json` et `.piste-credentials.json`), car Jules supprime les
variables d'environnement après le setup (sécurité).

Ce script installe les dépendances Python et configure l'accès Drive.

## Google Drive — CLI Python

Le projet expose un client Drive natif via `app/drive_client.py` :
(alternative aux outils MCP Docs quand ils sont indisponibles)

```bash
# Lister les fichiers du dossier cible
uv run python -m app.drive_client list

# Filtrer par type
uv run python -m app.drive_client list --type document
uv run python -m app.drive_client list --type folder

# Lire un Google Doc (export markdown)
uv run python -m app.drive_client export <FILE_ID> --format markdown --print

# Télécharger un fichier
uv run python -m app.drive_client download <FILE_ID> --output ./local.txt

# Uploader un fichier
uv run python -m app.drive_client upload ./monfichier.pdf --name "Mon Fichier"

# Créer un dossier
uv run python -m app.drive_client create-folder "Nouveau dossier"

# Chercher un fichier par nom
uv run python -m app.drive_client search --name "Assignation"
```

## MCP Servers disponibles

| Serveur | Usage | Auth |
|---------|-------|------|
| Google Docs (MCP) | Création/lecture/modification de documents | OAuth2 → `gcp-oauth.keys.json` |
| Légifrance | Recherche de lois, codes, textes légaux | OAuth2 Piste → `gcp_souverain_token.json` |
| Légifrance Prod | Version production de Légifrance | OAuth2 Piste → `gcp_souverain_token.json` |
| Judilibre | Recherche de jurisprudence (Cour de cassation) | OAuth2 Piste → `gcp_souverain_token.json` |
| Drive CLI (Python) | Opérations Drive avancées (upload, export, search, read-sheet) | OAuth2 → env vars |
| MCP Bridge (Python) | API juridiques Judilibre + Légifrance via Piste | OAuth2 Piste → `PISTE_CREDENTIALS` |

## Credentials requis

Ces fichiers doivent être présents dans `/home/crilocom/.opencode/` :

| Fichier | Contenu |
|---------|---------|
| `gcp-oauth.keys.json` | JSON OAuth2 Google (Client ID + Client Secret) |
| `gcp_souverain_token.json` | Token OAuth2 Piste (API juridiques françaises) |

**Variables d'environnement Drive** (configurer dans Jules Settings → Environment Variables) :

| Variable | Source |
|----------|--------|
| `GOOGLE_DRIVE_CLIENT_ID` | `gcp-oauth.keys.json` → `installed.client_id` |
| `GOOGLE_DRIVE_CLIENT_SECRET` | `gcp-oauth.keys.json` → `installed.client_secret` |
| `GOOGLE_DRIVE_REFRESH_TOKEN` | `~/.config/gcloud/application_default_credentials.json` → `refresh_token` |
| `GOOGLE_DRIVE_FOLDER_ID` | `16Qm2fEzojRQ3_yylsSwlkynbVv1L0SvB` (dossier Accident Main) |

**Ne JAMAIS commit ces fichiers dans Git.** Ils sont dans `.gitignore`.

## Bibliothèque juridique locale (`lois/`)

Le dossier `lois/` contient 16 textes juridiques (articles de code + jurisprudences) extraits du Drive dossier **00 Lois**, convertis en `.md`.

- `lois/INDEX.md` — tableau récapitulatif des 16 fichiers
- Lire un fichier : `cat lois/Article1242_CodeCivil.md`
- Chercher un texte : `grep -ri "responsabilité" lois/`

Utile quand les API juridiques ne sont pas disponibles.

## MCP Bridge — API juridiques (via Piste)

Le module `app/mcp_bridge/` contient les clients Judilibre et Légifrance adaptés pour un usage CLI (sans dépendance FastMCP).

```bash
# Vérifier la configuration
uv run python -m app.mcp_bridge.cli check

# Judilibre — rechercher
uv run python -m app.mcp_bridge.cli judilibre-search "responsabilité commerçant" --chamber civ1 --date-from 2020-01-01

# Judilibre — consulter une décision
uv run python -m app.mcp_bridge.cli judilibre-decision 5fca85dfa8ef0376a5ff647a

# Légifrance — rechercher dans les codes
uv run python -m app.mcp_bridge.cli legifrance-search "article 1242" --fond CODE

# Légifrance — consulter un article
uv run python -m app.mcp_bridge.cli legifrance-article LEGIARTI000032041559
```

## Google Sheets — Annuaire Lois

```bash
uv run python -m app.drive_client read-sheet --sheet-id 14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ
```

## Workflow typique pour Jules

### 1. Injection d'un .md vers Google Docs

Utiliser `app/injection.py` ou faire manuellement :

```python
# 1. Lire le fichier .md
with open('markdown_normalized/01_Assignation_...') as f:
    content = f.read()

# 2. Splitter sur === PAGE BREAK ===
segments = content.split('=== PAGE BREAK ===')

# 3. Segment 0 → replaceDocumentWithMarkdown (remplace tout le doc)
for i, seg in enumerate(segments):
    seg = seg.strip()
    if not seg:
        continue
    if i == 0:
        replaceDocumentWithMarkdown(
            documentId=doc_id,
            markdown=seg,
            firstHeadingAsTitle=True
        )
    else:
        appendMarkdown(documentId=doc_id, markdown=seg)
        insertPageBreak(documentId=doc_id, index=get_doc_length(doc_id) + 1)
```

### 2. Vérification

Lire les 500 premiers caractères du doc pour confirmer le rendu :
```
readDocument(documentId, maxLength=500)
```

### 3. Recherche juridique

- `legifrance_rechercher_code(query="...")` — recherche dans les codes
- `legifrance_rechercher_jurisprudence(query="...")` — recherche de décisions
- `judilibre_rechercher_jurisprudence(query="...")` — recherche Judilibre
- `judilibre_consulter_decision(decision_id="...")` — lecture intégrale

### 4. Gestion du Drive

- `google-docs_readDocument(documentId)` — lire un doc
- `google-docs_replaceDocumentWithMarkdown(documentId, markdown)` — injecter
- `google-docs_appendMarkdown(documentId, markdown)` — ajouter à la fin
- `google-docs_insertPageBreak(documentId, index)` — saut de page
- `google-docs_applyParagraphStyle(documentId, target, style)` — style paragraphe
- `google-docs_applyTextStyle(documentId, target, style)` — style texte

## Règles importantes

1. **Ne JAMAIS inventer de statut juridique** — si une info n'est pas dans les sources, ne pas l'inventer
2. **Toujours vérifier** les tokens d'anonymisation dans `memory/TOKEN_MAP.md` avant modification
3. **Les sauts de page** (`=== PAGE BREAK ===`) sont obligatoires : intro, sections, annexes
4. **Le mapping** fichier ↔ Google Doc est dans `memory/PIECES_MAP.md` — le consulter avant toute injection
5. **Ne pas modifier** directement les Google Docs avec find/replace ou regex — toujours passer par `replaceDocumentWithMarkdown`
