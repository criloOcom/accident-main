<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Environnement de Développement](../README.md) › jules coherence 2026-07-15 › M01 audit dates*
<hr>
<!-- /Breadcrumb -->

# MISSION 01 — Audit de cohérence des dates

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF

Vérifier que TOUTES les dates mentionnées dans l'ensemble du dépôt sont conformes à la Source Unique de Vérité (`Memory/STRICT VARIABLES.md`) et cohérentes entre elles.

## MÉTHODE

1. **Extraire** de `STRICT VARIABLES.md` les dates canoniques :
   - DATE_ACCIDENT : 29 mai 2026
   - DATE_CHIRURGIE_SOS_MAIN : 30 mai 2026
   - ITT : 56 jours (29/05/2026 → 23/07/2026)
   - Expertise UMJ : 12 novembre 2026 (⚠ correction récente, vérifier qu'aucune occurrence de « 29 mai 2027 » ne subsiste)
   - Consolidation médicale : 01 mars 2027
   - Toutes les dates de procédure (J+X)

2. **Parcourir** TOUS les fichiers dans `Actes/Token/`, `Rapports/`, `Memory/` et `Lois/`.

3. **Signaler** TOUTE occurrence de date qui dévie des valeurs canoniques, avec :
   - Le fichier exact et le numéro de ligne
   - La valeur erronée vs la valeur canonique
   - La gravité (CRITIQUE si la date est matériellement impossible, MAJEUR si contradictoire)

4. **Cas particulier** : les dates au format `J+X` (relatif) doivent être vérifiées contre le J+0 = 29/05/2026. Signaler tout décalage.

## LIVRABLE

`Rapports/85_Coherence_2026-07-15/M01_AUDIT_DATES.md`

Format : checklist avec cases à cocher. Chaque ligne = une date à corriger.