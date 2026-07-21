<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › jules night 2026-07-14*
<hr>
<!-- /Breadcrumb -->

# MISSION 13 — Audit de sécurité juridique des tokens et de la double strate

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF DE LA MISSION

Produis un rapport `Rapports/RAPPORT_SECURITE_TOKENS_2026-07-14.md` analysant la **résistance du système d'anonymisation** (tokens 🔑 ↔ identités réelles 👤) à une attaque de réidentification, et sa conformité avec l'obligation de secret/confidentialité en procédure.

## ANGLES

1. **Réversibilité du mapping** : TOKEN MAP.md est-il le seul point de vérité ? Est-il suffisamment protégé (hors Drive, accès restreint) ? Risque si le dépôt public + TOKEN MAP fuient ensemble.
2. **Cohérence des tokens** : tout token est-il défini une seule fois et résolu correctement ? Y a-t-il des tokens orphelins (utilisés dans un acte mais absents de TOKEN MAP) ou des variants (ex. `[La Victime]` vs `[Victime]`) ?
3. **Fuite résiduelle** : recherche dans les 96+ fichiers Token toute occurrence d'identité réelle (prénoms, noms, SIREN, adresses, emails, n° PV complets) qui aurait échappé à `batch_anonymize.py`. Recommande une commande de grep de surveillance.
4. **Versions réelles** : les fichiers Reel sont-ils conformes (mêmes tokens résolus, aucune divergence factuelle avec Token) ?
5. **Secret de l'instruction / confidentialité** : les versions réelles doivent-elles être marquées « CONFIDENTIEL » / « NE PAS DIFFUSER » pour respecter l'art. 11 CPP (secret de l'instruction) et le secret professionnel ?

## LIVRABLE

Rapport : score de résistance à la réidentification, liste des failles (tokens orphelins, fuites résiduelles), et plan de durcissement (grep de surveillance, marquage confidentiel, chiffrement TOKEN MAP). Tout fondement procédural vérifié.