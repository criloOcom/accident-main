<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Environnement de Développement](../README.md) › jules coherence 2026-07-15 › M05 audit token reel*
<hr>
<!-- /Breadcrumb -->

# MISSION 05 — Audit de la double strate Token/Reel

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF

Vérifier l'intégrité de la double strate : les fichiers `🔑 Token/` et `👤 Reel/` doivent être parfaitement synchronisés. Pas de dérive, pas d'orphelin, pas de fichier Reel sans équivalent Token (et inversement).

## MÉTHODE

1. **Lister** tous les fichiers dans `⚖️ Actes/🔑 Token/` (arborescence complète).

2. **Lister** tous les fichiers dans `⚖️ Actes/👤 Reel/` (arborescence complète).

3. **Pour chaque paire** :
   - Le fichier Token existe-t-il ? Le fichier Reel correspondant existe-t-il ?
   - Les contenus sont-ils identiques SAUF les noms/tokens qui sont dé-anonymisés ?
   - Le fichier Reel a-t-il été généré par `generate_real_versions.py` ou modifié manuellement ?
   - Y a-t-il des fichiers Reel qui n'ont PAS d'équivalent Token ?
   - Y a-t-il des fichiers Token qui n'ont PAS d'équivalent Reel ?

4. **Vérifier les tokens** : tous les tokens dans les fichiers Token sont-ils corrects selon `TOKEN MAP.md` ? Y a-t-il des noms réels qui subsistent dans les fichiers Token ?

5. **Vérifier les versions Reel** : les versions Reel contiennent-elles bien les vrais noms, adresses, numéros ? Pas de token oublié ?

## LIVRABLE

`📊 Rapports/85_Coherence_2026-07-15/M05_AUDIT_TOKEN_REEL.md`

Format : TODO list. Paires manquantes, tokens mal formés, noms réels dans Token, tokens dans Reel.