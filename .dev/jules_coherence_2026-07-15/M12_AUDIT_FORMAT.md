<!-- Breadcrumb -->
*[🏠](../../README.md) › [🛠️ Dev](../README.md) › [jules coherence 2026-07-15](./README.md)*
<hr>
<!-- /Breadcrumb -->

# MISSION 12 — Audit de format et conventions

[PREAMBULE COMMUN — voir PROMPT_COMMUN.md]

## OBJECTIF

Vérifier que tous les fichiers respectent les conventions de format définies dans le dépôt (CONVENTIONS.md, RULES.md, conventions implicites des fichiers existants).

## MÉTHODE

1. **Vérifier** pour chaque fichier :
   - Présence de front matter YAML (--- title: ... description: ... ---)
   - Présence du breadcrumb HTML (../ pour les rapports, ../../ pour les actes)
   - Nommage conforme au pattern : `TYPE_OBJET.md` ou `NOM_FICHIER.md` en majuscules avec underscores
   - Pas d'espaces dans les noms de fichiers
   - Encodage UTF-8
   - Retours à la ligne Unix (LF) et pas Windows (CRLF)
   - Cohérence de la casse dans les répertoires (emoji présents)

2. **Vérifier** les emojis dans les noms de dossiers (🧠, ⚖️, 📊, 👤, etc.) — sont-ils bien présents ? Le bon emoji ?

3. **Signaler** tout fichier qui déroge.

## LIVRABLE

[Rapports/85_Coherence_20260715/M12_AUDIT_FORMAT.md](../../Rapports/85_Coherence_20260715/M12_AUDIT_FORMAT.md)