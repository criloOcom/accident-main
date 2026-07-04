# AGENTS — Documentation Partagée

Ce fichier est le point d'entrée pour tous les agents (opencode, anti-gravity, etc.) travaillant sur le dossier Accident de la Main.

## Structure du projet

```
/home/crilocom/accident-main/
├── AGENTS.md              ← Ce fichier — point d'entrée des agents
├── memory/                ← Mémoire persistante partagée entre tous les agents
│   ├── STATUS.md          ← État d'avancement détaillé
│   ├── WORKFLOW.md        ← Procédure d'anonymisation
│   ├── TOKEN MAP.md       ← Correspondance jeton ↔ identité réelle
│   ├── DECISIONS.md       ← Décisions d'architecture et règles
│   ├── RULES.md           ← Règles permanentes (INTERDICTIONS incluses)
│   ├── STRICT VARIABLES.md ← Source Unique de Vérité (dates, montants, faits)
│   └── PIECES MAP.md      ← Correspondance document → pièces citées (Annexe C)
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

1. **Toute mémoire persistante** doit être dans `/home/crilocom/accident-main/memory/` — **PAS** dans un dossier privé d'agent
2. **Toute modification** de document Google Docs doit suivre le workflow décrit dans `memory/WORKFLOW.md`
3. **Les tokens d'anonymisation** sont définis dans `app/batch_anonymize.py` — toute modification des tokens doit être faite dans les DEUX endroits (script + TOKEN MAP.md)
4. **Compétences MCP** disponibles dans `/home/crilocom/.agents/skills/` :
   - `google-docs-linking` — insertion de liens Légifrance/Judilibre
   - `google-docs-design` — mise en page professionnelle
   - `accident-main-legal-research` — recherche juridique
   - `document-anonymization` — règles d'anonymisation
5. **Interdiction absolue** d'utiliser du markdown brut, regex, ou find/replace direct sur les Google Docs — toujours passer par le workflow local puis `replaceDocumentWithMarkdown`

## Workflow rapide (voir memory/WORKFLOW.md pour le détail)

1. Lire l'original (readDocument) → /tmp/
2. Anonymiser (batch_anonymize.py) → /tmp/
3. Vérifier noms résiduels
4. Structurer en markdown (titres #, tokens **en gras**, sauts de ligne après points)
5. Injecter (replaceDocumentWithMarkdown)
6. Appliquer styles (applyParagraphStyle JUSTIFIED, tailles police)
7. Ajouter hyperliens juridiques (applyTextStyle linkUrl)
8. Vérifier (readDocument)
