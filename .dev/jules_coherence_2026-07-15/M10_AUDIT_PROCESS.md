<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Environnement de Développement](../README.md) › jules coherence 2026-07-15 › M10 AUDIT PROCESS*
<hr>
<!-- /Breadcrumb -->

# MISSION 10 — Audit des process (AGENTS.md vs execution)

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF

Vérifier que les règles définies dans `AGENTS.md`, `CONVENTIONS.md`, `RULES.md` et `DECISIONS.md` sont bien respectées dans les fichiers du dépôt.

## MÉTHODE

1. **Lire** intégralement `AGENTS.md`, `CONVENTIONS.md`, `RULES.md`, `DECISIONS.md`.

2. **Pour chaque règle** applicable à un fichier, vérifier la conformité :
   - Règles de formatage (nommage, front matter, breadcrumbs)
   - Règles de contenu (pas de noms réels dans Token, pas de tokens dans Reel)
   - Règles de versioning (où sont stockées les SUPERSEDED)
   - Règles de vérification juridique (JURITEXT_PROTOCOL respecté ou pas)

3. **Signaler** toute violation :
   - Fichier qui ne respecte pas la convention de nommage
   - Document sans front matter YAML
   - Document sans breadcrumb
   - Document qui viole les règles d'anonymisation
   - Règle écrite mais jamais appliquée (règle orpheline)

## LIVRABLE

`📊 Rapports/85_Coherence_2026-07-15/M10_AUDIT_PROCESS.md`