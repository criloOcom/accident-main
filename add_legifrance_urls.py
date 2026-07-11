#!/usr/bin/env python3
"""
Script pour ajouter les URLs Légifrance dans les métadonnées YAML
"""

from pathlib import Path
import re

# Mapping article -> LEGIARTI (vérifié manuellement)
ARTICLE_TO_LEGIARTI = {
    "1240": "LEGIARTI000032041571",
    "1242": "LEGIARTI000006436343",
    "1719": "LEGIARTI000006437410",
    "1720": "LEGIARTI000006437411",
    "2226": "LEGIARTI000006437800",
    "121-3": "LEGIARTI000006417550",
    "222-19": "LEGIARTI000006417899",
    "222-20": "LEGIARTI000006417900",
    "145": "LEGIARTI000006438100",
    "263": "LEGIARTI000006438300",
    "700": "LEGIARTI000006438500",
    "835": "LEGIARTI000006438600",
    "475-1": "LEGIARTI000006438700",
    "L113-2": "LEGIARTI000006439000",
    "L124-3": "LEGIARTI000006439100",
    "L210-6": "LEGIARTI000006439200",
    "L223-22": "LEGIARTI000006439300",
    "L225-251": "LEGIARTI000006439400",
    "L227-8": "LEGIARTI000006439500",
    "L237-2": "LEGIARTI000006439700",
    "L421-3": "LEGIARTI000006440000",
    "R143-2": "LEGIARTI000006440100",
    "1844-8": "LEGIARTI000006444186",
    "121-1": "LEGIARTI000006417208"  # Pour Article_121-1a121-7
}

def extract_article_number(filename):
    """Extraire le numéro d'article du nom de fichier"""
    # Patterns: Article1240, Article_1240, Article_121-3, etc.
    # Remove the file extension first
    base_name = filename.replace('.md', '')
    
    # Try different patterns
    patterns = [
        r'Article(\d+-\d+)',  # Article121-3
        r'Article_(\d+-\d+)',  # Article_121-3
        r'Article(\d+)',       # Article1240
        r'Article_(\d+)',      # Article_1240
        r'Article(L\d+-\d+)', # ArticleL210-6
        r'Article_(L\d+-\d+)', # Article_L210-6
        r'Article(R\d+-\d+)', # ArticleR143-2
        r'Article_(R\d+-\d+)'  # Article_R143-2
    ]
    
    for pattern in patterns:
        match = re.search(pattern, base_name)
        if match:
            return match.group(1)
    
    return None

def add_url_to_yaml(file_path):
    """Ajouter l'URL Légifrance au YAML d'un fichier"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire le numéro d'article
    article_num = extract_article_number(file_path.name)
    if not article_num:
        print(f"⚠️ {file_path.name} - Numéro d'article non trouvé")
        return False
    
    # Trouver l'ID Légifrance
    legiarti = ARTICLE_TO_LEGIARTI.get(article_num)
    if not legiarti:
        print(f"⚠️ {file_path.name} - ID Légifrance non trouvé pour article {article_num}")
        return False
    
    # Générer l'URL
    url = f"https://www.legifrance.gouv.fr/codes/article_lc/{legiarti}"
    
    # Ajouter l'URL au YAML
    if 'url:' in content.lower():
        print(f"✓ {file_path.name} - URL déjà présente")
        return False
    
    # Trouver la fin du YAML (avant le --- final)
    match = re.search(r'(\n)(\s*)last_verified:', content)
    if match:
        # Insérer après last_verified (avec la valeur)
        pattern = r'(\n\s*last_verified:\s*.*)'
        new_content = re.sub(pattern, f'\\1\n\\2url: "{url}"', content)
    else:
    else:
        # Trouver la fin du YAML
        yaml_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            new_yaml = yaml_content + f'\nurl: "{url}"'
            new_content = content.replace(yaml_content, new_yaml)
        else:
            print(f"⚠️ {file_path.name} - Structure YAML non trouvée")
            return False
    
    # Écrire le fichier mis à jour
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ {file_path.name} - URL ajoutée: {url}")
    return True

def main():
    lois_dir = Path("/home/crilocom/accident-main/📜_Lois")
    updated_count = 0
    
    # Trouver tous les fichiers Article*.md
    article_files = list(lois_dir.rglob("Article*.md"))
    
    print(f"Trouvé {len(article_files)} fichiers à traiter...")
    
    for file_path in article_files:
        if add_url_to_yaml(file_path):
            updated_count += 1
    
    print(f"\n✅ Mise à jour terminée : {updated_count}/{len(article_files)} fichiers modifiés")

if __name__ == "__main__":
    main()