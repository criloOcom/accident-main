---
title: "DÉCISIONS CLÉS"
description: "- Utiliser le bon français avec articles : `**[La Victime]**` PAS `**[Victime]**`"
type: memory
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › DECISIONS*
<hr>
<!-- /Breadcrumb -->

# DÉCISIONS CLÉS

## Tokens
- Utiliser le bon français avec articles : `**[La Victime]**` PAS `**[Victime]**`
- `**[L'Exploitant du Commerce (La SAS)]**` (pas "Salon" — on ne précise pas la nature du commerce)
- `**[Le Préposé de l'Exploitation]**` (pas "Coiffeur" — on ne précise pas le métier)
- Tous les tokens de la table sont corrects et validés

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
- **Les annexes contenant la correspondance token ↔ identité réelle ne doivent PAS être incluses dans les copies UNIFIE_ANONYME**
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

## Markdown source files ([⚖️ Actes](../%E2%9A%96%EF%B8%8F%20Actes/README.md)) — RÈGLES DE STRUCTURE

- **H1 unique** : seul le titre du document est `# Titre`. Sections I./II./III. en `##`, sous-sections A./B. en `###`, sous-sous-sections 1./2. en `####`.
- **Articles de loi exclus des headings** : aucune référence législative entre parenthèses dans les titres. Les articles sont uniquement dans le corps du texte.
- **Liens Légifrance inline obligatoires** : toute occurrence « Article X du Code Y » DOIT être `[Article X du Code Y](L%C3%A9gifrance%20URL)`. Pas de texte non lié, pas de « Lien : » séparé sur une autre ligne.
- **Tokens en gras** : `[Token]` → `**[Token]**`.
- **Ligne vide** entre chaque phrase/idée/paragraphe.
- **Mise en page lettre** : en-tête (adresses, date, objet, réf) entre le H1 et `## INTRODUCTION`.
- **Sources des faits citées** : les déclarations non vérifiées sont attribuées à leur source (courriel, déclaration verbale) — pas présentées comme des faits avérés.
- **Script `app/batch_link_legifrance.py`** : outil de remplacement regex pour lier en masse. À exécuter après toute introduction de nouvelle référence légale.

## Séparation stricte tokens ↔ correspondance réelle (règle 2026-07-05)
- Les fichiers de travail (⚖️ Actes/, 🧠 Memory/, courriers en .md) sont **100% en tokens anonymes**
- Le **dossier de correspondance réelle** est un document séparé créé UNIQUEMENT au moment de l'envoi, par substitution via le TOKEN MAP.md
- Aucun fichier « mixte » tokens+réel ne doit exister
- Cette règle est permanente pour tout le cycle de vie du dossier

## Clôture des sessions Jules — DÉCISION 2026-07-08
- **Toute session Jules doit recevoir un message de clôture explicite** une fois le travail terminé (rapport reçu, PR créé, solution envoyée, etc.)
- Le message type : « Session terminée, tu peux clôturer et archiver. » ou équivalent.
- Les sessions bloquées qui reçoivent une réponse de déblocage doivent être informées : « Réponse envoyée — tu peux continuer ou clôturer si fini. »
- L'API REST Jules n'a pas de méthode `delete`/`archive` — le message de clôture est le seul mécanisme pour marquer la fin de la conversation.
- Google archivera automatiquement les sessions clôturées côté serveur.
- **Anti-pattern** : laisser des sessions en plan (« l'agent a fini, je passe à autre chose ») — les agents restent dans un état d'attente indéfini.
- **Propagation** : cette décision est enregistrée dans RULES.md (#12), AGENTS.md (règle #12), WORKFLOW.md et DECISIONS.md pour visibilité maximale.

## NotebookLM MCP — DÉCISION 2026-07-08
- **Un notebook NotebookLM** a été créé et chargé avec les sources du projet : ID `accident-main`, URL `https://notebooklm.google.com/notebook/3dbe69da-5e8a-4f23-bc0c-d277bcf993d6`
- **MCP server** `notebooklm` configuré dans `opencode.jsonc` et accessible à tous les agents opencode
- **Usage** : tout agent peut poser des questions contextuelles via `notebooklm_ask_question(notebook_id="accident-main")` pour obtenir des réponses ancrées dans les sources chargées
- **Audio Overview** : possible via la chaîne `generate_audio` → `get_audio_status` → `download_audio`
- **Auth** : cookies Google persistés ; `notebooklm_get_health` pour vérifier l'état ; `setup_auth` / `re_auth` pour reconnecter si besoin
- **Propagation** : cette décision est enregistrée dans AGENTS.md (section NotebookLM), RULES.md (#13) et DECISIONS.md

## Format des fils d'Ariane — DÉCISION 2026-07-11
- **Format** : commentaire HTML `` sur la **ligne 1**
- **Pas de "Accueil"** : utiliser `[🏠]` (emoji maison) comme lien racine
- **Un seul breadcrumb par fichier** — script dédié `.dev/app/generate_breadcrumbs.py`
- **Détection par script** : le script cherche tous les patterns connus (code blocks, HTML comments, texte brut) et les remplace par le format canonique unique
- **Scripts et fichiers à la racine interdits** : tout .py va dans `.dev/app/`, tout rapport va dans [📊 Rapports](../%F0%9F%93%8A%20Rapports/README.md)
- **Propreté du projet** : `__pycache__`, `.pytest_cache` sont à supprimer après exécution — le `.gitignore` les couvre déjà
- **PRs terminées à fermer** : toute PR dont le contenu est intégré dans `main` DOIT être fermée (sans merge) et sa branche supprimée

## Limitations du script batch_anonymize.py
- Utilise `str.replace()` → ne capture que les chaînes exactes
- Les prénoms seuls ("Sébastien") et les noms en casse mixte ("Mountasser Sabir", ancien format inversé) ne sont pas remplacés
- Doc 11 a nécessité une correction manuelle pour les noms résiduels
- **À améliorer (optionnel)** : passer à une approche regex insensible à la casse