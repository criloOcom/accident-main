# Audit et recommandations pour l'organisation du dossier "Actes"

## 1. Constat général
L'analyse de l'arborescence actuelle du dossier `actes/` révèle une discordance majeure avec le document de référence `INDEX Etat Final Dossier.md`.
Le dossier physique est organisé par matière juridique (`contentieux-civil`, `contentieux-penal`, `annexes`), alors que l'index préconise un classement chronologique/logique par type de pièce (cotes `00` à `05`).

## 2. Documents mal rangés (à reclasser)
L'ensemble des documents actuels devrait être renommé et déplacé pour correspondre à la nomenclature de l'index :

*   `actes/contentieux-civil/ASSIGNATION Refere Provision.md` -> Devrait être renommé en `01_Assignation - V1` et placé dans un sous-dossier `01_Actes_proceduraux`.
*   `actes/contentieux-penal/CONSTITUTION Partie Civile.md` (ou la plainte) -> Correspond probablement à `02_Plainte - V1` dans `01_Actes_proceduraux`.
*   `actes/contentieux-penal/ANALYSE Plaidoirie Dirigeants.md` -> Correspond à `07_Plaidoirie dirigeants - V1` dans `03_Analyses_juridiques`.
*   `actes/SYNTHESE FAQ.md` -> Correspond à `09_FAQ - V1` dans `03_Analyses_juridiques`.
*   `actes/contentieux-penal/ANALYSE Responsabilites Legales.md` -> Correspond à `13_Responsabilites legales - V1` dans `03_Analyses_juridiques`.
*   `actes/contentieux-civil/ETUDE Indemnisation MAX.md` -> Correspond à `11_Etude indemnisation - V1` dans `04_Etudes_indemnisation`.
*   `actes/PLAN Action Chronologie.md` -> Correspond à `10_Plan action - V1` dans `05_Organisation`.
*   `actes/INDEX Etat Final Dossier.md` -> Devrait être renommé `00_Index` dans `05_Organisation` (ou laissé à la racine mais renommé).

## 3. Documents manquants (à retrouver ou créer)
De nombreux éléments listés dans l'index sont introuvables dans l'arborescence actuelle :
*   **00 — Preuves officielles :**
    *   CR opératoire (2026-05-30)
    *   Dossier plainte (Copie complète)
    *   PV Police
    *   CR opératoire de contrôle (2026-06-19)
    *   Forensic Evidence File
*   **02 — Courriers :**
    *   03_Courrier SAS - V1
    *   04_Courrier Assureur - V1
    *   05_Courrier Proprietaire - V1
    *   06_Courrier Président + DG - V1

## 4. Documents obsolètes ou non indexés (à archiver)
Certains documents présents dans les dossiers ne figurent pas dans l'index final et encombrent l'espace de travail. Il est recommandé de les archiver :

*   `actes/PRESENTATION Dossier.md`
*   Tout le dossier `actes/annexes/` (`ANNEXE A Lexique Tokens.md`, `ANNEXE B Lois Jurisprudence.md`, `ANNEXE C Pieces.md`)
*   `actes/contentieux-civil/ACTION Directe Assureur RC.md`
*   `actes/contentieux-civil/ANALYSE Correction Juridique.md`
*   `actes/contentieux-civil/STRATEGIE Contentieux Civil.md`
*   `actes/contentieux-civil/ANALYSE Jurisprudence.md`
*   `actes/contentieux-penal/PLAINTE Complement Defaut Assurance RC.md`
*   `actes/contentieux-penal/STRATEGIE Contentieux Penal.md`

**Point d'attention sur les préjudices :**
L'index mentionne "12_Tableau prejudices - V1" dans la section 04, mais une note en bas de page de l'index indique que le tableau financier a été "RETIRÉ du dossier". Il y a là une contradiction interne à l'index à corriger (soit supprimer l'entrée 12, soit clarifier s'il s'agit d'un autre document). Le document physique est par ailleurs introuvable.

## 5. Recommandation d'arborescence cible
Il est fortement recommandé de restructurer le dossier `actes/` comme suit pour s'aligner sur l'index :

```text
actes/
├── 00_Preuves_officielles/
│   ├── [Insérer les CR, PV et Forensic files manquants]
├── 01_Actes_proceduraux/
│   ├── 01_Assignation - V1.md
│   └── 02_Plainte - V1.md
├── 02_Courriers/
│   ├── [Insérer les courriers 03 à 06 manquants]
├── 03_Analyses_juridiques/
│   ├── 07_Plaidoirie dirigeants - V1.md
│   ├── 09_FAQ - V1.md
│   └── 13_Responsabilites legales - V1.md
├── 04_Etudes_indemnisation/
│   └── 11_Etude indemnisation - V1.md
├── 05_Organisation/
│   ├── 00_Index.md
│   └── 10_Plan action - V1.md
└── archives/
    ├── annexes/
    └── [Insérer tous les autres documents non indexés]
```
