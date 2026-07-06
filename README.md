# Accident de la Main — Dossier Juridique

**Contentieux civil et pénal** suite à un accident corporel survenu le 29 mai 2026
dans un commerce de Foix (section nerveuse/tendineuse de la main droite, défaut
d'assurance RC, préjudices estimés à 59 600 €).

**Échéances clés :** 14 juillet 2026 (fin phase amiable) → 31 juillet 2026
(audience référé) → 12 novembre 2026 (expertise médicale).

## Arborescence

```
accident-main/
├── actes/
│   ├── 00_Preuves_officielles/   ← Inventaire et preuves physiques
│   ├── 01_Actes_proceduraux/     ← Assignations, conclusions, requêtes
│   ├── 02_Courriers/             ← Mises en demeure, courriers administratifs
│   ├── 03_Analyses_juridiques/   ← Plaidoiries, FAQ, analyses
│   ├── 04_Etudes_indemnisation/  ← Évaluations Dintilhac
│   ├── 05_Organisation/          ← Index, calendrier, statistiques
│   ├── 06_Archives/              ← Annexes (lois, lexique, pièces)
│   └── reel/                     ← Versions réelles (identités réelles résolues)
├── memory/                       ← Mémoire persistante pour les agents IA
├── app/                          ← Scripts Python
└── pieces/                       ← Pièces originales extraites des PDFs
```

### Principe token / reel

Le dossier repose sur une **double strate de documents** :

| Dossier | Contenu | Usage |
|---------|---------|-------|
| `actes/token/` (dossiers 00-06) | **Versions tokenisées** — identités remplacées par `[La Victime]` | Travail courant, révision, partage |
| `actes/reel/` | **Versions réelles** — tokens résolus → noms, adresses, email | Impression, envoi, audience |

Les versions réelles sont générées par le script
`app/generate_real_versions.py` qui copie les fichiers tokenisés et
remplace chaque token par sa valeur réelle (définie dans
`memory/TOKEN MAP.md`).

## Documents principaux

### Actes procéduraux

| # | Document | Description |
|---|----------|-------------|
| 01 | Assignation - V1 | Assignation référé-provision 5 000 € (Art. 835 CPC) |
| 02 | Plainte - V1 | Plainte complémentaire défaut assurance RC |
| 03 | Assignation Art. 145 - V1 | Communication forcée police d'assurance (Art. 145 CPC) |
| 04 | Bordereau de pièces - V1 | Récapitulatif des pièces |
| 05 | Conclusions Référé - V1 | Conclusions pour l'audience du 31 juillet 2026 |
| 06 | Requête Constat Huissier - V1 | Requête constat d'huissier (Art. 145 CPC) |

### Courriers et gabarits (02_Courriers/)

- `03` à `21` : Courriers (mises en demeure, relances, administrations)
- `22` à `24` : Gabarits d'attestations (témoin client, pompier SAMU, employé)

### Analyses juridiques (03_Analyses_juridiques/)

- Plaidoirie dirigeants (Arrêt SATI, Art. L.124-3 C. assur.)
- FAQ juridique, Dossier de plaidoirie pour l'audience référé

### Mémoire persistante — `memory/`

Fichiers essentiels pour les agents IA (lire `AGENTS.md` avant toute action) :

| Fichier | Rôle |
|---------|------|
| `VACCIN.md` | 🔴 Protocole obligatoire avant chaque action |
| `STATUS.md` | État d'avancement détaillé |
| `TODO.md` | Plans restants et priorités |
| `STRICT VARIABLES.md` | Source unique de vérité (dates, montants, faits) |
| `TOKEN MAP.md` | Correspondance jeton ↔ identité réelle |
| `PIECES MAP.md` | Correspondance document → pièces citées |
| `DECISIONS.md` | Décisions d'architecture et règles |
| `RULES.md` | Règles permanentes et interdictions |
| `NOTE_SYNTHESE_AVOCAT.md` | Note de synthèse pour l'avocat |
| `RAPPORT_JURISPRUDENCES.md` | Vérification des citations juridiques |
| `RAPPORT_STRICT_UPDATE.md` | Mise à jour STRICT VARIABLES post-audits |
| `RAPPORT_YAML.md` | Audit de standardisation YAML |
| `RAPPORT_CONSOLIDATION.md` | Consolidation des 7 audits |
| `RAPPORT_PLAN_H.md` | Uniformisation assignations / bordereaux |

## Pour les agents IA

1. **Lire `AGENTS.md`** en premier — point d'entrée contenant la structure,
   les workflows et les règles essentielles
2. **Lire `memory/VACCIN.md`** avant toute action — protocole de vaccination
   obligatoire, non négociable
3. **Lire `memory/`** pour comprendre le contexte complet (STATUS, TODO,
   STRICT VARIABLES, TOKEN MAP, DECISIONS, RULES)
4. **Respecter la logique token/reel** : les fichiers dans `actes/token/`
   doivent toujours rester tokenisés ; les versions réelles vont dans
   `actes/reel/`
5. **GitHub Token** stocké dans Google Secret Manager
   (`projects/crilo-prod-automation/secrets/GITHUB_TOKEN`)
   et en local dans `~/.git-credentials`

## Conventions

| Règle | Description |
|-------|-------------|
| `=== PAGE BREAK ===` | Marqueur de saut de page dans les actes |
| `**[Token]**` | Identité anonymisée (ex: `**[La Victime]**`) |
| YAML front matter | Métadonnées sur tous les fichiers .md dans actes/ |
| Format | `Arial JUSTIFIED` pour tous les documents juridiques |
| Identifiant pièce | Triplet `(date, émetteur, objet)` |

## Scripts disponibles

| Script | Rôle |
|--------|------|
| `app/check_consistency.py` | Vérification transversale du dossier |
| `app/batch_link_legifrance.py` | Insertion de liens Légifrance/Judilibre |
| `app/generate_real_versions.py` | Génération des versions réelles (token → réel) |
| `app/batch_anonymize.py` | Anonymisation de documents |
| `app/drive_client.py` | Client Google Drive |
| `app/injection.py` | Injection de documents dans Google Docs |
| `app/consolidate_sheet.py` | Consolidation de Google Sheets |

Voir `app/README.md` pour le détail de chaque script.

## Dépendances techniques

Python 3.13+, uv, Google ADK, Tesseract OCR français, Poppler-utils.
