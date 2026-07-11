#!/usr/bin/env python3
"""
Script de validation de l'organisation du projet
"""

from pathlib import Path
import re

def validate_breadcrumbs():
    """Valider que tous les fichiers ont des breadcrumbs conformes"""
    lois_dir = Path("/home/crilocom/accident-main/📜 Lois")
    errors = []
    
    for md_file in lois_dir.rglob("Article*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        
        if not first_line.startswith("🏠"):
            errors.append(f"{md_file}: Pas de breadcrumb en première ligne")
    
    return len(errors) == 0, errors

def validate_yaml_urls():
    """Valider que tous les fichiers ont des URLs"""
    lois_dir = Path("/home/crilocom/accident-main/📜 Lois")
    missing_urls = []
    
    for md_file in lois_dir.rglob("Article*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'url:' not in content.lower():
            missing_urls.append(str(md_file))
    
    return len(missing_urls) == 0, missing_urls

def validate_readme_files():
    """Valider la présence des README requis"""
    required_readmes = [
        "/home/crilocom/accident-main/🧠 Memory/README.md",
        "/home/crilocom/accident-main/📊 Rapports/README.md",
        "/home/crilocom/accident-main/.dev/README.md",
        "/home/crilocom/accident-main/📜 Lois/📒 Code general des collectivites territoriales/README.md"
    ]
    
    missing = []
    for readme in required_readmes:
        if not Path(readme).exists():
            missing.append(readme)
    
    return len(missing) == 0, missing

def main():
    print("🔍 Validation de l'organisation du projet...")
    print("=" * 50)
    
    # Valider les breadcrumbs
    print("\n1. Validation des fils d'Ariane...")
    breadcrumbs_ok, breadcrumb_errors = validate_breadcrumbs()
    if breadcrumbs_ok:
        print("   ✅ Tous les breadcrumbs sont conformes")
    else:
        print(f"   ❌ {len(breadcrumb_errors)} erreurs trouvées:")
        for error in breadcrumb_errors[:5]:
            print(f"      - {error}")
    
    # Valider les URLs
    print("\n2. Validation des URLs Légifrance...")
    urls_ok, missing_urls = validate_yaml_urls()
    if urls_ok:
        print("   ✅ Toutes les URLs sont présentes")
    else:
        print(f"   ❌ {len(missing_urls)} fichiers sans URL:")
        for url in missing_urls[:5]:
            print(f"      - {url}")
    
    # Valider les README
    print("\n3. Validation des fichiers README...")
    readmes_ok, missing_readmes = validate_readme_files()
    if readmes_ok:
        print("   ✅ Tous les README requis sont présents")
    else:
        print(f"   ❌ {len(missing_readmes)} README manquants:")
        for readme in missing_readmes:
            print(f"      - {readme}")
    
    # Résumé
    print("\n" + "=" * 50)
    all_ok = breadcrumbs_ok and urls_ok and readmes_ok
    if all_ok:
        print("🎉 VALIDATION RÉUSSIE - Tous les critères sont respectés!")
    else:
        print("⚠️  VALIDATION ÉCHOUEE - Corrections nécessaires")
    
    return all_ok

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)