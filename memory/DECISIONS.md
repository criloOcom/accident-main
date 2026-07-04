# DÉCISIONS CLÉS

## Tokens
- Utiliser le bon français avec articles : `[La Victime]` PAS `[Victime]`
- `[L'Exploitant du Commerce]` (pas "Salon" — on ne précise pas la nature du commerce)
- `[Le Préposé de l'Exploitation]` (pas "Coiffeur" — on ne précise pas le métier)
- Tous les jetons de la table sont corrects et validés

## Méthode locale validée
- Le workflow local (Python → .txt → .md → replaceDocumentWithMarkdown) a été validé
- Il est plus fiable que replaceAllText de l'API Google Docs (pas de décalage d'index)
- Le formatage (titres, listes, tables) est préservé par replaceDocumentWithMarkdown

## Références légales
- Les hyperliens sont ajoutés via applyTextStyle avec linkUrl
- L'annuaire des lois est dans le spreadsheet `14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ`

## Nettoyage initial
- 14 copies UNIFIE_ANONYME corrompues ont été supprimées du Drive
- Les fichiers .md résiduels ont été supprimés du Drive
- Le dossier ARCHIVES contient les originaux en sécurité

## Annexes dans UNIFIE_ANONYME — RÈGLE 2026-07-02
- **Les annexes contenant la correspondance jeton ↔ identité réelle ne doivent PAS être incluses dans les copies UNIFIE_ANONYME**
- Ces annexes (ANNEXE 1 — Tableau des acteurs) exposent les noms réels et annulent l'anonymisation
- Les docs 1, 2, 4 ont dû être corrigés a posteriori pour retirer ces annexes
- La table de correspondance est conservée uniquement dans TOKEN MAP.md (hors Drive)

## Identifiants des pièces — RÈGLE 2026-07-02
- **L'identifiant d'une pièce est le triplet (date, émetteur, objet)** — pas un numéro
- Les numéros de pièce du spreadsheet `1KNRJpDE24jpDXkLBTCZcVXsUbOueoe6Lg-7FJdM9jEE` sont **provisoires et non validés par l'utilisateur**
- Dans Annexe C : formater en `date — émetteur complet — objet — 🔗 Drive` sans numéro
- L'ordre de numérotation est inconnu de l'utilisateur — ne pas l'utiliser comme source de vérité

## Limitations du script batch_anonymize.py
- Utilise `str.replace()` → ne capture que les chaînes exactes
- Les prénoms seuls ("Sébastien") et les noms en casse mixte ("Mountasser Sabir") ne sont pas remplacés
- Doc 11 a nécessité une correction manuelle pour les noms résiduels
- **À améliorer (optionnel)** : passer à une approche regex insensible à la casse
