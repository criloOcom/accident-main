<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › [jules coherence 2026-07-15](./README.md)*
<hr>
<!-- /Breadcrumb -->

# MISSION 04 — Audit des jurisprudences (JURITEXT)

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF

Vérifier que CHAQUE décision de justice citée (Cour de cassation, Conseil d'État, cours d'appel) EXISTE RÉELLEMENT via son JURITEXT et est correctement référencée.

## MÉTHODE

1. **Extraire** toutes les citations de JURITEXT (identifiants commençant par `JURITEXT`, `CETATEXT`, `CONSTEXT`, etc.) dans les fichiers du dépôt.

2. **Pour chaque JURITEXT** : suivre le protocole strict de `JURITEXT_PROTOCOL.md` :
   - Étape 1 : Vérifier sur `legifrance-prod` via `consulter_decision`
   - Étape 2 : Vérifier sur `openlegi` via `get_decision_judiciaire` (ou administrative, constitutionnelle selon le type)
   - Les deux doivent confirmer l'existence

3. **Signaler** :
   - JURITEXT inexistant (retourne une erreur)
   - JURITEXT mal formaté
   - Décision citée qui ne correspond pas à ce que le dossier prétend (ex. décision sur un autre sujet)
   - Décision citée sans vérification (pas de mention de vérification)

4. **Cas particulier** : les décisions mentionnées par leur seul nom (ex. « Civ. 2e, 19 févr. 1997 ») sans JURITEXT doivent être marquées « À VÉRIFIER ».

## LIVRABLE

[Rapports/85_Coherence_20260715/M04_AUDIT_JURITEXT.md](../../Rapports/85_Coherence_20260715/M04_AUDIT_JURITEXT.md)

Format : TODO list. Chaque item = une JURITEXT avec statut (✓ existant, ✗ inexistant, ? non vérifié).