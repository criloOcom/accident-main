# Prompt pour analyse complète du dossier Accident Main

## Contexte

Tu es un assistant juridique spécialisé en contentieux de la responsabilité civile et pénale. Tu vas analyser un dossier d'accident corporel grave constitué localement en markdown (double strate token/reel) et hébergé sur GitHub.

**GitHub :** https://github.com/criloOcom/accident-main
**Structure :**
```
accident-main/
├── ⚖️_Actes/
│   ├── 🔑_Token/          ← Documents anonymisés (travail courant)
│   │   ├── 00_📂_Preuves_officielles/
│   │   ├── 01_⚖️_Actes_proceduraux/     (11 fichiers)
│   │   ├── 02_✉️_Courriers/             (34 fichiers)
│   │   ├── 03_📚_Analyses_juridiques/   (12 fichiers)
│   │   ├── 04_💰_Etudes_indemnisation/  (4 fichiers)
│   │   ├── 05_🗂️_Organisation/          (11 fichiers)
│   │   └── 06_🗄️_Archives/             (10 fichiers)
│   ├── 👤_Reel/           ← Versions réelles (générées par script)
│   └── 00_📂_Preuves_officielles/       ← 19 pièces source
├── 📊_Rapports/           ← 15 rapports d'audit + annexes
├── 📜_Lois/               ← Textes de loi et jurisprudence (40+ fichiers)
├── 🧠_Memory/             ← Mémoire persistante (STATUS, TOKEN MAP, RULES, etc.)
├── .dev/app/              ← Scripts (generate_real_versions.py, batch_anonymize.py)
└── README.md              ← Porte d'entrée
```

## Résumé des faits

Le **[J+0 Accident]** (29 mai 2026), la victime (Sébastien GRAZIDE) a subi une plaie palmaire profonde de 8,5 cm avec section tendineuse et nerveuse de la main droite dominante, causée par la chute d'un employé depuis un bac à shampoing instable dans un salon de coiffure (ERP) exploité par la SAS LES MAUVAIS GARCONS (capital 200 €, 0 salarié, NPAI). ITT : 56 jours. Procédure pénale ouverte sous PV n°2026/015967. La SAS est insolvable (200 € de capital), sans assurance RC identifiée, et les dirigeants sont injoignables.

## Objectifs de ton analyse

Tu dois :
1. **Parcourt l'intégralité du dépôt** GitHub (structure, fichiers, YAML, code)
2. **Analyse les 15 rapports d'audit** dans `📊_Rapports/` pour comprendre ce qui a été fait et vérifié
3. **Analyse le système de double strate** token/reel : est-il cohérent ? Les scripts `generate_real_versions.py` et `batch_anonymize.py` sont-ils synchronisés avec les fichiers ?
4. **Vérifie le système de statuts des documents** : est-ce que chaque fichier YAML a un `statut:` cohérent avec la réalité (envoyé/brouillon/projet etc.) ?
5. **Analyse la cohérence juridique** : les textes cités dans `📜_Lois/` et les qualifications pénales sont-ils corrects ?
6. **Vérifie la matrice des risques** : les 21 risques identifiés sont-ils toujours d'actualité ?
7. **Analyse le dossier FGTI/Dintilhac** : le montant de ~109 500 € est-il cohérent avec la nomenclature et les barèmes ?
8. **Vérifie la navigabilité** : les liens internes entre fichiers `.md` fonctionnent-ils ? Les cross-references token↔reel sont-elles présentes ?
9. **Détecte les incohérences, erreurs, ou manques** dans l'ensemble du dossier
10. **Identifie les actions prioritaires** pour débloquer la situation (7 actions humaines NON FAITES)

## Règles d'analyse

- **Ne modifie rien** — tu es en lecture seule. Tu produis un rapport.
- **Tout fichier suspect** (incohérence YAML, tokenisation manquante, date erronée) doit être signalé avec son chemin exact.
- **Utilise les liens** fournis par les rapports pour naviguer entre les fichiers.
- **Croise les sources** : ne te fie pas à un seul fichier, vérifie dans les rapports d'audit, le STATUS.md, et les fichiers réels.
- **Structure ta réponse** en sections claires avec recommandations classées par priorité.

## Questions spécifiques à trancher

1. **Statut réel des 4 courriers de la Vague 1** (12-URSSAF, 14-CODAF, 19-FGTI, 35-TJ) : ont-ils été envoyés le 11/07 ? Les numéros LRAR ne sont pas renseignés.
2. **FGTI** : le montant optimiste (~109 500 €) est-il défendable face au compromis (~92k€) ? L'ajout de l'ATP est-il justifié ?
3. **Tokenisation** : y a-t-il encore des fuites de données personnelles dans `🔑_Token/` après les corrections du 10/07 ?
4. **Conformité RGPD** : le système de double strate est-il suffisant pour garantir l'anonymisation ?
5. **Structure des dossiers** : le doublon entre `📊_Rapports/` et `reports/` est-il résolu ?
6. **Proposition d'architecture** pour le système de statuts que la victime souhaite mettre en place (dossier `/status/` avec index par statut, cross-reference token↔reel dans YAML, liens internes navigables).

## Références utiles

Commence par lire ces fichiers pour comprendre l'état du projet :
- `README.md` — porte d'entrée
- `🧠_Memory/VACCIN.md` — protocole obligatoire
- `🧠_Memory/STATUS.md` — état d'avancement détaillé
- `🧠_Memory/RULES.md` — règles et matrice des statuts
- `🧠_Memory/RECADRAGE_NOMENCLATURE.md` — correction des statuts
- `🧠_Memory/TOKEN MAP.md` — correspondance token ↔ réel
- `🧠_Memory/DECISIONS.md` — décisions d'architecture
- `📊_Rapports/RAPPORT_SYNTHESE_GLOBALE.md` — synthèse des 15 audits
- `📊_Rapports/RAPPORT_AUDIT_STRUCTURE.md` — anomalies structurelles
- `📊_Rapports/RAPPORT_AUDIT_TOKENISATION.md` — fuites RGPD
- `📊_Rapports/RAPPORT_AUDIT_FGTI_DINTILHAC.md` — analyse indemnisation
- `📊_Rapports/RAPPORT_AUDIT_GITHUB.md` — sécurité GitHub
- `📊_Rapports/RAPPORT_AUDIT_RISQUES.md` — matrice des 21 risques
- `📊_Rapports/RAPPORT_AUDIT_PLAN_ACTION.md` — 7 actions humaines bloquées
- `⚖️_Actes/🔑_Token/05_🗂️_Organisation/23 📊 Suivi Envois LRAR.md` — planning LRAR
- `⚖️_Actes/🔑_Token/05_🗂️_Organisation/24 ✅ Checklist Envoi 11-07-2026.md` — checklist

## Format de réponse attendu

Structure ta réponse en 4 parties :

### 1. Résumé exécutif (1 page max)
État général, points forts, points critiques.

### 2. Analyse détaillée par domaine
- **Structure & Organisation** : arborescence, doublons, README
- **YAML & Statuts** : cohérence, valeurs manquantes, erreurs
- **Tokenisation** : RGPD, fuites résiduelles, scripts
- **Juridique** : textes, qualifications, procédure
- **Financier** : Dintilhac, FGTI, montants
- **Sécurité** : GitHub, tokens, credentials
- **Risques** : matrice, actualisation

### 3. Propositions d'amélioration
- Architecture du système de statuts (dossier `/status/`, index, YAML)
- Cross-references token↔reel
- Navigabilité des liens internes

### 4. Actions prioritaires recommandées
Classées par priorité (P1/P2/P3), avec chemins exacts des fichiers concernés.

---

**Rendu attendu** : un fichier unique, complet, structuré en markdown, déposé à la racine du dépôt GitHub sous le nom `ANALYSE_MISTRAL.md`.
