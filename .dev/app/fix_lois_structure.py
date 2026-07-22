#!/usr/bin/env python3
"""
Script pour corriger la structure des fichiers dans Lois/
1. Corriger la nomenclature des breadcrumbs (🏠 au lieu de 🏠 HUB)
2. Ajouter des README.md dans chaque dossier
3. Réorganiser les articles de loi dans les bons dossiers
4. Ajouter des métadonnées YAML
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path("/home/crilocom/accident-main/Lois")
CODE_PENAL_ARTICLES = [
    "121-3", "221-1", "222-19", "222-20", "223-1", "314-7", "434-4", "434-15", "434-15-1"
]
CODE_CIVIL_ARTICLES = ["1240", "1242", "1719", "1720", "2226"]
CODE_PROCEDURE_CIVILE_ARTICLES = ["145", "263", "700", "835"]
CODE_PROCEDURE_PENALE_ARTICLES = ["475-1", "706-3"]
CODE_ASSURANCES_ARTICLES = ["L113-2", "L124-3"]
CODE_COMMERCE_ARTICLES = ["L210-6", "L223-22", "L225-251", "L227-1", "L227-8", "L237-2"]

def fix_breadcrumb_content(content):
    """Corriger la nomenclature des breadcrumbs"""
    # Remplacer 🏠 HUB par 🏠
    content = re.sub(r'🏠 \[HUB\]', '🏠', content)
    content = re.sub(r'🏠\[Accueil\]\.\.\.\.\.\.\/README\.md', '🏠 [Accueil](../README.md)', content)
    return content

def add_yaml_frontmatter(content, title, code, article):
    """Ajouter des métadonnées YAML"""
    yaml_text = f"""title: {title}
code: {code}
article: {article}
date: {datetime.now().strftime('%Y-%m-%d')}
source: Légifrance
status: En vigueur"""
    
    # Vérifier si YAML existe déjà
    if content.startswith('---'):
        # Extraire le frontmatter existant
        match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
        if match:
            return content  # Garder le YAML existant
    
    return f"---\n{yaml_text}\n---\n\n{content}"

def create_readme_for_directory(dir_path, parent_readme_path):
    """Créer un README.md pour un dossier"""
    dir_name = dir_path.name
    parent_depth = parent_readme_path.count('../') + 1
    
    breadcrumb = ' > '.join(['🏠'] + ['[📁 ' + p.name + '](../README.md)' for p in dir_path.parents if p != BASE_DIR] + ['[📄 README.md](./README.md)'])
    
    readme_content = f"""# {dir_name}

```
{breadcrumb}
```

---

**Dossier contenant les articles de loi relatifs à {dir_name}.**

## Liste des articles

"""
    
    # Lister les fichiers Markdown
    md_files = sorted([f for f in dir_path.glob('*.md') if f.name != 'README.md'])
    
    for md_file in md_files:
        # Extraire le numéro d'article du nom de fichier
        match = re.search(r'Article[_:-]([^_\-\.]+)', md_file.name)
        if match:
            article_num = match.group(1).replace('-', '.')
            readme_content += f"- [{article_num}]({md_file.name})\n"
    
    readme_content += f"\n---\n\n> **Dernière mise à jour :** {datetime.now().strftime('%d %B %Y')}\n"
    
    with open(dir_path / 'README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

def reorganize_articles():
    """Réorganiser les articles dans les bons dossiers"""
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
                print(f"Déplacé: {filename} → {target_dir.name}/")

def process_directory(directory):
    """Traiter tous les fichiers Markdown dans un dossier"""
    for md_file in directory.glob('*.md'):
        if md_file.name == 'README.md':
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corriger les breadcrumbs
        new_content = fix_breadcrumb_content(content)
        
        # Extraire le numéro d'article pour les métadonnées
        article_match = re.search(r'Article[_:-]([^_\-\.]+)', md_file.name)
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
        
        print(f"Traité: {directory.name}/{md_file.name}")

def main():
    print("🔧 Correction de la structure des fichiers dans Lois/")
    print("=" * 60)
    
    # 1. Réorganiser les articles
    print("\n1. Réorganisation des articles de loi...")
    reorganize_articles()
    
    # 2. Créer des README.md pour chaque dossier
    print("\n2. Création des README.md pour chaque dossier...")
    for dir_path in BASE_DIR.iterdir():
        if dir_path.is_dir() and not (dir_path / 'README.md').exists():
            parent_depth = len(list(dir_path.parents)) - len(list(BASE_DIR.parents))
            create_readme_for_directory(dir_path, '../README.md' * parent_depth)
            print(f"Créé: {dir_path.name}/README.md")
    
    # 3. Traiter tous les fichiers Markdown
    print("\n3. Correction des breadcrumbs et ajout des métadonnées YAML...")
    for dir_path in BASE_DIR.iterdir():
        if dir_path.is_dir():
            process_directory(dir_path)
    
    # 4. Mettre à jour le README principal
    print("\n4. Mise à jour du README principal...")
    update_main_readme()
    
    print("\n✅ Correction terminée!")

def update_main_readme():
    """Mettre à jour le README principal de Lois"""
    readme_path = BASE_DIR / "README.md"
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corriger les breadcrumbs
    content = fix_breadcrumb_content(content)
    
    # Mettre à jour les comptes d'articles
    code_penal_count = len(list((BASE_DIR / "Code penal").glob("Article*.md")))
    code_civil_count = len(list((BASE_DIR / "Code_civil").glob("Article*.md")))
    code_proc_civile_count = len(list((BASE_DIR / "Code procedure civile").glob("Article*.md")))
    code_proc_penale_count = len(list((BASE_DIR / "Code procedure penale").glob("Article*.md")))
    code_assurances_count = len(list((BASE_DIR / "Code_assurances").glob("Article*.md")))
    code_commerce_count = len(list((BASE_DIR / "Code_commerce").glob("Article*.md")))
    autres_codes_count = len(list((BASE_DIR / "Autres_codes").glob("Article*.md")))
    
    # Mettre à jour les comptes
    content = re.sub(r'### Code_pénal \(\d+ articles\)', f'### Code_pénal ({code_penal_count} articles)', content)
    content = re.sub(r'### Code_civil \(\d+ articles\)', f'### Code_civil ({code_civil_count} articles)', content)
    content = re.sub(r'### Code de procédure civile \(\d+ articles\)', f'### Code de procédure civile ({code_proc_civile_count} articles)', content)
    content = re.sub(r'### Code de procédure pénale \(\d+ articles\)', f'### Code de procédure pénale ({code_proc_penale_count} articles)', content)
    content = re.sub(r'### Code des assurances \(\d+ articles\)', f'### Code des assurances ({code_assurances_count} articles)', content)
    content = re.sub(r'### Code de commerce \(\d+ articles\)', f'### Code de commerce ({code_commerce_count} articles)', content)
    content = re.sub(r'### Autres_codes \(\d+ articles\)', f'### Autres_codes ({autres_codes_count} articles)', content)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Mis à jour: README.md principal")

if __name__ == "__main__":
    main()