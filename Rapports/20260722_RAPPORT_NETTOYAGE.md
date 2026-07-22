# Rapport de Nettoyage

- Suppression des dossiers `__pycache__/`, `.pytest_cache/` et fichiers `*.pyc`.

- Déplacement du script `audit_acts.py` de la racine vers `.dev/app/audit_acts.py`.

- Suppression des fichiers `.bak`, `.backup`, `.orig`.

- Les fichiers vides ont été conservés (ex: `.gitkeep` pour maintenir les répertoires de tokens).

- Ajout de `.pytest_cache/` au fichier `.gitignore`.

- Vérification que le hook `pre-commit` est bien exécutable.

- Espace libéré : 0 octets

- Nombre de fichiers supprimés : 0
