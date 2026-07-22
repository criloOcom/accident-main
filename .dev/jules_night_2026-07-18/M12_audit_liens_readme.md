<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › jules night 2026-07-18*
<hr>
<!-- /Breadcrumb -->

# MISSION 12 — Audit liens internes + synchronisation README

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF DE LA MISSION

Produis un rapport [Rapports/RAPPORT_AUDIT_LIENS_README_2026-07-18.md](../../Rapports/RAPPORT_AUDIT_LIENS_README_2026-07-18.md) vérifiant l'intégrité des **liens internes** du dépôt et la synchronisation du **README.md** avec la structure réelle.

## CONTEXTE

Le pre-commit hook exécute 3 audits (README, liens internes, citations). Il y avait ~20 warnings pour le README et ~85 liens cassés. Ces vérifications sont scriptées dans `.dev/app/`.

## ANGLES

1. **Liens internes cassés** : exécute (ou simule) l'audit via `.dev/app/audit_internal_links.py` et `.dev/app/fix_internal_links.py`. List les liens cassés par fichier.

2. **README non synchronisé** : exécute (ou simule) `.dev/app/sync_readme_listings.py` et `.dev/app/audit_readme_integrity.py`. Quels dossiers/fichiers manquent dans le README ?

3. **Citations non liées** : exécute (ou simule) `.dev/app/audit_citation_links.py`. Y a-t-il des citations de dossiers/fichiers internes qui ne sont pas des liens cliquables ?

4. **Conventions** : les fichiers récents respectent-ils CONVENTIONS.md (breadcrumb, séparateurs, fils d'Ariane) ?

5. **Propreté** : caches (`__pycache__`, `.pytest_cache`), fichiers oubliés à la racine, rapports mal placés ?

## LIVRABLE

Rapport listant : tous les liens cassés, tous les fichiers non répertoriés dans le README, toutes les citations non liées, les infractions aux conventions. Priorisé par sévérité (cassé / cassé mais redirigeable / esthétique).