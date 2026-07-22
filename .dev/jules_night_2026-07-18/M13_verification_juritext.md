<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › jules night 2026-07-18*
<hr>
<!-- /Breadcrumb -->

# MISSION 13 — Vérification JURITEXT exhaustive (protocole 2 étapes)

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF DE LA MISSION

Produis un rapport `Rapports/RAPPORT_VERIFICATION_JURITEXT_2026-07-18.md` vérifiant **toutes les citations d'articles de loi, de codes et de décisions de justice** dans le dossier, selon le protocole strict défini dans `JURITEXT_PROTOCOL.md`.

## PROTOCOLE

1. **Phase 1 — Légifrance-prod** : interroge `legifrance-prod` pour chaque article cité (API `rechercher_code` / `consulter_article`). Si trouvé, valide. Si introuvable, passe en Phase 2.

2. **Phase 2 — OpenLegi** : interroge OpenLegi pour le même article (API `rechercher_code` / `lister_codes_juridiques`). Si trouvé, valide.

3. **Si introuvable dans les deux** : marque « ⚠️ À VÉRIFIER » dans le rapport.

## MÉTHODE

Parcourt les fichiers les plus cites juridiquement :
- Les analyses juridiques (`Analyses_juridiques/`)

- Les actes de procédure (`Actes_proceduraux/`)

- Les conclusions TJ Foix

- Les rapports dans `Rapports/` (notamment les audits JURITEXT précédents)

- Les Décisions.md, RULES.md, STRICT VARIABLES.md

Pour chaque article/arrêt trouvé, vérifie :
- L'article existe au code indiqué

- La version est en vigueur à la date pertinente (mai/juin 2026)

- Le contenu cité correspond bien à l'article

## ATTENTION

Ne vérifie PAS les articles trivialement évidents (ex: art. 1240 C. civ. — responsabilité civile). Vérifie les articles moins connus, les textes spéciaux, les jurisprudences citées avec JURITEXT.

## LIVRABLE

Rapport structuré : article vérifié → résultat (✅ trouvé / ⚠️ À vérifier / ❌ introuvable). Prioriser les ⚠️ et ❌ pour correction manuelle.