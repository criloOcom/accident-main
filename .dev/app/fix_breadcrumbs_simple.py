#!/usr/bin/env python3
"""
Script simple pour corriger les fils d'Ariane dans les fichiers Article*.md
"""

from pathlib import Path

def main():
    lois_dir = Path("/home/crilocom/accident-main/📜_Lois")
    fixed_count = 0
    
    # Trouver tous les fichiers Article*.md
    article_files = list(lois_dir.rglob("Article*.md"))
    
    print(f"Trouvé {len(article_files)} fichiers à traiter...")
    
    for file_path in article_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si le fil d'Ariane est déjà présent
        if content.startswith("🏠"):
            print(f"✓ {file_path.name} - Fil d'Ariane déjà présent")
            continue
        
        # Générer un fil d'Ariane simple
        relative_path = file_path.relative_to(lois_dir)
        parent_dir = relative_path.parent
        
        # Compter le nombre de niveaux pour les ..
        depth = len(parent_dir.parts) if parent_dir != Path(".") else 0
        home_link = "../" * (depth + 1) + "README.md"
        
        breadcrumb = f"🏠 [Accueil]({home_link}) > 📁 [📜_Lois](README.md)"
        
        # Ajouter le dossier spécifique si ce n'est pas la racine
        if parent_dir != Path("."):
            breadcrumb += f" > 📁 [{parent_dir.name}](README.md)"
        
        breadcrumb += f" > 📄 [{file_path.name}]({file_path.name})"
        
        # Ajouter le fil d'Ariane avant le contenu
        new_content = f"{breadcrumb}\n\n{content}"
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ {file_path.name} - Fil d'Ariane ajouté")
        fixed_count += 1
    
    print(f"\n✅ Correction terminée : {fixed_count}/{len(article_files)} fichiers modifiés")

if __name__ == "__main__":
    main()