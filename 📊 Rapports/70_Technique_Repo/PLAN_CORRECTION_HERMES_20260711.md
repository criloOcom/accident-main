---
title: "PLAN DE CORRECTION HERMÈS — Audit 2026-07-11"
date: 2026-07-11
description: "Plan d'actions ciblé (P0-P3) pour corriger les anomalies du RAPPORT_AUDIT_HERMES_20260711.md. Aucune modification sans feu vert."
type: rapport
statut: projet
---
<!-- Breadcrumb -->
*[🏠](../../README.md) › [📊 Rapports et Analyses](../README.md) › [70_Technique_Repo — Journal de bord technique](./README.md) › PLAN CORRECTION HERMES 20260711*
<hr>
<!-- /Breadcrumb -->

# PLAN DE CORRECTION HERMÈS<br>Audit 2026-07-11

**Mode** : read-only (ce document est un plan ; aucune modification du dépôt n'est effectuée).
**Référence** : [📊 Rapports/RAPPORT_AUDIT_HERMES_20260711.md](../60_Audits_Qualite/RAPPORT_AUDIT_HERMES_20260711.md)
**Dépôt** : `/home/crilocom/accident-main/`

> Chaque action ci-dessous est exécutable de façon déterministe. Les actions **[SCRIPT]** sont automatisables via un script Python (approved par l'utilisateur au cas par cas). Les actions **[MANUEL]** nécessitent une décision humaine ou une vérification (RGPD, statuts juridiques).

---

## I — P0 — Correctifs bloquants (intégrité des liens)

### I.1 — P0-1 — Index `🚦 Status/` : chemins absolus → relatifs  [SCRIPT]
- **Cible** : `🚦 Status/01_PREPARATION.md`, `🚦 Status/02_PRET_POUR_ENVOI.md`, `🚦 Status/03_ENVOYE.md`

- **Défaut** : tous les liens internes utilisent des chemins absolus `/⚖️ Actes/...` (ex. `/⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/📜 Contentieux civil/Référé - Assignation Provision.md`) → morts sur GitHub/HTML.

- **Correction** : remplacer `](/%E2%9A%96%EF%B8%8F%20Actes/%60%20par%20%60%5D%28../%E2%9A%96%EF%B8%8F%20Actes/%60%20%28et%20%60%5D%28/%F0%9F%93%8A%20Rapports/%60%20par%20%60%5D%28../%F0%9F%93%8A%20Rapports/%60%20si%20pr%C3%A9sent).

- **Impact** : 164 liens réparés. À rejouer `check_consistency.py` après.

### I.2 — P0-2 — [⚖️ Actes/README.md](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) : dossiers renommés  [SCRIPT]
- **Lignes** : L21-40 (arborescence).

- **Défaut** : `token/` et `reel/` n'existent plus (renommés `🔑 Token`/`👤 Reel`).

- **Correction** : `token/` → `🔑 Token/`, `reel/` → `👤 Reel/` dans les liens (9 occ.).

- **Note** : vérifier aussi `📂 Preuves officielles/` existe bien sous `🔑 Token/`.

### I.3 — P0-3 — Liens jurisprudence : sous-dossier `📜 Jurisprudence/README.md` manquant  [SCRIPT]
- **Cibles** :

  - [⚖️ Actes/🔑 Token/📚 Analyses juridiques/Note - Analyse Responsabilités Légales.md](%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%F0%9F%93%9A%20Analyses%20juridiques/13%20%F0%9F%93%9C%20Responsabilites%20legales.md) (L92-98, 4 liens `../../../📜 Lois/X.md`)
  - [⚖️ Actes/🔑 Token/📚 Analyses juridiques/Note - Stratégie Jurisprudentielle.md](%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%F0%9F%93%9A%20Analyses%20juridiques/14%20Strat%C3%A9gie%20jurisprudentielle.md) (L30-37, ~11 liens `../../📜 Lois/X.md`)
  - (et les 2 versions `👤 Reel/` correspondantes → total ~30 liens)
- **Correction** : insérer `📜 Jurisprudence/README.md` → `../../../📜 Lois/📜 Jurisprudence/README.mdX.md` (token) / `../../📜 Lois/📜 Jurisprudence/README.mdX.md` (reel).

- **Vérifier** cible existe : [📜 Lois/📜 Jurisprudence/README.md89-18.422_CourCassation.md](../../%F0%9F%93%9C%20Lois/%F0%9F%93%9C%20Jurisprudence/%F0%9F%8F%9B%EF%B8%8F%20Responsabilit%C3%A9%20du%20fait%20des%20choses/89-18.422_CourCassation.md) ✅ présent.

### I.4 — P0-4 — `Référé - Assignation Provision.md` : chemins d'annexe  [SCRIPT]
- **Cibles** : `⚖️ Actes/{🔑 Token,👤 Reel}/⚖️ Actes proceduraux/Référé - Assignation Provision.md` (L106-126, 347-349)

- **Correction appliquée (juil. 2026)** : les 3 ANNEXES ont été déplacées dans [📜 Lois/📜 Jurisprudence/](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) — voir `63-13.613`, `90-14.591`, `11-13.384`.

### I.5 — P0-5 — `05 Note - Dossier Spécial CERFA.md` : 6 liens `file://` cassés  [MANUEL + SCRIPT]
- **Cibles** : `⚖️ Actes/{🔑 Token,👤 Reel}/🗂️ Organisation/05 Note - Dossier Spécial CERFA.md` (L43-45)

- **Défaut** : pointe vers `file:///.../✉️ Courriers/26 ✉️ Attestation - Témoin Client.md` etc. → le 📋 est faux (fichiers réels = `📧`) ET `file://` absolu interdit.

- **Deux options** :

  - (a) Renommer les fichiers cibles `26/27/28 📋 ...` → `26/27/28 📧 ...` (à valider avec l'utilisateur car touche nommage).
  - (b) Corriger les liens en chemins relatifs `../✉️ Courriers/26 📧✉️ Attestation - Témoin Client.md` (sans `file://`).
- **Recommandation** : option (b) (non destructif). Les fichiers réels sont `26 📧✉️ Attestation - Témoin Client.md`, `27 📧✉️ Attestation - Pompier SAMU.md`, `28 📧✉️ Attestation - Employé.md` ✅.

### I.6 — P0-6 — 8 fichiers `statut: final` contenant `[...]`  [MANUEL]
- **Cibles** :

  - [⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/Référé - Assignation Provision.md](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9A%96%EF%B8%8F%20Actes%20proceduraux/%F0%9F%93%9C%20Contentieux%20civil/R%C3%A9f%C3%A9r%C3%A9%20-%20Assignation%20Provision.md)
  - [⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/Constitution - Partie Civile.md](%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9A%96%EF%B8%8F%20Actes%20proceduraux/02b%20Constitution%20-%20Partie%20Civile.md)
  - [⚖️ Actes/🔑 Token/✉️ Courriers/✉️ Signalement - INPI.md](%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9C%89%EF%B8%8F%20Courriers/31%20%E2%9C%89%EF%B8%8F%20Courrier%20INPI%20Opposition.md)
  - [⚖️ Actes/🔑 Token/💰 Etudes indemnisation/Note - Évaluation Dintilhac Consolidée.md](%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%F0%9F%92%B0%20Etudes%20indemnisation/11%2B12%20%F0%9F%93%8A%20Evaluation%20Dintilhac%20consolidee.md)
  - (et les 4 versions `👤 Reel/`)
- **Défaut** : `statut: final` mais `[...]` non résolu dans le corps → incohérent avec RULES #15.

- **Action** : soit compléter le contenu, soit rétrograder en `statut: projet`. **Décision humaine requise** (le contenu `[...]` peut être volontaire en attendant une donnée réelle).

---

## II — P1 — Conformité frontmatter & navigation

### II.1 — P1-1 — README de sous-dossiers sans frontmatter  [SCRIPT + MANUEL]
- **Cibles** (~15) : tous les `⚖️ Actes/Preuves officielles/{date}*/README.md`, [⚖️ Actes/🔑 Token/🗄️ Archives/annexes/README.md](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md), [⚖️ Actes/📎 Annexes/README.md](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md), `.dev/jules_recommandations/README.md`.

- **Correction** : insérer après le breadcrumb (ligne 4) :
  ```
  ---
  title: "📁 {Nom du dossier}"
  description: "Index des pièces / documents de ce dossier"
  type: readme
  ---
  ```
- **Vérifier** que `Preuves officielles/README.md` parent existe (voir P2-1).

### II.2 — P1-2 — Types YAML hors nomenclature  [MANUEL]
- **Valeurs observées hors liste** (`readme|memory|loi|rapport|acte|courrier|annexe`) : `document` (22), `preuve` (2), `assignation` (24), `courrier` (76 — OK), `analyse_juridique` (24), `etude_indemnisation` (8), `archive` (21), `loi` (55 — OK), `jurisprudence` (22), `memory` (19 — OK), `rapport` (53 — OK), `status` (3).

- **Décision requise** : choisir l'une des deux voies :

  - (a) **Élargir la nomenclature** dans AGENTS.md/RULES.md pour inclure `assignation`, `analyse_juridique`, `etude_indemnisation`, `jurisprudence`, `archive`, `preuve`, `document`, `status`.
  - (b) **Remapper** : `assignation`→`acte`, `analyse_juridique`→`analyse`(à ajouter), `preuve`→`annexe`, `jurisprudence`→`loi`, `archive`→`rapport`/nouveau, `status`→`memory`.
- **Recommandation** : voie (a) — moins destructif, reflète la réalité du dossier.

### II.3 — P1-3 — `🔙` et « Retour à l'accueil »  [SCRIPT]
- **Cibles** : 20 README de sous-dossiers (`⚖️ Actes/Preuves officielles/{date}*/README.md` L7 : `🔙 [📁 ...](../README.md)`) + [📊 Rapports/RAPPORT_NAVIGATION_INTERACTIVE_20260711.md](RAPPORT_NAVIGATION_INTERACTIVE_20260711.md) L78 (`Retour à l'accueil`).

- **Correction** : supprimer les lignes contenant `🔙` et `Retour à l'accueil` (le fil d'Ariane suffit).

### II.4 — P1-4 — `README_OLD.md` interdit  [MANUEL]
- **Cible** : `📜 Lois/README_OLD.md` (62 lignes, obsolète).

- **Action** : archiver dans [📊 Rapports/🗄️ Archives](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) ou supprimer (après confirmation qu'il ne sert plus). Génère 45 liens fantômes.

---

## III — P2 — Structure

### III.1 — P2-1 — `Preuves officielles/README.md` manquant  [SCRIPT]
- **Défaut** : 13 sous-dossiers `Preuves officielles/{date}*/README.md` pointent vers `../README.md` (parent absent).

- **Correction** : créer [⚖️ Actes/Preuves officielles/README.md](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) (frontmatter `type: readme`) listant les 13 sous-dossiers.

### III.2 — P2-2 — `.pytest_cache/README.md` altéré  [SCRIPT]
- **Défaut** : breadcrumb injecté dans le README natif de pytest (lignes 1-3).

- **Correction** : restaurer le contenu d'origine pytest (sans breadcrumb) — ce fichier est hors périmètre de nommage.

---

## IV — P3 — Liens & propreté

### IV.1 — P3-1 — Références `.md` en texte brut → liens  [SCRIPT partiel]
- **Volume** : ~1095 occurrences (AGENTS.md, README.md, STATUS.md, TODO.md, etc.).

- **Action** : pour les fichiers « vivants » (AGENTS.md, README.md, STATUS.md, TODO.md), convertir `NOM.md` en `[NOM.md](chemin/relatif/NOM.md)`.

- **Note** : les rapports d'audit historiques peuvent rester en texte (toléré). Script à exécuter avec précaution (risque de faux positifs sur les noms partiels).

### IV.2 — P3-2 — 37 fichiers orphelins  [MANUEL]
- **Cibles** : rapports `RAPPORT_AUDIT_*.md`, `RAPPORT_CORRECTION_*.md`, `RAPPORT_*.md` du 11-07 + `🧠 Memory/{JULES_MCP_GUIDELINES, NOTE_SYNTHESE_AVOCAT, RECADRAGE_NOMENCLATURE, JUSTIFICATION_PROVISION_15000}.md`.

- **Action** : relier depuis un index ([📊 Rapports/README.md](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md)) ou archiver dans [📊 Rapports/🗄️ Archives](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md).

### IV.3 — P3-3 — URLs Légifrance `ceta/...`  [MANUEL]
- **Cibles** : `11+12 … Dintilhac consolidee.md` L265, `12 … Dintilhac détaillée.md` L147 (+ reel).

- **Action** : vérifier via MCP Légifrance que `CETATEXT000049375170` est bien un arrêt du Conseil d'État (et non une JURITEXT de Cassation). Corriger si besoin.

### IV.4 — P3-4 — README quasi-vide  [SCRIPT]
- **Cible** : [⚖️ Actes/👤 Reel/📂 Preuves officielles/README.md](../../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) (3 lignes).

- **Action** : compléter ou supprimer (doublon du token ?).

---

## V — ORDRE D'EXÉCUTION RECOMMANDÉ

1. **P0-1** (164 liens) — plus gros gain immédiat.

2. **P0-2, P0-3, P0-4, P0-5** — liens morts restants (script + 1 décision).

3. **P2-1, P2-2** — structure/cache.

4. **P1-1, P1-3** — frontmatter + navigation (script).

5. **P1-2, P1-4, P0-6, P3-2, P3-3** — décisions humaines (MANUEL).

6. **P3-1, P3-4** — polish.

**Validation finale** : relancer `python3 .dev/app/check_consistency.py` (0 erreur attendue) + re-scan breadcrumbs/liens (script Hermès).

---
_Generé par Hermès — plan read-only. Aucune action exécutée._