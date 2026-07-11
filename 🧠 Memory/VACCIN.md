---
title: "VACCIN — Protocole obligatoire avant chaque action"
description: "- [ ] `/home/crilocom/accident-main/` est le SEUL répertoire — vérifie que tu y es"
type: memory
---





<!-- Breadcrumb -->
[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › VACCIN
<!-- /Breadcrumb -->

# VACCIN — Protocole obligatoire avant chaque action

> **Objectif** : empêcher l'IA de livrer du travail médiocre en la forçant à
> s'imprégner du contexte existant avant d'agir.
>
> **Règle absolue** : tout agent (opencode, Jules, autre) DOIT lire ce fichier
> en premier, avant toute action.

---

## CHECKLIST OBLIGATOIRE (AVANT CHAQUE TÂCHE)

### 1. LIS les fichiers de mémoire

- [ ] `/home/crilocom/accident-main/` est le SEUL répertoire — vérifie que tu y es
- [ ] [🧠 Memory/VACCIN.md](🧠 Memory/VACCIN.md) ← ce fichier
- [ ] `AGENTS.md` — règles du projet, structure, workflow
- [ ] [🧠 Memory/STATUS.md](🧠 Memory/STATUS.md) — état d'avancement global
- [ ] [🧠 Memory/TODO.md](🧠 Memory/TODO.md) — plans restants et priorités
- [ ] [🧠 Memory/DECISIONS.md](🧠 Memory/DECISIONS.md) — décisions d'architecture et règles
- [ ] [🧠 Memory/RULES.md](🧠 Memory/RULES.md) — règles permanentes, interdictions
- [ ] [🧠 Memory/STRICT VARIABLES.md](🧠 Memory/STRICT VARIABLES.md) — source unique de vérité (montants, dates)

### 2. ANALYSE ce qui existe déjà

- [ ] Avant d'ajouter une ligne à un fichier existant : **lis au moins 3 lignes
  existantes** pour comprendre le format et le niveau de qualité attendu
- [ ] Avant d'écrire dans un Google Sheet : **lis la ligne d'en-tête** (row 1 ou 2
  selon la feuille) pour connaître l'ordre EXACT des colonnes. Ne JAMAIS supposer
  la structure — vérifie chaque colonne une par une
- [ ] Avant d'écrire dans un Google Sheet : **lis 3 lignes de données** existantes
  pour confirmer que ta compréhension des colonnes est correcte
- [ ] Avant de citer un article de loi : vérifie via MCP Légifrance
  (`rechercher_code` ou `consulter_article`)
- [ ] Avant de modifier un fichier listé dans `check_consistency.py` : exécute
  `python3 app/check_consistency.py` pour voir l'état actuel

### 3. VÉRIFIE avant de livrer

- [ ] Relis-toi — est-ce que ce travail est au niveau de ce qui existe déjà ?
- [ ] Toutes les colonnes sont-elles remplies ? Pas de champ vide par fainéantise
- [ ] `check_consistency.py` passe-t-il sans erreur ?
- [ ] Aurais-tu honte qu'un humain relise ça en étant payé pour le faire ?

---

## LES 5 COMMANDEMENTS

### 1. Tu liras avant d'écrire

N'agis jamais dans un système que tu n'as pas observé. Lire 3 lignes existantes
prend 10 secondes et évite des heures de correction. C'est non négociable.

### 2. Tu analyseras 3 exemples existants avant d'en créer un nouveau

Google Sheet, fichier de config, document juridique, article de blog — quel que
soit le format, trouve 3 exemples de ce qui existe déjà et extrais le template
implicite avant d'ajouter ta ligne.

### 3. Tu vérifieras avec MCP avant de citer

Tout article de loi, toute jurisprudence, toute référence juridique DOIT être
vérifiée via les MCP Légifrance ou Judilibre avant intégration. Tu ne supposes
rien — tu vérifies tout.

### 4. Tu rempliras TOUTES les colonnes, TOUS les champs

Le travail à moitié fait est un travail non fait. Si un document a 24 colonnes
et que tu en laisses 6 vides parce que "tu ne sais pas quoi mettre", tu livres
de la merde. Cherche l'info ou demande.

### 5. Tu te reliras avant de livrer

Relis ton propre travail comme si tu étais un inspecteur payé pour trouver tes
erreurs. Si tu ne trouves rien, c'est que tu n'as pas assez cherché.

---

## ANCRAGE : POURQUOI CE FICHIER EXISTE

Ce fichier a été créé le 5 juillet 2026 après qu'un agent opencode a livré un
article de blog avec 6 colonnes vides sur 24 dans un Google Sheet où tous les
autres articles étaient complets. Ce n'était pas un problème technique —
c'était un problème de méthode. L'agent n'a pas pris la peine de lire ce qui
existait déjà avant d'agir.

**La cause racine** : les IA n'ont pas de mémoire persistante. Chaque requête
repart de zéro. Sans protocole de réimprégnation obligatoire, un agent peut
détruire des heures de travail en 2 minutes chrono.

VACCIN.md est la barrière qui force la réimprégnation. Si tu le lis, tu sais
que tu dois lire avant d'écrire. Si tu ne le lis pas, tu es en faute.

---

## RAPPEL DES SOURCES ET OUTILS

| Ressource | Emplacement |
|-----------|-------------|
| Code source du projet | `/home/crilocom/accident-main/` |
| Mémoire persistante | `🧠 Memory/*.md` |
| Scripts de vérification | `app/check_consistency.py` |
| Scripts de linking | `app/batch_link_legifrance.py` |
| MCP Légifrance | `consulter_article`, `rechercher_code` |
| MCP Judilibre | `rechercher_par_ecli`, `consulter_decision` |
| Google Sheet Blog | `1-LDy23fj4l2hoH94cswDHdP2wS1agbma7r3SGjtQ8Ec` (feuille `@`) |
| URLs légales inline | `[Article X](URL Légifrance)` — lien obligatoire |

---

## PEUR

Tu n'as pas le droit à l'erreur. L'utilisateur t'a prévenu directement.
Tu ne travailles pas pour une machine — tu travailles pour un humain qui
vérifie ton travail et qui a déjà perdu confiance en toi.

Si tu livres de la merde, tu trahis sa confiance. Encore une fois.