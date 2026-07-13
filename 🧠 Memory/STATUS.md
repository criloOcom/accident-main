---
title: "STATUT D'AVANCEMENT — 13 juillet 2026"
description: "- **Phase 21** Navigation Interactive Cross-Document : 1 766 liens relatifs créés (✅ TERMINÉ)"
type: memory
---

<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Mémoire du Projet](./README.md) › STATUS*
<hr>
<!-- /Breadcrumb -->

# STATUT D'AVANCEMENT<br>13 juillet 2026

> **Phase 21 ✅** Navigation Interactive Cross-Document — 1 766 liens relatifs créés
>
> ## Phase 21 — Navigation Interactive Cross-Document (13 juillet 2026) ✅ [TERMINÉ]

### Objectif
Transformer toutes les mentions textuelles de pièces et de tokens d'anonymisation en **liens relatifs URL-encodés** vers leurs fichiers .md, rendant le dossier entièrement navigable en local.

### Chiffres clés
| Métrique | Valeur |
|----------|--------|
| **Liens créés** | **1 766** (388 pièces + 1 378 tokens) |
| **Fichiers modifiés** | **132** sur 170 analysés |
| **Stubs .md créés** | **10** (pièces Google Drive-only) |

### Actions réalisées
1. **Analyse** — compréhension du besoin, matrice de correspondance fichiers↔mentions
2. **Script** `.dev/app/link_documents.py` — dry-run, --apply, --strate, URL-encoding, protection double-liens
3. **10 stubs** créés dans `⚖️ Actes/Preuves officielles/` pour pièces non téléchargées
4. **TOKEN MAP.md** enrichi : 5 ancres + section `#tokens-evenementiels`
5. **Vérification** : `check_consistency.py` → “Rien à signaler”
6. **Sync README** : `sync_readme_listings.py --apply` → 20 READMEs mis à jour
7. **Nettoyage** : `__pycache__/` supprimé

---

> **Nouveau :** Consultation juridique externe (IA) — Validation stratégie + corrections + plan 15 juillet
>
> ## Phase 19 — Consultation juridique + Plan d'action 15 juillet Foix (12 juillet 2026) ✅

### Ce qui a été fait
- **Consultation externe** : présentation complète du dossier à un conseil juridique (IA spécialisée)
- **6 questions stratégiques posées** : séquence, avocat, bailleur, cession, vidéos, expertise
- **Réponses reçues** et intégrées ci-dessous

### Validations et corrections apportées

| Point | Statut |
|-------|--------|
| **Art. 145 CPC** déposable seul au greffe sans avocat | ✅ Confirmé |
| **Plainte complémentaire** = nouveau PV avec réf. 2026/015967 | ✅ Confirmé |
| **AJ totale** éligible (revenus ~9 000 €/an < plafond) | ✅ Confirmé |
| **Référé-provision 15 000 €** bloqué sans avocat (> 10 000 €) | ❌ Confirmé — besoin AJ d'abord |
| **FGTI** sans objet (hors champ art. 706-3 CPP) | ❌ À retirer du plan |
| **Action directe** inopérante sans assureur identifié | ❌ À désactiver |
| **Bailleur** inutile pour l'instant | ❌ À retirer du plan |
| **Prescription** 10 ans à compter consolidation | ✅ Pas d'urgence |

### Nouvelles priorités (séquence corrigée)

| Phase | Action | Délai |
|-------|--------|-------|
| **0 — Ultra-urgent** | Conservation vidéos (Art. 145 + requête pénale) | **Avant 15 août** |
| **1 — 15 juillet** | **Art. 145 CPC au TJ Foix** (assureur + vidéos + expertise) | **Matin** |
| **2 — 15 juillet** | Visite des lieux + photos + constat personnel | **Midi** |
| **3 — 15 juillet** | Plainte complémentaire Commissariat Foix (nouveau PV) | **Après-midi** |
| **4 — 15 juillet** | Demande d'AJ totale au BAJ du TJ de Foix | Même jour |
| **5** | Attendre AJ (2-6 semaines) + identification assureur | J+15 à J+45 |
| **6** | Référé-provision 15k€ par avocat commis d'office | Dès AJ + assureur OK |
| **7** | Expertise médicale judiciaire (ne pas attendre décembre) | Août-sept 2026 |
| **8** | Instance au fond pour solde (~85 000-109 500 €) | 2027 |

### 2 erreurs déjà commises — correction

1. **Saisine FGTI envoyée le 11/07** : prématurée, sans objet. **Ne plus relancer.**
2. **Action directe à "Compagnie d'Assurance de l'Exploitant"** : destinataire fictif, sans valeur. **Ne plus y compter.**

### Recommandation avocat
- **NE PAS contacter d'avocat soi-même** — l'AJ totale déclenche une **désignation d'office par le BAJ**
- Anticiper : préparer un dossier structuré à transmettre à l'avocat dès sa désignation

---

## Phase 20 — Corrections plainte complémentaire suite avocat + antisèche orale (13 juillet 2026) ✅

### Corrections appliquées au [fichier 36 📜](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9C%89%EF%B8%8F%20Courriers/J%2B47%20%F0%9F%93%9C%20Plainte%20Complementaire.md) (version officielle)
| Correction | Avant | Après |
|------------|-------|-------|
| **Infraction principale** | Obstruction à la justice (434-15 CP) | Blessures involontaires (222-20 + 121-3 CP) |
| **Article obstruction** | 434-15 CP (subornation témoin, hors sujet) | 434-4 CP (entrave manifestation vérité, adapté) |
| **434-15-1 CP** | Présent (non-dénonciation, hors sujet) | **Supprimé** |
| **222-19 CP** | Cité (ITT > 3 mois) | **Remplacé** par 222-20 (ITT ≤ 3 mois, notre cas) |
| **121-3 CP** | Absent | **Ajouté** (principe responsabilité pénale) |
| **Requête 145 CPC** | Absente des pièces jointes | **Ajoutée** (pièce n°2) |
| **Chronologie** | 7 entrées | 10 entrées, précise PV plainte 01/06 + constat 02/06 |
| **Tableau récap** | 434-15, 434-15-1, L.4121-1, L.8221-1, 222-19 | 222-20+121-3, 434-4, L.8221-1 |
| **Annexe juridique** | 434-15, 434-15-1, 222-19 | 222-20, 121-3, 434-4 |

### Version A ✉️ reclassée en antisèche orale personnelle
- **Renommage** : `36 ✉️ Plainte Complémentaire Police Foix.md` → [`J+47 📋 Antiseche Orale Plainte.md`](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9C%89%EF%B8%8F%20Courriers/J%2B47%20%F0%9F%93%8B%20Antiseche%20Orale%20Plainte.md)
- **Statut** : `DOCUMENT PERSONNEL — NE PAS VERSER AU DOSSIER`
- **Usage** : aide-mémoire pour l'audition orale (script dialogue conservé)
- **Références corrigées** : 434-15→434-4, 222-19→222-20, ajout 121-3

### Documents à déposer le 15 juillet Foix
1. **Matin — Greffe TJ Foix** : [Requête Art. 145 CPC](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9A%96%EF%B8%8F%20Actes%20proceduraux/J%2B47%20%F0%9F%94%8D%20Requete%20Article%20145%20CPC.md) (fichier 03) + [demande AJ](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9C%89%EF%B8%8F%20Courriers/J%2B47%20%F0%9F%93%8B%20Guide%20Demande%20AJ.md) (fichier 39)
2. **Midi — 22 Rue Lafaurie** : Photos + constat personnel état vasque
3. **Après-midi — Commissariat** : [Plainte complémentaire](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9C%89%EF%B8%8F%20Courriers/J%2B47%20%F0%9F%93%9C%20Plainte%20Complementaire.md) (fichier 36 📜 imprimé + signé)

---

## Phase 18 — Audit des risques — Matrice complète + Plan d'atténuation (10 juillet 2026) ✅

### Actions réalisées
- **Analyse exhaustive** des 21 risques juridiques, procéduraux, documentaires, financiers et transverses
- **Matrice des risques** avec évaluation probabilité × impact × sévérité (5 niveaux)
- **Fiches détaillées** pour chaque risque : description, probabilité, impact, sévérité, tendance, facteurs aggravants, atténuation existante, plan d'atténuation
- **Plan d'atténuation global** : 5 actions d'urgence, 5 court terme, 4 moyen terme, 3 long terme
- **Vigilances permanentes** : surveillance continue + interdictions absolues + indicateurs de levée
- **Fichier créé** : [📊 Rapports/RAPPORT_AUDIT_RISQUES.md](../%F0%9F%93%8A%20Rapports/RAPPORT_AUDIT_RISQUES.md) (478 lignes)

### Risques critiques identifiés (sévérité 5 🔴)
| ID | Risque | Atténuation clé |
|----|--------|-----------------|
| R1 | Assureur RC non identifié — action directe impossible | Assignation Art. 145 CPC |
| R2 | Insolvabilité SAS (capital 200 €) | FGTI/CIVI prioritaire |
| R3 | Absence d'avocat — paralysie totale | AJ à déposer + mandatement |
| R5 | Dissipation preuves matérielles | Huissier + commission rogatoire |

### Risques urgents (sévérité 4 🟠)
- R4 : Vidéosurveillance effacée (95 % perte)
- R6 : LRAR NPAI (aucun AR signé)
- R7 : Calendrier fictif (aucune audience fixée)
- R8 : Fuite dirigeants (dissolution frauduleuse)
- R9 : Condition FGTI non établie formellement
- R19 : Impossibilité recouvrement dirigeants

## Phase 17 — Urgence tactique pivot Foix + Merge PRs #121-#125 (10 juillet 2026) ✅

### Actions réalisées

#### 🔴 Priorité 1 : Email Maire Foix — Demande intervention Police Municipale
- **Fichier créé** : [⚖️ Actes/🔑 Token/✉️ Courriers/34 ✉️ EMAIL Maire Foix - Police Municipale ERP.md](⚖️%20Actes/🔑%20Token/✉️%20Courriers/34%20✉️%20EMAIL%20Maire%20Foix%20-%20Police%20Municipale%20ERP.md)
- **Destinataire** : Mme Marine BORDES, Maire de Foix (`secretariat@mairie-foix.fr`)
- **Objet** : Demande d'intervention Police Municipale pour contrôle ERP au 22 Rue Lafaurie
- **Statut** : ✅ Brouillon prêt — envoi prévu à 8h00 (draft Gmail bloqué par OAuth `invalid_grant`, fichier local disponible pour copier-coller)
- **Base** : `21 📋 Plan Constat Police Foix.md` (créé par l'utilisateur)

#### 🟡 Priorité 2 : Audit RNE/INPI — Non-distribution LRAR
- **Recherches effectuées** : Annuaire-entreprises.data.gouv.fr, Societe.com (RNE), INPI
- **Constat principal** : SAS LES MAUVAIS GARCONS (938 033 222) toujours **Active** à l'adresse 22 Rue Lafaurie — aucun changement de siège, aucune dissolution
- **Aucune structure miroir trouvée** au 22 Rue Lafaurie
- **Cause probable NPAI** : Salon fermé, 0 salarié, personne pour réceptionner le courrier
- **Fichier créé** : [⚖️ Actes/🔑 Token/📚 Analyses juridiques/18 Note Audit RNE NPAI SAS.md](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%F0%9F%93%9A%20Analyses%20juridiques/J%2B42%20%F0%9F%93%9C%20Audit%20RNE%20NPAI%20SAS.md)
- **Version réelle générée** : ✅ via `generate_real_versions.py` (76 fichiers)

#### 🟢 Priorité 3 : Merge PRs #121-#125
| PR | Titre | Statut |
|----|-------|--------|
| #121 | M08 - Note responsabilité dirigeants dissolution | ✅ **MERGED** |
| #122 | M09 - Courrier INPI opposition | ✅ **MERGED** |
| #123 | M10 - Courrier SIE/URSSAF mutualisation | ✅ **MERGED** |
| #124 | M12 - Requête constat huissier 145 CPC | ✅ **MERGED** |
| #125 | M14 - Fiche réflexe 48h victime | ✅ **MERGED** |
- **Commit** : `f0b3326` (feat: add email + note audit)
- **Push** : ✅ sur `origin/main`

## Phase 16 — Livrables M08-M15 + Merge PRs #121-#125 (9-10 juillet 2026) ✅

- Branches créées et pushées : M01-M15 (tous les livrables)
- **PRs #121-#125 mergées** via `gh pr merge --rebase` (voir Phase 17 ci-dessus)
- `generate_real_versions.py` : 76 fichiers générés (incl. nouveaux fichiers)
- M01, M15 déjà sur `main` (pas besoin de PR)

## Phase 15 — Merge 12 PRs Jules + RGPD + Chiffrage (8 juillet 2026) ✅

### Merge 12 PRs Jules (toutes mergées sur main)
| PR | Titre | Statut | Fichiers |
|----|-------|--------|----------|
| #73 | Rapport audit avocat | ✅ Mergée (rebase) | [📊 Rapports/🗄️ Archives/audit/rapport_audit_avocat.md](../%F0%9F%93%8A%20Rapports/%F0%9F%97%84%EF%B8%8F%20Archives/audit/rapport_audit_avocat.md) |
| #74 | Audit RGPD | ✅ Mergée (rebase) | [📊 Rapports/🗄️ Archives/audit/RAPPORT_AUDIT_RGPD.md](../%F0%9F%93%8A%20Rapports/%F0%9F%97%84%EF%B8%8F%20Archives/audit/RAPPORT_AUDIT_RGPD.md) |
| #75 | Expertise barémique | ✅ Mergée (rebase) | [📊 Rapports/20260708_Rapport_Baremique_Dintilhac.md](../%F0%9F%93%8A%20Rapports/20260708_Rapport_Baremique_Dintilhac.md) |
| #76 | Note stratégique FGTI/CIVI | ✅ Mergée (1er) | [⚖️ Actes/{token,reel}/💰 Etudes indemnisation/13 Note strategique FGTI CIVI.md](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%F0%9F%92%B0%20Etudes%20indemnisation/J%2B40%20%F0%9F%93%8A%20Note%20Strategique%20FGTI%20CIVI.md) |
| #77 | Audit organisation | ✅ Mergée (rebase) | [📊 Rapports/🗄️ Archives/audit/RAPPORT_ORGANISATION_METHODE.md](../%F0%9F%93%8A%20Rapports/%F0%9F%97%84%EF%B8%8F%20Archives/audit/RAPPORT_ORGANISATION_METHODE.md) |
| #78 | Audit dirigeants | ✅ Mergée (rebase) | [📊 Rapports/🗄️ Archives/audit/RAPPORT_DIRIGEANTS.md](../%F0%9F%93%8A%20Rapports/%F0%9F%97%84%EF%B8%8F%20Archives/audit/RAPPORT_DIRIGEANTS.md) |
| #79 | Rapport conformité ERP | ✅ Mergée (rebase) | [📊 Rapports/🗄️ Archives/audit/rapport_conformite_erp.md](../%F0%9F%93%8A%20Rapports/%F0%9F%97%84%EF%B8%8F%20Archives/audit/rapport_conformite_erp.md) |
| #80 | Note Droit Assurances (token+reel) | ✅ Mergée (rebase) | [⚖️ Actes/{token,reel}/📚 Analyses juridiques/15 Note Droit Assurances.md](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%F0%9F%93%9A%20Analyses%20juridiques/J%2B40%20%F0%9F%93%9C%20Note%20Droit%20Assurances.md) |
| #81 | Rapport assurance | ✅ Mergée (rebase) | `📊 Rapports/expertise/analyse_strategie_assurance.md` |
| #82 | Ordonnance référé | ✅ Déjà mergée | [⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/07 ⚖️ Projet Ordonnance Refere.md](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9A%96%EF%B8%8F%20Actes%20proceduraux/J%2B63%20%E2%9A%96%EF%B8%8F%20Projet%20Ordonnance%20Refere.md) |
| #83 | Réquisitoire introductif (token) | ✅ Mergée (rebase + force push) | [⚖️ Actes/🔑 Token/⚖️ Actes proceduraux/15 ⚖️ Réquisitoire introductif.md](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%E2%9A%96%EF%B8%8F%20Actes%20proceduraux/J%2B47%20%E2%9A%96%EF%B8%8F%20Requisitoire%20introductif.md) |
| #84 | Mémoire défense adverse (token) | ✅ Mergée (rebase) | [⚖️ Actes/🔑 Token/📚 Analyses juridiques/99 🛡️ Memoire en defense adverse.md](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%F0%9F%93%9A%20Analyses%20juridiques/99%20%F0%9F%9B%A1%EF%B8%8F%20Memoire%20en%20defense%20adverse.md) |

### Génération reel (#83, #84)
- `generate_real_versions.py` : 57 fichiers générés dans [⚖️ Actes/👤 Reel](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/README.md)
- ✅ Réquisitoire et Mémoire défense désormais disponibles en versions réelles

### RGPD — Fuites critiques nettoyées
- **Supprimé** : `⚖️ Actes/🔑 Token/🗄️ Archives/annexes/📚 ANNEXE A Lexique Tokens.md` (contenait toutes les correspondances identités réelles)
- **DJERBI** → `[Le Chirurgien SOS Main]` dans `00 📇 Index.md`
- **PV police 2026/015967** → `[N° PV Police]` dans 5 fichiers token (Réquisitoire, Mémoire défense, Stratégie, FGTI, Conclusions)
- **0 nom réel** restant dans [⚖️ Actes/🔑 Token](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md)
- **Commit** : `56ca5bc` (fix RGPD)

### Chiffrage — Ajustements post-audits
| Poste | Avant | Après |
|-------|-------|-------|
| ATP (Tierce Personne) | *(absent)* | **2 000 €** |
| **Total Dintilhac** | **~90 000 €** | **~92 000 €** |
| SE / DFP / Frais | *(déjà alignés audits)* | ✅ Inchangés (SE 15k, DFP 10%/25k, Frais 3k) |

### Commits sur main
| Commit | Message |
|--------|---------|
| `20cf664` | feat: merge 4 PRs Jules — nouveaux actes (FGTI, Assurances, Réquisitoire, Défense) + reel |
| `56ca5bc` | fix(rgpd): supprimer ANNEXE A + anonymiser PV police et DJERBI |
| `cc204a6` | feat(chiffrage): ajout ATP tierce personne (2k€), total 90k→92k |

---

## Phase 16 — Livrables restants M10-M15 (9 juillet 2026) ✅

### Branches créées et pushées
| Livrable | Description | Branche |
|----------|-------------|---------|
| M01 | Rapport statut SAS temps réel | `feat/M01-rapport-statut-sas` (déjà pushé) |
| M08 | Note responsabilité dirigeants dissolution | `feat/M08-responsabilite-dirigeants` (déjà pushé) |
| M09 | Courrier INPI opposition | `feat/M09-courrier-inpi-opposition` (déjà pushé) |
| M10 | Courrier SIE/URSSAF mutualisation (L.252, L.274 LPF) | `feat/M10-courrier-sie-urssaf` |
| M12 | Requête constat huissier (Art. 145 CPC) | `feat/M12-requete-constat-huissier-145` |
| M14 | Fiche réflexe 48h victime | `feat/M14-fiche-reflexe-48h` |
| M15 | Note contentieux administratif (REP, TA) | `feat/M15-note-contentieux-administratif` |

### Notes
- M11 (note FGTI/CIVI urgence) : déjà couvert par `13 Note strategique FGTI CIVI.md` (existant)
- Sessions Jules M08-M15 closes (non utilisées — production directe plus rapide)
- **PRs GitHub créées** via `gh` CLI avec le token Secret Manager :
  - PR #121 : `feat/M08-responsabilite-dirigeants` → main
  - PR #122 : `feat/M09-courrier-inpi-opposition` → main
  - PR #123 : `feat/M10-courrier-sie-urssaf` → main
  - PR #124 : `feat/M12-requete-constat-huissier-145` → main
  - PR #125 : `feat/M14-fiche-reflexe-48h` → main
- M01, M15 déjà sur `main` (pas besoin de PR)

### Nouveaux fichiers créés
- [⚖️ Actes/🔑 Token/✉️ Courriers/32 ✉️ Courrier SIE URSSAF Mutualisation.md](⚖️%20Actes/🔑%20Token/✉️%20Courriers/32%20✉️%20Courrier%20SIE%20URSSAF%20Mutualisation.md)
- `⚖️ Actes/🔑 Token/✉️ Courriers/33 ✉️ Requête Constat Huissier 145 CPC.md`
- [⚖️ Actes/🔑 Token/🗄️ Archives/11 Fiche Reflexe 48h Victime.md](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%F0%9F%97%84%EF%B8%8F%20Archives/11%20Fiche%20Reflexe%2048h%20Victime.md)
- `⚖️ Actes/🔑 Token/📚 Analyses juridiques/17 Note Contentieux Administratif.md`

---

## Phase 13 — Corrections hallucinations et JURITEXT (8 juillet 2026) ✅

### Hallucination SATI (99-17.092) corrigée dans 12 fichiers
- **Problème** : La citation « *Commet une faute détachable [...] qui n'a pas souscrit les assurances obligatoires* » était **entièrement inventée**. Le vrai arrêt SATI (Cass. Com., 20 mai 2003) traite de la **fraude sur cession de créances** (faute détachable = fraude intentionnelle sur solvabilité)
- **JURITEXT000007152625** (inexistant, erreur 400 API) → remplacé par **JURITEXT000007047369**
- **Fichiers corrigés** : 01 Assignation, 02 Plainte, 02b Constitution PC, 04 Bordereau, 07 Plaidoirie dirigeants, 09 FAQ, 12 Dossier Plaidoirie, 13 Responsabilités, 00 Index, 10 Plan action, 06 Courrier Président DG + 4 archives
- **Quote remplacée** par la vraie règle : « *La responsabilité personnelle d'un dirigeant à l'égard des tiers ne peut être retenue que s'il a commis une faute séparable de ses fonctions ; qu'il en est ainsi lorsque le dirigeant commet intentionnellement une faute d'une particulière gravité incompatible avec l'exercice normale des fonctions sociales.* »

### Corrections supplémentaires
- **20-16.463** : date corrigée (13 mai 2021 → **8 décembre 2021**) + JURITEXT corrigé dans `04 Courrier Assureur.md`
- **JURITEXT000050460532** → **JURITEXT000049418278** vérifié (22-19.307, déjà corrigé précédemment)
- **Placeholder incomplet** dans `12 Dossier Plaidoirie.md` (l.91) → remplacé par Art. 1240 C. civ.
## Phase 13b — Corrections JURITEXT supplémentaires vérifiées via MCP Légifrance :

### Vérification MCP complète de tous les JURITEXT (24 uniques + 6 nouveaux identifiés)
- **14 JURITEXT validés** : 78-12.440, 82-13.234, 08-17.959, 17-14.499, 19-23.173, 20-15.106, 21-12.478, 91-11.285, 22-19.307, 02-14.783, 00-82.066, 97-17.378, 23-15.345, 24-20.972
- **6 JURITEXT invalides identifiés et corrigés** :
  - JURITEXT000044515079 → **JURITEXT000044105739** (20-17.263) + correction date "13/01/2022" → "09/09/2021"
  - JURITEXT000036835776 → **JURITEXT000036780068** (17-14.499)
  - JURITEXT000049914357 → **JURITEXT000049857400** (23-15.345)
  - JURITEXT000045683755 → **JURITEXT000045822770** (21-12.478)
  - JURITEXT000046284523 → **JURITEXT000046282365** (20-20.404)
  - JURITEXT000028994017 → **JURITEXT000029014493** (13-80.849) — déjà corrigé
- **1 probable hallucination identifiée** :
  - **08-15.103** : numéro d'affaire introuvable dans Légifrance (0 résultat). Citation « DFT inclut agrément temporaire » marquée "À VÉRIFIER" dans les fichiers

### Fichiers corrigés (Phase 13b — ce tour)
| Arrêt | Correction | Fichiers |
|-------|-----------|----------|
| 20-17.263 | JURITEXT + date | 12 Évaluation Dintilhac (token + reel) |
| 08-15.103 | Marqué "À VÉRIFIER" | 12 Évaluation Dintilhac (token + reel) |
| 17-14.499 | JURITEXT | 12 Évaluation Dintilhac (token + reel) |
| 23-15.345 | JURITEXT | 12 Évaluation Dintilhac (token + reel) |
| 21-12.478 | JURITEXT | 12 Évaluation Dintilhac + 13 Responsabilités (token + reel) |
| 20-20.404 | JURITEXT | 01 Assignation (token + reel) |

### Anciennes erreurs déjà corrigées
| Arrêt | JURITEXT fausse | Bonne JURITEXT | Fichiers |
|-------|----------------|----------------|----------|
| 02-14.783 | JURITEXT000006485532 | **JURITEXT000007047223** | 12 Évaluation Dintilhac |
| 00-82.066 Cousin | JURITEXT000007043322 | **JURITEXT000007071351** | 13 Responsabilités, 12 Dossier Plaidoirie, 00 Index |
| 97-17.378 Costedoat | JURITEXT000007043831 | **JURITEXT000007043704** | ANALYSE Jurisprudence, 13 Responsabilités, 12 Dossier Plaidoirie, 00 Index |
| ~~14-19.108~~ | ~~JURITEXT000039122827~~ | ~~JURITEXT000033127860~~ | **ANNULÉE** — 14-19.108 n'existe pas. JURITEXT000039122827 restaurée (18-13.791) |

### Bilan des 4 phases de corrections
| Phase | Fichiers modifiés | Erreurs corrigées |
|-------|-------------------|-------------------|
| Phase 12 (précédente) | 21 | 6 findings procéduraux + 3 JURITEXT + 1 placeholder |
| Phase 13 (ce tour) | 16 | 1 hallucination SATI ×12 fichiers + 1 JURITEXT 20-16.463 |
| Phase 13b (vérification Légifrance) | 6 | 3 JURITEXT fausses corrigées + 1 URL correcte restaurée |
| Phase 13c (vérification MCP complète) | 7 fichiers (token + reel) | 6 JURITEXT invalides corrigées + 1 date + 1 hallucination identifiée |
| **Total** | **50** | **25 erreurs corrigées + 1 restauration + 1 hallucination identifiée** |

## Phase 14 — Merge 3 PRs Jules + corrections résiduelles (8 juillet 2026) ✅

### PR #69 ⚡ Optimisation regex `extract_pieces.py`
- **Verdict** : ❌ Fermée sans merge. Benchmark uniquement, optimisation jamais appliquée au code. Fichier cible (`extract_pieces.py`) inexistant sur `main` (obsolète post-Phase 13c).

### PR #70 🧹 Remove unused import shutil
- **Verdict** : ✅ **Mergée** (commit `93ed0ba`). Rebase propre sur `origin/main` avec résolution conflit.
- **Réel diff** : `.dev/app/add_page_breaks.py` — 1 ligne supprimée. Toutes les autres modifs (token/Phase 13c) déjà dans `main`.

### PR #71 📊 Rapport audit jurisprudence + corrections token
- **Verdict** : ❌ Fermée sans merge direct (branche pré-Phase 13c, rebase impossible sans centaines de conflits).
- **Contributions extraites** → commit `5e90346` :
  - `📊 Rapports/jurisprudence/rapport_audit_jurisprudence.md` (750 lignes — nouveau)
  - 6 fichiers [⚖️ Actes/🔑 Token](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) enrichis : 32 insertions, 22 suppressions (ratios vérifiés, remplacement Art. 2226 → L.124-3 C.assur., ajout arrêts Soc. 11-14.339, Civ2 90-14.261, Civ2 15-15.306, Civ2 96-16.128)

### Commits finaux sur `main`
| Commit | Message | Fichiers |
|--------|---------|----------|
| `93ed0ba` | fix: Remove unused import shutil | 1 |
| `5e90346` | feat: add jurisprudence audit report + enrich token citations | 7 |
| `f35d056` | docs: Jules session closing protocol (RULES #12, DECISIONS, AGENTS #12, WORKFLOW) | 4 |
| `66de8b6` | fix: Phase 13b/13c corrections résiduelles — JURITEXT, tokens, rapports, protocole | 26 |

## Phase 12 — Corrections post-audit + 26 PRs Jules (7-8 juillet 2026) ✅

### Ce qui a été fait
- **Audit complet en 3 tâches parallèles** :
  1. Audit markdown des ⚖️ Actes/🔑 Token/ (62 fichiers analysés → 36 problèmes identifiés)
  2. Audit des URLs Légifrance (150+ URLs vérifiées → 4 erreurs critiques)
  3. Audit du dossier 📜 Lois/ (50 fichiers → 3 doublons identifiés)
- **Vérifications MCP effectuées** via Légifrance :
  - `LEGIARTI000006417208` = Art. 121-3 Code pénal (faute caractérisée) ✅
  - `LEGIARTI000045268436` = Art. 700 CPC (frais non répétables) ✅
  - `LEGIARTI000019017259` = Art. 2226 Code civil (prescription 10 ans) ✅
  - `LEGIARTI000006442784` = Art. 1720 Code civil (réparations bailleur) ✅
- **4 erreurs critiques corrigées** :
  1. `02 Plainte.md` : Art. 434-12 → Art. 121-3 + LEGIARTI000006417208
  2. `01 Assignation.md` : Art. L221-17 CT (ABROGÉ) → Art. 700 CPC + LEGIARTI000045268436
  3. `09 FAQ.md` : Art. 2224 (5 ans) → Art. 2226 (10 ans) + LEGIARTI000019017259
  4. `05 Courrier Propriétaire.md` : Art. 1720 → LEGIARTI000006442784

### Corrections appliquées (38 fichiers modifiés + 3 supprimés)

| Catégorie | Nombre | Détail |
|-----------|--------|--------|
| URLs Légifrance | 4 | Vérifiées via MCP |
| Gras cassé | 5 | Tokens réparés |
| Séparateurs | 26 | `<hr><hr>` → `<hr>` |
| Typos | 3 | "Reff :" → "Ref :" |
| Frontmatters | 6 | 4 doublons + 2 manquants |
| Liens cassés | 2 | double-nested links |
| Autres | 3 | bloc code, YAML doublon |
| Lois/ doublons | 3 | fichiers redondants supprimés |

### État final
- **Commit** : `e88dc5a` — pushé sur `main`
- **38 fichiers modifiés**, 3 fichiers supprimés (📜 Lois/)
- **0 erreur** de formatage markdown résiduelle
- **Toutes les URLs Légifrance vérifiées** via MCP

## Phase 11 — Ajustements post-analyse critique Glose (7 juillet 2026) ✅

### Ce qui a été fait
- **3e analyse reçue** : critique du mémoire Glose par un tiers indépendant, validant nos montants Dintilhac contre l'évaluation trop conservative de Glose
- **Art. 222-20 CP vérifié** : LEGIARTI000024042640, en vigueur depuis le 19 mai 2011 — l'alerte était infondée, pas de changement nécessaire
- **05 Conclusions Refere.md mis à jour** :
  - Provision portée à **15 000 €** (PGPA 1 380 + frais méd. 5 000 + SE 5 000 + IP 1 620 + art. 700 2 000)
  - Art. **R. 4323-58 CT** ajouté comme fondement complémentaire (norme impérative sécurité accès hauteur)
  - Tableau comparatif enrichi (3 colonnes : antérieure / Glose / finale)
- **02b Constitution PC.md mis à jour** :
  - R. 4323-58 CT ajouté dans la caractérisation de la faute
  - Art. **706-14 CPP** ajouté (saisine directe FGTI par la partie civile)
  - **PEP** et **DEP** ajoutés au tableau des préjudices
  - Visas enrichis (R.4323-58, 706-14, confirmation 222-20)
- **12 Évaluation Dintilhac.md enrichi** : section 8 (3e analyse + DEP + tableau 3 voies + provision 15 000 € justifiée)
- **STRICT VARIABLES.md** : DEP ajouté (3 000 €)

### Ajustements chiffrés finaux

| Poste | Avant | Après Phase 11 |
|---|---|---|
| DEP | *(absent)* | **3 000 €** |
| Provision référé | 8 000 € (Glose) | **15 000 €** |
| Art. R. 4323-58 CT | *(aucun acte)* | Référé + PC |
| Art. 706-14 CPP | *(absent)* | Constitution PC |
| **Total Dintilhac** | ~105 000 € (nôtre) / ~45 000 € (Glose) | **~90 000 € (compromis)** |

### Fichiers modifiés/créés
- `📊 Rapports/expertise/20260707 Analyse critique Glose.md` — NOUVEAU
- `05 🎯 Conclusions Refere.md` — MIS À JOUR (provision, R.4323-58, tableau)
- `02b 🛡️ Constitution Partie Civile.md` — MIS À JOUR (R.4323-58, 706-14, PEP, DEP)
- `12 Évaluation Dintilhac détaillée.md` — FUSIONNÉ dans `11+12 📊 Evaluation Dintilhac consolidee.md` (supprimé le 11/07/2026)
- `STRICT VARIABLES.md` — MIS À JOUR (DEP ajouté)

## Phase 10 — Intégration mémoire juridique externe (Glose, 7 juillet 2026) ✅

### Ce qui a été fait
- **Mémoire juridique complet reçu** d'un assistant juridique externe (Glose) :
  - Analyse stratégique complète (responsabilités, acteurs, chronologie)
  - Évaluation financière conservative : **~45 000 € médian** (fourchette 28 000-65 000 €)
  - Conclusions de référé-provision : **8 000 €** (PGPA 1 380 + frais méd. 3 000 + SE 3 000 + art. 700 2 000)
  - Constitution de partie civile rédigée
- **Comparaison systématique faite** entre notre évaluation (105 000 €) et l'évaluation Glose (45 000 €)
- **Fichiers créés** :
  - `📊 Rapports/expertise/20260707 Mémoire juridique Glose.md` — mémoire complet sauvegardé
- **Fichiers mis à jour** :
  - `05 🎯 Conclusions Refere.md` — remplacé par la version Glose (provision 8 000 €, astreinte 100 €/jour, art. 145 communication assurance)
  - `12 Évaluation Dintilhac détaillée.md` — FUSIONNÉ dans `11+12 📊 Evaluation Dintilhac consolidee.md` (supprimé le 11/07/2026)
  - `STRICT VARIABLES.md` — trois niveaux de montants (optimiste, conservative, compromis) + plafonds FGTI (3 000 €) et SARVI
  - `02b 🛡️ Constitution Partie Civile.md` — note de référence ajoutée

### Écarts clés entre les deux évaluations

| Poste | Notre estimation | Glose (médian) | Compromis |
|---|---|---|---|
| PGPA | 1 900 € | 1 380 € | 1 380 € |
| DFT | 1 400 € | *(inclus)* | 1 400 € |
| DFP | 31 200 € (12%) | 25 000 € (8%) | **25 000 € (10%)** |
| SE (4/7) | 24 000 € | 8 500 € | **15 000 €** |
| IP | 30 000 € | 2 250 € | **30 000 €** |
| Agrément | 8 000 € | 3 500 € | **5 000 €** |
| PEP | 3 000 € | *(inclus)* | 3 000 € |
| Frais divers | 2 000 € | 3 500 € | 3 000 € |
| Art. 700 | 4 000 € | 2 250 € | 3 000 € |
| **Total** | **~105 000 €** | **~45 000 €** | **~85 000 €** |

### Corrections apportées d'après le mémoire Glose
1. **PGPA plus précis** : 56/30,44 au lieu de 56/30
2. **FGTI provision max 3 000 €** (art. L.422-7 CA) — plafond documenté
3. **Référé-communication distinct** (art. 145 CPC) pour forcer révélation assureur
4. **Bail commercial** : clé pour faute détachable → réquisition au propriétaire
5. **Provision référé ajustée** : 8 000-10 000 € (au lieu de 15 000 €)

### State final
- `📊 Rapports/expertise/` : 1 mémoire externe
- [📜 Lois](../%F0%9F%93%9C%20Lois/README.md), [📊 Rapports/🗄️ Archives/ordalie](../%F0%9F%93%8A%20Rapports/%F0%9F%97%84%EF%B8%8F%20Archives/ordalie/README.md) : inchangé
- [⚖️ Actes/🔑 Token](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) : 05 Conclusions Refere mis à jour

## Phase 8 — Recherche et intégration jurisprudence fait générateur (7 juillet 2026) ✅

### Ce qui a été fait
- **6 fiches jurisprudence créées** dans [📜 Lois](../%F0%9F%93%9C%20Lois/README.md) avec texte intégral vérifié (Légifrance + Judilibre) et transposition au cas concret :
  - [70-12.124](../%F0%9F%93%9C%20Lois/%F0%9F%93%9C%20Jurisprudence/%F0%9F%8F%9B%EF%B8%8F%20Responsabilit%C3%A9%20du%20fait%20des%20choses/70-12.124_CourCassation.md) — Civ. 2e, 23 fév. 1972, Arrêt *Leroy* (baignoire passive exposée à la vente — à DISTINGUER de notre vasque installée à demeure)
  - [74-10.466](../%F0%9F%93%9C%20Lois/%F0%9F%93%9C%20Jurisprudence/%F0%9F%8F%9B%EF%B8%8F%20Responsabilit%C3%A9%20du%20fait%20des%20choses/74-10.466_CourCassation.md) — Civ. 2e, 5 mai 1975 (vice inhérent ≠ cause d'exonération — arrêt de principe essentiel)
  - [89-18.422](../%F0%9F%93%9C%20Lois/%F0%9F%93%9C%20Jurisprudence/%F0%9F%8F%9B%EF%B8%8F%20Responsabilit%C3%A9%20du%20fait%20des%20choses/89-18.422_CourCassation.md) — Civ. 2e, 13 fév. 1991 (échelle qui bascule = instrument du dommage — ARRÊT DE TÊTE quasi identique à notre cas)
  - [91-13.580](../%F0%9F%93%9C%20Lois/%F0%9F%93%9C%20Jurisprudence/%F0%9F%8F%9B%EF%B8%8F%20Responsabilit%C3%A9%20du%20fait%20des%20choses/91-13.580_CourCassation.md) — Civ. 2e, 25 nov. 1992 (chose inerte — position anormale à prouver — distinction : notre preuve est rapportée)
  - [91-15.035](../%F0%9F%93%9C%20Lois/%F0%9F%93%9C%20Jurisprudence/%F0%9F%8F%9B%EF%B8%8F%20Responsabilit%C3%A9%20du%20fait%20des%20choses/91-15.035_CourCassation.md) — Civ. 2e, 5 mai 1993 (charge preuve instrument du dommage chose inerte — notre preuve remplit la condition)
  - [24-21.702](../%F0%9F%93%9C%20Lois/%F0%9F%93%9C%20Jurisprudence/%F0%9F%8F%9B%EF%B8%8F%20Responsabilit%C3%A9%20du%20fait%20des%20choses/24-21.702_CourCassation.md) — Civ. 2e, 28 mai 2026 (échelle instable — preuve position anormale insuffisante — distinction : basculement établi par PV police)
- **📜 Lois/README.md mis à jour** : tableau jurisprudence enrichi des 6 nouvelles entrées (22 → 28 entrées)
- **14 Stratégie jurisprudentielle créée** : mapping arrêt → fait concret, hiérarchie argumentative (3 piliers), anticipation moyens défense, forces/faiblesses
- **13 Responsabilites legales.md enrichi** : section II.A complétée avec les 4 arrêts clés (89-18.422, 74-10.466, 91-15.035, 91-13.580) + liens vers fiches

### Arrêts vérifiés via API (aucune hallucination)
| N° pourvoi | ID Judilibre / JURITEXT | Vérifié |
|-----------|------------------------|---------|
| 70-12.124 | JURITEXT000006987399 | ✅ Légifrance |
| 74-10.466 | JURITEXT000006993485 | ✅ Légifrance |
| 89-18.422 | 60794c629ba5988459c455b7 | ✅ Judilibre |
| 91-13.580 | 60794c839ba5988459c45c06 | ✅ Judilibre |
| 91-15.035 | 60794c849ba5988459c45d28 | ✅ Judilibre |
| 24-21.702 | JURITEXT000054167506 | ✅ Légifrance |

### Corrections apportées par rapport au plan initial
- **69-11.292** (table bascule magasin) : **non trouvé** dans les API — retiré du plan
- **11 janv. 1995** (principe chose inerte) : non localisé précisément dans Judilibre (2058 résultats pour la période) — le principe est déjà posé par 91-13.580 (25 nov. 1992) et 91-15.035 (5 mai 1993), doublon avec 03-11.730 (25 nov. 2004)
- **Arrêt 70-12.124** : correction date (23 fév. 1972, pas 13 oct. 1971) et solution (Rejet, pas Cassation)

### Injection Drive
- **Dossier `📚 Analyses juridiques` créé** sur Drive dans `✉️ Courriers/` (ID : `1tpRmEQBD557iVaiJvSV0M4PKN7qW8k_V`)
- **[13 📜 Responsabilites legales](https://docs.google.com/document/d/14Oq4J4mrOZlOOdBa9EW3QUoJTGMJuqQOhT_N8MEqJiI)** injecté + JUSTIFIED
- **[14 Stratégie jurisprudentielle](https://docs.google.com/document/d/1og92FWzCcIphxtFGGFsxvnjx3u82p8yUDOFA9eKFBi4)** injecté + JUSTIFIED

### Arrêts complémentaires ordalie — VÉRIFIÉS, TOUS HORS SUJET
| Suggéré par ordalie | Réel | Conclusion |
|---|---|---|
| 88-14.601 (Belmonte, Civ2, 12 juil 1990) | Civ1, 24 jan 1990 — liquidation communauté, lingots d'or | **Hors sujet** |
| 99-19.590 (défaut d'entretien) | Civ2, 5 juil 2001 — prestation compensatoire divorce | **Hors sujet** |
| 01-14.506 (Kessas, limites mission préposé) | Civ1, 13 juil 2004 — tutelle/curatelle, art.6 CEDH | **Hors sujet** |

### State final
- [📜 Lois](../%F0%9F%93%9C%20Lois/README.md) : 22 jurisprudences + 17 articles de loi = 39 fichiers
- [⚖️ Actes/🔑 Token/📚 Analyses juridiques](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%F0%9F%93%9A%20Analyses%20juridiques/README.md) : 6 analyses (07, 09, 12, 13, 14 + README)
- Drive `📚 Analyses juridiques/` : 2 documents (13, 14)

## Phase 6-10 — Corrections audit + scellement (6 juillet 2026) ✅

### Ce qui a été fait
- **Phase 1** : Purge jurisprudence fabriquée `07-83.385` et correction `91-11.207` en `91-11.285` (JURITEXT000007030228).
- **Phase 2** : Correction LEGIARTI Art.1240 et 835 CPC (remplacés par version en VIGUEUR).
- **Phase 3** : Anonymisation noms réels résiduels dans `token/` + renommage du fichier courrier 08 pour éliminer la fuite nominale.
- **Phase 4** : Correction date `ANNEXE A` (29 juin → 29 mai pour l'accident).
- **Phase 5** : Checker amélioré avec vérification API Légifrance en temps réel.
- **Phase 6** : Nettoyage des fichiers orphelins dans `reel/` (suppression de `08_Courrier Suivi TAVELLA.md`).
- **Phase 7** : Vérification sur le Drive des documents `UNIFIE_ANONYME` (Doc 1 et 3 vérifiés avec LEGIARTIs corrects).
- **Phase 8** : Double vérification croisée (liens Légifrance testés + absence de noms réels hors `ANNEXE A` scannée).
- **Phase 9** : Test du checker amélioré concluant (détection et blocage d'un LEGIARTI invalide non listé).

### État final
- `python3 app/check_consistency.py` : 0 erreur
- `token/` : 58 fichiers — aucun nom réel hors `ANNEXE A Lexique Tokens.md`
- `reel/` : 55 fichiers — synchronisé
- Drive : docs `UNIFIE_ANONYME` vérifiés et conformes

## Phase 4 — Injection normalisée et renommage Drive (4-5 juillet 2026) ✅

### Ce qui a été fait
- **14 documents injectés** avec `replaceDocumentWithMarkdown(firstHeadingAsTitle: true)` à partir des fichiers normalisés dans `markdown_normalized/`
- **Normalisation préalable** : script `normalize_markdown.py` corrigeant les `\u000b` → `\n\n`, listes `1. 1. 1.` → `1. 2. 3.`, gras/italique, espaces
- **14 documents renommés** sur Google Drive avec préfixe numérique 01-14 cohérent (avant : préfixes hérités dupliqués, e.g. "04 ANALYSE..." pour le doc 11)
- **Vérification confirmée** : contenu correct pour les 14 docs (titre, date, INTRODUCTION, tokens)

### Drive names actuels (14/14)
| # | Drive name |
|---|-----------|
| 01 | 01 Assignation Reféré Provision FINAL - UNIFIE_ANONYME |
| 02 | 02 Action Directe Assureur RC (Art. L.124-3) - UNIFIE_ANONYME |
| 03 | 03 Plainte Complément Défaut Assurance RC - UNIFIE_ANONYME |
| 04 | 04 Assignation Référé Provision V1 - UNIFIE_ANONYME |
| 05 | 05 Constitution Partie Civile - UNIFIE_ANONYME |
| 06 | 06 Dossier de Présentation - UNIFIE_ANONYME |
| 07 | 07 ETUDE Indemnisation MAX - UNIFIE_ANONYME |
| 08 | 08 Index Etat Final Dossier - UNIFIE_ANONYME |
| 09 | 09 Plan Action Chronologie - UNIFIE_ANONYME |
| 10 | 10 Synthèse FAQ - UNIFIE_ANONYME |
| 11 | 11 ANALYSE correction juridique - UNIFIE_ANONYME |
| 12 | 12 ANALYSE Jurisprudence - UNIFIE_ANONYME |
| 13 | 13 ANALYSE Plaidoirie Dirigeants - UNIFIE_ANONYME |
| 14 | 14 ANALYSE Responsabilités Légales Dirigeants - UNIFIE_ANONYME |

## Phase 3 — Annexe C ajoutée aux 14 documents ✅

### Ce qui a été fait
- PIECES MAP.md créé dans [🧠 Memory](README.md) avec mapping complet document→pièces
- Annexe C générée sur mesure pour chaque document (listes à puces, liens Drive cliquables)
- Chaque Annexe C liste les pièces spécifiquement citées dans le contenu du document
- Docs 1-4 (procéduraux) → pièces financières, médicales, pénales, CPAM
- Docs 5-6 (bordereau pièces) → pièces 1-10 explicitement listées
- Docs 7-12 (analytiques) → pièces médicales clés + CPAM + URSSAF
- Docs 13-14 (dirigeants) → pièces INSEE/INPI + plainte + CPAM

### Documents désormais complets (Annexes A+B+C)
Tous les 14 documents UNIFIE_ANONYME contiennent :
1. ✅ Contenu principal avec tokens en gras (V2)
2. ✅ Corrections factuelles appliquées
3. ✅ Liens Légifrance/Judilibre cachés (7 docs : 6,7,8,9,10,11,14)
4. ✅ Annexe A — Lexique des tokens
5. ✅ Annexe B — Textes de loi et jurisprudence cités
6. ✅ Annexe C — Liste des pièces citées avec liens Drive

## Correction #2026-07-02 — Mensonges factuels + Date de naissance

### Date de naissance erronée
- Doc 1 (Assignation FINAL) : « né le **12 mars** 1982 » → corrigé en « né le **18 janvier** 1982 »
- Cause racine : contamination par template sans boucle de vérification
- Solution : création de `STRICT VARIABLES.md` + règle Double-Pass dans `RULES.md`

### Correction factuelle (mensonges éradiqués)

**Source de vérité** : Dossier de Presentation original (`1CPMOR23awztNxiJYVoEZkRkKMxuXDfJzFrVB4ioxbGw`) — le coiffeur est monté sur la vasque → basculement → main droite a percuté une cassure préexistante.

### Corrections appliquées

| Doc | Mensonge | Correction |
|-----|----------|------------|
| 1 | « s'est effondrée et brisée / débris de céramique » | ✅ « basculement brutal... cassure majeure préexistante » |
| 1 | « incapacité physique absolue d'utiliser un outil informatique » | ✅ « incapacité d'utiliser sa main droite » |
| 1 | « le paralyse entièrement dans son activité professionnelle » | ✅ « limite gravement son activité professionnelle » |
| 1 | « défaut d'entretien ou d'installation » | ✅ « escalade du préposé... cassure préexistante non signalée » |
| 2 | « incapacité absolue d'exercer son activité professionnelle » | ✅ « incapacité d'utiliser sa main droite » |
| 10 | « totalement paralysée » | ✅ « gravement compromise » |

## Correction #2026-07-03 — Fausse liquidation (hallucination IA)

### Problème
Doc 11 (ANALYSE et correction juridique) affirmait comme un fait certain :
> *"L'Exploitant est actuellement engagé dans un processus de liquidation"*

**C'est une hallucination de l'IA génératrice.** Aucun document source (PJ, KBIS, INPI, etc.) ne contient cette information.

### Correction appliquée
- Doc 11 UNIFIE_ANONYME ✅ → remplacé par constat d'incertitude
- Source 🔬 ANALYSE et correction juridique ✅ → idem
- Anciennes versions contaminées (2 docs) → corbeille

### Nouveau texte
> *"À ce jour, le statut exact de L'Exploitant demeure incertain : les courriers recommandés adressés le 29 juin 2026 à la société et à ses dirigeants sont restés sans réponse ni accusé de réception signé."*

### Règles ajoutées
- **STRICT VARIABLES.md** : ⚠ Statut de la SAS inconnu — ne jamais inventer
- **RULES.md** : INTERDICTION D'INVENTER UN STATUT JURIDIQUE — pas de statut sans source

## Correction #2026-07-03b — Pages d'introduction insérées dans les 13 documents

### Problème
Les 13 documents UNIFIE_ANONYME (hors Doc 14 modèle déjà fait) n'avaient pas de page d'introduction narrative (TITLE + date + « INTRODUCTION » HEADING_1 + prose + saut de page).

### Travail effectué
- **13 introductions rédigées en prose juridique** (phrases complètes, pas de listes à puces)
- Chaque introduction est propre au document : contexte de l'affaire, fondements juridiques, objectif du document
- « INTRODUCTION » stylé en HEADING_1 (vérifié en JSON)
- Saut de page inséré entre l'introduction et le contenu original
- Contenu original préservé (liens, listes, tableaux, gras)

### Réparations effectuées
- **Docs 1-4, 5-7** : introduction insérée sans dommage au contenu
- **Docs 8, 9, 11** : contenu original rogné par deleteRange → réinséré manuellement + page break
- **Docs 10, 12, 13** : contenu rogné → réinséré et vérifié le 3 juillet 2026
- **Doc 14** : untouched (modèle déjà existant)

### État final (3 juillet 2026)
| # | Titre | Introduction | HEADING_1 | Page break |
|---|-------|-------------|-----------|------------|
| 1 | Assignation RÉFÉRÉ PROVISION FINAL | ✅ Prose | ✅ | ✅ |
| 2 | ActionDirecteAssureurRC | ✅ Prose | ✅ | ✅ |
| 3 | Plainte Complément Défaut Assurance RC | ✅ Prose | ✅ | ✅ |
| 4 | Assignation Référé Provision 5000€ V1 | ✅ Prose | ✅ | ✅ |
| 5 | Pièce 11 Constitution Partie Civile | ✅ Prose | ✅ | ✅ |
| 6 | Dossier de Presentation | ✅ Prose | ✅ | ✅ |
| 7 | ETUDE Indemnisation MAX | ✅ Prose | ✅ | ✅ |
| 8 | Index EtatFinalDuDossier | ✅ Prose | ✅ | ✅ |
| 9 | PlanAction ChronologieProcédure | ✅ Prose | ✅ | ✅ |
| 10 | Synthèse FAQ JuridiqueProcédure | ✅ Prose | ✅ | ✅ |
| 11 | ANALYSE correction juridique | ✅ Prose | ✅ | ✅ |
| 12 | ANALYSE Jurisprudence AccidentCorporel | ✅ Prose | ✅ | ✅ |
| 13 | ANALYSE Plaidoirie Responsabilité Dirigeants | ✅ Prose | ✅ | ✅ |
| 14 | ANALYSE ResponsabilitesLegales (modèle) | ✅ (préexistant) | ✅ | ✅ |

## Dossier Drive
- ID dossier de travail : `1LnXAHlLLLHN0quyhiRq4CdVAKHRGolWk`
- Annuaire Lois : `14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ`
- ARCHIVES : `1poohpxlkv79P5QcvVcXoYXj80nKFEDPV`

## Documents traités avec tokens V2 (14/14 — COMPLET)

Tous les 14 documents ont été anonymisés, injectés et **corrigés factuellement** (mensonges #2026-07-02).

| # | Drive name | ID Original | ID UNIFIE_ANONYME (actif) |
|---|-----------|------------|---------------------------|
| 1 | 01 Assignation Reféré Provision FINAL | `1FpD4dc4JlgVutHR1sdY-g5-aedI2jdw6iL6C5C5a2hA` | `1ZIfWjszjl5VoxBxourQiDeRATbkckkWPzbU9tYmg5yg` |
| 2 | 02 Action Directe Assureur RC (Art. L.124-3) | `1-5wPPbmfrpP4UzFCysGMYgaThI4wZfkZOQ7Gg1IQ7Bg` | `1_tNTGHf1VGnx1zD0PvyrdvqHLAyYDBU_7wRibBwWlJY` |
| 3 | 03 Plainte Complément Défaut Assurance RC | `1KXeatBLQ1WvtKdU4APU5PyAdRSVmogApSMNteEybUqc` | `1TVN7SyAWgTLQtOvUzpWqqlfF7fyzT8H8yLziKLQhelc` |
| 4 | 04 Assignation Référé Provision V1 | `1J1bmCek8imtkgJnXniJg-9RXNapGjzTvnxJPgF_HFh4` | `1L3lJuFQ3CmswKlBg8P5YF6whQQ1AV7QTCLQ_arWo39A` |
| 5 | 05 Constitution Partie Civile | `19X-lkkBYiri7DXP5nMgHkKuxgI8DB4M1LQFf6fDDgLQ` | `1tdFbDxNceGVjaABoYiHkUR1jxd8y0OaezWUOoV3ZDGc` |
| 6 | 06 Dossier de Présentation | `1CPMOR23awztNxiJYVoEZkRkKMxuXDfJzFrVB4ioxbGw` | `1DdpbOypghzt9XE09oxtzx46ngPdU4pnc4gayLQEZ_TU` |
| 7 | 07 ETUDE Indemnisation MAX | `1FKb_mrP_JwMd49KRU74LCuHmOtnsYkzxKA1vNxXuCi8` | `1PiBFn1oA1DtkT61N-zvdPmsCYsmR0au9V4BA9IZzrH4` |
| 8 | 08 Index Etat Final Dossier | `1810cAMY1636YPs99QCBojuy9RZzDVAbYTg8qHCf06ps` | `1Zp-JK9kz0V0DTqNbA7QDDfHliWAqv7Ebyw4Yu3Li6lU` |
| 9 | 09 Plan Action Chronologie | `1u0oort0Z2a63GU86Rt2DMVO16mvxw-BrGisEONdI960` | `153cOANMpw-OoxZqq3jgo34NsWHPY_-cRXZntM_Ydf9s` |
| 10 | 10 Synthèse FAQ | `1cO7WKREKbwXKg1M_OTzX3dCf1u01te6Xaf4HDiMAS8s` | `1eoOJ-bcHBNnLsKYo7_mVz7K1w0gFfhZE_NHdUj3CBoM` |
| 11 | 11 ANALYSE correction juridique | `1hipg8_VqZil-iISUKikWEEW8ElMgpgvSoUUx8vp-5cE` | `1Ikk9wlfyLuFlTofsyLiz6836bHM5g4_ejQhGuRdUkes` |
| 12 | 12 ANALYSE Jurisprudence | `1-aZHyfr5DoPsB2dtjpkYM7TSDHJzsOMVguGI3kXKWVs` | `1AO7GLNpbNGa9ChiUVa5rbbhLtmppzMTgOcg9qCIJBRU` |
| 13 | 13 ANALYSE Plaidoirie Dirigeants | `1Dm7bs3MepNwzxZSVgIy3l40tdHTUZYzKDYvTWVVpi0I` | `1uHOesWZrUf16NVs7kC_dr15JtthOfaJnUNo6e3Z7W90` |
| 14 | 14 ANALYSE Responsabilités Légales Dirigeants | `12M7PJyq4F6uCF_TslK48eFCYvHPeZQTqQD4lI_2NXzE` | `1lUKoGE8kozmE3KA4zErv9GYmJZ0yctOk9tn92O8KT34` |

---

## Infrastructure Jules — Drive CLI + Setup (4 juillet 2026)

### Nouveaux fichiers
| Fichier | Rôle |
|---------|------|
| `setup.sh` | Script d'initialisation : `uv sync` + config Drive |
| `app/drive_auth.py` | Module d'authentification Drive (OAuth → env vars ou ADC) |
| `app/drive_client.py` | CLI Drive pour Jules : list, upload, download, export, search, create-folder |

### Authentification Drive
- **Méthode primaire** : OAuth refresh token (même client que `gcp-oauth.keys.json`)
- **Méthode fallback** : Application Default Credentials (ADC)
- **Pas de SA key** : l'org policy `iam.disableServiceAccountKeyCreation` bloque la création de clés
- **Variables d'environnement** : `GOOGLE_DRIVE_CLIENT_ID`, `GOOGLE_DRIVE_CLIENT_SECRET`, `GOOGLE_DRIVE_REFRESH_TOKEN`

### Testé et vérifié
- ✅ `uv run python -m app.drive_client list` → liste les 4 sous-dossiers du dossier Accident Main
- ✅ `uv run python -m app.drive_client upload` → upload fonctionnel
- ✅ `uv run python -m app.drive_client search` → recherche par nom
- ✅ `uv run python -m app.drive_client export --format markdown --print` → export Google Doc vers stdout

### Nouveaux ajouts — 4 juillet 2026 (soir)
| Ajout | Détail |
|-------|--------|
| [📜 Lois](../%F0%9F%93%9C%20Lois/README.md) | 16 textes juridiques (PDF→.md) du dossier Drive **00 Lois** + INDEX.md |
| `app/mcp_bridge/` | Clients Judilibre et Légifrance sans FastMCP, utilisables en CLI |
| `app/drive_client.py` | Nouvelle commande `read-sheet` pour Google Sheets |
| `setup.sh` | Mis à jour : support Piste + MCP Bridge |
| `pyproject.toml` | requires-python → >=3.12, dépendances : pylegifrance, requests, pypdf |

### À faire pour toi (Jules Settings → jules.google.com/settings)

| Variable | Source |
|----------|--------|
| `GOOGLE_DRIVE_CLIENT_ID` | `gcp-oauth.keys.json` → `installed.client_id` |
| `GOOGLE_DRIVE_CLIENT_SECRET` | `gcp-oauth.keys.json` → `installed.client_secret` |
| `GOOGLE_DRIVE_REFRESH_TOKEN` | `application_default_credentials.json` → `refresh_token` |
| `PISTE_CREDENTIALS` | JSON complet de `app/tools.py` → `get_secret("PISTE_CREDENTIALS")` |
| Setup script | `./setup.sh` (pas `echo do setup`) |

**Important** : le setup script doit être `./setup.sh` (pas `echo do setup`),
car Jules supprime les env vars après le setup. setup.sh matérialise les
credentials dans `.drive-token.json` et `.piste-credentials.json`, que le
code Python lit ensuite en fallback.

### Credentials déjà configurés (tu les as mis)
- ✅ `GOOGLE_DRIVE_CLIENT_ID`
- ✅ `GOOGLE_DRIVE_CLIENT_SECRET`
- ✅ `GOOGLE_DRIVE_REFRESH_TOKEN`
- ✅ `PISTE_CREDENTIALS`
- ❌ **Setup script** : encore `echo do setup` → à changer en `./setup.sh`

## Phase 5b — Création et anonymisation des courriers 03-06 (5 juillet 2026) ✅

### Ce qui a été fait
- **03_Courrier SAS.md** : créé et anonymisé depuis `pieces/20260629 ✉️ LR MiseEnDemeure SAS LesMauvaisGarcons.md`
- **04_Courrier Assureur.md** : créé depuis `archives/ActionDirecte_AssureurRC.md` + alignement montant global 59 600€
- **05_Courrier Proprietaire.md** : créé et anonymisé depuis `pieces/20260629 ✉️ LR MiseEnDemeure Bailleur MrDELRIEU.md`
- **06_Courrier President DG.md** : créé par fusion des pièces MOUNTASSER et ANDISSAC en courrier unique double destinataire
- **Tous les courriers** : YAML frontmatter, liens Légifrance, tokens en **gras**
- **Scripts mis à jour** : `add_yaml_actes.py` (4 entrées), `batch_link_legifrance.py` (chemins corrigés + support JURITEXT)
- **Index mis à jour** : stats (14 docs), mention fichiers à insérer supprimée, travaux restants nettoyés
- `python3 app/check_consistency.py` : 0 erreur, 1 avertissement (bénin)
- **Sync NotebookLM** : `.dev/app/sync_notebooklm.py` + `.github/workflows/sync-notebooklm.yml` créés. Sync automatique vers Drive `Accident Main - NotebookLM/` (Actes Reel, Memory, Lois). Secrets GitHub configurés (GOOGLE_DRIVE_CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN). 126 fichiers uploadés lors du premier sync.
- **Unification chiffrage (juil. 2026)** : Passages 59 600 € → ~90 000 € dans analyses actives (📚 Analyses juridiques/07, 09, 12, 13 + Plainte). Provision alignée 15 000 € (11+12). STRICT VARIABLES : note adresse PV police ajoutée.

## Phase 5c — Injection des 4 courriers sur Drive (5 juillet 2026) ✅

### Ce qui a été fait
- **4 Google Docs créés** sur Drive dans le dossier de travail :
  - `03 Courrier SAS Mise en Demeure - UNIFIE_ANONYME` (`1s5_z0l9yti3Ir6yBGH5xlZE-2LMs8uMJGlVcQA_sHKc`)
  - `04 Action Directe Assureur RC - UNIFIE_ANONYME` (`14VIXTJK4n9eH66eVNZ6hJO6gLkiRBqnJpWijsDbkE2k`)
  - `05 Courrier Proprietaire - UNIFIE_ANONYME` (`1W-C6nM5G_GUPzHjnaq56kRzdHwMuwTfaWQE8nNS9hj4`)
  - `06 Courrier President DG - UNIFIE_ANONYME` (`1pheN3_rudxydYS2AQI7a1KGeFRr3PKD5Zett6Ac899I`)
- **Markdown injecté** avec `replaceDocumentWithMarkdown(firstHeadingAsTitle: true)`
- **JUSTIFIED appliqué** sur les 4 documents
- **drive_id mis à jour** dans les fichiers locaux YAML
- **Consistency check : 0 erreur**

### Vérification PV Police (OCR)
- **OCR effectué** sur le scan PDF original du PV (n°2026/015967, 3 pages, 300 DPI)
- **Texte confirmé** : le PV dit bien « monté sur une vasque en céramique » — aucune erreur de transcription
- Cohérence documentaire vérifiée (PV original = transcription = actes juridiques)

## Phase 5 — Correction audit de coherence (5 juillet 2026) ✅

### Corrections appliquees
- Montants 58 100€ → 59 600€ dans 4 fichiers (Plainte, Plaidoirie, FAQ, Responsabilites)
- Contradiction interne 11_Etude indemnisation corrigee (texte aligne sur tableau)
- Frontmatter YAML duplique supprime dans 6 fichiers
- Nesting de liens Legifrance nettoie (5 niveaux → 1 niveau) dans 10 fichiers
- Tokens d'anonymisation corriges : civilite supprimee, "coiffeur" → **[Le Prépose de l'Exploitation]**
- Chemins obsoletes dans RULES.md et WORKFLOW.md mis a jour
- Date STATUS.md corrigee (4→5 juillet), date ANNEXE C corrigee (27/05→29/06)
- `python3 app/check_consistency.py` : 0 erreur, 1 avertissement (benin)

## Phase 5c — Injection des 4 courriers sur Drive (5 juillet 2026) ✅

### Ce qui a été fait
- **4 Google Docs créés** sur Drive dans le dossier de travail :
  - `03 Courrier SAS Mise en Demeure - UNIFIE_ANONYME` (`1s5_z0l9yti3Ir6yBGH5xlZE-2LMs8uMJGlVcQA_sHKc`)
  - `04 Action Directe Assureur RC - UNIFIE_ANONYME` (`14VIXTJK4n9eH66eVNZ6hJO6gLkiRBqnJpWijsDbkE2k`)
  - `05 Courrier Proprietaire - UNIFIE_ANONYME` (`1W-C6nM5G_GUPzHjnaq56kRzdHwMuwTfaWQE8nNS9hj4`)
  - `06 Courrier President DG - UNIFIE_ANONYME` (`1pheN3_rudxydYS2AQI7a1KGeFRr3PKD5Zett6Ac899I`)
- **Markdown injecté** avec `replaceDocumentWithMarkdown(firstHeadingAsTitle: true)`
- **JUSTIFIED appliqué** sur les 4 documents
- **drive_id mis à jour** dans les fichiers locaux YAML
- **Consistency check : 0 erreur**

### Vérification PV Police
- **OCR effectué** sur le scan PDF original du PV (2026/015967, 3 pages)
- **Texte confirmé** : le PV dit bien « monté sur une vasque en céramique » — aucune erreur de transcription
- Cohérence documentaire vérifiée (PV original = transcription = actes juridiques)

## Phase 5d — Courrier Consolidation Dr DJERBI (Plan E) (5 juillet 2026) ✅

### Ce qui a été fait
- **07_Courrier Consolidation.md** : créé et injecté sur Drive
- Contenu : demande de certificat médical de consolidation pour permettre l'évaluation DFP/IP/SE
- Mention : Nomenclature Dintilhac + Cass. Civ. 2e, 4 avril 2024, n° 22-19.307
- **JUSTIFIED appliqué** sur le document
- **drive_id mis à jour** dans le fichier local YAML
- Drive ID : `1PSv6c0YFvLa0WDEbwc3AVxL14z7ARi5ne50ctJgCvWI`
- Dossier : `20269999 xx FUTUR xx`

## Phase 6a — Courriers Suivi TAVELLA + Inspection Travail (Plan B) (5 juillet 2026) ✅

### Ce qui a été fait
- **08_Courrier Suivi TAVELLA.md** : créé et injecté — réponse à l'adjoint au maire pour demande de suivi Inspection du Travail + CODAF + demande de communication des rapports
- **09_Courrier Inspection Travail.md** : créé et injecté — demande directe à la DDETS/DREETS avec liste des manquements présumés (DUERP, assurance RC, équipement, formation, travail dissimulé)
- **JUSTIFIED appliqué** sur les 2 documents
- **drive_id mis à jour** dans les fichiers locaux YAML
- Drive IDs : `1Xj4wf-v-ShCeq44vjb6XulUM_y2WnuLKO68flsuPKNw` (08), `1tStFiBk8gxB6kWk_HQGPSLH2-QCQVxkARBz7SDer2gM` (09)

## Phase 6b — Rédaction des 12 courriers d'alerte preventives (⚠️ PROJETS — NON ENVOYÉS) (5 juillet 2026) ✅

### ⚠️ IMPORTANT — Statut réel de ces courriers
**Aucun de ces courriers n'a été expédié par LRAR ou email.** Ils ont été rédigés et injectés sur Google Drive uniquement. Tous les fichiers contiennent des `[À compléter]` dans les adresses destinataires et 0 numéro LRAR.

La mention "Phase 6b" dans STATUS.md signifie uniquement **rédaction + injection Drive**, pas envoi postal. Voir `RULES.md` Avenant n°15 pour la nomenclature stricte.

### Ce qui a été fait
- **Règle permanente ajoutée** dans RULES.md et DECISIONS.md : séparation stricte tokens ↔ dossier de correspondance réelle
- **12 nouveaux courriers créés** dans `⚖️ Actes/✉️ Courriers/` (nos 10 à 21) :

| # | Fichier | Destinataire | Objet | Type |
|---|---------|-------------|-------|------|
| 10 | `10_Courrier Greffe TC.md` | Greffe TC Foix | Inscription observation RCS | LRAR |
| 11 | `11_Courrier INPI.md` | INPI / RNE | Signalement litige en cours | LRAR |
| 12 | `12_Courrier URSSAF.md` | URSSAF Midi-Pyrénées | Signalement travail dissimulé | LRAR |
| 13 | `13_Courrier Prefecture.md` | Préfecture 09 | Confirmation signalement | LRAR |
| 14 | `14_Courrier CODAF.md` | CODAF 09 | Signalement officiel manquements | LRAR |
| 15 | `15_Courrier SIE.md` | SIE Foix | Information litige | LRAR |
| 16 | `16_Courrier Conseil Departemental.md` | CD 09 | Signalement sécurité ERP | LRAR |
| 17 | `17_Courrier CARSAT.md` | CARSAT Midi-Pyrénées | Signalement risque pro | Email |
| 18 | `18_Courrier SDIS.md` | SDIS 09 | Signalement sécurité ERP | Email |
| 19 | `19_Courrier FGTI.md` | FGTI | Information conservatoire | LRAR + Email |
| 20 | `20_Relance Police.md` | Police Foix | Suivi plainte + demande vidéos | Email |
| 21 | `21_Relance CPAM.md` | CPAM Haute-Garonne | Suivi dossier RCT | Email |

- **Tous rédigés en version longue** (contexte + faits + fondements juridiques), conformément aux courriers 03-06
- **Consistency check** : 0 erreur, 13 avertissements bénins `[Adresse a completer]` (inchangé)
- **Délai respecté** : pas de relance SAS/dirigeants avant le 14 juillet (délai légal 15 jours)

### Règle permanente instaurée
- Les fichiers de travail (⚖️ Actes/, 🧠 Memory/, courriers .md) sont **100% en tokens anonymes**
- Un dossier de correspondance réelle séparé sera créé UNIQUEMENT au moment de l'envoi
- Aucun fichier « mixte » tokens+réel ne doit exister

## Phase 6c — Corrections post-audit (5 juillet 2026) ✅

### Problèmes identifiés par l'audit externe

| Point | Statut |
|-------|--------|
| Greffe TC incompétent pour litige civil individuel | ✅ Supprimé |
| CARSAT incompétente pour client tiers | ✅ Supprimé |
| URSSAF recentré travail dissimulé uniquement | ✅ Reformulé |
| Plainte : victime client, pas salarié | ✅ Requalifié |
| Assureur RC inconnu → Article 145 CPC | ✅ Créé |

### Fichiers supprimés
- `⚖️ Actes/✉️ Courriers/10_Courrier Greffe TC.md` — Greffe TC incompétent (observation RCS pas pour litige civil individuel)
- `⚖️ Actes/✉️ Courriers/17_Courrier CARSAT.md` — CARSAT incompétente (pas de pouvoir sur client tiers)

### Fichiers modifiés
- `⚖️ Actes/✉️ Courriers/12_Courrier URSSAF.md` — Recentré sur travail dissimulé pur (plus de récit accident/victime)
- `⚖️ Actes/⚖️ Actes proceduraux/02_Plainte.md` — Ajout « en qualité de client » pour requalification
- `⚖️ Actes/🗂️ Organisation/00_Index.md` — Tableau mis à jour (suppressions + Article 145)

### Fichiers créés
- `⚖️ Actes/⚖️ Actes proceduraux/03_Assignation Article 145.md` — Assignation en référé Article 145 CPC pour communication police d'assurance RC Pro sous astreinte (150€/jour)

### État après corrections
- **17 courriers** (03-09, 11-16, 18-21)
- **3 actes procéduraux** (01 Assignation, 02 Plainte, 03 Article 145)
- **0 erreur** à la consistency check (a vérifier)

## Phase 6d — Injection Drive des 11 documents (⚠️ INJECTION DRIVE — PAS D'ENVOI POSTAL) (5 juillet 2026) ✅

### Documents injectés sur Drive (dossier `1LnXAHlLLLHN0quyhiRq4CdVAKHRGolWk`)

| # | Drive name | ID |
|---|-----------|-----|
| 03 | 03 Assignation Article 145 - UNIFIE_ANONYME | `1R26179ks7vLkzw0hYEHL888i0p1VS9ppa6s8R8kQ_gg` |
| 11 | 11 Courrier INPI - UNIFIE_ANONYME | `1gFhTi6GhD6uDRW_XZcbk13JgpaJOOfGxEXb9ZX0KV4E` |
| 12 | 12 Courrier URSSAF - UNIFIE_ANONYME | `1LdLfCnWLiD2v1N1SMF3FAeh681znM0kXOrAlBXeOe8w` |
| 13 | 13 Courrier Prefecture - UNIFIE_ANONYME | `1sIkiScOSFZyXcfEqyuxEW8q0NC_g4YoAYLmEBsuYXbM` |
| 14 | 14 Courrier CODAF - UNIFIE_ANONYME | `1Lva-hW9g9d6B4TITlttg28HD6y06MxaUtjzSVQyC4EY` |
| 15 | 15 Courrier SIE - UNIFIE_ANONYME | `1yl55r__e8V0Rjnf3DETzaOCuhNX1CedEvcJo8FVIxAA` |
| 16 | 16 Courrier Conseil Departemental - UNIFIE_ANONYME | `1pBi3ofZ86aGKRkL9X367bHZvHj0fU55iMC_Izmz6gHQ` |
| 18 | 18 Courrier SDIS - UNIFIE_ANONYME | `1CCl3bFp_jkYtAF8yEDNtJn5Tic8miKsxLOSGNP2peoE` |
| 19 | 19 Courrier FGTI - UNIFIE_ANONYME | `1rtaTa6scRGc0TmelWNMrX6bN-kqe98b1dhT5OT-qsXc` |
| 20 | 20 Relance Police - UNIFIE_ANONYME | `171CF_LzNopYxIS6Tn4i3t3Ghx3ut14F1gh6-KjHevCA` |
| 21 | 21 Relance CPAM - UNIFIE_ANONYME | `1MHhZf_KN4b3jcym5DRJefVGCEjhHQm6ZHT1hOuJ-W4k` |

### Travail effectué
- **11 Google Docs créés** avec `replaceDocumentWithMarkdown(firstHeadingAsTitle: true)`
- **JUSTIFIED appliqué** sur les 11 documents
- **drive_id mis à jour** dans les fichiers locaux YAML
- **Total Drive** : 18 documents UNIFIE_ANONYME (03-09, 11-16, 18-21 + 03 Article 145 + anciens 01-14)

## Correction #2026-07-05 — Récit erroné 09 Courrier Inspection Travail ✅

### Problème
La version initiale du **09 Courrier Inspection Travail** contenait une erreur factuelle dans la description de l'accident et dans le fondement juridique :

- **Ligne 51** (INTRODUCTION) : « le préposé a escaladé le bac à shampoing **pour effectuer sa tâche** » — c'est faux. Il est monté sur le bac pour **régler le poste de télévision**.
- **Ligne 74** (liste manquements) : le fondement invoqué était la **formation sécurité** (L. 4141-2) — inadapté. Il s'agit d'un défaut d'**équipement d'accès en hauteur** (L. 4121-1 + R. 4323-58 et suivants).

### Correction appliquée
- **INTRODUCTION** : remplacé par « sur lequel il avait dû monter **pour accéder au poste de télévision, faute d'équipement d'accès adapté (escabeau)** »
- **Liste des manquements (puce 4)** : remplacée par **Absence d'équipement d'accès en hauteur** avec articles L. 4121-1 (obligation générale de sécurité) et R. 4323-58 et suivants (travaux en hauteur)
- **Version Drive mise à jour** via `replaceDocumentWithMarkdown` (même ID : `1tStFiBk8gxB6kWk_HQGPSLH2-QCQVxkARBz7SDer2gM`)
- **Fichier local corrigé** : `⚖️ Actes/✉️ Courriers/09_Courrier Inspection Travail.md`

---

## Phase 7 — Restructuration token/reel + README.md + Checker (6 juillet 2026) ✅

### Ce qui a été fait
- **Restructuration token/reel** : `⚖️ Actes/00-06` → `⚖️ Actes/🔑 Token/00-06/`, `⚖️ Actes/07_Reel` → [⚖️ Actes/👤 Reel](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/README.md), script `generate_real_versions.py` réécrit (scan multi-dossiers, génération dans [⚖️ Actes/👤 Reel](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/README.md) avec sous-dossiers miroirs + README.md)
- **17 README.md riches** créées : fil d'Ariane, emoji, table des fichiers, navigation verticale
- **INDEX.md → README.md** : 7 fichiers renommés
- **Règle répertoire souverain érigée** : AGENTS.md règle #10, RULES.md règle #0, DECISIONS.md, VACCIN.md
- **Clone parasite supprimé** (`/tmp/opencode/accident-main/`)
- **check_consistency.py corrigé** : patch URL decode (urllib.parse.unquote) + path ANNEXES [⚖️ Actes/🔑 Token/🗄️ Archives/annexes](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/%F0%9F%97%84%EF%B8%8F%20Archives/annexes/README.md) → **0 erreur, 65 avertissements bénins** (`[À compléter]` placeholders)
- **Règle #1 RULES.md** : interdiction de poser des questions au conditionnel (vérifier par soi-même d'abord)
- **Plan H vérifié** : assignations 01 et 03 avec "PAR CES MOTIFS" conformes, visas corrects, bordereaux présents

### Vérification faite
- `check_consistency.py` : 0 erreur ✅
- Plan H : assignation 01 (visas 145+835 CPC / 1240+1242 CC, pièces 1-6, bordereau ✅), assignation 03 (visas 145 CPC / L.124-3 C. Assur, pièces 7-10, bordereau ✅)
- 14 PRs mergées (#28–#41), 0 PR ouverte

## Phase 7b — Bordereau séquentiel + Justification provision + Emails témoins (6 juillet 2026) ✅

### Ce qui a été fait
- **Nouveau bordereau séquentiel** : `04_Bordereau_Audience.md` créé — 25 pièces en 6 groupes thématiques (A-F), numérotation propre, dédoublonnée
- **Assignation 01 enrichie** : nouveau §D *Justification du montant de la provision* (5 arguments : fourchette référentiel, proportionnalité, provision *ad litem*, silence de l'exploitant, jurisprudence Cass.)
- **Email relance Dr DJERBI** : `25_Email Relance Dr DJERBI.md` — relance certificat consolidation
- **3 emails transmission attestations** : `26/27/28_Email Attestation` pour client/pompier/employé
- **Génération versions réelles** : 46 fichiers regénérés dans [⚖️ Actes/👤 Reel](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%91%A4%20Reel/README.md) (incl. 5 nouveaux)
- **Document clé identifié** : Réquisition Police UMJ 02/06/2026 (PDF) + retranscription téléphonique — confirme le rendez-vous réel du **12 novembre 2026** à Purpan
- **Compréhension corrigée** : plus de dates fabriquées (31 juillet, expertise médicale civile) — seules dates réelles : 14 juillet (fin amiable), 12 novembre (UMJ ITT)
- **Check consistency** : 0 erreur, 65 avertissements bénins (inchangé)
- **2 commits + push** : phase 7b complète (modifs + generate_real_versions)

## Phase 8 — Reformatation Citations Juridiques (7 juillet 2026) ✅

### Objectif
Standardiser TOUTES les citations de lois et jurisprudences dans [⚖️ Actes/🔑 Token](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md) selon un format unique :
- Articles de loi : blockquote avec citation > **Code > Section** > [lien LEGIARTI]
- Arrêts de cassation : blockquote avec résumé du principe > **Cour, Date** > [lien JURITEXT]
- Liens inline dans le texte courant → convertis en texte brut

### Commits
- `c411671` — Phases 1-2 (Assignation, 02b, Courriers 03-06)
- `859538f` — Phase 3 (Analyses juridiques)
- `6192221` — Phase 4 (Études indemnisation)
- `1c62201` — Phase 5 (Plan action, Index)
- `7fbe5af` — Phase 6 (🗄️ Archives — 8 fichiers)
- `df21e34` — Corrections post-audit (Plainte, Bordereau, Courriers, Dossier Plaidoirie)
- `061679b` — Corrections montants IP/DFP/SE obsolètes (Courrier Assureur, FGTI, Bordereau)

### Résultats (scan final confirmé)
- **Liens inline legifrance** : **0** (hors blockquotes)
- **Liens dans blockquotes** : **77**
- **Montants IP 15 000€ obsolète** : **0** (hors tableaux comparatifs)
- **Montants DFP 25 200€ obsolète** : **0** (hors tableaux comparatifs)
- **Montants SE 12 000€ obsolète** : **0** (hors tableaux comparatifs)
- **Audit multi-agent** : Gemini ✅, Grok ✅, Copilot (faux positifs), Mistral (faux positifs)

### Fichiers traités
- **21 fichiers principaux** (⚖️ Actes proceduraux, ✉️ Courriers, 03_Analyses, 04_Etudes, 🗂️ Organisation)
- **8 fichiers archives** (🗄️ Archives)
- **63 fichiers total** dans [⚖️ Actes/🔑 Token](../%E2%9A%96%EF%B8%8F%20Actes/%F0%9F%94%91%20Token/README.md)

### Montants finaux validés
- Provision : **15 000€** | DFP : **25 000€** (10%) | IP : **30 000€** | SE : **15 000€** | PEP : **3 000€** | DEP : **3 000€** | Agrément : **5 000€** | Total : **~90 000€**