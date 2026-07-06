# TODO — PLANS D'ACTION PRIORITAIRES

> Généré le 5 juillet 2026. Mis à jour après analyse des 6 rapports Jules (PR #4-#9) et
> détection de l'erreur L.211-26 C. assurances (assurance véhicules, pas RC Pro salon).
>
> **Règle absolue (post-Plan A) :** tout nouvel article de loi cité DOIT être lu via MCP
> Légifrance (`consulter_article` ou `rechercher_code`) pour vérifier le contexte (livre,
> titre, section) AVANT intégration.

---

## ~~PLAN A — CORRECTION L.211-26 C. ASSURANCES~~ ✅ TERMINÉ

### Résumé
- L.211-26 supprimé de `STRATEGIE Contentieux Penal.md` (§2.2, §3.3),
  `PLAINTE Complement Defaut Assurance RC.md` (tags, §intro, §II.A),
  `app/add_yaml_actes.py`, `app/check_consistency.py`, `app/batch_link_legifrance.py`.
- Remplacement par signalement de fait + Art. 706-3 CPP + Art. L.124-3 C. assur.
- Règle absolue instaurée : vérification Légifrance avant toute citation.
- 706-3 CPP ajouté aux dictionnaires de `batch_link_legifrance.py`.

---

## PLAN B — PREUVES MATÉRIELLES

### Constat (PR #7)
- Absence de témoignages/attestations Cerfa
- Vidéosurveillance non sécurisée
- Constat huissier non réalisé
- Attestation RC Pro jamais obtenue

### Actions
1. Relancer les autres clients présents (attestations)
2. Vérifier si vidéosurveillance existe toujours
3. Faire constat d'huissier si possible
4. Relancer l'Inspection du Travail / CODAF (pas d'accusé réception)

---

## ~~PLAN C — CIVI / FGTI~~ ✅ TERMINÉ

### Résumé
- `STRATEGIE Contentieux Civil.md` : nouveau §3.3 « Voie CIVI / FGTI (subsidiaire) » avec conditions, procédure, délais Art. 706-5 CPP (10 ans / 1 an). §1 mis à jour. Ligne ajoutée au calendrier §5.
- `STRATEGIE Contentieux Penal.md` : nouveau §3.5 « Indemnisation par le FGTI / CIVI » consolidant les mentions éparses + délais. §1 mis à jour.

---

## ~~PLAN D — CORRECTION MONTANTS FINANCIERS (PR #8)~~ ✅ TERMINÉ

### Résumé
- `ETUDE Indemnisation MAX.md` : Art. 700 1 500 € → 3 000 €, total 58 100 → 59 600 €
- `STRATEGIE Contentieux Civil.md` : Art. 700 1 500 € → 3 000 €, total 58 100 → 59 600 €
- `ASSIGNATION Refere Provision.md` : 15 000 € requalifié DSF → IP (Incidence Professionnelle)
- `STRICT VARIABLES.md` : total mis à jour 58 100 → 59 600 €

---

## PLAN E — CERTIFICAT DE CONSOLIDATION (PR #9)

### Constat
- Évaluation DFP (25 200 €) prématurée sans consolidation médicale.
- Nécessaire avant finalisation expertise et évaluation Dintilhac.

### Actions
1. Demander certificat médical de consolidation au Dr DJERBI

---

## ~~PLAN F — RESTRUCTURATION `actes/` (PR #4)~~ ✅ TERMINÉ

### Résumé
- Nouvelle arborescence créée : `01_Actes_proceduraux/`, `02_Courriers/`, `03_Analyses_juridiques/`, `04_Etudes_indemnisation/`, `05_Organisation/`
- 14 fichiers copiés+renommés selon la nomenclature YAML (01-14)
- `add_yaml_actes.py` : recherche récursive activée, STRATEGIE ajoutées au YAML_MAP
- `batch_link_legifrance.py` : chemins mis à jour vers les nouveaux dossiers
- Ancienne arborescence (contentieux-civil/, contentieux-penal/) conservée intacte
- `check_consistency.py` OK

---

## ~~PLAN G — TABLES DES MATIÈRES (PR #6)~~ ✅ TERMINÉ

### Résumé
- Script `app/add_tdm.py` créé : auto-génère TdM depuis les headings (H2-H4) pour tout fichier .md sans TdM existante
- 30 fichiers traités (tous les .md de `actes/` sauf annexes)
- `check_consistency.py` mis à jour pour ignorer les liens de TdM (faux positifs)
- Check OK, 0 erreur 0 avertissement

---

## ~~PLAN H — RÉDACTION (PR #5)~~ ✅ TERMINÉ

### Résumé
- Assignation 01 : "PAR CES MOTIFS" avec visas 145+835 CPC / 1240+1242 CC, pièces n°1-6, bordereau présent
- Assignation 03 : "PAR CES MOTIFS" avec visas 145 CPC / L.124-3 C. Assur, pièces n°7-10, bordereau présent
- Vérifié par lecture directe des fichiers le 6 juillet 2026

---

## ~~RESTRUCTURATION TOKEN/REEL + README.md~~ ✅ TERMINÉ

### Actions
1. ✅ `actes/token/{00-06}` créé (documents anonymisés)
2. ✅ `actes/reel/{01-06}` généré par `generate_real_versions.py`
3. ✅ 17 README.md riches créées (navigation, table des fichiers, fil d'Ariane)
4. ✅ INDEX.md → README.md (7 fichiers)
5. ✅ `check_consistency.py` : 0 erreur, patch URL decode + path ANNEXES
6. ✅ Règle #1 ajoutée à RULES.md

---

## PHASE 7B — BORDEREAU + JUSTIFICATION PROVISION + EMAILS TÉMOINS ✅ TERMINÉ

### Actions (6 juillet 2026)
1. ✅ `04_Bordereau_Audience - V1.md` créé — 25 pièces séquentielles (6 groupes)
2. ✅ Assignation 01 enrichie — §D Justification du montant de la provision
3. ✅ `25_Email Relance Dr DJERBI - V1.md` créé
4. ✅ `26/27/28_Email Attestation` créés (client/pompier/employé)
5. ✅ Versions réelles générées (46 fichiers)
6. ✅ 0 erreur check_consistency, 2 commits + push

---

## À FAIRE ENCORE

### Court terme
1. **Envoyer les emails aux témoins** — besoin des adresses email des clients, SAMU, employé
2. **Envoyer relance Dr DJERBI** — besoin email du chirurgien
3. **Générer les PDF des Cerfa n° 11527\*03** à joindre aux emails
4. **Planifier constat d'huissier** (recommandation critique EVALUATION_CRITIQUE.md)

### Préparation 12 novembre 2026
5. **Rassembler tous les documents médicaux** pour l'UMJ (CR opératoire, arrêts de travail, ordonnances, comptes rendus kiné)
6. **Préparer un dossier médical complet** à remettre au médecin légiste

### Preuves matérielles (Plan B)
7. **Vérifier si les vidéos de vidéosurveillance existent encore** (délai 30 jours → échu)
8. **Relancer inspection du Travail / CODAF** si pas de réponse sous 15 jours
9. **Vérifier l'AR de la SAS** (retour ? signé ?)

---

## ~~PLAN I — ARTICLE BLOG~~ ✅ TERMINÉ

### Résumé
- Article « Comment une Erreur de Droit a Réformé Notre Processus de Vérification Juridique » ajouté au Google Sheet `06 📢 Blog` (colonne `@`, ligne 108)
- Slug : `erreur-l211-26-process-verification-juridique`
- Catégorie : Retour d'Expérience
- Statut : published
- Contenu : introduction (l'erreur L.211-26), le nouveau process (4 étapes), les outils (3 scripts), tableau Avant/Après, 4 leçons apprises

---

## VÉRIFICATION SYSTÉMATIQUE

- `app/check_consistency.py` avant chaque commit
- Validation croisée ANNEXE B ↔ ANNUAIRE Lois ↔ actes
- MCP Légifrance `rechercher_code` pour tout nouvel article
- MCP Légifrance `consulter_article` si API fonctionne (sinon `rechercher_code`)
