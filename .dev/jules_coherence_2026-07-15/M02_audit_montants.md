<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Environnement de Développement](../README.md) › jules coherence 2026-07-15 › M02 audit montants*
<hr>
<!-- /Breadcrumb -->

# MISSION 02 — Audit de cohérence des montants Dintilhac

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF

Vérifier que TOUS les montants d'indemnisation mentionnés dans le dépôt correspondent aux **valeurs canoniques §1 de STRICT VARIABLES.md** (post-expertise), et non aux valeurs historiques SUPERSEDED.

## MÉTHODE

1. **Extraire** les valeurs canoniques de STRICT VARIABLES.md §1 :
   - DFP_CANONIQUE : 25 200 €
   - SE_CANONIQUE : 14 000 €
   - PEP_CANONIQUE : 3 500 €
   - AGRÉMENT_CANONIQUE : 4 500 €
   - DFT_CANONIQUE : 2 031 €
   - PGPA_CANONIQUE : 1 380 €
   - IP_CANONIQUE : 28 000 €
   - DSA_CANONIQUE : 790,23 €
   - TOTAL_EXTRA_PATRIMONIAL_STRICT : 47 200 €
   - TOTAL_ESTIMATIF_GLOBAL_CANONIQUE : 120 000 – 160 000 €
   - Provisions et astreintes (15 000 €, 100 €/j, 150 €/j, etc.)

2. **Parcourir** TOUS les fichiers : Actes, Rapports, Analyses, Mémoires, Notes.

3. **Signaler** chaque écart :
   - Montant différent des valeurs canoniques (ex. SE à 24 000 € au lieu de 14 000 €)
   - Montant qui utilise encore les valeurs SUPERSEDED (§2 de STRICT VARIABLES)
   - Montant qui n'a pas de source vérifiable

4. **Attention spéciale** : les montants dans les fichiers `👤 Reel/` doivent être identiques à ceux de `🔑 Token/` (mêmes valeurs, seuls les noms changent).

## LIVRABLE

`📊 Rapports/85_Coherence_2026-07-15/M02_AUDIT_MONTANTS.md`

Format : TODO list avec cases. Chaque item = un montant à corriger ou un fichier à mettre à jour.
