<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › jules night 2026-07-18*
<hr>
<!-- /Breadcrumb -->

# MISSION 11 — Relecture TOKEN MAP + cohérence token téléphone préposé

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF DE LA MISSION

Produis un rapport `Rapports/RAPPORT_AUDIT_TOKENS_2026-07-18.md` vérifiant la **cohérence de l'ensemble des tokens d'anonymisation**, avec un focus particulier sur le nouveau token `**[Le Téléphone du Préposé]**` récemment créé.

## MÉTHODE

1. **Lire TOKEN MAP.md** — vérifier que tous les tokens sont listés avec :

   - Un nom unique
   - Une description claire
   - La correspondance réelle (ou « à déterminer »)
   - Pas de doublon ni d'absence

2. **Lire les fichiers token individuels** dans `Memory/Tokens/` — vérifier la complétude de chacun, en particulier `token-exploitation-prepose-telephone.md` (nouveau token) et `token-exploitation-prepose-nom.md` (mis à jour avec coordonnées).

3. **Vérifier la double strate** :

   - Le script `generate_real_versions.py` contient-il bien le mapping pour tous les tokens ?
   - Le script `batch_anonymize.py` contient-il bien tous les tokens ?
   - Les README des dossiers Tokens mentionnent-ils le nouveau token ?

4. **Vérifier l'insertion du nouveau token** : les 26 fichiers où le téléphone préposé a été ajouté (première mention de chaque document) sont-ils corrects ? Le token est-il bien utilisé partout où le téléphone apparaît ?

5. **Vérifier les fuites potentielles** : y a-t-il des fichiers Token qui contiennent encore des données réelles (téléphone, nom, adresse) non tokenisées ?

## LIVRABLE

Rapport : matrice de complétude des tokens, corrections nécessaires, fuites détectées, plan d'action pour sécuriser l'anonymisation.