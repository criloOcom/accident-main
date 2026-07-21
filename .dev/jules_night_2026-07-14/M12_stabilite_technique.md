<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Environnement de Développement](../README.md) › jules night 2026-07-14 › M12 stabilite technique*
<hr>
<!-- /Breadcrumb -->

# MISSION 12 — Stabilité technique et robustesse des scripts du dépôt

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF DE LA MISSION

Produis un rapport `Rapports/RAPPORT_STABILITE_TECHNIQUE_2026-07-14.md` évaluant la **robustesse technique** du dépôt (scripts Python d'anonymisation, de vérification, de génération des versions réelles) pour garantir qu'aucune régression ou fuite de données réelles ne survienne.

## ANGLES

1. **Pipeline d'anonymisation** : `app/batch_anonymize.py` (str.replace) — limites connues (casse mixte, prénoms seuls non remplacés). Risque de fuite d'identité réelle dans la strate Token ? Recommande une approche regex insensible à la casse.
2. **`generate_real_versions.py`** : lit-il correctement TOKEN MAP et produit-il les 96+ fichiers Reel sans doublon ni perte ?
3. **`check_consistency.py`** : couvre-t-il tous les risques (liens morts, tokens inconnus, LEGIARTI/JURITEXT invalides, frontmatter) ? Faux négatifs possibles ?
4. **`normalize_sections.py`**, `linkify_citations.py`, `audit_citation_links.py` : conformité aux conventions.
5. **Gestion d'erreur** : les scripts gèrent-ils les cas limites (fichier manquant, encodage, YAML corrompu) ?
6. **Sécurité** : les fichiers contenant de vraies identités (TOKEN MAP, scripts de génération) sont-ils correctement exclus du dépôt public / .gitignore ?

## LIVRABLE

Rapport : audit par script (fiabilité, risque de fuite, correctifs recommandés), et une checklist de tests à ajouter. Ne modifie pas les scripts — recommande uniquement.