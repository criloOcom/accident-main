---
title: "WORKFLOW D'ANONYMIZATION"
description: "1. **Lire** l'original avec `readDocument` (format text)"
type: memory
---
<!-- Breadcrumb -->
*[🏠](../README.md) › [🧠 Memory](./README.md)*
<hr>
<!-- /Breadcrumb -->

# WORKFLOW D'ANONYMIZATION

## RÉFÉRENCE DE FORMATAGE
- Toutes les conventions de formatage des fichiers `.md` sont définies dans [Memory/CONVENTIONS.md](CONVENTIONS.md) : ordre canonique, hiérarchie H1–H4, séparateurs `<hr><hr>`, citations, tokens, liens, pipeline d'unification.

- **Tout agent** DOIT lire CONVENTIONS.md avant de créer ou modifier un fichier `.md` dans le dépôt.

- Le script `.dev/app/normalize_sections.py` applique automatiquement la convention `<hr><hr>` sur tous les fichiers Token/Reel. Exécuter après toute modification structurelle.

## Pour chaque document original :
1. **Lire** l'original avec `readDocument` (format text)

2. **Copier** le fichier avec `copyFile` → nouveau nom = "UNIFIE_ANONYME - " + titre original

3. **Sauvegarder** le texte original dans `/tmp/original_docX.txt`

4. **Anonymiser** : `python3 /home/crilocom/accident-main/app/batch_anonymize.py /tmp/original_docX.txt /tmp/anonymized_docX.txt`

5. **Vérifier** le fichier anonymisé pour les noms résiduels (chercher prénoms, noms en casse mixte)

6. **Créer le markdown** avec structuration (titres #, sections ##, listes, ---)

7. **Injecter** avec `replaceDocumentWithMarkdown` sur le doc UNIFIE_ANONYME

8. **Vérifier** qu'aucun nom réel n'est visible (relire la copie UNIFIE_ANONYME avec `readDocument`)

## Après injection (application de la charte DESIGN.md) :
- **NE PAS** inclure l'ANNEXE 1 (tableau des acteurs) dans les copies UNIFIE_ANONYME — elle contient la correspondance token ↔ identité réelle

- Les tables de correspondance sont conservées dans TOKEN MAP.md (hors du Drive)

- **Appliquer la charte graphique** définie dans [Memory/DESIGN.md](DESIGN.md) :

  1. `applyParagraphStyle` → JUSTIFIED sur tout le document
  2. `applyTextStyle` → liens Légifrance/Judilibre sur les refs légales
  3. `applyTextStyle` → bold sur les tokens `[**[La Victime]**](../Memory/Tokens/token-victime-nom-complet.md)`, `**[L'Exploitant]**`, etc.
  4. Vérifier TITLE = 20pt CENTER (pas le 36pt par défaut)

## Scripts disponibles :
- `/home/crilocom/accident-main/app/batch_anonymize.py` — script de remplacement par chaînes exactes

## Fichiers temporaires :
- `/tmp/original_docX.txt` — texte brut original

- `/tmp/anonymized_docX.txt` — texte anonymisé

- `/tmp/verify_docX.txt` — texte vérifié (après correction manuelle si nécessaire)

## ÉTAPE OBLIGATOIRE : VÉRIFICATION CROSS-DOCUMENT
- Après toute modification d'un acte, d'une annexe, ou d'un fichier mémoire :

  1. `cd /home/crilocom/accident-main && python3 app/check_consistency.py`
  2. Le script signale les liens morts, tokens inconnus, LEGIARTI invalides, dates incohérentes
  3. Corriger les erreurs signalées avant de commit
  4. Vérifier que [Actes/Token/Archives/Archive - Stratégie Contentieux Civil.md](../Actes/Token/Archives/Archive%20-%20Strat%C3%A9gie%20Contentieux%20Civil.md) et [Actes/Token/Archives/Archive - Stratégie Contentieux Pénal.md](../Actes/Token/Archives/Archive%20-%20Strat%C3%A9gie%20Contentieux%20P%C3%A9nal.md) listent bien le nouvel acte

## Gestion des sessions Jules — CYCLE DE VIE
- Une session Jules est créée avec `jules_create_session` pour exécuter une tâche de code.

- **Surveiller** l'état avec `jules_get_session_state` — statuts : `busy` (travail en cours), `stable` (en attente), `failed` (erreur système).

- **Débloquer** les sessions bloquées en lisant l'état, puis en envoyant la réponse appropriée via `jules_send_reply_to_session`.

- **CLÔTURER IMPÉRATIVEMENT** toute session terminée par un message de clôture explicite.

  - Session réussie (PR créé, rapport reçu) → « Mission terminée, tu peux clôturer et archiver cette session. »
  - Session débloquée (réponse envoyée) → « Réponse envoyée ci-dessus. Tu peux continuer ou clôturer si fini. »
  - Session en échec irrécupérable → « Session en échec. Tu peux clôturer. »
- **Pourquoi c'est indispensable** : l'API REST Jules n'a pas de endpoint `delete` ou `archive`. Un message de clôture est le SEUL moyen de dire à l'agent que son travail est fini. Sans cela, l'agent reste en attente indéfinie.

- Google archivera automatiquement les sessions clôturées côté serveur.

## Pièges connus :
- `batch_anonymize.py` utilise `str.replace()` donc **ne capture pas** les variantes en casse mixte non listées

- Les noms en "Prénom Nom" (ex. "Mountasser Sabir" — ancien format inversé — ou "Sabir MOUNTASSER" — format correct) ne sont pas remplacés → à ajouter manuellement dans le script

- Les prénoms seuls ("Sébastien", "Catherine") ne sont pas dans la table → correction manuelle dans le markdown avant injection

- Vérifier les annexes des originaux qui contiennent des tableaux de correspondance (docs 1, 2, 4) → les supprimer des copies UNIFIE_ANONYME