<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › [jules coherence 2026-07-15](./README.md)*
<hr>
<!-- /Breadcrumb -->

# MISSION 07 — Audit des redondances et contradictions

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF

Détecter les informations dupliquées ou contradictoires entre les différents fichiers du dépôt.

## MÉTHODE

1. **Par domaine** — comparer les mêmes informations entre :
   - `STATUS.md` vs `TODO.md` vs les fichiers d'actes
   - Les montants Dintilhac dans les rapports vs les actes
   - Les dates dans les mémoires vs STRICT VARIABLES
   - Les tokens dans les fichiers Token vs TOKEN MAP

2. **Signaler** :
   - Duplications exactes (même info écrite 3 fois dans 3 fichiers différents)
   - Contradictions (une info dit X, une autre dit Y)
   - Informations orphelines (mentionnées une fois, jamais reprises)

3. **Cas particulier** : les fichiers PIECES MAP et le bordereau de communication — les pièces listées sont-elles bien toutes présentes ?

## LIVRABLE

[Rapports/85_Coherence_2026-07-15/M07_AUDIT_REDONDANCE.md](../../Rapports/85_Coherence_2026-07-15/M07_AUDIT_REDONDANCE.md)