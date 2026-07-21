<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Environnement de Développement](../README.md) › jules night 2026-07-14 › M04 organisation*
<hr>
<!-- /Breadcrumb -->

# MISSION 4 — Audit de l'organisation et de la navigabilité du dépôt

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF DE LA MISSION

Produis un rapport `📊 Rapports/RAPPORT_ORGANISATION_DEPOT_2026-07-14.md` évaluant **l'organisation, la navigabilité et la maintenabilité** du dépôt accident-main (arborescence, liens internes, index, README, doubles strates).

## ANGLES

1. **Arborescence** : lis `README.md` (racine) et tous les `README.md` de sous-dossiers. L'arborescence reflète-t-elle fidèlement le contenu réel ? Y a-t-il des fichiers orphelins, des dossiers non documentés, des doublons ?
2. **Liens internes** : vérifie (via `app/check_consistency.py` si exécutable, sinon manuellement) que tous les liens relatifs pointent vers des cibles existantes. Signale les liens morts (Règle AGENTS #15/#17).
3. **Breadcrumbs** : tout fichier a-t-il son fil d'Ariane correct (YAML ligne 1 + breadcrumb HTML, Règle #14) ?
4. **Index et statuts** : le dossier `🚦 Status/` et `📊 Rapports/` sont-ils à jour et cohérents avec `STATUS.md` / `TODO.md` ?
5. **Séparateurs `<hr><hr>`** : applique (en lecture) la convention — repère les fichiers non conformes.
6. **Propreté** : présence de fichiers à la racine, `__pycache__`, scripts orphelins (Règle #13 DECISIONS).

## LIVRABLE

Rapport avec : cartographie des écarts organisationnels, liste priorisée des corrections (impact/maintenance), proposition de structure optimale, et un diagramme Mermaid de l'arborescence cible. Ne modifie rien, contente-toi de recommander.