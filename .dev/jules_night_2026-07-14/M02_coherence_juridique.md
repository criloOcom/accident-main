<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › [jules night 2026-07-14](./README.md)*
<hr>
<!-- /Breadcrumb -->

# MISSION 2 — Audit de cohérence juridique transversale

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF DE LA MISSION

Produis un rapport `Rapports/RAPPORT_COHERENCE_JURIDIQUE_2026-07-14.md` vérifiant la **cohérence de l'ensemble des actes et analyses juridiques** du dépôt : aucune contradiction de fait, de montant, de date, de fondement entre les 44+ documents.

## MÉTHODE

1. Lis TOUS les actes Token ([Actes/Token](../../Actes/Token/README.md)) et les rapports ([Rapports](../../Rapports/README.md)).
2. Croise chaque donnée factuelle (dates d'accident/chirurgie, montants Dintilhac, numéros LRAR, numéros de PV, identités tokenisées) avec `STRICT VARIABLES.md`.
3. Repère les écarts, les doublons, les versions obsolètes (ex. montants DFP/IP/SE des anciennes évaluations vs avis Dintilhac 2026-07-13).
4. Vérifie que les fondements légaux cités dans les actes sont cohérents entre eux (pas de contradiction de qualification pénale, de base de responsabilité, etc.).

## ANGLES

- **Cohérence des montants** : tableau comparatif (interdit les tableaux à colonne de numéros — utilise une liste ou un vrai tableau de données) entre évaluation initiale, Glose, compromis, avis Dintilhac prudent/médian. Quelle est la référence à privilégier et pourquoi ?
- **Cohérence des dates** : chronologie de l'accident au 15 juillet 2026 — vérifie chaque date citée.
- **Cohérence des citations JURITEXT** : signale toute JURITEXT douteuse (voir JURITEXT_PROTOCOL.md et l'historique des corrections en STATUS.md).
- **Cohérence de la stratégie** : la séquence (Art. 145 CPC → AJ → plainte → référé → expertise → fond) est-elle logique et juridiquement tenable ?

## LIVRABLE

Rapport listant chaque incohérence détectée (gravité + localisation fichier + correction recommandée), et une synthèse « état de vérité » du dossier. Citations vérifiées Légifrance.