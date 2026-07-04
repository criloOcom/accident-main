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

- **Tokens d'anonymisation** (`**[La Victime]**`, `**[L'Exploitant du Commerce]**`, `**[Le Président de l'Exploitation]**`…) : appliquer **Bold** (`textStyle.bold = true`) dans le corps du texte. Ne pas mettre en gras les guillemets, parenthèses ou texte autour.
- **Références législatives et jurisprudentielles** (ex. `article 1242 du Code civil`, `Cass. Com., 20 mai 2003, n° 99-17.092`) : appliquer **souligné** + **couleur bleue `#1166CC`** + **`linkUrl`** pointant vers Légifrance ou Judilibre.
- **Puces et listes** : alignement JUSTIFIED, même police Arial 11 pt.

## Application obligatoire après chaque injection

Après chaque `replaceDocumentWithMarkdown` sur une copie UNIFIE_ANONYME :

1. **`applyParagraphStyle`** → `namedStyleType: NORMAL_TEXT`, `alignment: JUSTIFIED` sur la totalité du document (ou vérifier que les styles nommés sont corrects).
2. **`applyTextStyle`** → liens hypertextes Légifrance/Judilibre sur toutes les références légales.
3. **`applyTextStyle`** → **Bold** sur chaque token d'anonymisation dans le corps.
4. **Vérifier** que le TITLE est bien en 20 pt centré (et non le 36 pt par défaut).

## Document de référence

Le document **Doc 14** (`1lUKoGE8kozmE3KA4zErv9GYmJZ0yctOk9tn92O8KT34`) est le modèle "jolie" approuvé par l'utilisateur. Se référer à son rendu final pour toute question d'apparence.
