#!/usr/bin/env python3
"""
Script pour corriger le format des URLs Légifrance
Supprime la date incorrecte ajoutée après les URLs
"""

from pathlib import Path
import re

def fix_url_format(file_path):
    """Corriger le format de l'URL dans un fichier"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver et corriger les URLs avec la date indésirable
    # Pattern: url: "URL" "2026-07-11" -> url: "URL"
    corrected_content = re.sub(
        r'url: "(https://[^"]+)" "2026-07-11"',
        r'url: "\1"',
        content
    )
    
    # Écrire le fichier corrigé seulement si des changements ont été faits
    if corrected_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(corrected_content)
        print(f"✓ {file_path.name} - URL corrigée")
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
        if fix_url_format(file_path):
            fixed_count += 1
    
    print(f"\n✅ Correction terminée : {fixed_count}/{len(article_files)} fichiers modifiés")

if __name__ == "__main__":
    main()