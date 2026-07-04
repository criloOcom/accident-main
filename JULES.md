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

## MCP Servers disponibles

| Serveur | Usage | Auth |
|---------|-------|------|
| Google Docs (MCP) | Création/lecture/modification de documents | OAuth2 → `gcp-oauth.keys.json` |
| Légifrance | Recherche de lois, codes, textes légaux | OAuth2 Piste → `gcp_souverain_token.json` |
| Légifrance Prod | Version production de Légifrance | OAuth2 Piste → `gcp_souverain_token.json` |
| Judilibre | Recherche de jurisprudence (Cour de cassation) | OAuth2 Piste → `gcp_souverain_token.json` |

## Credentials requis

Ces fichiers doivent être présents dans `/home/crilocom/.opencode/` :

| Fichier | Contenu |
|---------|---------|
| `gcp-oauth.keys.json` | JSON OAuth2 Google (Client ID + Client Secret) |
| `gcp_souverain_token.json` | Token OAuth2 Piste (API juridiques françaises) |

**Ne JAMAIS commit ces fichiers dans Git.** Ils sont dans `.gitignore`.

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
