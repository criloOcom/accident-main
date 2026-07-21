#!/usr/bin/env python3
"""
Script pour corriger les URLs en utilisant les legiarti existants
"""

from pathlib import Path
import re

def fix_url_from_legiarti(file_path):
    """Corriger l'URL en utilisant le legiarti existant"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire le legiarti existant (sans guillemets)
    legiarti_match = re.search(r'legiarti:\s*(LEGIARTI\d+)', content)
    if not legiarti_match:
        print(f"⚠️ {file_path.name} - Aucun legiarti trouvé")
        return False
    
    legiarti = legiarti_match.group(1)
    
    # Générer l'URL correcte à partir du legiarti existant
    correct_url = f'url: "https://www.legifrance.gouv.fr/codes/article_lc/{legiarti}"'
    
    # Remplacer l'URL existante (quelle qu'elle soit) par la bonne
    corrected_content = re.sub(
        r'url:\s*"[^"]+"',
        correct_url,
        content
    )
    
    # Écrire le fichier corrigé seulement si des changements ont été faits
    if corrected_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(corrected_content)
        print(f"✓ {file_path.name} - URL corrigée vers {legiarti}")
        return True
    else:
        print(f"✓ {file_path.name} - URL déjà correcte")
        return False

def main():
    lois_dir = Path("/home/crilocom/accident-main/Lois")
    fixed_count = 0
    
    # Trouver tous les fichiers Article*.md
    article_files = list(lois_dir.rglob("Article*.md"))
    
    print(f"Trouvé {len(article_files)} fichiers à vérifier...")
    
    for file_path in article_files:
        if fix_url_from_legiarti(file_path):
            fixed_count += 1
    
    print(f"\n✅ Correction terminée : {fixed_count}/{len(article_files)} fichiers modifiés")

if __name__ == "__main__":
    main()