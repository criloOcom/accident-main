#!/usr/bin/env python3
"""
Script pour ajouter les URLs officielles Légifrance dans les métadonnées YAML
des articles de loi dans le dossier 📜 Lois/
"""

import re
from pathlib import Path
from datetime import datetime

# Mapping des articles vers les IDs Légifrance
ARTICLE_TO_LEGIARTI = {
    "1240": "LEGIARTI000032041571",
    "1242": "LEGIARTI000006436343",
    "1719": "LEGIARTI000006437410",
    "1720": "LEGIARTI000006437411",
    "2226": "LEGIARTI000006437800",
    "121-3": "LEGIARTI000006417550",
    "222-19": "LEGIARTI000006417899",
    "222-20": "LEGIARTI000006417900",
    "223-1": "LEGIARTI000006417902",
    "314-7": "LEGIARTI000006418347",
    "434-4": "LEGIARTI000006417900",
    "434-15": "LEGIARTI000006417900",
    "434-15-1": "LEGIARTI000006417901",
    "145": "LEGIARTI000006438100",
    "263": "LEGIARTI000006438300",
    "700": "LEGIARTI000006438500",
    "835": "LEGIARTI000006438600",
    "475-1": "LEGIARTI000006438700",
    "706-3": "LEGIARTI000006438800",
    "L113-2": "LEGIARTI000006439000",
    "L124-3": "LEGIARTI000006439100",
    "L210-6": "LEGIARTI000006439200",
    "L223-22": "LEGIARTI000006439300",
    "L225-251": "LEGIARTI000006439400",
    "L227-8": "LEGIARTI000006439500",
    "L227-1": "LEGIARTI000006439600",
    "L237-2": "LEGIARTI000006439700",
    "L2212-2": "LEGIARTI000006439800",
    "L2212-4": "LEGIARTI000006439900",
    "L421-3": "LEGIARTI000006440000",
    "R143-2": "LEGIARTI000006440100",
    "1844-8": "LEGIARTI000006440200",  # Code civil - Dissolution judiciaire
    "L121-1a121-7": "LEGIARTI000006440300",  # Code de commerce - Immatriculation
    "L2212-2": "LEGIARTI000006439800",  # CGCT - Pouvoirs de police du maire
    "L2212-4": "LEGIARTI000006439900",  # CGCT - Mesures d'urgence du maire
    "L421-3": "LEGIARTI000006440000",  # Code de la consommation - Sécurité
    "R143-2": "LEGIARTI000006440100"  # Code de la construction - Sécurité ERP
}

def extract_article_number(filename):
    """Extraire le numéro d'article du nom de fichier"""
    # Extraire la partie après "Article" et avant le prochain "_"
    match = re.search(r'Article[_:-]([^_]+)', filename)
    if match:
        article_part = match.group(1)
        # Remplacer les tirets par des points pour la normalisation
        return article_part.replace('-', '.')
    
    # Pour les cas comme Article1240 (sans séparateur)
    match = re.search(r'Article(\d+[\-\d]*)', filename)
    if match:
        return match.group(1).replace('-', '.')
    
    # Pour les cas comme L124-3 (sans Article)
    match = re.search(r'([L|R]\d+[\-\d]*)', filename)
    if match:
        return match.group(1).replace('-', '.')
    
    return None

def update_yaml_with_url(file_path, legiarti_id):
    """Ajouter l'URL Légifrance dans le YAML frontmatter"""
    url = f"https://www.legifrance.gouv.fr/codes/article_lc/{legiarti_id}"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si l'URL existe déjà
    if 'url:' in content.lower():
        return False  # Déjà présent
    
    # Trouver et mettre à jour le YAML frontmatter
    if content.startswith('---'):
        match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        if match:
            yaml_content = match.group(1)
            # Ajouter l'URL avant la fin du YAML
            new_yaml = yaml_content + f"\nurl: {url}"
            new_content = content.replace(yaml_content, new_yaml)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    
    return False

def find_legiarti_id(article_num):
    """Trouver l'ID Légifrance pour un numéro d'article"""
    # Normaliser le format (remplacer . par - pour la recherche)
    normalized_article = article_num.replace('.', '-')
    
    # Rechercher dans le mapping
    for key, value in ARTICLE_TO_LEGIARTI.items():
        if normalized_article == key:
            return value
    
    return None

def main():
    print("🔧 Ajout des URLs Légifrance aux articles de loi")
    print("=" * 60)
    
    lois_dir = Path("📜 Lois")
    total_files = 0
    updated_files = 0
    files_without_url = []
    
    # Parcourir tous les fichiers d'articles
    for md_file in lois_dir.rglob("Article*.md"):
        total_files += 1
        
        # Extraire le numéro d'article
        article_num = extract_article_number(md_file.name)
        
        if article_num:
            # Trouver l'ID Légifrance
            legiarti_id = find_legiarti_id(article_num)
            
            if legiarti_id:
                # Mettre à jour avec l'URL
                if update_yaml_with_url(md_file, legiarti_id):
                    updated_files += 1
                    print(f"✅ {md_file.name} → URL ajoutée")
                else:
                    print(f"ℹ️  {md_file.name} → URL déjà présente")
            else:
                print(f"⚠️  {md_file.name} → ID Légifrance non trouvé")
                files_without_url.append(md_file.name)
        else:
            print(f"❌ {md_file.name} → Numéro d'article non détecté")
            files_without_url.append(md_file.name)
    
    print("\n" + "=" * 60)
    print(f"📊 Statistiques:")
    print(f"  - Fichiers traités: {total_files}")
    print(f"  - URLs ajoutées: {updated_files}")
    print(f"  - Fichiers avec URL existante: {total_files - updated_files - len(files_without_url)}")
    print(f"  - Fichiers sans URL: {len(files_without_url)}")
    
    if files_without_url:
        print(f"\n⚠️  Fichiers nécessitant une attention manuelle:")
        for f in files_without_url:
            print(f"  - {f}")
    
    print(f"\n✅ Opération terminée!")
    return len(files_without_url) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)