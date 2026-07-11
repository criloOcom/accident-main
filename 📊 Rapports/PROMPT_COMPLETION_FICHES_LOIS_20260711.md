---
title: "PROMPT — Complétion des 5 fiches 📜 Lois (MCP Légifrance)"
description: "Prompt à confier à l'agent disposant du MCP Légifrance/Judilibre pour compléter le corps des 5 fiches marquées À VÉRIFIER."
type: rapport
---





<!-- Breadcrumb -->
[🏠](../README.md) › [📊 Rapports et Analyses](./README.md) › PROMPT COMPLETION FICHES LOIS 20260711
<!-- /Breadcrumb -->

# PROMPT — Complétion des 5 fiches 📜 Lois

## Contexte
5 fiches ont été créées dans [📜 Lois](📜%20Lois/README.md) avec un frontmatter valide mais un corps marqué `⚠️ À VÉRIFIER` (texte légal non récupéré car Légifrance était bloqué par Cloudflare dans l'environnement de création). Leur nom de fichier et leur emplacement respectent déjà les liens du [📜 Lois/README.md](📜%20Lois/README.md), donc les liens ne sont PAS morts — seul le corps légal est à compléter.

## Règle absolue (Règle #16 + JURITEXT_PROTOCOL)
**NE JAMAIS deviner un texte de loi.** Chaque article/arrêt doit être vérifié via le MCP Légifrance (ou Judilibre) AVANT écriture. Si introuvable, conserver le marqueur `À VÉRIFIER` et le signaler. Ne PAS publier de texte non sourcé.

## Fichiers à compléter (avec emplacement exact)
1. [📜 Lois/📒 Autres codes/Article_223-1_Code_Legifrance.md](📜%20Lois/📒%20Autres%20codes/Article_223-1_Code_Legifrance.md)
   → Art. 223-1 Code pénal — Mise en danger d'autrui.
2. [📜 Lois/📒 Autres codes/Article_L123-2_Code_Legifrance.md](📜%20Lois/📒%20Autres%20codes/Article_L123-2_Code_Legifrance.md)
   → Art. L. 123-2 Code de commerce — Immatriculation des commerçants au RCS.
3. [📜 Lois/📒 Autres codes/Article_L611-3_Code_Legifrance.md](📜%20Lois/📒%20Autres%20codes/Article_L611-3_Code_Legifrance.md)
   → Art. L. 611-3 Code de commerce — Ouverture de la procédure de sauvegarde.
4. [📜 Lois/📒 Code commerce/Article_L227-1_Code_Legifrance.md](📜%20Lois/📒%20Code%20commerce/Article_L227-1_Code_Legifrance.md)
   → Art. L. 227-1 Code de commerce — Pouvoirs du président de la SAS.
5. [📜 Lois/📜 Jurisprudence/17-26.282_CourCassation.md](📜%20Lois/📜%20Jurisprudence/17-26.282_CourCassation.md)
   → Arrêt 17-26.282, Civ. 2e, Cour de cassation (thème : réserve d'aggravation / incidence professionnelle).

## Procédure pour chaque fichier
1. Interroger le MCP Légifrance (ou Judilibre) avec le numéro d'article / le numéro de pourvoiExact.
2. Récupérer le texte officiel EN VIGUEUR (version consolidée à la date du jour).
3. Remplacer le bloc suivant (dans le corps, après le `---` de fermeture du frontmatter) :
   ```
   ⚠️ **À VÉRIFIER** — ... (bloc entier jusqu'à la fin du fichier)
   ```
   par la structure standard utilisée dans les fiches existantes (ex. [📜 Lois/📒 Autres codes/Article_121-3_Code_Legifrance.md](📜%20Lois/📒%20Autres%20codes/Article_121-3_Code_Legifrance.md)) :
   - `> **Nature** : Code` (ou `Jurisprudence`)
   - `---`
   - Pour un article : `CODE\nVERSION EN VIGUEUR AU <date>\n\nArticle <num>\n<texte officiel>`
   - Pour un arrêt : en-tête (date, chambre, pourvoi, ECLI) + `Texte de la décision` + corps.
4. **Ne toucher QU'AU CORPS** — conserver le frontmatter (title/description/type/date/source/code/article) et le fil d'Ariane (`<!-- Breadcrumb -->`).
5. Pour l'arrêt 17-26.282 : récupérer la date exacte de rendu et mettre à jour le champ `description` du frontmatter (actuellement « À VÉRIFIER — date de rendu à confirmer »).

## Vérification finale à fournir
- Les 5 fichiers ne contiennent plus de marqueur `À VÉRIFIER`.
- Rejouer `python3 .dev/app/audit_readme_integrity.py` → 0 erreur.
- Rejouer `python3 .dev/app/check_consistency.py` → conforme.
- Signaler tout article/arrêt introuvable (le laisser `À VÉRIFIER` et lister).

## Interdictions
- Pas de texte inventé ou approximatif.
- Pas de modification du frontmatter (sauf `description` de l'arrêt 17-26.282 pour la date).
- Pas de lien absolu.