#!/usr/bin/env python3
"""
Script pour corriger les fils d'Ariane dans les fichiers Article*.md
Conforme au protocole : fil d'Ariane en ligne 1, puis YAML, puis contenu
"""

from pathlib import Path
import re

def generate_breadcrumb(file_path):
    """Génère le fil d'Ariane basé sur la position du fichier"""
    parts = []
    current = file_path.parent
    
    # Remonter jusqu'à la racine du projet
    while str(current) != "/home/crilocom/accident-main":
        if current.name == "📜_Lois":
            parts.insert(0, f"📄 [{file_path.name}]({file_path.name})"
            parts.insert(0, f"📁 [{current.name}](../README.md)")
        elif current.name.startswith("📒_"):
            parts.insert(0, f"📁 [{current.name}](../README.md)")
        current = current.parent
    
    # Ajouter le lien vers l'accueil
    depth = len(parts) - 1
    home_link = "../" * depth + "README.md"
    parts.insert(0, f"🏠 [Accueil]({home_link}) > ")
    
    return " > ".join(parts)

def fix_breadcrumb_in_file(file_path):
    """Corrige le fil d'Ariane dans un fichier spécifique"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le fil d'Ariane est déjà présent
    if content.startswith("🏠"):
        print(f"✓ {file_path.name} - Fil d'Ariane déjà présent")
        return False
    
    # Générer le nouveau fil d'Ariane
    breadcrumb = generate_breadcrumb(file_path)
    
    # Ajouter le fil d'Ariane avant le YAML
    new_content = f"{breadcrumb}\n\n{content}"
    
    # Écrire le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ {file_path.name} - Fil d'Ariane ajouté")
    return True

def main():
    lois_dir = Path("/home/crilocom/accident-main/📜_Lois")
    fixed_count = 0
    
    # Trouver tous les fichiers Article*.md
    article_files = list(lois_dir.rglob("Article*.md"))
    
    print(f"Trouvé {len(article_files)} fichiers à traiter...")
    
    for file_path in article_files:
        if fix_breadcrumb_in_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ Correction terminée : {fixed_count}/{len(article_files)} fichiers modifiés")

if __name__ == "__main__":
    main()