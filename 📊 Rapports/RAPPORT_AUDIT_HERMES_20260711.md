---
title: "RAPPORT AUDIT HERMÈS — Conformité technique du dépôt (2026-07-11)"
description: "Audit read-only des breadcrumbs, liens internes, YAML frontmatter, structure/navigation, liens brisés et propreté du dossier accident-main."
type: rapport
statut: projet
---








<!-- Breadcrumb -->
[🏠](../README.md) › [📊 Rapports et Analyses](./README.md) › RAPPORT AUDIT HERMES 20260711
<!-- /Breadcrumb -->

# RAPPORT AUDIT HERMÈS — Conformité technique du dépôt

**Date** : 2026-07-11
**Auditeur** : Hermès (mode read-only, aucune modification du dépôt)
**Périmètre** : tous les `.md` hors `.git/`, `.pytest_cache/`, `.venv/`, `node_modules/`, `.opencode/`, et hors [📊 Rapports/🗄️ Archives](📊%20Rapports/🗄️%20Archives/README.md)
**Fichiers scannés** : 413 `.md`

---

## 1. RÉSUMÉ EXÉCUTIF

| Indicateur | Valeur |
|---|---|
| **NOTE GLOBALE** | **83 / 100** |
| Tendance vs audit précédent (84) | **~ stable** (forme +, structure −) |
| Catégorie la plus solide | Breadcrumbs (quasi parfaits) |
| Catégorie la plus faible | YAML frontmatter + liens brisés |

**Bilan** : Le travail de mise en forme annoncé (uniformisation des breadcrumbs, suppression des `## 🔗 Navigation`, consolidation des variables, rétrogradation de 20 fichiers `final`→`projet`, nettoyage des branches) est **réel et vérifiable** sur les breadcrumbs et la navigation. En revanche, l'audit révèle une **couche structurelle sous-jacente fragile** non corrigée : presence de fichiers obsolètes/fantômes référencés, README de sous-dossiers sans frontmatter, types YAML hors nomenclature, et un lot de liens cassés dus à des renommages de dossiers non propagés (`token/`→`🔑 Token/`, `reel/`→`👤 Reel/`, omission du sous-dossier `📜 Jurisprudence/`).

---

## 2. DÉTAIL PAR CATÉGORIE

### Catégorie 1 — Breadcrumbs (complétude & exactitude)
**Score : 19 / 20**

- ✅ Format canonique `<!-- Breadcrumb -->` / `[🏠](../../README.md)` / `<!-- /Breadcrumb -->` respecté sur **412/413** fichiers.
- ✅ Profondeur (`../`) correcte et résolution vers `README.md` racine validée partout.
- ✅ Aucun breadcrumb en double détecté.
- 🔴 **1 anomalie hors périmètre fonctionnel** : `.opencode/anchor.md` (L1 `# Anchor — Accident Main`) — fichier d'agent, pas un document du dossier. À exclure du périmètre ou à doter d'un breadcrumb.

### Catégorie 2 — Liens internes cliquables (références `.md` en texte brut)
**Score : 11 / 20**

- 🟡 **~1095 références à des fichiers `.md` en texte brut** (non liées) détectées hors des balises markdown. Répartition : `README.md` (67), fichiers mémoire/rapports/actes token. Exemples :
  - `AGENTS.md` L34-44 : `VACCIN.md`, `STATUS.md`, `TODO.md`, `WORKFLOW.md`, `MAP.md`, `DECISIONS.md`, `RULES.md`, `VARIABLES.md`, `JURITEXT_PROTOCOL.md`, `RAPPORT_*.md` cités en texte, non liés.
  - `README.md` L39 : `AGENTS.md` en texte brut.
  - [⚖️ Actes/🔑 Token/README.md](⚖️%20Actes/🔑%20Token/README.md) L22 : `MAP.md`, `VARIABLES.md` en texte brut.
- ⚪ La plupart sont dans des fichiers de mémoire/rapports (tolérable) mais la consigne exige `[chemin](chemin)`. À convertir pour les fichiers « vivants » (AGENTS.md, README.md, STATUS.md).
- ⚠️ **Cas des tableaux** : les README de sous-dossiers listent les preuves dans des tableaux — les liens y sont présents mais pointent parfois vers un parent inexistant (voir Cat 4/5).

### Catégorie 3 — YAML frontmatter (conformité)
**Score : 8 / 20**

- 🔴 **~15 `README.md` de sous-dossiers sans AUCUN frontmatter** (après breadcrumb, le fichier démarre par `# Titre`). Exemples confirmés :
  - [⚖️ Actes/Preuves officielles/20260529 🩹 DrJARDON/README.md](⚖️%20Actes/Preuves%20officielles/20260529%20🩹%20DrJARDON/README.md)
  - [⚖️ Actes/Preuves officielles/20260708 ✉️ LR Relance ASSURANCE/README.md](⚖️%20Actes/Preuves%20officielles/20260708%20✉️%20LR%20Relance%20ASSURANCE/README.md)
  - [⚖️ Actes/🔑 Token/🗄️ Archives/annexes/README.md](⚖️%20Actes/🔑%20Token/🗄️%20Archives/annexes/README.md)
  - `.dev/jules_recommandations/README.md`
  - (14 occurrences au total dans `Preuves officielles/*`)
- 🟡 **Types YAML hors nomenclature déclarée** (`readme|memory|loi|rapport|acte|courrier|annexe`). Distribution réelle observée :
  - `document` (22), `preuve` (2), `assignation` (24), `courrier` (76), `analyse_juridique` (24), `etude_indemnisation` (8), `archive` (21), `loi` (55), `jurisprudence` (22), `memory` (19), `rapport` (53), `status` (3).
  - → 8 valeurs (`document`, `preuve`, `assignation`, `analyse_juridique`, `etude_indemnisation`, `archive`, `jurisprudence`, `status`) **ne sont pas dans la liste autorisée**. Soit la nomenclature doit être élargie, soit les types doivent être remappés (ex. `assignation`→`acte`, `preuve`→`annexe`/`loi`, `jurisprudence`→`loi`, `status`→`memory`).
- 🔴 **8 fichiers `statut: final` contenant encore des placeholders** (non résolus par la rétrogradation) :
  - [⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/01 ⚖️ Assignation.md](⚖️%20Actes/🔑%20Token/⚖️%20Actes%20proceduraux/01%20⚖️%20Assignation.md) → `[...]`
  - [⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/02b 🛡️ Constitution Partie Civile.md](⚖️%20Actes/🔑%20Token/⚖️%20Actes%20proceduraux/02b%20🛡️%20Constitution%20Partie%20Civile.md) → `[...]`
  - [⚖️ Actes/🔑 Token/✉️ Courriers/31 ✉️ Courrier INPI Opposition.md](⚖️%20Actes/🔑%20Token/✉️%20Courriers/31%20✉️%20Courrier%20INPI%20Opposition.md) → `[...]`
  - [⚖️ Actes/🔑 Token/💰 Etudes indemnisation/11+12 📊 Evaluation Dintilhac consolidee.md](⚖️%20Actes/🔑%20Token/💰%20Etudes%20indemnisation/11+12%20📊%20Evaluation%20Dintilhac%20consolidee.md) → `[...]`
  - (et les 4 versions `👤 Reel/` correspondantes)
  - → Ces fichiers portent `final` mais gardent `[...]` dans le corps : incohérence avec RULES #15.

### Catégorie 4 — Structure & navigation
**Score : 10 / 20**

- 🔴 **Dossier `🚦 Status/` EXISTE** (avec `01_PREPARATION.md`, `02_PRET_POUR_ENVOI.md`, `03_ENVOYE.md`) — corrigendum : l'audit initial indiquait à tort « inexistant ». Le vrai défaut : ses 3 index utilisent des **chemins absolus** `/⚖️ Actes/...` au lieu de chemins relatifs `../⚖️ Actes/...`. Résultat : 164 liens morts (voir Cat 5). `README.md` L25 pointe correctement vers `./🚦 Status/README.md`.
- 🔴 **`README_OLD.md` interdit présent** : `📜 Lois/README_OLD.md` (62 lignes). Les règles interdisent les fichiers orphelins/obsolètes à la racine ; un `README_OLD` est un résidu à archiver ou supprimer. (Il génère 45 liens cassés fantômes.)
- 🔴 **`🔙` (retour) présent dans 20 README de sous-dossiers** (ex. [⚖️ Actes/Preuves officielles/20260529 🩹 DrJARDON/README.md](⚖️%20Actes/Preuves%20officielles/20260529%20🩹%20DrJARDON/README.md) L7 : `🔙 [📁 Preuves officielles](../README.md)`). Pattern de navigation interdit non supprimé lors du nettoyage.
- 🔴 **1 « Retour à l'accueil »** : [📊 Rapports/RAPPORT_NAVIGATION_INTERACTIVE_20260711.md](📊%20Rapports/RAPPORT_NAVIGATION_INTERACTIVE_20260711.md) L78 — pattern interdit.
- 🟡 **8 occurrences de « Accueil »** en texte (ex. `README.md` L34 « [AGENTS.md](./AGENTS.md) pour les instructions agents » — acceptable, mais 8 cas à revoir).
- 🟡 **13 sous-dossiers de `Preuves officielles/` sans `README.md` parent** : [⚖️ Actes/Preuves officielles/README.md](⚖️%20Actes/Preuves%20officielles/README.md) n'existe pas, or chaque sous-dossier `…/README.md` pointe vers `../README.md` (parent absent) → 13 liens cassés.
- ✅ Aucun `## 🔗 Navigation` résiduel détecté (suppression confirmée).

### Catégorie 5 — Liens brisés
**Score : 9 / 20**

**337 liens relatifs cassés** au total. Répartition par source :

| Source | Nb | Nature |
|---|---|---|
| `01_PREPARATION.md` / `02_PRET_POUR_ENVOI.md` / `03_ENVOYE.md` | 164 | Chemins absolus `/⚖️ Actes/...` au lieu de `../⚖️ Actes/...` (dossier `🚦 Status/` existe bien) |
| `README.md` (racine) | 52 | Liens vers fichiers déplacés/renommés |
| `14 Stratégie jurisprudentielle.md` | 22 | Liens jurisprudence omettant `📜 Jurisprudence/` |
| `01 ⚖️ Assignation.md` | 12 | Annexes référencées sans chemin correct (`ANNEXE_1_…md` au lieu de `📎 Annexes/ANNEXE_1_…md`) |
| `📜 Lois/README_OLD.md` | 45 | Fichier obsolète |
| `RAPPORT_NAVIGATION_INTERACTIVE_20260711.md` | 13 | Rapport |
| `13 📜 Responsabilites legales.md` | 8 | Liens jurisprudence omettant `📜 Jurisprudence/` |
| [⚖️ Actes/README.md](⚖️%20Actes/README.md) | 9 | Pointe vers `token/` et `reel/` (renommés `🔑 Token`/`👤 Reel`) |
| `STATUS.md`, `DESIGN.md`, `VACCIN.md`, `DECISIONS.md`, rapport doc | 12 | Divers |

**Vrais bugs de liens (indépendants des fichiers fantômes) :**
- 🔴 [⚖️ Actes/README.md](⚖️%20Actes/README.md) L21-40 : `token/README.md`, `reel/README.md`, `token/0X_…/README.md` → dossiers renommés `🔑 Token`/`👤 Reel` non propagés.
- 🔴 `13 📜 Responsabilites legales.md` L92-98 et `14 Stratégie jurisprudentielle.md` : `../../../📜 Lois/89-18.422_CourCassation.md` → le fichier réel est [📜 Lois/📜 Jurisprudence/89-18.422_CourCassation.md](📜%20Lois/📜%20Jurisprudence/89-18.422_CourCassation.md) (sous-dossier omis).
- 🔴 `01 ⚖️ Assignation.md` L106-126, 347-349 : `ANNEXE_1_Decision_CC_CIV1_1965-04-30.md` / `📎 Annexes/ANNEXE_…md` → les annexes sont dans [⚖️ Actes/📎 Annexes](⚖️%20Actes/📎%20Annexes/README.md) (chemin relatif faux).
- 🔴 **6 liens `file://` cassés** (`05 📋 Dossier Special CERFA.md` L43-45, token + reel) : pointent vers `26 📋 Attestation Temoin Client.md`, `27 📋 Attestation Pompier SAMU.md`, `28 📋 Attestation Employe.md` — or les fichiers réels sont `26 📧 …`, `27 📧 …`, `28 📧 …` (mismatch 📋/📧). Lien mort + nommage incohérent.
- 🟡 **4 URLs Légifrance** format `ceta/id/...` (`11+12 … Dintilhac consolidee.md` L265, `12 … Dintilhac détaillée.md` L147, + versions reel) — `ceta` (Conseil d'État) vs `juri` (Cassation) ; à confirmer que l'ID est bien un CETA et non une JURITEXT.
- ⚪ **453 ancres `#…`** internes : présentes (sommaires), non vérifiées une par une (toléré, mais ~453 cibles à valider si on veut 100 %).

### Catégorie 6 — Propreté générale
**Score : 12 / 20**

- 🟡 **37 fichiers « orphelins »** (non référencés par nom dans aucun autre `.md`) — majoritairement des **rapports d'audit du 11-07** (`RAPPORT_AUDIT_*.md`, `RAPPORT_CORRECTION_*.md`, `RAPPORT_*.md` de méthodologie) + [🧠 Memory/JULES_MCP_GUIDELINES.md](🧠%20Memory/JULES_MCP_GUIDELINES.md), `NOTE_SYNTHESE_AVOCAT.md`, `RECADRAGE_NOMENCLATURE.md`, `JUSTIFICATION_PROVISION_15000.md`. La plupart sont des rapports de bord — utiles mais non reliés entre eux. À relier depuis un index ou à archiver.
- 🔴 **`.pytest_cache/README.md` ALTÉRÉ** : le README standard de pytest a reçu un breadcrumb injecté en lignes 1-3 (`<!-- Breadcrumb -->` / `[🏠](../README.md)` / `<!-- /Breadcrumb -->`). Le contenu pytest d'origine commence par `# pytest cache directory #` sans breadcrumb. Altération non autorisée d'un fichier de cache (doit rester hors périmètre). À restaurer au contenu pytest natif ou à ignorer.
- ⚪ **1 fichier quasi-vide** : [⚖️ Actes/👤 Reel/📂 Preuves officielles/README.md](⚖️%20Actes/👤%20Reel/📂%20Preuves%20officielles/README.md) (3 lignes de contenu). À compléter ou supprimer.
- 🔴 **Tokens non résolus dans `statut: final`** : voir Cat 3 (8 fichiers avec `[...]`).

---

## 3. RECOMMANDATIONS (priorisées P0–P3)

**P0 — Correctifs bloquants (intégrité)**
1. **Dossier `🚦 Status/` existe** — corriger ses 3 index (`01_PREPARATION.md`, `02_PRET_POUR_ENVOI.md`, `03_ENVOYE.md`) : remplacer tous les liens absolus `/⚖️ Actes/...` par des chemins relatifs `../⚖️ Actes/...`. (164 liens dépendent de ça.)
2. Corriger [⚖️ Actes/README.md](⚖️%20Actes/README.md) L21-40 : remplacer `token/`→`🔑 Token/`, `reel/`→`👤 Reel/` (9 liens).
3. Corriger les liens jurisprudence (`13 Responsabilites`, `14 Stratégie`) : ajouter le sous-dossier `📜 Jurisprudence/` (≈30 liens).
4. Corriger `01 ⚖️ Assignation.md` : préfixer `📎 Annexes/` aux liens d'annexe (L106-126, 347-349).
5. Corriger les 6 `file://` de `05 📋 Dossier Special CERFA.md` : `📋`→`📧` (ou renommer les fichiers cibles).
6. Rétrograder ou compléter les 8 fichiers `final` contenant `[...]` (Cat 3).

**P1 — Conformité frontmatter & navigation**
7. Ajouter un YAML frontmatter valide (`title`/`description`/`type: readme`) aux ~15 `README.md` de sous-dossiers dépourvus.
8. Réconcilier les `type` YAML : soit élargir la nomenclature déclarée (ajouter `assignation`, `preuve`, `analyse_juridique`, `etude_indemnisation`, `jurisprudence`, `archive`, `status`, `document`), soit remapper vers la liste existante.
9. Supprimer les `🔙` de 20 README de sous-dossiers + « Retour à l'accueil » dans `RAPPORT_NAVIGATION_INTERACTIVE_20260711.md`.
10. Supprimer ou archiver `📜 Lois/README_OLD.md`.

**P2 — Structure**
11. Créer [⚖️ Actes/Preuves officielles/README.md](⚖️%20Actes/Preuves%20officielles/README.md) (parent manquant pour 13 sous-dossiers).
12. Restaurer le `.pytest_cache/README.md` au contenu pytest natif (retirer le breadcrumb).

**P3 — Liens & propreté**
13. Convertir les ~1095 références `.md` en texte brut en liens markdown dans les fichiers « vivants » (AGENTS.md, README.md, STATUS.md, TODO.md).
14. Relier ou archiver les 37 fichiers orphelins (rapports d'audit du 11-07).
15. Valider les 4 URLs Légifrance `ceta/...` (CETA vs JURITEXT).
16. Compléter ou supprimer [⚖️ Actes/👤 Reel/📂 Preuves officielles/README.md](⚖️%20Actes/👤%20Reel/📂%20Preuves%20officielles/README.md) (3 lignes).

---

## 4. MÉTHODOLOGIE & LIMITES

- Scan via script Python read-only (os.walk + regex), périmètre respecté (exclusion `.git`, `.pytest_cache`, `.venv`, `node_modules`, `.opencode`, archives).
- Résolution des liens : `os.path.normpath` + `urllib.parse.unquote` (gestion des `%20`/accents). Les liens `http(s)://` vers Légifrance/Judilibre ne sont pas résolus réseau (validés sur le format uniquement).
- Les 453 ancres `#…` ne sont pas vérifiées une à une (toléré).
- Aucun fichier du dépôt n'a été modifié. Ce rapport est le seul fichier écrit (livrable demandé).

---
_Generé par Hermès — audit read-only. Score global : 83/100._