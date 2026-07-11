# Anchor — Accident Main

> **Mission:** Audit de conformité des articles de loi et fichiers de jurisprudence, puis injection YAML frontmatter.

---

## Work State

### Completed

- **24 articles de loi** vérifiés sur OpenLegi MCP — LEGIARTI identifiés, contenus confirmés
- **22 jurisprudences** vérifiées sur OpenLegi MCP + Légifrance-prod — JURITEXT identifiés (sauf 2 RNSM non indexés par l'API)
- **YAML frontmatter injecté** dans les 46 fichiers (`title`, `type`, `code`/`jurisdiction`, `article`/`pourvoi`, `legiarti`/`juritext`, `status`, `last_verified`)
- **Métadonnées corrigées :** chambre 11-15.699 (Com. → Soc.), 2 arrêts RNSM flaggés, fichier renommé
- **Art. 1242 CC** déjà à jour (version post-juin 2025 présente)
- **Script réutilisable** : `.dev/app/inject_frontmatter.py`

### Active

- Aucun blocage immédiat

### Next Move (à la demande)

- Surveiller l'abrogation différée de l'art. 475-1 CPP (prévue 2029)
- Programmer un ré-audit périodique via le script d'injection
