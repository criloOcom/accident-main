# Accident de la Main — Dossier Juridique

**Contentieux civil et pénal** suite à un accident corporel survenu le 29 mai 2026 dans un commerce (section nerveuse/tendineuse de la main droite, défaut d'assurance RC, préjudices estimés à 58 100 €).

## Navigation rapide

- **[STRATEGIE Contentieux Civil](actes/STRATEGIE%20Contentieux%20Civil.md)** — actions civiles, référé-provision, action directe assureur, expertise médicale
- **[STRATEGIE Contentieux Penal](actes/STRATEGIE%20Contentieux%20Penal.md)** — plaintes, constitution partie civile, défaut assurance
- **[Index complet du dossier](actes/Index%20Etat%20Final%20Dossier.md)** — état final, récapitulatif de toutes les pièces et actes
- **[Plan d'action et chronologie](actes/Plan%20Action%20Chronologie.md)** — calendrier des prochaines étapes
- **[Synthèse juridique et FAQ](actes/Synthese%20FAQ.md)** — questions/réponses sur l'affaire

## Arborescence

```
accident-main/
├── actes/                  ← Documents juridiques (.md)
│   ├── annexes/            ← Annexes (A: lexique, B: lois, C: pièces)
│   ├── STRATEGIE Contentieux Civil.md
│   ├── STRATEGIE Contentieux Penal.md
│   ├── ANALYSE Correction Juridique.md
│   ├── ANALYSE Jurisprudence.md
│   ├── ANALYSE Plaidoirie Dirigeants.md
│   ├── ANALYSE Responsabilites Legales.md
│   └── ...
├── pieces/                 ← 19 pièces originales extraites des PDFs
├── memory/                 ← Mémoire persistante pour les agents IA
└── app/                    ← Scripts Python
```

## Documents

### Contentieux civil

| Document | Description |
|----------|-------------|
| [STRATEGIE Contentieux Civil](actes/STRATEGIE%20Contentieux%20Civil.md) | Stratégie globale, fondements juridiques, évaluation Dintilhac 58 100 € |
| [Assignation Refere Provision FINAL](actes/Assignation%20Refere%20Provision%20FINAL.md) | Assignation référé 5 000 € + expertise médicale |
| [Action Directe Assureur RC](actes/Action%20Directe%20Assureur%20RC.md) | Mise en demeure fondée sur l'art. L.124-3 C. assur. |
| [Etude Indemnisation MAX](actes/Etude%20Indemnisation%20MAX.md) | Évaluation Dintilhac complète (58 100 €) |
| [ANALYSE Correction Juridique](actes/ANALYSE%20Correction%20Juridique.md) | Mémorandum d'audit et restructuration |
| [ANALYSE Jurisprudence](actes/ANALYSE%20Jurisprudence.md) | Analyse des préjudices et jurisprudences |

### Contentieux pénal

| Document | Description |
|----------|-------------|
| [STRATEGIE Contentieux Penal](actes/STRATEGIE%20Contentieux%20Penal.md) | Stratégie pénale, infractions, calendrier |
| [Plainte Complement Defaut Assurance RC](actes/Plainte%20Complement%20Defaut%20Assurance%20RC.md) | Complément plainte — défaut d'assurance RC |
| [Constitution Partie Civile](actes/Constitution%20Partie%20Civile.md) | Constitution de partie civile |
| [ANALYSE Plaidoirie Dirigeants](actes/ANALYSE%20Plaidoirie%20Dirigeants.md) | Faute détachable des dirigeants (Arrêt SATI) |
| [ANALYSE Responsabilites Legales](actes/ANALYSE%20Responsabilites%20Legales.md) | Fondements de la responsabilité |

### Transversaux

| Document | Description |
|----------|-------------|
| [Presentation Dossier](actes/Presentation%20Dossier.md) | Présentation complète du dossier |
| [Index Etat Final Dossier](actes/Index%20Etat%20Final%20Dossier.md) | Index récapitulatif |
| [Plan Action Chronologie](actes/Plan%20Action%20Chronologie.md) | Chronologie et plan d'action |
| [Synthese FAQ](actes/Synthese%20FAQ.md) | Synthèse juridique et questions fréquentes |

### Annexes

- [ANNEXE A — Lexique des jetons](actes/annexes/ANNEXE%20A%20Lexique%20Tokents.md)
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
