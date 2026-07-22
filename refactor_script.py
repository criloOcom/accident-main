import re

with open(".dev/app/fix_lois_structure.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace process_directory
new_process_dir = r"""
def process_markdown_file(md_file):
    \"\"\"Traiter un seul fichier Markdown\"\"\"
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Corriger les breadcrumbs
    new_content = fix_breadcrumb_content(content)

    # Extraire le numéro d'article pour les métadonnées
    article_match = re.search(r'Article[_:-]([^_\-]+)', md_file.name)
    article_num = article_match.group(1).replace('-', '.') if article_match else "Inconnu"

    # Déterminer le code
    directory = md_file.parent
    code = directory.name.replace('📒_', '').replace('_', ' ').title()

    # Extraire le titre
    title_match = re.search(r'^#\s+(.*?)\s*$', new_content, re.MULTILINE)
    title = title_match.group(1) if title_match else code

    # Ajouter YAML si nécessaire
    if not new_content.startswith('---'):
        new_content = add_yaml_frontmatter(new_content, title, code, article_num)

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Traité: {directory.name}/{md_file.name}")

def process_directory(directory):
    \"\"\"Traiter tous les fichiers Markdown dans un dossier\"\"\"
    for md_file in directory.glob('*.md'):
        if md_file.name == 'README.md':
            continue
        process_markdown_file(md_file)
"""

old_process_dir = r"""def process_directory(directory):
    \"\"\"Traiter tous les fichiers Markdown dans un dossier\"\"\"
    for md_file in directory.glob('*.md'):
        if md_file.name == 'README.md':
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Corriger les breadcrumbs
        new_content = fix_breadcrumb_content(content)

        # Extraire le numéro d'article pour les métadonnées
        article_match = re.search(r'Article[_:-]([^_\-]+)', md_file.name)
        article_num = article_match.group(1).replace('-', '.') if article_match else "Inconnu"

        # Déterminer le code
        code = directory.name.replace('📒_', '').replace('_', ' ').title()

        # Extraire le titre
        title_match = re.search(r'^#\s+(.*?)\s*$', new_content, re.MULTILINE)
        title = title_match.group(1) if title_match else code

        # Ajouter YAML si nécessaire
        if not new_content.startswith('---'):
            new_content = add_yaml_frontmatter(new_content, title, code, article_num)

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"Traité: {directory.name}/{md_file.name}")"""

content = content.replace(old_process_dir, new_process_dir.strip())


# Replace reorganize_articles
new_reorg = r"""
def get_target_directory(filename):
    \"\"\"Déterminer le dossier cible pour un fichier article\"\"\"
    # Vérifier Code pénal
    for article in CODE_PENAL_ARTICLES:
        if article.replace('-', '_') in filename or article.replace('-', '') in filename:
            return BASE_DIR / "Code penal"

    # Vérifier Code civil
    for article in CODE_CIVIL_ARTICLES:
        if article in filename:
            return BASE_DIR / "Code_civil"

    # Vérifier Code de procédure civile
    for article in CODE_PROCEDURE_CIVILE_ARTICLES:
        if article in filename or f"Article{article}" in filename:
            return BASE_DIR / "Code procedure civile"

    # Vérifier Code de procédure pénale
    for article in CODE_PROCEDURE_PENALE_ARTICLES:
        if article in filename or f"Article{article}" in filename:
            return BASE_DIR / "Code procedure penale"

    # Vérifier Code des assurances
    for article in CODE_ASSURANCES_ARTICLES:
        if article in filename:
            return BASE_DIR / "Code_assurances"

    # Vérifier Code de commerce
    for article in CODE_COMMERCE_ARTICLES:
        if article.replace('-', '_') in filename or article.replace('-', '') in filename:
            return BASE_DIR / "Code_commerce"

    return None

def reorganize_articles():
    \"\"\"Réorganiser les articles dans les bons dossiers\"\"\"
    autres_codes = BASE_DIR / "Autres_codes"

    if not autres_codes.exists():
        return

    for md_file in autres_codes.glob('Article*.md'):
        filename = md_file.name
        target_dir = get_target_directory(filename)

        # Si un dossier cible est trouvé, déplacer le fichier
        if target_dir and target_dir.exists():
            new_path = target_dir / filename
            if not new_path.exists():
                md_file.rename(new_path)
                print(f"Déplacé: {filename} → {target_dir.name}/")
"""

old_reorg = r"""def reorganize_articles():
    \"\"\"Réorganiser les articles dans les bons dossiers\"\"\"
    autres_codes = BASE_DIR / "Autres_codes"

    if not autres_codes.exists():
        return

    for md_file in autres_codes.glob('Article*.md'):
        filename = md_file.name

        # Déterminer le bon dossier
        target_dir = None

        # Vérifier Code pénal
        for article in CODE_PENAL_ARTICLES:
            if article.replace('-', '_') in filename or article.replace('-', '') in filename:
                target_dir = BASE_DIR / "Code penal"
                break

        # Vérifier Code civil
        if not target_dir:
            for article in CODE_CIVIL_ARTICLES:
                if article in filename:
                    target_dir = BASE_DIR / "Code_civil"
                    break

        # Vérifier Code de procédure civile
        if not target_dir:
            for article in CODE_PROCEDURE_CIVILE_ARTICLES:
                if article in filename or f"Article{article}" in filename:
                    target_dir = BASE_DIR / "Code procedure civile"
                    break

        # Vérifier Code de procédure pénale
        if not target_dir:
            for article in CODE_PROCEDURE_PENALE_ARTICLES:
                if article in filename or f"Article{article}" in filename:
                    target_dir = BASE_DIR / "Code procedure penale"
                    break

        # Vérifier Code des assurances
        if not target_dir:
            for article in CODE_ASSURANCES_ARTICLES:
                if article in filename:
                    target_dir = BASE_DIR / "Code_assurances"
                    break

        # Vérifier Code de commerce
        if not target_dir:
            for article in CODE_COMMERCE_ARTICLES:
                if article.replace('-', '_') in filename or article.replace('-', '') in filename:
                    target_dir = BASE_DIR / "Code_commerce"
                    break

        # Si un dossier cible est trouvé, déplacer le fichier
        if target_dir and target_dir.exists():
            new_path = target_dir / filename
            if not new_path.exists():
                md_file.rename(new_path)
                print(f"Déplacé: {filename} → {target_dir.name}/")"""

content = content.replace(old_reorg, new_reorg.strip())

with open(".dev/app/fix_lois_structure.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Refactored successfully")
