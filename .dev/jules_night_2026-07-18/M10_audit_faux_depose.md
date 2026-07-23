<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › [jules night 2026-07-18](./README.md)*
<hr>
<!-- /Breadcrumb -->

# MISSION 10 — Audit des mentions « ✅ Déposé » fausses / hallucinations

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF DE LA MISSION

Produis un rapport [Rapports/RAPPORT_AUDIT_FAUX_DEPOSE_2026-07-18.md](../../Rapports/RAPPORT_AUDIT_FAUX_DEPOSE_2026-07-18.md) qui **parcourt l'intégralité du dossier** pour traquer les mentions d'actes présentés comme accomplis (déposés, envoyés, transmis, signifiés, notifiés) mais qui n'ont **pas été réellement effectués**.

## CONTEXTE CRITIQUE

Plusieurs agents IA ont travaillé sur ce dossier et ont parfois écrit des documents comme si des actes avaient été accomplis (ex: « Demande d'AJ totale: ✅ Déposée (BAJ Foix, 15/07) »), alors que ces actes n'ont en réalité **jamais été déposés**. C'est une forme d'hallucination documentaire qu'il faut éradiquer.

## MÉTHODE

1. **Parcours TOUS les fichiers** du dépôt (Token + Reel + Rapport), sans exception

2. Cherche les motifs suivants :

   - `✅ Déposé` / `✅ Transmis` / `✅ Envoyé` / `✅ Fait` / `✅ Signifié`
   - `Déposée le` / `Transmise le` / `Envoyé le`
   - `A été déposé` / `A été transmis` / `A été envoyé`
   - Toute checkbox cochée `✅` ou `[x]` qui concerne une action extérieure
3. Pour chaque occurrence, **ne fais PAS confiance au contexte** — vérifie si l'acte en question a réellement été accompli :

   - La demande d'AJ n'a PAS été déposée
   - La requête Art. 145 CPC n'a PAS été déposée
   - Les courriers n'ont PAS été envoyés
   - Seule la visite du 16/07 a réellement eu lieu
4. Compile tout dans un rapport avec le format :

   - Fichier concerné (chemin complet)
   - Ligne exacte (citation)
   - Acte présenté comme fait
   - Réalité (fait ou pas fait)
   - Correction proposée

## LIVRABLE

Rapport exhaustif listant TOUTES les occurrences avec les corrections à appliquer. Format permettant une correction manuelle ou automatisée. Le rapport servira de base à la mission M10b (correction effective des fichiers).