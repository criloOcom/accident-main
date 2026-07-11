<!-- Breadcrumb -->
[🏠](../README.md) › [📊 Rapports et Analyses](./README.md) › PLAN CORRECTION HERMES 20260711
<!-- /Breadcrumb -->

---
title: "PLAN DE CORRECTION HERMÈS — Audit 2026-07-11"
description: "Plan d'actions ciblé (P0-P3) pour corriger les anomalies du RAPPORT_AUDIT_HERMES_20260711.md. Aucune modification sans feu vert."
type: rapport
statut: projet
---

# PLAN DE CORRECTION HERMÈS — Audit 2026-07-11

**Mode** : read-only (ce document est un plan ; aucune modification du dépôt n'est effectuée).
**Référence** : [📊_Rapports/RAPPORT_AUDIT_HERMES_20260711.md](📊_Rapports/RAPPORT_AUDIT_HERMES_20260711.md)
**Dépôt** : `/home/crilocom/accident-main/`

> Chaque action ci-dessous est exécutable de façon déterministe. Les actions **[SCRIPT]** sont automatisables via un script Python (approved par l'utilisateur au cas par cas). Les actions **[MANUEL]** nécessitent une décision humaine ou une vérification (RGPD, statuts juridiques).

---

## P0 — Correctifs bloquants (intégrité des liens)

### P0-1 — Index `🚦 Status/` : chemins absolus → relatifs  [SCRIPT]
- **Cible** : `🚦_Status/01_PREPARATION.md`, `🚦_Status/02_PRET_POUR_ENVOI.md`, `🚦_Status/03_ENVOYE.md`
- **Défaut** : tous les liens internes utilisent des chemins absolus `/⚖️_Actes/...` (ex. `/⚖️_Actes/🔑_Token/01_⚖️_Actes_proceduraux/01 ⚖️ Assignation.md`) → morts sur GitHub/HTML.
- **Correction** : remplacer `](/⚖️_Actes/` par `](../⚖️_Actes/` (et `](/📊_Rapports/` par `](../📊_Rapports/` si présent).
- **Impact** : 164 liens réparés. À rejouer `check_consistency.py` après.

### P0-2 — [⚖️_Actes/README.md](⚖️_Actes/README.md) : dossiers renommés  [SCRIPT]
- **Lignes** : L21-40 (arborescence).
- **Défaut** : `token/` et `reel/` n'existent plus (renommés `🔑_Token`/`👤_Reel`).
- **Correction** : `token/` → `🔑_Token/`, `reel/` → `👤_Reel/` dans les liens (9 occ.).
- **Note** : vérifier aussi `00_📂_Preuves_officielles/` existe bien sous `🔑_Token/`.

### P0-3 — Liens jurisprudence : sous-dossier `📜_Jurisprudence/` manquant  [SCRIPT]
- **Cibles** :
  - [⚖️_Actes/🔑_Token/03_📚_Analyses_juridiques/13 📜 Responsabilites legales.md](⚖️_Actes/🔑_Token/03_📚_Analyses_juridiques/13 📜 Responsabilites legales.md) (L92-98, 4 liens `../../../📜_Lois/X.md`)
  - [⚖️_Actes/🔑_Token/03_📚_Analyses_juridiques/14 Stratégie jurisprudentielle.md](⚖️_Actes/🔑_Token/03_📚_Analyses_juridiques/14 Stratégie jurisprudentielle.md) (L30-37, ~11 liens `../../📜_Lois/X.md`)
  - (et les 2 versions `👤_Reel/` correspondantes → total ~30 liens)
- **Correction** : insérer `📜_Jurisprudence/` → `../../../📜_Lois/📜_Jurisprudence/X.md` (token) / `../../📜_Lois/📜_Jurisprudence/X.md` (reel).
- **Vérifier** cible existe : [📜_Lois/📜_Jurisprudence/89-18.422_CourCassation.md](📜_Lois/📜_Jurisprudence/89-18.422_CourCassation.md) ✅ présent.

### P0-4 — `01 ⚖️ Assignation.md` : chemins d'annexe  [SCRIPT]
- **Cibles** : `⚖️_Actes/{🔑_Token,👤_Reel}/01_⚖️_Actes_proceduraux/01 ⚖️ Assignation.md` (L106-126, 347-349)
- **Défaut** : `ANNEXE_1_Decision_CC_CIV1_1965-04-30.md` (fichier à la racine du dossier) et `📎_Annexes/ANNEXE_...md` (dossier `📎_Annexes` introuvable depuis ce chemin).
- **Correction** : préfixer `📎_Annexes/` → `📎_Annexes/ANNEXE_1_Decision_CC_CIV1_1965-04-30.md` (les 3 annexes sont dans [⚖️_Actes/📎_Annexes](⚖️_Actes/📎_Annexes/README.md)).
- **Vérifier** : `⚖️_Actes/📎_Annexes/ANNEXE_1/2/3_Decision_CC_CIV1_*.md` ✅ présents.

### P0-5 — `05 📋 Dossier Special CERFA.md` : 6 liens `file://` cassés  [MANUEL + SCRIPT]
- **Cibles** : `⚖️_Actes/{🔑_Token,👤_Reel}/05_🗂️_Organisation/05 📋 Dossier Special CERFA.md` (L43-45)
- **Défaut** : pointe vers `file:///.../02_✉️_Courriers/26 📋 Attestation Temoin Client.md` etc. → le 📋 est faux (fichiers réels = `📧`) ET `file://` absolu interdit.
- **Deux options** :
  - (a) Renommer les fichiers cibles `26/27/28 📋 ...` → `26/27/28 📧 ...` (à valider avec l'utilisateur car touche nommage).
  - (b) Corriger les liens en chemins relatifs `../02_✉️_Courriers/26 📧 Attestation Temoin Client.md` (sans `file://`).
- **Recommandation** : option (b) (non destructif). Les fichiers réels sont `26 📧 Attestation Temoin Client.md`, `27 📧 Attestation Pompier SAMU.md`, `28 📧 Attestation Employe.md` ✅.

### P0-6 — 8 fichiers `statut: final` contenant `[...]`  [MANUEL]
- **Cibles** :
  - [⚖️_Actes/🔑_Token/01_⚖️_Actes_proceduraux/01 ⚖️ Assignation.md](⚖️_Actes/🔑_Token/01_⚖️_Actes_proceduraux/01 ⚖️ Assignation.md)
  - [⚖️_Actes/🔑_Token/01_⚖️_Actes_proceduraux/02b 🛡️ Constitution Partie Civile.md](⚖️_Actes/🔑_Token/01_⚖️_Actes_proceduraux/02b 🛡️ Constitution Partie Civile.md)
  - [⚖️_Actes/🔑_Token/02_✉️_Courriers/31 ✉️ Courrier INPI Opposition.md](⚖️_Actes/🔑_Token/02_✉️_Courriers/31 ✉️ Courrier INPI Opposition.md)
  - [⚖️_Actes/🔑_Token/04_💰_Etudes_indemnisation/11+12 📊 Evaluation Dintilhac consolidee.md](⚖️_Actes/🔑_Token/04_💰_Etudes_indemnisation/11+12 📊 Evaluation Dintilhac consolidee.md)
  - (et les 4 versions `👤_Reel/`)
- **Défaut** : `statut: final` mais `[...]` non résolu dans le corps → incohérent avec RULES #15.
- **Action** : soit compléter le contenu, soit rétrograder en `statut: projet`. **Décision humaine requise** (le contenu `[...]` peut être volontaire en attendant une donnée réelle).

---

## P1 — Conformité frontmatter & navigation

### P1-1 — README de sous-dossiers sans frontmatter  [SCRIPT + MANUEL]
- **Cibles** (~15) : tous les `⚖️_Actes/00_Preuves_officielles/{date}*/README.md`, [⚖️_Actes/🔑_Token/06_🗄️_Archives/annexes/README.md](⚖️_Actes/🔑_Token/06_🗄️_Archives/annexes/README.md), [⚖️_Actes/📎_Annexes/README.md](⚖️_Actes/📎_Annexes/README.md), `.dev/jules_recommandations/README.md`.
- **Correction** : insérer après le breadcrumb (ligne 4) :
  ```
  ---
  title: "📁 {Nom du dossier}"
  description: "Index des pièces / documents de ce dossier"
  type: readme
  ---
  ```
- **Vérifier** que `00_Preuves_officielles/README.md` parent existe (voir P2-1).

### P1-2 — Types YAML hors nomenclature  [MANUEL]
- **Valeurs observées hors liste** (`readme|memory|loi|rapport|acte|courrier|annexe`) : `document` (22), `preuve` (2), `assignation` (24), `courrier` (76 — OK), `analyse_juridique` (24), `etude_indemnisation` (8), `archive` (21), `loi` (55 — OK), `jurisprudence` (22), `memory` (19 — OK), `rapport` (53 — OK), `status` (3).
- **Décision requise** : choisir l'une des deux voies :
  - (a) **Élargir la nomenclature** dans AGENTS.md/RULES.md pour inclure `assignation`, `analyse_juridique`, `etude_indemnisation`, `jurisprudence`, `archive`, `preuve`, `document`, `status`.
  - (b) **Remapper** : `assignation`→`acte`, `analyse_juridique`→`analyse`(à ajouter), `preuve`→`annexe`, `jurisprudence`→`loi`, `archive`→`rapport`/nouveau, `status`→`memory`.
- **Recommandation** : voie (a) — moins destructif, reflète la réalité du dossier.

### P1-3 — `🔙` et « Retour à l'accueil »  [SCRIPT]
- **Cibles** : 20 README de sous-dossiers (`⚖️_Actes/00_Preuves_officielles/{date}*/README.md` L7 : `🔙 [📁 ...](../README.md)`) + [📊_Rapports/RAPPORT_NAVIGATION_INTERACTIVE_20260711.md](📊_Rapports/RAPPORT_NAVIGATION_INTERACTIVE_20260711.md) L78 (`Retour à l'accueil`).
- **Correction** : supprimer les lignes contenant `🔙` et `Retour à l'accueil` (le fil d'Ariane suffit).

### P1-4 — `README_OLD.md` interdit  [MANUEL]
- **Cible** : `📜_Lois/README_OLD.md` (62 lignes, obsolète).
- **Action** : archiver dans [📊_Rapports/🗄️_Archives](📊_Rapports/🗄️_Archives/README.md) ou supprimer (après confirmation qu'il ne sert plus). Génère 45 liens fantômes.

---

## P2 — Structure

### P2-1 — `00_Preuves_officielles/README.md` manquant  [SCRIPT]
- **Défaut** : 13 sous-dossiers `00_Preuves_officielles/{date}*/README.md` pointent vers `../README.md` (parent absent).
- **Correction** : créer [⚖️_Actes/00_Preuves_officielles/README.md](⚖️_Actes/00_Preuves_officielles/README.md) (frontmatter `type: readme`) listant les 13 sous-dossiers.

### P2-2 — `.pytest_cache/README.md` altéré  [SCRIPT]
- **Défaut** : breadcrumb injecté dans le README natif de pytest (lignes 1-3).
- **Correction** : restaurer le contenu d'origine pytest (sans breadcrumb) — ce fichier est hors périmètre de nommage.

---

## P3 — Liens & propreté

### P3-1 — Références `.md` en texte brut → liens  [SCRIPT partiel]
- **Volume** : ~1095 occurrences (AGENTS.md, README.md, STATUS.md, TODO.md, etc.).
- **Action** : pour les fichiers « vivants » (AGENTS.md, README.md, STATUS.md, TODO.md), convertir `NOM.md` en `[NOM.md](chemin/relatif/NOM.md)`.
- **Note** : les rapports d'audit historiques peuvent rester en texte (toléré). Script à exécuter avec précaution (risque de faux positifs sur les noms partiels).

### P3-2 — 37 fichiers orphelins  [MANUEL]
- **Cibles** : rapports `RAPPORT_AUDIT_*.md`, `RAPPORT_CORRECTION_*.md`, `RAPPORT_*.md` du 11-07 + `🧠_Memory/{JULES_MCP_GUIDELINES, NOTE_SYNTHESE_AVOCAT, RECADRAGE_NOMENCLATURE, JUSTIFICATION_PROVISION_15000}.md`.
- **Action** : relier depuis un index ([📊_Rapports/README.md](📊_Rapports/README.md)) ou archiver dans [📊_Rapports/🗄️_Archives](📊_Rapports/🗄️_Archives/README.md).

### P3-3 — URLs Légifrance `ceta/...`  [MANUEL]
- **Cibles** : `11+12 … Dintilhac consolidee.md` L265, `12 … Dintilhac détaillée.md` L147 (+ reel).
- **Action** : vérifier via MCP Légifrance que `CETATEXT000049375170` est bien un arrêt du Conseil d'État (et non une JURITEXT de Cassation). Corriger si besoin.

### P3-4 — README quasi-vide  [SCRIPT]
- **Cible** : [⚖️_Actes/👤_Reel/00_📂_Preuves_officielles/README.md](⚖️_Actes/👤_Reel/00_📂_Preuves_officielles/README.md) (3 lignes).
- **Action** : compléter ou supprimer (doublon du token ?).

---

## ORDRE D'EXÉCUTION RECOMMANDÉ

1. **P0-1** (164 liens) — plus gros gain immédiat.
2. **P0-2, P0-3, P0-4, P0-5** — liens morts restants (script + 1 décision).
3. **P2-1, P2-2** — structure/cache.
4. **P1-1, P1-3** — frontmatter + navigation (script).
5. **P1-2, P1-4, P0-6, P3-2, P3-3** — décisions humaines (MANUEL).
6. **P3-1, P3-4** — polish.

**Validation finale** : relancer `python3 .dev/app/check_consistency.py` (0 erreur attendue) + re-scan breadcrumbs/liens (script Hermès).

---
_Generé par Hermès — plan read-only. Aucune action exécutée._
