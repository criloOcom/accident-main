# AGENTS — Documentation Partagée

Ce fichier est le point d'entrée pour tous les agents (opencode, anti-gravity, etc.) travaillant sur le dossier Accident de la Main.

## Structure du projet

```
/home/crilocom/accident-main/
├── AGENTS.md              ← Ce fichier — point d'entrée des agents
├── README.md              ← Porte d'entrée publique — MAINTENIR À JOUR
├── actes/
│   ├── token/                 ← Versions tokenisées (travail courant)
│   │   ├── 00_Preuves_officielles/
│   │   ├── 01_Actes_proceduraux/
│   │   ├── 02_Courriers/
│   │   ├── 03_Analyses_juridiques/
│   │   ├── 04_Etudes_indemnisation/
│   │   ├── 05_Organisation/
│   │   └── 06_Archives/
│   └── reel/                  ← Versions réelles (identités réelles résolues)
├── memory/                ← Mémoire persistante partagée entre tous les agents
│   ├── VACCIN.md          ← 🔴 À LIRE EN PREMIER — obligatoire avant toute action
│   ├── STATUS.md          ← État d'avancement détaillé
│   ├── TODO.md            ← Plans restants et priorités
│   ├── WORKFLOW.md        ← Procédure d'anonymisation
│   ├── TOKEN MAP.md       ← Correspondance jeton ↔ identité réelle
│   ├── DECISIONS.md       ← Décisions d'architecture et règles
│   ├── RULES.md           ← Règles permanentes (INTERDICTIONS incluses)
│   ├── STRICT VARIABLES.md ← Source Unique de Vérité (dates, montants, faits)
│   ├── PIECES MAP.md      ← Correspondance document → pièces citées (Annexe C)
│   └── RAPPORT_*.md       ← Rapports d'audits, vérifications, synthèses
├── app/
│   ├── agent.py           ← Définition du multi-agent ADK
│   ├── batch_anonymize.py ← Script d'anonymisation (source officielle des tokens)
│   ├── tools.py           ← Outils MCP (Légifrance, Judilibre, Drive)
│   └── ...
├── skills/                ← Compétences partagées (à créer)
│   └── ...
└── ...
```

## Règles essentielles

0. 🔴 **Lire `memory/VACCIN.md` AVANT toute action** — protocole de vaccination
   obligatoire. Ne pas le lire constitue une faute professionnelle.
1. **Toute mémoire persistante** doit être dans `/home/crilocom/accident-main/memory/` — **PAS** dans un dossier privé d'agent
2. **Toute modification** de document Google Docs doit suivre le workflow décrit dans `memory/WORKFLOW.md`
3. **Les tokens d'anonymisation** sont définis dans `app/batch_anonymize.py` — toute modification des tokens doit être faite dans les DEUX endroits (script + TOKEN MAP.md)
4. **Compétences MCP** disponibles dans `/home/crilocom/.agents/skills/` :
   - `google-docs-linking` — insertion de liens Légifrance/Judilibre
   - `google-docs-design` — mise en page professionnelle
   - `accident-main-legal-research` — recherche juridique
   - `document-anonymization` — règles d'anonymisation
5. **Interdiction absolue** d'utiliser du markdown brut, regex, ou find/replace direct sur les Google Docs — toujours passer par le workflow local puis `replaceDocumentWithMarkdown`
6. **Google Sheets — RÈGLE ABSOLUE** : ne JAMAIS supposer la structure des colonnes. Avant d'écrire dans une feuille, **lis la ligne d'en-tête** et **3 lignes de données** pour valider le mapping exact. Supposer = cracher à la gueule de l'utilisateur.
7. **Double strate token/reel** : les fichiers dans `actes/token/` (dossiers 00-06) DOIVENT toujours rester tokenisés (identités anonymisées). Les versions réelles (noms, adresses, email réels) sont générées dans `actes/reel/` via `app/generate_real_versions.py` — ne JAMAIS écrire de version réelle dans `actes/token/`.
8. **GitHub Token** : stocké dans Google Secret Manager (`projects/crilo-prod-automation/secrets/GITHUB_TOKEN`). En local, il est aussi dans `~/.git-credentials` (solution de repli). Tout agent DOIT lire depuis Secret Manager, pas depuis une variable d'environnement ou un fichier `.env`.
9. **README.md** : doit être maintenu à jour après chaque modification de la structure du projet. C'est une consigne absolue — toute création/déplacement/suppression de dossier ou fichier notable doit être répercuté dans README.md.

## Workflow création d'un document

1. Lire l'original (readDocument) → `/tmp/`
2. Anonymiser (batch_anonymize.py) → `/tmp/`
3. Vérifier noms résiduels
4. Structurer en markdown (titres #, tokens **en gras**, sauts de ligne après points)
5. Injecter dans Google Docs (replaceDocumentWithMarkdown)
6. Appliquer styles (applyParagraphStyle JUSTIFIED, tailles police)
7. Ajouter hyperliens juridiques (applyTextStyle linkUrl) + vérifier avec MCP Légifrance
8. Vérifier (readDocument)
9. **Générer version réelle** : si le document doit exister en version réelle, le créer dans `actes/token/{dossier}/` puis lancer `python3 app/generate_real_versions.py`
10. **Mettre à jour README.md** si nouveau fichier notable ajouté

## Workflow maintien du dossier

1. Avant toute action : lire `memory/VACCIN.md` + `AGENTS.md` + `memory/STATUS.md`
2. Après toute modification de structure : **mettre à jour README.md**
3. Après toute création de document tokenisé : **générer version réelle** si nécessaire
4. Token GitHub indisponible ? Vérifier dans Secret Manager avant d'utiliser le fallback `~/.git-credentials`
