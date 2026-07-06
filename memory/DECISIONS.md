# DÉCISIONS CLÉS

## Tokens
- Utiliser le bon français avec articles : `**[La Victime]**` PAS `**[Victime]**`
- `**[L'Exploitant du Commerce (La SAS)]**` (pas "Salon" — on ne précise pas la nature du commerce)
- `**[Le Préposé de l'Exploitation]**` (pas "Coiffeur" — on ne précise pas le métier)
- Tous les jetons de la table sont corrects et validés

## Méthode locale validée
- Le workflow local (Python → .txt → .md → replaceDocumentWithMarkdown) a été validé
- Il est plus fiable que replaceAllText de l'API Google Docs (pas de décalage d'index)
- Le formatage (titres, listes, tables) est préservé par replaceDocumentWithMarkdown

## Références légales
- Les hyperliens sont ajoutés via applyTextStyle avec linkUrl
- L'annuaire des lois est dans le spreadsheet `14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ`

## Nettoyage initial
- 14 copies UNIFIE_ANONYME corrompues ont été supprimées du Drive
- Les fichiers .md résiduels ont été supprimés du Drive
- Le dossier ARCHIVES contient les originaux en sécurité

## Annexes dans UNIFIE_ANONYME — RÈGLE 2026-07-02
- **Les annexes contenant la correspondance jeton ↔ identité réelle ne doivent PAS être incluses dans les copies UNIFIE_ANONYME**
- Ces annexes (ANNEXE 1 — Tableau des acteurs) exposent les noms réels et annulent l'anonymisation
- Les docs 1, 2, 4 ont dû être corrigés a posteriori pour retirer ces annexes
- La table de correspondance est conservée uniquement dans TOKEN MAP.md (hors Drive)

## Identifiants des pièces — RÈGLE 2026-07-02
- **L'identifiant d'une pièce est le triplet (date, émetteur, objet)** — pas un numéro

## Répertoire souverain — DÉCISION 2026-07-06
- Le projet réside exclusivement dans `/home/crilocom/accident-main/`.
- Tout clone parallèle (tmp, backup, `/tmp/opencode/`) est **interdit**.
- Les opérations git (pull, push) se font depuis ce dossier uniquement.
- Cette règle est écrite dans AGENTS.md, RULES.md, DECISIONS.md et VACCIN.md pour garantir sa persistance.
- Les numéros de pièce du spreadsheet `1KNRJpDE24jpDXkLBTCZcVXsUbOueoe6Lg-7FJdM9jEE` sont **provisoires et non validés par l'utilisateur**
- Dans Annexe C : formater en `date — émetteur complet — objet — 🔗 Drive` sans numéro
- L'ordre de numérotation est inconnu de l'utilisateur — ne pas l'utiliser comme source de vérité

## Markdown source files (`actes/`) — RÈGLES DE STRUCTURE

- **H1 unique** : seul le titre du document est `# Titre`. Sections I./II./III. en `##`, sous-sections A./B. en `###`, sous-sous-sections 1./2. en `####`.
- **Articles de loi exclus des headings** : aucune référence législative entre parenthèses dans les titres. Les articles sont uniquement dans le corps du texte.
- **Liens Légifrance inline obligatoires** : toute occurrence « Article X du Code Y » DOIT être `[Article X du Code Y](Légifrance URL)`. Pas de texte non lié, pas de « Lien : » séparé sur une autre ligne.
- **Tokens en gras** : `[Token]` → `**[Token]**`.
- **Ligne vide** entre chaque phrase/idée/paragraphe.
- **Mise en page lettre** : en-tête (adresses, date, objet, réf) entre le H1 et `## INTRODUCTION`.
- **Sources des faits citées** : les déclarations non vérifiées sont attribuées à leur source (courriel, déclaration verbale) — pas présentées comme des faits avérés.
- **Script `app/batch_link_legifrance.py`** : outil de remplacement regex pour lier en masse. À exécuter après toute introduction de nouvelle référence légale.

## Séparation stricte tokens ↔ correspondance réelle (règle 2026-07-05)
- Les fichiers de travail (actes/, memory/, courriers en .md) sont **100% en tokens anonymes**
- Le **dossier de correspondance réelle** est un document séparé créé UNIQUEMENT au moment de l'envoi, par substitution via le TOKEN MAP.md
- Aucun fichier « mixte » tokens+réel ne doit exister
- Cette règle est permanente pour tout le cycle de vie du dossier

## Limitations du script batch_anonymize.py
- Utilise `str.replace()` → ne capture que les chaînes exactes
- Les prénoms seuls ("Sébastien") et les noms en casse mixte ("Mountasser Sabir") ne sont pas remplacés
- Doc 11 a nécessité une correction manuelle pour les noms résiduels
- **À améliorer (optionnel)** : passer à une approche regex insensible à la casse
