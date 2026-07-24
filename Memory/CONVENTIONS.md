---
uid: 5Yp3Etay6
title: "CONVENTIONS DE FORMATAGE UNIFIÉES"
description: "Document unique et souverain définissant toutes les règles de formatage des fichiers .md du projet. Tout agent DOIT s'y conformer."
type: memory
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Memory](./README.md) › CONVENTIONS*
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

### Schéma de référence
Le schéma JSON canonique est dans `.dev/app/yaml_schema.json` — source unique de vérité pour la structure YAML.

### Champs obligatoires
```yaml
---
title: "Mon Titre"
type: voir types canoniques ci-dessous
---
```

### Champs recommandés
```yaml
emoji: 📜                            # Emoji représentatif
subtitle: "Sous-titre contextuel"    # Contexte du document
objective: "Objectif du document"    # Pourquoi ce document existe
summary: "Résumé en 1-2 phrases"     # Résumé du contenu
key_points:                          # Points clés structurés
  - Point important 1
  - Point important 2
recipient: "Destinataire nominal"    # Qui reçoit
jurisdiction: "Juridiction"         # Tribunal compétent
legal_basis:                         # Fondement juridique
  - Article X du Code Y
description: "Description libre"     # Résumé court (fallback)
tags:
  - mot-cle-1
  - mot-cle-2
urgence: haute                       # haute|moyenne|basse|critique
```

### Types canoniques
Liste exhaustive (source : `CANONICAL_TYPES` dans `.dev/app/yaml_utils.py`) :

| Type | Description |
|------|-------------|
| `loi` | Article de code juridique |
| `jurisprudence` | Décision de justice (arrêt) |
| `courrier` | Courrier / correspondance |
| `assignation` | Acte d'assignation en justice |
| `plainte` | Plainte pénale |
| `analyse` | Analyse ou mémorandum juridique |
| `analyse_juridique` | Analyse ou mémorandum juridique |
| `etude_indemnisation` | Étude d'indemnisation (Dintilhac) |
| `rapport` | Rapport d'audit ou d'expertise |
| `projet` | Projet, simulation ou version de travail |
| `readme` | Fichier d'index / porte d'entrée |
| `memory` | Fichier mémoire du projet |
| `status` | Suivi d'état d'envoi |
| `preuve` | Pièce de preuve brute |
| `archive` | Document archivé |
| `fiche` | Fiche réflexe / note |
| `document` | Document général |
| `directory` | Index de répertoire |
| `attestation` | Attestation de témoin |
| `organisation` | Fiche organisation / synthèse |
| `email` | Email / message électronique |
| `session` | Session de travail / audit |

### Valeurs de `statut`
`brouillon` | `projet` | `preparation` | `envoye` | `final` | `archive` | `fusionne` | `recueillie`

### Champs de cross-reference (dans Token)
```yaml
reel_path: ../../Reel/{subdir}/{fichier}.md   # Obligatoire dans Token
drive_id: {Google Drive ID}                     # Optionnel
calendar_event_id: "{Google Calendar event ID}" # Optionnel
calendar_event_ids:                             # Optionnel (multi-événements)
  - "{event_id_1}"
  - "{event_id_2}"
statut: brouillon|projet|preparation|envoye|final|archive
jx: J+52                # Code J±XX du jour par rapport à l'accident
legiarti: LEGIARTI...   # ID Légifrance article
juritext: JURITEXT...   # ID Légifrance décision
```

### Règles
1. **Ligne 1 = `---`** : toujours, sans rien avant

2. **`title` et `type` obligatoires**, tout le reste est facultatif mais encouragé

3. **`type`** : valeur canonique uniquement (pas d'invention). Voir la liste exhaustive ci-dessus

4. **`description`** : ne pas confondre avec `auteur` ou `destinataire`. Champ de texte libre décrivant le document

5. **Pas de quotes systématiques** : les valeurs sans `:`, `#`, `{`, `}`, `[`, `]`, `,`, `&`, `*`, `?`, `|`, `-`, `<`, `>`, `!`, `@`, `` ` `` n'ont pas besoin de quotes. En cas de doute, utiliser des **single quotes** `'...'` (doubler les apostrophes : `'L''exemple'`)

6. **Validation automatique** : `.dev/app/yaml_validator.py` vérifie types, statuts, dates, et liens. Intégré au pre-commit hook (Règle #23)

7. **Schéma JSON** : `.dev/app/yaml_schema.json` est le schéma de référence pour les IDE et pipelines CI

8. Les champs `drive_id`, `calendar_event_id`, `calendar_event_ids`, `statut` : optionnels mais encouragés

9. `reel_path` : obligatoire dans Token, interdit dans Reel

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

### Règle des Blocs Objet (Courriers et Actes)
7. **RÈGLE STRICTE DES BLOCS OBJET** : Tout bloc d'objet dans un courrier ou un acte DOIT être encadré par des séparateurs simples `<hr>` et balisé par des commentaires HTML `<!-- Objet -->` et `<!-- /Objet -->`. Les doubles séparateurs `<hr><hr>` autour d'un bloc `Objet` sont STRICTEMENT INTERDITS.

```markdown
<!-- Objet -->
<hr>

Objet : [Texte clair et propre de l'objet]

<hr>
<!-- /Objet -->
```

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
1. Toute citation d'article de loi DOIT être lue et vérifiée via MCP Légifrance (`consulter_article` ou `rechercher_code` via MCP Légifrance) (legifrance-prod PUIS openlegi)

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
1. **Toujours en gras** : `[**[La Victime]**](../Memory/Tokens/token-victime-nom-complet.md)`, pas `[La Victime]`

2. **Toujours avec article** : `[**[La Victime]**](../Memory/Tokens/token-victime-nom-complet.md)`, pas `**[Victime]**`

3. **Français correct** : `[**[L'Exploitant du Commerce (La SAS)]**](../Memory/Tokens/token-exploitation-raison-sociale.md)`, pas de franglais

4. **Pas de civilité** : supprimer "Monsieur/Madame/Dr" devant les tokens

5. **Jamais de version réelle dans les fichiers Token** — uniquement dans `Reel/`

6. Correspondance token ↔ réel dans [Memory/TOKEN MAP.md](TOKEN MAP.md) uniquement

<hr><hr>

## VII — LIENS

### Liens internes (dans le dépôt)
- **Toujours relatifs** : `[texte](chemin/relatif.md)`, jamais `file://` ou `/absolu/`

- **Toujours cliquables** : pas de chemin entre backticks sans lien — `[Rapports](../Rapports/README.md)` ✓, `` [Rapports](../Rapports/README.md) `` ✗

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
- **Lien croisé Token↔Reel (OBLIGATOIRE)** : dans la double strate `Actes/Token/X ↔ Actes/Reel/X`, le fil d'ariane se termine par un lien cliquable vers l'autre monde :
  - Fichier **Token** : `... › Nom du dossier (👤)` où `👤` pointe vers `Actes/Reel/X` correspondant
  - Fichier **Reel** : `... › Nom du dossier (🎭)` où `🎭` pointe vers `Actes/Token/X` correspondant
  - Calculé dynamiquement par `cross_world_link()` (symétrie `Token`↔`Reel`, sans champ YAML `reel_path`). Lien cliquable UNIQUEMENT si la cible existe (zéro lien mort, Règle #16).
  - Régénéré pour tout le dépôt par `python3 .dev/app/generate_breadcrumbs.py --apply` (à lancer APRÈS `generate_real_versions.py`).
  - Exemple Token : `*[🏠](../../../README.md) › [📁 Actes](../../README.md) › [🎭 Token](../README.md) › [Preuves officielles](./README.md) › Preparation Expertise UMJ ([👤](../../Reel/Preuves_officielles/Preparation_Expertise_UMJ.md))*`
  - Exemple Reel : `*[🏠](../../../README.md) › [📁 Actes](../../README.md) › [👤 Reel](../README.md) › [Preuves officielles](./README.md) › Preparation Expertise UMJ ([🎭](../../Token/Preuves_officielles/Preparation_Expertise_UMJ.md))*`
- **UID dans le YAML (OBLIGATOIRE)** : chaque fichier `.md` DOIT avoir un champ `uid:` unique dans son front matter (voir Règle #33). Le `uid` est la clé de cross-référencement entre Token et Reel (même `uid` pour la paire), l'indexation Google Sheet PJ, et le lien entre les deux mondes. Un fichier sans `uid:` est en violation de Règle #30/#33. Le générateur `generate_real_versions.py` copie le `uid` Token vers le Reel ; le fil d'ariane n'affiche pas l'UID mais l'élément `(👤)`/`(🎭)` en fin de chaîne EST le repère visuel de la double strate.

<hr><hr>

## XI — PIPELINE D'UNIFICATION
Après TOUTE création ou modification importante de fichiers `.md`, exécuter dans l'ordre :

```bash
python3 .dev/app/normalize_sections.py --apply         # <hr><hr> entre sections
python3 .dev/app/unify_headings.py --apply              # titres en chiffres romains
python3 .dev/app/normalize_blank_lines.py               # lignes vides entre paragraphes
python3 .dev/app/normalize_blocks.py --apply             # citations canoniques
python3 .dev/app/dedup_citation_text.py --apply          # dédoublonnage
python3 .dev/app/generate_real_versions.py               # sync Reel ← Token (OBLIGATOIRE après toute modif de liens)
python3 .dev/app/generate_breadcrumbs.py --apply        # fil d'ariane + lien croisé 🎭/👤 (APRÈS generate_real_versions)
python3 .dev/app/check_consistency.py                    # validation finale
```

### Règle d'or des liens internes (NON-RÉGRESSION)
- **TOUTE correction de lien interne se fait DANS LE TOKEN** (et les sources non-Reel : `Rapports/`, `Memory/`, `Lois/`, `Status/`). **JAMAIS dans `Actes/Reel/`** (Règle #22 INTERDICTION #1 : le Reel est un artifact généré, toute édition manuelle est écrasée au prochain `generate_real_versions.py` et constitue une violation).
- Après avoir corrigé les liens dans les fichiers Token, lancer `generate_real_versions.py` : les miroirs Reel sont recréés avec les liens corrigés. Corriger le Reel à la main est DU TRAVAIL PERDU + une violation de Règle #22.
- Un lien interne DOIT être un chemin relatif calculé DEPUIS le fichier le contenant (jamais un chemin « racine projet » collé tel quel, ex. `Lois/Code/X.md` sans `../`). Voir Règle #15-bis.
- **UID unique obligatoire** : chaque fichier `.md` du dépôt DOIT porter un champ `uid:` dans son YAML (source unique de vérité, voir Règle #33). Le fil d'ariane de chaque fichier se termine par l'élément entre parenthèses `(👤)` / `(🎭)` (lien croisé Token↔Reel, Règle #15-bis) ; l'UID sert au cross-référencement et à l'indexation (Google Sheet PJ, Règle #32/#33). Un fichier sans `uid:` est en violation.

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

## XIII — BLOCS D'EN-TÊTE DES COURRIERS

### Format canonique

Chaque fichier de type `courrier` DOIT avoir trois blocs séparés dans l'en-tête :

```markdown
<!-- Auteur -->
[**[L'Expéditeur]**](...)  
[**[L'Adresse de l'Expéditeur]**]
<!-- /Auteur -->

<!-- Destinataire -->
...
<!-- /Destinataire -->

<!-- Date -->
**[La Ville]**, le 18 juillet 2026
<!-- /Date -->
```

### Règles

1. **Trois blocs distincts obligatoires** : `<!-- Auteur -->`, `<!-- Destinataire -->`, `<!-- Date -->` — chacun avec sa propre paire `<!-- XXX -->`/`<!-- /XXX -->`.

2. **Ligne vide** entre chaque bloc (après `<!-- /XXX -->`).

3. **Ordre impératif** : Auteur → Destinataire → Date.

4. **INTERDICTION ABSOLUE** : ne JAMAIS fusionner Auteur + Destinataire + Date sous un seul `<!-- Auteur -->`. Chacun son bloc.

### Anti-exemple (non conforme)

```markdown
✗ <!-- Auteur -->
✗ [**[L'Expéditeur]**]  
✗ [**[Le Destinataire]**]  
✗ **[La Ville]**, le ...
✗ <!-- /Auteur -->
```

### Exemple complet (conforme)

```markdown
<!-- Auteur -->
[**[La Victime]**](...)  
[L'Adresse de la Victime](../Memory/Tokens/token-victime-adresse.md)  
[L'Email de la Victime](../Memory/Tokens/token-victime-email.md)
<!-- /Auteur -->

<!-- Destinataire -->
Monsieur le Directeur  
GHT des Pyrénées Ariégeoises CHIVA  
Chemin de la Plaine  
09000 Saint-Jean-de-Verges
<!-- /Destinataire -->

<!-- Date -->
**[Foix]**, le 18 juillet 2026
<!-- /Date -->
```

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

<hr><hr>

## XV — RÈGLES DE MISE EN PAGE ET TYPOGRAPHIE GOOGLE DOCS (CHARTE CANONIQUE)

### 1. En-tête des courriers
- **Bloc Expéditeur** : Seul le **Nom Prénom** est en **gras**. L'adresse postale (voie et CP/ville sur une seule ligne séparées par une virgule) et l'adresse email (transformée en **hyperlien cliquable `mailto:` en Bleu Lien Google + Souligné**) sont en **texte normal (non gras)**. Retours à la ligne au sein du bloc gérés par des sauts doux (**Shift+Entrée** / 2 espaces) pour maintenir un interlignage compact.

- **Bloc Destinataire** : Seule la **Raison sociale / Organisme** est en **gras**. Les lignes de service et d'adresse postale (voie et CP/ville sur la même ligne séparées par une virgule) sont en **texte normal (non gras)**. Retours à la ligne au sein du bloc gérés par **Shift+Entrée**.

- **Séparation des blocs** : Séparer le bloc Expéditeur, Destinataire, Date et Objet par des sauts de paragraphe clairs (`&nbsp;` en Markdown).

- **Ligne Objet** : L'intitulé de la ligne **Objet : ...** est intégralement en **gras**. La ligne *Ref : ...* qui suit est en texte normal.

### 2. Taille des titres et typographie
- **Titres majeurs de sections** : La taille de police des titres de section (ex. `I — OBJET DE LA RELANCE`) est fixée à **16 pt** en **GRAS (BOLD)** (structure H3 / Heading 3).

- **Corps de texte** : Police standard 11 pt ou 12 pt, texte justifié.

### 3. Notes de bas de page (Footnotes)
- **Fonctionnalité native obligatoire** : Toute référence jurisprudentielle ou légale citée en note doit être insérée avec le composant native **Footnote** de Google Docs (`createFootnote` avec segment dédié).

- **Interdiction** : Ne jamais recréer de section factice "Sources" en simple texte au bas du document.

### 4. Section PIECES JOINTES
- **Titre de la section** : `PIECES JOINTES` en **16 pt GRAS**.

- **Puces de pièces jointes** :

  - **Intitulé de la pièce** (à gauche du tiret ` — `) : En **Bleu Lien Google + GRAS + Souligné + Hyperlien cliquable vers le fichier Google Drive**.
  - **Description explicative** (après le tiret ` — `) : Strictement en **Texte Noir normal (non gras, non souligné, non bleu)**.
- **Règle absolue** : Tous les agents (AntiGravity, OpenCode, Hermès, Jules) DOIVENT appliquer ce standard sans dérogation.

<hr><hr>

## XVI — GOOGLE SHEET PJ (PIÈCES JOINTES) — MAPPING CENTRALISÉ

### 1. Périmètre
Le Google Sheet **PJ** (`1cwb8L5fc7HqsAHP6IH32gSFwKRIdSztcYk1XmfbaYIg`) est l'index unique de tous les documents du projet, dans la feuille **`@`**.

### 2. Structure des colonnes (ligne 2 = en-têtes)

| Colonne | Champ | Contenu |
|---------|-------|---------|
| **A** | uid Preuve | uid du fichier source dans `Actes/Preuves_officielles/` |
| **B** | URL GitHub Preuve | Lien GitHub vers le fichier Preuve |
| **C** | 📄Fichier 🔑ID Drive | Google Drive ID du fichier source |
| **D** | Image ID | ID Google Drive de l'image |
| **E** | Docs ID | ID Google Docs du document |
| **F** | *(vide)* | Réserve |
| **G** | uid TOKEN | uid du fichier tokenisé (dans `Actes/Token/`) |
| **H** | uid TOKEN Url | URL GitHub du fichier Token |
| **I** | *(vide)* | Réserve |
| **J** | uid REEL | uid du fichier réel (identique à G) |
| **K** | uid REEL Url | URL GitHub du fichier Reel |

### 3. Règles de mapping
- Token et Reel partagent toujours le **même uid** (colonne G = colonne J).

- Les URLs GitHub sont dans la branche `main`.

- Les drive_id vides (colonne C/E vides) = document non encore lié à Google Drive.

- La ligne 1 du sheet contient le titre de la feuille. Les données commencent ligne 3 (en-têtes ligne 2).

## XVII — Protocole UID→YAML Cross-Reference Sheet

### Objectif
Garantir que toute URL écrite dans le Sheet PJ correspond à un fichier réel sur le dépôt.

### Workflow
1. **Scan** : Parcourir `Actes/Token/` récursivement, extraire `uid:` du YAML front matter de chaque `.md`.

2. **Mapping** : Produire `{uid: chemin_relatif}`.

3. **Vérification** : Avant d'écrire A–C ou G–K, vérifier que l'uid cible existe dans le mapping.

4. **Écriture** : URL GitHub = `https://github.com/criloOcom/accident-main/blob/main/Actes/Token/{chemin}`.

5. **Orphelins** : Tout uid sheet sans fichier .md est un orphelin — ne PAS écrire A–C.

### Colonnes concernées
| Colonne | Opération |
|---------|-----------|
| **A** | uid → vérifier mapping |
| **B** | URL → construire depuis mapping |
| **G** | uid Token → vérifier mapping |
| **H** | URL Token → construire depuis mapping |
| **J** | uid Reel → doit être identique à G |
| **K** | URL Reel → construire depuis mapping |

### Script de vérification
`.dev/app/verify_sheet_urls.py` : extrait tous les uids → URLs. Lancer après chaque modification du sheet pour confirmer que toutes les URLs répondent 200.