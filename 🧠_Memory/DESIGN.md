# DESIGN — Charte Graphique Google Docs

## Police unique
- **Arial** obligatoire sur 100 % du document (police héritée par défaut via le thème Google Docs ; ne pas utiliser de police différente dans les `textStyle` explicites).

## Marges et page
- Marges : **~2 cm** (56,69 pt) — identique sur les 4 côtés.
- Format : **A4** (595,28 × 841,89 pt).

## Hiérarchie des styles

| Style Google Docs | Usage | Taille | Gras | Casse | Souligné | Alignement |
|---|---|---|---|---|---|---|
| **TITLE** | Titre principal du document | **20 pt** | **OUI** | Normale | **NON** | **CENTER** |
| **HEADING_1** | Sections principales (I., II., III., INTRODUCTION) | **14 pt** | **OUI** | **MAJUSCULES** | **OUI** | JUSTIFIED |
| **HEADING_2** | Sous-sections (A., B., C.) | **12 pt** | **OUI** | **1ʳᵉ lettre CAP seulement** | **OUI** | JUSTIFIED |
| **HEADING_3** | Sous-sous-sections (1., 2., 3.) / Questions FAQ | **10 pt** | **OUI** | Normale | **NON** | JUSTIFIED |
| **NORMAL_TEXT** | Corps du texte | **11 pt** | **NON** | Normale | **NON** | **JUSTIFIED** |

**Remarque** : les valeurs par défaut du thème Google Docs (36 pt pour TITLE, 14 pt pour HEADING_3, etc.) **ne doivent pas être utilisées** — seuls les tailles et styles ci-dessus sont valides.

## Règles de formatage du corps

- **Tokens d'anonymisation** (`**[La Victime]**`, `**[L'Exploitant du Commerce (La SAS)]**`, `**[Le Président de l'Exploitation]**`…) : appliquer **Bold** (`textStyle.bold = true`) dans le corps du texte. Ne pas mettre en gras les guillemets, parenthèses ou texte autour.
- **Références législatives et jurisprudentielles** (ex. `article 1240 du Code civil`, `Cass. Com., 20 mai 2003, [n° 99-17.092](https://www.legifrance.gouv.fr/juri/id/JURITEXT000007047369)`) : appliquer **souligné** + **couleur bleue `#1166CC`** + **`linkUrl`** pointant vers Légifrance ou Judilibre.
- **Puces et listes** : alignement JUSTIFIED, même police Arial 11 pt.

## Citations d'articles de code (OBLIGATOIRE)

Tout article de code cité dans un document DOIT être présenté sous forme de **bloc de citation complet** `>` avec les 3 éléments :

1. **Citation du texte** entre guillemets `« ... »` (extrait pertinent, 1-3 phrases max)
2. **Chemin législatif hiérarchique** complet en **gras** (`Code > Partie > Livre > Titre > Chapitre > Section`)
3. **Lien hypertexte** Légifrance sur le numéro d'article

**Format obligatoire :**
```
> « [Texte exact de l'article extrait via Légifrance MCP]... » <br>
> **[Nom du Code] > [Chemin hiérarchique complet]** <br>
> [Article XXX](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI...)
```

**Règles :**
- Le texte est extrait de `openlegi_rechercher_code` ou `legifrance_rechercher_code` — jamais inventé.
- Le chemin hiérarchique doit correspondre exactement au `Chemin complet` retourné par le tool Légifrance.
- Pour les articles longs (> 3 lignes), utiliser `[...]` pour les parties non pertinentes.
- Le bloc `>` suit immédiatement la phrase ou le paragraphe qui mentionne l'article.
- Ne JAMAIS mettre un article en simple lien inline `[Art. XXX](url)` — toujours le format bloc complet.

## Citations de jurisprudence (RÈGLE ABSOLUE — SANS EXCEPTION)

**TOUTE** décision de justice citée dans **TOUS** les documents (actes procéduraux, courriers, analyses, plaideries, études, archives, index) DOIT être présentée sous forme de **bloc de citation complet** `>` avec les 3 éléments :

1. **Ratio decidendi** extrait du texte intégral de la décision (texte exact entre guillemets `« ... »`)
2. **Identification complète** de la juridiction en **gras** (juridiction, chambre, date, numéro de pourvoi)
3. **Lien hypertexte** vers Légifrance ou Judilibre

**Format obligatoire :**
```
> « [Ratio decidendi extrait du texte intégral de la décision]... » <br>
> **Cour de [juridiction], [chambre], [date], n° [numéro de pourvoi]** <br>
> [Arrêt](https://www.legifrance.gouv.fr/juri/id/...)
```

**Règles :**
- Le ratio decidendi est extrait de `judilibre_consulter_decision` ou `openlegi_get_decision_judiciaire` — jamais inventé.
- L'identification de la juridiction doit être exacte (vérifiée via le tool Légifrance/Judilibre).
- Pour les arrêts longs, sélectionner le passage le plus pertinent (1-3 phrases).
- Le bloc `>` suit immédiatement la phrase ou le paragraphe qui mentionne l'arrêt.
- **Ne JAMAIS** mettre un arrêt en simple lien inline `[Cass. ..., n° XXX](url)` — **toujours** le format bloc complet.
- **Aucune exception** : les courriers LRAR, les index, les tableaux de synthèse, les analyses contextuelles — **TOUT** document doit respecter cette règle.
- **Sans exception** : toute référence à une Cour de cassation (Civ. 1ère, 2e, 3e, Crim., Com., Soc.), Conseil d'État (CE, CAA), tribunal administratif, cour d'appel, etc. doit être en blockquote complet avec lien.

## Application obligatoire après chaque injection

Après chaque `replaceDocumentWithMarkdown` sur une copie UNIFIE_ANONYME :

1. **`applyParagraphStyle`** → `namedStyleType: NORMAL_TEXT`, `alignment: JUSTIFIED` sur la totalité du document (ou vérifier que les styles nommés sont corrects).
2. **`applyTextStyle`** → liens hypertextes Légifrance/Judilibre sur toutes les références légales.
3. **`applyTextStyle`** → **Bold** sur chaque token d'anonymisation dans le corps.
4. **Vérifier** que le TITLE est bien en 20 pt centré (et non le 36 pt par défaut).

## Document de référence

Le document **Doc 14** (`1lUKoGE8kozmE3KA4zErv9GYmJZ0yctOk9tn92O8KT34`) est le modèle "jolie" approuvé par l'utilisateur. Se référer à son rendu final pour toute question d'apparence.
