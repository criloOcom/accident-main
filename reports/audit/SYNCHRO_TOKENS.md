# SYNCHRONISATION TOKEN MAP ↔ BATCH_ANONYMIZE.PY

## Méthodologie

Une analyse programmatique a été effectuée pour comparer les tokens utilisés dans `app/batch_anonymize.py` avec ceux documentés dans `memory/TOKEN MAP.md`.

*   **Extraction côté Python :** Un script a extrait tous les éléments cibles de remplacement (colonne de droite de la table `REPLACEMENTS`) dont la valeur débute par `[`.
*   **Extraction côté Markdown :** Un script a parcouru tous les tableaux du document `TOKEN MAP.md` pour extraire les tokens formatés selon la syntaxe Markdown `[Token]`.

## Résultats de la comparaison

*   **Tokens présents dans `app/batch_anonymize.py` mais avec une orthographe différente du `TOKEN MAP.md` :**
    *   `[LA VILLE DE L'ACCIDENT]` dans le script (au lieu de `[La Ville de l'Accident]` comme défini dans le MAP).
*   **Tokens présents dans `TOKEN MAP.md` mais inactifs dans `app/batch_anonymize.py` :**
    *   `[Nom de l'Avocat de la Victime]` (ce token était documenté dans le MAP mais commenté dans le script Python).

## Corrections apportées

Pour garantir une stricte correspondance entre les deux fichiers (nom de token et casse identiques) :

1.  **Harmonisation de la casse pour la ville de l'accident :**
    Dans `app/batch_anonymize.py`, le remplacement `("FOIX", "[LA VILLE DE L'ACCIDENT]")` a été corrigé en `("FOIX", "[La Ville de l'Accident]")` pour correspondre précisément à la déclaration du `TOKEN MAP.md`.
2.  **Activation du token pour l'avocat :**
    Dans `app/batch_anonymize.py`, la ligne commentée `# ("Nom Prénom de l'Avocat", "[Nom de l'Avocat de la Victime]"),` a été décommentée, rendant le token `[Nom de l'Avocat de la Victime]` actif dans le script d'anonymisation.

Les deux fichiers partagent désormais une liste de tokens strictement identiques.
