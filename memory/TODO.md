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

## PLAN H — RÉDACTION (PR #5)

### Constat
- Clarté, dispositif, bordereaux à uniformiser
- Charte de présentation à harmoniser

### Actions
1. Uniformiser les dispositions des assignations
2. Ajouter bordereau de pièces systématique
3. Vérifier cohérence des références aux pièces

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
