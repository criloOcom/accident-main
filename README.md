# Accident de la Main — Dossier Juridique

**Contentieux civil et pénal** suite à un accident corporel survenu le 29 mai 2026 dans un commerce (section nerveuse/tendineuse de la main droite, défaut d'assurance RC, préjudices estimés à 58 100 €).

## Navigation rapide

- **[Contentieux Civil](actes/15_Strategie_Contentieux_Civil.md)** — actions civiles, référé-provision, action directe assureur, expertise médicale
- **[Contentieux Pénal](actes/16_Strategie_Contentieux_Penal.md)** — plaintes, constitution partie civile, défaut assurance
- **[Index complet du dossier](actes/08_Index_EtatFinal_Dossier.md)** — état final, récapitulatif de toutes les pièces et actes
- **[Plan d'action et chronologie](actes/09_PlanAction_Chronologie.md)** — calendrier des prochaines étapes
- **[Synthèse juridique et FAQ](actes/10_Synthese_FAQ.md)** — questions/réponses sur l'affaire

## Arborescence

```
accident-main/
├── actes/                  ← Documents juridiques (.md)
│   ├── annexes/            ← Annexes canoniques (A: lexique, B: lois, C: pièces)
│   ├── 15_Strategie_Contentieux_Civil.md
│   ├── 16_Strategie_Contentieux_Penal.md
│   └── 01_Assignation...md à 14_Analyse...md
├── pieces/                 ← 19 pièces originales extraites des PDFs
├── memory/                 ← Mémoire persistante pour les agents IA
└── app/                    ← Scripts Python
```

## Documents clés

### Contentieux civil

| Acte | Description |
|------|-------------|
| [01 — Assignation Référé-Provision](actes/01_Assignation_REFERE_PROVISION_FINAL.md) | Assignation référé 5 000 € + expertise médicale |
| [02 — Action Directe Assureur](actes/02_ActionDirecte_AssureurRC.md) | Mise en demeure fondée sur l'art. L.124-3 C. assur. |
| [04 — Projet Assignation V1](actes/04_Assignation_Refere_Provision_V1.md) | Version brouillon de l'assignation |
| [07 — Étude Indemnisation](actes/07_ETUDE_Indemnisation_MAX.md) | Évaluation Dintilhac (58 100 €) |
| [11 — Audit Stratégique](actes/11_ANALYSE_correction_juridique.md) | Mémorandum d'audit et restructuration |
| [12 — Analyse Jurisprudence](actes/12_ANALYSE_Jurisprudence.md) | Analyse des préjudices et jurisprudences |

### Contentieux pénal

| Acte | Description |
|------|-------------|
| [03 — Défaut Assurance](actes/03_Plainte_Complet_Defaut_Assurance.md) | Complément plainte — défaut d'assurance RC |
| [05 — Constitution Partie Civile](actes/05_Constitution_Partie_Civile.md) | Constitution de partie civile |
| [13 — Responsabilité Dirigeants](actes/13_ANALYSE_Plaidoirie_Dirigeants.md) | Faute détachable des dirigeants (Arrêt SATI) |
| [14 — Analyse Responsabilités](actes/14_ANALYSE_Responsabilites_Legales.md) | Fondements de la responsabilité |

### Transversaux

| Acte | Description |
|------|-------------|
| [06 — Dossier Présentation](actes/06_Dossier_Presentation.md) | Présentation complète du dossier |
| [08 — Index État Final](actes/08_Index_EtatFinal_Dossier.md) | Index récapitulatif |
| [09 — Plan Action](actes/09_PlanAction_Chronologie.md) | Chronologie et plan d'action |
| [10 — Synthèse FAQ](actes/10_Synthese_FAQ.md) | Synthèse juridique |

### Annexes (canoniques)

- [ANNEXE A — Lexique des jetons](actes/annexes/ANNEXE_A_Lexique_Tokens.md)
- [ANNEXE B — Lois et Jurisprudence](actes/annexes/ANNEXE_B_Lois_Jurisprudence.md)
- [ANNEXE C — Liste des pièces](actes/annexes/ANNEXE_C_Pieces.md)

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
