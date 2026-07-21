---
title: "RECOVERY CHECKPOINT — 18 juillet 2026"
description: "Snapshot d'état pour reprise après compression mémoire. Contient tout le nécessaire pour continuer les 15 vérifications Jules."
type: memory
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › RECOVERY CHECKPOINT*
<hr>
<!-- /Breadcrumb -->

# RECOVERY CHECKPOINT<br>18 juillet 2026

## État Git
- **Branche :** `main`

- **Remote :** `origin → https://github.com/criloOcom/accident-main.git`

- **Auth :** `~/.git-credentials` (fallback)

- **Dernier commit :** `64be139 feat(rapport): add RAPPORT_SYNTHESE_AVOCAT_2026-07-18.md`

- **Fichiers modifiés non commit :** 211

## Travail effectué (Phases 1a→2)

### Phase 1a — Purge 5 fuites token
- 0 fuite résiduelle (✅ 18/07)

### Phase 1b — 5 corrections JURITEXT
- Vérifiées MCP dans 4 fichiers `.dev/app/` (✅ 18/07)

### Phase 1c — Infrastructure token
- +14 entrées `batch_anonymize.py`

- +14 mappings `generate_real_versions.py`

- Section Finance `TOKEN MAP.md`

### Phase 1d — Bandeau HB BARBER
- 80 fichiers Token/ mis à jour avec lien vers Erratum

### Phase 1e — Liens cassés
- 34 auto-corrigés, 3 stubs créés

- token-assureur-rc.md, token-j-63-assignation-145.md, token-exploitation-nom-commercial.md

- **50 liens historiques restants** (non bloquants)

### Phase 2 — Urgences 31 juillet
- Demande AJ Totale créée (`📝 Procédure/✉️ AJ - Demande Totale.md`)

- Assignation Référé-Provision finalisée (audience 31 juillet)

- Erratum Correction Société finalisé

- TJ Foix - TJ Foix - Mémo - Audience 31-07-2026.md réécrit (logistique + plaidoirie 3 min + HB BARBER)

- Versions Reel générées (115 fichiers)

- READMEs synchronisés (103 à jour, 3 table-format MAJ manuelle)

### Fixes post-Phase 2
- `token-hopital-urgence-medecin` : 10 liens path depth corrigés (12 fichiers Token + 12 Reel)

- `token-metropole-regionale` → `token-accident-metropole` : 2 fichiers

- `SAS Assureur.md` → `SAS Assureur RC.md` : 5 fichiers référence

- Tokens README : +12 tokens ajoutés (88 fiches)

- Preuves officielles README : +1 ligne Rapport Expertise

- Procédure README : +1 ligne Demande AJ Totale

- `__pycache__` supprimé

## Fichiers critiques

### Actes finalisés (audience 31 juillet)
- `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/📋 Preparation Foix/📜 Police - Note Erratum Identité.md`

- `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/📋 Preparation Foix/TJ Foix - TJ Foix - Mémo - Audience 31-07-2026.md`

- `⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/📜 Contentieux civil/Référé Provision - Assignation.md`

- `⚖️ Actes/🔑 Token/✉️ Courriers/📝 Procédure/✉️ AJ - Demande Totale.md`

### Infra token
- `🧠 Memory/TOKEN MAP.md`

- `🧠 Memory/🗂️ Tokens/README.md`

- `.dev/app/batch_anonymize.py`

- `.dev/app/generate_real_versions.py`

### Stubs à compléter
- `🧠 Memory/🗂️ Tokens/token-assureur-rc.md`

- `🧠 Memory/🗂️ Tokens/token-j-63-assignation-145.md`

- `🧠 Memory/🗂️ Tokens/token-exploitation-nom-commercial.md`

## Prochaine action
**Lancer 15 vérifications Jules** — voir PLAN ci-dessous.

---

## PLAN — 15 vérifications Jules

### Étape 1 : Commit & Push
```
git add -A && git commit -m "feat: Phase 1a→2 complete — AJ, Assignation, Erratum, Reel 115, fixes liens, READMEs" && git push origin main
```

### Étape 2 : Clôture 15 sessions Batch 8
Chaque session reçoit : *"Mission clôturée — implémentations réalisées par opencode. Passage en vérification."*

Session IDs:
- M01: 11500201233044822502

- M02: 5629017950384422605

- M03: 10102808889233645521

- M04: 987403715759435362

- M05: 14398442053003273380

- M06: 15506563858622126387

- M07: 1353864396770670977

- M08: 3823380336442206742

- M09: 9024090879013311107

- M10: 5835767582474031144

- M11: 8428641977659595451

- M12: 6173308142549219569

- M13: 15147189954702675284

- M14: 5735397749844847186

- M15: 7049455188294447707

### Étape 3 : Créer prompts dans .dev/jules_verification_2026-07-18/
15 fichiers M01.md → M15.md + PROMPT_COMMUN.md

### Étape 4 : Lancer 15 missions (3 lots de 5)
Lot 1 (V01-V05) → Lot 2 (V06-V10) → Lot 3 (V11-V15)

Chaque session : `{repo: "criloOcom/accident-main", branch: "main", autoPr: true, interactive: false}`

### Mapping Vérification → Batch 8 original
| V# | Batch 8 source | Fichiers à vérifier |
|----|----------------|---------------------|
| V01 | M01 HB BARBER | 80 fichiers Token/, Erratum, tokens HB |
| V02 | M02 Abs assurance | Actes procéduraux, Courriers |
| V03 | M03 Stratégie | Mémo stratégie, Note synthèse avocat |
| V04 | M04 Note étape | Notes d'étape, Frise |
| V05 | M05 Demande AJ | ✉️ AJ - Demande Totale.md |
| V06 | M06 Requête 145 | Référé Provision - Assignation.md |
| V07 | M07 Plainte + Erratum | Plainte complémentaire, Erratum |
| V08 | M08 Plan déplacement | TJ Foix - TJ Foix - Mémo - Audience 31-07-2026.md |
| V09 | M09 LRARs | Courriers LRAR (Mises en demeure) |
| V10 | M10 Fausses mentions | Vérifier mentions "Déposé" |
| V11 | M11 TOKEN MAP | TOKEN MAP, batch_anonymize, generate_real_versions |
| V12 | M12 Liens + README | Audit liens internes, READMEs |
| V13 | M13 JURITEXT | JURITEXT vérifiées MCP |
| V14 | M14 Scénario pire | Rapports scénario pire |
| V15 | M15 Synthèse | RAPPORT_SYNTHESE_AVOCAT.md |

---

*Généré le 18 juillet 2026 — En cas de perte de contexte, lire ce fichier d'abord.*