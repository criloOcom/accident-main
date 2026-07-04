# WORKFLOW D'ANONYMIZATION

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
- **NE PAS** inclure l'ANNEXE 1 (tableau des acteurs) dans les copies UNIFIE_ANONYME — elle contient la correspondance jeton ↔ identité réelle
- Les tables de correspondance sont conservées dans TOKEN_MAP.md (hors du Drive)
- **Appliquer la charte graphique** définie dans `memory/DESIGN.md` :
  1. `applyParagraphStyle` → JUSTIFIED sur tout le document
  2. `applyTextStyle` → liens Légifrance/Judilibre sur les refs légales
  3. `applyTextStyle` → bold sur les tokens `[La Victime]`, `[L'Exploitant]`, etc.
  4. Vérifier TITLE = 20pt CENTER (pas le 36pt par défaut)

## Scripts disponibles :
- `/home/crilocom/accident-main/app/batch_anonymize.py` — script de remplacement par chaînes exactes

## Fichiers temporaires :
- `/tmp/original_docX.txt` — texte brut original
- `/tmp/anonymized_docX.txt` — texte anonymisé
- `/tmp/verify_docX.txt` — texte vérifié (après correction manuelle si nécessaire)

## Pièges connus :
- `batch_anonymize.py` utilise `str.replace()` donc **ne capture pas** les variantes en casse mixte non listées
- Les noms en "Prénom Nom" (ex. "Mountasser Sabir" au lieu de "Mountasser SABIR") ne sont pas remplacés → à ajouter manuellement dans le script
- Les prénoms seuls ("Sébastien", "Catherine") ne sont pas dans la table → correction manuelle dans le markdown avant injection
- Vérifier les annexes des originaux qui contiennent des tableaux de correspondance (docs 1, 2, 4) → les supprimer des copies UNIFIE_ANONYME
