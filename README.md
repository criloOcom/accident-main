# Accident de la Main — Dossier Juridique

**Contentieux civil et pénal** suite à un accident corporel survenu le 29 mai 2026 dans un commerce (section nerveuse/tendineuse de la main droite, défaut d'assurance RC, préjudices estimés à 58 100 €).

## Navigation rapide

- **[STRATEGIE Contentieux Civil](actes/contentieux-civil/STRATEGIE%20Contentieux%20Civil.md)** — actions civiles, référé-provision, action directe assureur
- **[STRATEGIE Contentieux Penal](actes/contentieux-penal/STRATEGIE%20Contentieux%20Penal.md)** — plaintes, constitution partie civile, défaut assurance
- **[Index complet du dossier](actes/INDEX%20Etat%20Final%20Dossier.md)** — récapitulatif de toutes les pièces et actes
- **[Plan d'action et chronologie](actes/PLAN%20Action%20Chronologie.md)** — calendrier des prochaines étapes

## Arborescence

```
accident-main/
├── actes/
│   ├── contentieux-civil/   ← Actes civils (assignation, action directe, indemnisation)
│   ├── contentieux-penal/   ← Actes pénaux (plaintes, constitution partie civile)
│   ├── annexes/             ← Annexes (A: lexique, B: lois, C: pièces)
│   ├── ...                  ← 4 transversaux à la racine
  │   ├── PRESENTATION Dossier.md
  │   ├── INDEX Etat Final Dossier.md
  │   ├── PLAN Action Chronologie.md
  │   └── SYNTHESE FAQ.md
├── pieces/                  ← 19 pièces originales extraites des PDFs
├── memory/                  ← Mémoire persistante pour les agents IA
└── app/                     ← Scripts Python
```

## Documents

### Contentieux civil

Tous les actes civils sont dans le dossier [`actes/contentieux-civil/`](actes/contentieux-civil/).

| Document | Description |
|----------|-------------|
| [STRATEGIE Contentieux Civil](actes/contentieux-civil/STRATEGIE%20Contentieux%20Civil.md) | Stratégie globale, fondements juridiques, évaluation Dintilhac 58 100 € |
| [ASSIGNATION Refere Provision](actes/contentieux-civil/ASSIGNATION%20Refere%20Provision.md) | Assignation référé 5 000 € + expertise médicale |
| [ACTION Directe Assureur RC](actes/contentieux-civil/ACTION%20Directe%20Assureur%20RC.md) | Mise en demeure fondée sur l'art. L.124-3 C. assur. |
| [ETUDE Indemnisation MAX](actes/contentieux-civil/ETUDE%20Indemnisation%20MAX.md) | Évaluation Dintilhac complète (58 100 €) |
| [ANALYSE Correction Juridique](actes/contentieux-civil/ANALYSE%20Correction%20Juridique.md) | Mémorandum d'audit et restructuration |
| [ANALYSE Jurisprudence](actes/contentieux-civil/ANALYSE%20Jurisprudence.md) | Analyse des préjudices et jurisprudences |

### Contentieux pénal

Tous les actes pénaux sont dans le dossier [`actes/contentieux-penal/`](actes/contentieux-penal/).

| Document | Description |
|----------|-------------|
| [STRATEGIE Contentieux Penal](actes/contentieux-penal/STRATEGIE%20Contentieux%20Penal.md) | Stratégie pénale, infractions, calendrier |
| [PLAINTE Complement Defaut Assurance RC](actes/contentieux-penal/PLAINTE%20Complement%20Defaut%20Assurance%20RC.md) | Complément plainte — défaut d'assurance RC |
| [CONSTITUTION Partie Civile](actes/contentieux-penal/CONSTITUTION%20Partie%20Civile.md) | Constitution de partie civile |
| [ANALYSE Plaidoirie Dirigeants](actes/contentieux-penal/ANALYSE%20Plaidoirie%20Dirigeants.md) | Faute détachable des dirigeants (Arrêt SATI) |
| [ANALYSE Responsabilites Legales](actes/contentieux-penal/ANALYSE%20Responsabilites%20Legales.md) | Fondements de la responsabilité |

### Transversaux

| Document | Description |
|----------|-------------|
| [PRESENTATION Dossier](actes/PRESENTATION%20Dossier.md) | Présentation complète du dossier |
| [INDEX Etat Final Dossier](actes/INDEX%20Etat%20Final%20Dossier.md) | Index récapitulatif |
| [PLAN Action Chronologie](actes/PLAN%20Action%20Chronologie.md) | Chronologie et plan d'action |
| [SYNTHESE FAQ](actes/SYNTHESE%20FAQ.md) | Synthèse juridique et questions fréquentes |

### Annexes

- [ANNEXE A — Lexique des jetons](actes/annexes/ANNEXE%20A%20Lexique%20Tokens.md)
- [ANNEXE B — Lois et Jurisprudence](actes/annexes/ANNEXE%20B%20Lois%20Jurisprudence.md)
- [ANNEXE C — Liste des pièces](actes/annexes/ANNEXE%20C%20Pieces.md)

## Pour les agents IA

- Lire [AGENTS.md](AGENTS.md) en premier, puis tous les fichiers dans `memory/`
- Google Jules : lire [JULES.md](JULES.md) pour le workflow d'injection et les MCP servers
- Gemini Code Assist : lire [GEMINI.md](GEMINI.md) pour le cycle de développement ADK
- **Respecter impérativement** `memory/RULES.md` (interdictions incluses)

## Conventions

| Règle | Description |
|-------|-------------|
| `=== PAGE BREAK ===` | Marqueur de saut de page dans les actes |
| `🔒 PIÈCE ORIGINALE` | Bandeau d'immutabilité sur les pièces |
| YAML front matter | Métadonnées sur tous les fichiers .md |
| Identifiant pièce | Triplet `(date, émetteur, objet)` |

## Dépendances techniques

Python 3.13+, uv, Google ADK, Terraform, Tesseract OCR français, Poppler-utils.
