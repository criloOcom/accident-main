<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › [jules coherence 2026-07-15](./README.md) › M03 audit fondements juridiques*
<hr>
<!-- /Breadcrumb -->

# MISSION 03 — Audit des fondements juridiques (articles de loi)

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF

Vérifier que CHAQUE article de loi, code ou règlement cité dans le dépôt EXISTE RÉELLEMENT sur Légifrance et est correctement référencé (numéro d'article, code, alinéa).

## MÉTHODE

1. **Extraire** toutes les citations d'articles de loi dans les fichiers de [Actes/Token](../../Actes/Token/README.md) et [Rapports](../../Rapports/README.md).

2. **Pour chaque citation** : utiliser l'outil `rechercher_code` ou `consulter_article` de Légifrance pour vérifier l'existence et la conformité du texte.

3. **Signaler** :
   - Articles inexistants (code faux, numéro faux)
   - Articles cités sans vérification préalable (pas de source Légifrance)
   - Articles qui ne correspondent pas au contexte (ex. article du Code de la santé publique cité pour un litige civil)
   - Articles corrects mais mal formatés (ex. « 1242-1 » au lieu de « 1242 al. 1er »)

4. **Vérification obligatoire** via `rechercher_code` (OpenLegi MCP) ou `legifrance_rechercher_code` / `legifrance_consulter_article`.

## LIVRABLE

[Rapports/85_Coherence_20260715/M03_AUDIT_FONDEMENTS_JURIDIQUES.md](../../Rapports/85_Coherence_20260715/M03_AUDIT_FONDEMENTS_JURIDIQUES.md)

Format : TODO list. Chaque item = fondement à vérifier ou corriger. Statut vérifié/non vérifié/inexistant.