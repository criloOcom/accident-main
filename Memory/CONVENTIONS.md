---
title: "CONVENTIONS DE FORMATAGE UNIFIÉES"
description: "Document unique et souverain définissant toutes les règles de formatage des fichiers .md du projet. Tout agent DOIT s'y conformer."
type: memory
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › CONVENTIONS*
<hr>
<!-- /Breadcrumb -->

# CONVENTIONS DE FORMATAGE UNIFIÉES
> **Règle absolue** : tout fichier `.md` du projet DOIT respecter ces conventions. Aucune exception sans décision explicite dans [DECISIONS.md](DECISIONS.md). En cas de conflit entre CONVENTIONS.md et tout autre fichier, **CONVENTIONS.md prévaut**.

<hr><hr>

## I — ORDRE CANONIQUE DU FICHIER

Chaque fichier `.md` suit strictement cet ordre :

```
1.  ---                                # YAML front matter (ligne 1)
2.  title: "..."
3.  description: "..."
4.  type: "..."
5.  ---
6.                                      # ligne vide
7.  <!-- Breadcrumb -->                # breadcrumb en commentaire HTML
8.  *[🏠](../README.md) › ...
9.  <!-- /Breadcrumb -->
10. <hr>                               # séparateur unique après breadcrumb
11.                                     # ligne vide
12. # TITRE DU DOCUMENT                 # H1 unique
13. [> Citation éventuelle]
14. <hr><hr>                           # double séparateur AVANT section I
15. ## I — PREMIÈRE SECTION
16. ...
17. <hr><hr>                           # double séparateur AVANT section II
18. ## II — DEUXIÈME SECTION
...
```

### Règles d'ordre
1. **Ligne 1 = `---`** : le YAML commence à la ligne 1 obligatoirement (prévisualisation GitHub)

2. **Breadcrumb immédiatement après le YAML** : commentaire HTML `<!-- Breadcrumb -->`, pas d'autre contenu entre YAML et breadcrumb

3. **`<hr>` simple** après le breadcrumb (séparation breadcrumb/titre)

4. **H1 unique** `# Titre` : un seul titre de niveau 1 par fichier

5. **`<hr><hr>`** avant chaque section de premier niveau (sauf la 1ère — vient après le bloc citation si présent)

<hr><hr>

## II — YAML FRONT MATTER

### Champs obligatoires
```yaml
---
title: "Mon Titre"
description: "Résumé court."
type: acte|analyse|courrier|organisation|memory|rapport
---
```

### Champs de cross-reference (dans Token)
```yaml
reel_path: ../../Reel/{subdir}/{fichier}.md
drive_id: {Google Drive ID}
calendar_event_id: "{Google Calendar event ID}"
calendar_event_ids:
  - "{event_id_1}"
  - "{event_id_2}"
statut: brouillon|projet|preparation|final|archive
```

- `calendar_event_id`: pour un fichier correspondant à **un seul événement** Google Calendar `[AM]`

- `calendar_event_ids`: liste pour un fichier correspondant à **plusieurs événements** (ex: envoi courrier + sa date butoir)

### Règles
1. **Ligne 1 = `---`** : toujours, sans rien avant

2. `title` et `description` : obligatoires

3. `type` : valeur canonique (pas d'invention)

4. Les champs `drive_id`, `calendar_event_id`, `calendar_event_ids`, `statut` : optionnels mais encouragés

5. `reel_path` / `token_path` : obligatoires pour la double strate

<hr><hr>

## III — HIÉRARCHIE DES TITRES

| Niveau | Format | Usage |
|--------|--------|-------|
| `# Titre` | H1 unique | Titre du document (un seul par fichier) |
| `## I — TITRE` | H2 romain | Section majeure (I., II., III., IV.) |
| `## A.` / `## PAR CES MOTIFS` | H2 nommé | Section spéciale (exposé, dispositif, annexes) |
| `### A. TITRE` | H3 lettre | Sous-section d'une section majeure |
| `### 1. Titre` | H3 chiffre | Sous-section numérotée |
| `#### a) Titre` | H4 lettre | Sous-sous-section |
| `#### i. Titre` | H4 romain | Sous-sous-section (i., ii., iii.) |

### Règles
1. **H1 unique** : un seul `# Titre` par fichier, correspond au titre du document

2. **Sections majeures en `## I — TITRE`** : chiffres romains (I, II, III, IV, V, VI, VII)

3. **Tiret cadratin ` — `** : entre le numéro romain et le titre (espace + em dash + espace)

4. **Sous-sections en `###`** : lettres A./B./C. ou chiffres 1./2./3.

5. **Sous-sous-sections en `####`** : lettres a)/b) ou romains i./ii.

6. **Pas de saut de hiérarchie** : on ne passe pas de `##` à `####` sans `###` intermédiaire

7. **Articles de loi exclus des headings** : pas de référence législative entre parenthèses dans les titres

<hr><hr>

## IV — SÉPARATEURS DE SECTION

### Principe
Les sections de premier niveau sont séparées par `<hr><hr>` (double `<hr>`) pour marquer visuellement un saut de section majeur, à l'image d'un saut de page.

### Règle
1. `<hr><hr>` est inséré **AVANT** chaque section de premier niveau (`## I —`, `### I.`, `## EXPOSÉ`, `## PAR CES MOTIFS`, `## A.`, `## B.`, `## C.`, etc.) **sauf la 1ère section**

2. `<hr><hr>` remplace tout séparateur existant (`<hr>`, `<hr><hr>`, `---` HR)

3. **Pas de séparateur** entre les sous-sections `### A./B./C.` ou `### 1./2./3.` d'une même section

4. **Pas de séparateur** entre un titre `##` et sa première sous-section `###`

5. Le `---` (triple tiret) **n'est pas utilisé comme séparateur de section** — il est réservé au YAML front matter. Tout `---` dans le corps du fichier (hors code blocks) qui sert de HR doit être remplacé par `<hr><hr>`

6. Le `<hr>` simple après le breadcrumb est conservé (c'est un usage différent — séparation navigation/contenu)

### Exemple visuel
```markdown
# Titre du document

<hr><hr>

## I — PREMIÈRE SECTION

Contenu...

### A. Sous-section
### B. Sous-section

<hr><hr>

## II — DEUXIÈME SECTION
```

<hr><hr>

## V — CITATIONS

### Format canonique d'un bloc de citation juridique
```markdown
> « Texte de l'article ou extrait de jurisprudence » <br>
> **[Code > Article/Section > Alinéa]** <br>
> [Article X du Code Y](https://www.legifrance.gouv.fr/...)
```

### Ordre des lignes
1. **Texte** : l'extrait entre `« »` (guillemets français)

2. **Filiation** : `**[Code > Article > ...]**` en gras

3. **Lien** : `[Article X](URL%20L%C3%A9gifrance)` — lien inline obligatoire

4. Chaque ligne se termine par `<br>` (sauf la dernière si elle termine le bloc)

### Règles
1. Toute citation d'article de loi DOIT être vérifiée via MCP Légifrance (legifrance-prod PUIS openlegi)

2. Le lien Légifrance est obligatoire sur toute citation

3. Privilégier la citation courte — un extrait suffit, pas besoin de l'article entier

4. Ne jamais citer de mémoire — toujours vérifier

<hr><hr>

## VI — TOKENS D'ANONYMISATION

### Format
```
**[Token en français avec article]**
```

### Règles
1. **Toujours en gras** : `**[La Victime]**`, pas `[La Victime]`

2. **Toujours avec article** : `**[La Victime]**`, pas `**[Victime]**`

3. **Français correct** : `**[L'Exploitant du Commerce (La SAS)]**`, pas de franglais

4. **Pas de civilité** : supprimer "Monsieur/Madame/Dr" devant les tokens

5. **Jamais de version réelle dans les fichiers Token** — uniquement dans `Reel/`

6. Correspondance token ↔ réel dans `Memory/TOKEN MAP.md` uniquement

<hr><hr>

## VII — LIENS

### Liens internes (dans le dépôt)
- **Toujours relatifs** : `[texte](chemin/relatif.md)`, jamais `file://` ou `/absolu/`

- **Toujours cliquables** : pas de chemin entre backticks sans lien — `[Rapports](Rapports/README.md)` ✓, `` `Rapports` `` ✗

- **Dossier cité** → lien vers son `README.md`

- **Fichier cité** → lien direct vers le fichier

- **URL-encoding** des caractères spéciaux (espaces → `%20`, émojis → encodés)

### Liens externes
- **URL absolues autorisées** : Légifrance (`https://www.legifrance.gouv.fr/...`), Judilibre, sites web

- **Drive** : `https://drive.google.com/open?id=<ID>`

- **Toujours HTTPS** : pas de HTTP nu

<hr><hr>

## VIII — DRIVE LINK

Tout fichier avec `drive_id:` dans son YAML DOIT exposer un lien cliquable juste après le YAML, avant le breadcrumb :

```markdown
> 🔗 Source Google Drive : [ID court](https://drive.google.com/open?id=<ID>)
```

Généré automatiquement par `.dev/app/add_drive_links.py`.

<hr><hr>

## IX — GESTION DES `[À COMPLÉTER]`

### Format standard
```
**[À compléter : description précise]**
```

### Règles
1. Toujours entre `**[...]**` (gras)

2. Toujours avec un descriptif : pas de `**[À compléter]**` seul

3. Exemples valides : `**[À compléter : adresse du destinataire]**`, `**[À compléter : numéro LRAR après envoi]**`

4. Un fichier contenant des `**[À compléter]**` ne peut pas avoir `statut: final` — doit être `brouillon` ou `projet`

<hr><hr>

## X — README ET INDEX

### Règles pour les listes de fichiers
- **Listes à puces** Markdown (pas de tableaux à colonne de numéros)

- Format : `- **[Nom lisible](chemin.md)** — *Fondement* — Résumé court.`

- Inclure un diagramme **Mermaid** dans les README de dossier pour la navigation

### Fils d'Ariane (breadcrumbs)
- Commentaire HTML `<!-- Breadcrumb -->...<!-- /Breadcrumb -->`

- Toujours après YAML, avant `# Titre`

- `[🏠](../README.md)` comme lien racine (pas le mot "Accueil")

- Généré par `.dev/app/generate_breadcrumbs.py` — ne pas éditer à la main

<hr><hr>

## XI — PIPELINE D'UNIFICATION

Après TOUTE création ou modification importante de fichiers `.md`, exécuter dans l'ordre :

```bash
python3 .dev/app/normalize_sections.py --apply         # <hr><hr> entre sections
python3 .dev/app/unify_headings.py --apply              # titres en chiffres romains
python3 .dev/app/normalize_blank_lines.py               # lignes vides entre paragraphes
python3 .dev/app/normalize_blocks.py --apply             # citations canoniques
python3 .dev/app/dedup_citation_text.py --apply          # dédoublonnage
python3 .dev/app/generate_real_versions.py               # sync Reel ← Token
python3 .dev/app/check_consistency.py                    # validation finale
```

Les caches (`__pycache__`, `.pytest_cache`) sont supprimés après exécution.

<hr><hr>

## XII — INTERDICTIONS

1. **Jamais de liens absolus internes** (`file://` ou `/Actes/...`)

2. **Jamais de `---` comme séparateur de section** (sauf YAML front matter)

3. **Jamais de `<hr>` simple entre sections** — toujours `<hr><hr>`

4. **Jamais de backtick sans lien** pour citer un fichier/dossier interne

5. **Jamais de version réelle dans `Token/`** (uniquement dans `Reel/`)

6. **Jamais de markdown brut / regex / find-replace direct sur Google Docs**

7. **Jamais de tableau à numéros pour les listings** (listes à puces seulement)

8. **Jamais d'article de loi dans les headings** (corps du texte seulement)

9. **Jamais d'espace insécable** dans les liens ou chemins relatifs

10. **Jamais de titre `#` en double** dans un même fichier

11. **Jamais de liens Markdown dans le YAML** (`[texte](url)` interdit dans `---`...`---` — le YAML est un format de données, pas du Markdown)

<hr><hr>

## XIV — PIECES JOINTES

### Format canonique (OBLIGATOIRE)
```markdown
## PIECES JOINTES

- **[Nom du document lisible](chemin/relatif/vers/fichier.md)** — Description contextuelle avec [placeholders] si besoin
```

### Règles
1. **Titre** : `## PIECES JOINTES` (toujours H2, en majuscules)

2. **Ligne vide** entre le titre et la première puce

3. **Chaque pièce = une puce** avec `- ` (pas de liste numérotée)

4. **Lien sur le nom** : le lien est dans la partie en gras, pas dans la description

5. **Bold + link** : `- **[Display](path)** — texte` — la **double astérisque englobe le lien**

6. **Séparateur ` — `** : espace + em-dash + espace entre le lien et la description

7. **Description** : texte libre après ` — `, peut contenir des tokens `[**[Token]**]` ou des `[placeholders]`

8. **Pas de double lien** : ne pas mettre un lien dans le nom ET un lien dans la description

9. **Pas de `/` entre deux pièces** : chaque document sur sa propre ligne

10. **Pas de `(description)`** à la place de ` — description`

11. **Puce simple** : `- ` sans numéro, même pour des listes longues

### Exemple concret (conforme)
```markdown
- **[PV n°2026/015967](../../Preuves%20officielles/20260602%20...)** — Depot de plainte du [J+4]

- **[Mise en demeure J+31 — SAS](../%F0%9F%93%9C%20Mises%20en%20demeure/J%2B31%20...)** — LRAR n° [N° LRAR Exploitant]
```

### Anti-exemples (non conformes)
```markdown
✗ - **PV** — [path](url)              ← lien dans la description, pas dans le gras
✗ - **[Doc](path)**                    ← pas de description après ` — `
✗ - **[Doc](path)** / [Doc2](path2)   ← deux documents sur une ligne
✗ - **[Doc](path)** (description)      ← parenthèses au lieu de ` — `
✗ 1. **Doc** — description             ← liste numérotée au lieu de puces
```

### Règle
Tout bloc de texte DOIT être séparé du bloc précédent par **une ligne vide** (`\n\n`), sauf exceptions ci-dessous.

### Blocs concernés
- Paragraphe → `##` / `###` heading

- `###` heading → `-` bullet

- `1. **Titre**` → `-` bullet

- `**Titre gras:**` → blockquote `>`

- Blockquote `>` → `##` heading

- `##` heading → paragraphe

- Item numéroté `N. **...**` → item numéroté suivant `N+1. **...**`

- Item à puce `- ...` (ou `* ...`) → item à puce suivant `- ...`

- Item à puce indenté `   - ...` → item à puce indenté suivant `   - ...`

> **🔴 POLITIQUE DE FORMATAGE DES LISTES À PUCES**
> Toute liste à puces (`- `, `* `, `- [ ]`) DOIT être en format **loose** :
> ```
> - item 1
> 
> - item 2
> 
> - item 3
> ```
> **→ Une ligne vide entre chaque item de même niveau.**
> Les sous-listes indentées sont également concernées (même règle à leur niveau).
> Script de correction : `.dev/app/normalize_list_spacing.py --apply`
> Audit pré-commit : intégré dans `.dev/hooks/pre-commit`

### Exceptions (pas de ligne vide)
1. **Headings consécutifs** : `## I — Section` suivi de `### A. Sous-section` — pas de vide

2. **YAML front matter** : toujours lignes 1 à ~5, pas de vide interne

3. **`<hr>` simple** après breadcrumb : formatage fixe

4. **Blockquote multi-lignes** : lignes `>` consécutives sans vide = même citation

5. **`<hr><hr>` séparateur** : déjà entouré de lignes vides par convention

### Exemple visuel
```markdown
Texte du paragraphe.

## I — SECTION

### A. Sous-section
### B. Sous-section

1. **Titre**

   - Premier élément

   - Second élément

**Fondement :**

> « Citation... » <br>
> [Article X](url)
```