#!/usr/bin/env python3
"""
Script pour générer automatiquement des fils d'Ariane (breadcrumbs) 
selon le protocole spécifié pour le projet accident-main.

Format requis :
```
🏠 [Accueil](../../README.md) > 📁 [Dossier](../README.md) > 📄 [Fichier](./fichier.md)
```
"""

import os
import re
from pathlib import Path

def generate_breadcrumb(file_path, root_path="/home/crilocom/accident-main"):
    """
    Génère un fil d'Ariane pour un fichier Markdown donné.
    
    Args:
        file_path: Chemin complet du fichier
        root_path: Chemin racine du projet
    
    Returns:
        String: Fil d'Ariane formaté
    """
    # Convertir en Path pour manipulation facile
    full_path = Path(file_path)
    root = Path(root_path)
    
    # Calculer le chemin relatif depuis la racine
    try:
        relative_path = full_path.relative_to(root)
    except ValueError:
        # Le fichier n'est pas dans l'arborescence du projet
        return None
    
    # Diviser en parties
    parts = list(relative_path.parts)
    
    # Construire le fil d'Ariane
    breadcrumb_parts = []
    current_path = ""
    
    # Ajouter l'accueil (racine)
    breadcrumb_parts.append("🏠 [Accueil](../README.md)")
    
    # Ajouter les dossiers intermédiaires
    for i, part in enumerate(parts[:-1]):  # Exclure le fichier final
        current_path = os.path.join(current_path, part) if current_path else part
        # Calculer le chemin relatif pour le lien
        relative_link = os.path.join(".." * (len(parts) - i - 1), "README.md")
        breadcrumb_parts.append(f"📁 [ {part} ]({relative_link})")
    
    # Ajouter le fichier courant
    filename = parts[-1]
    breadcrumb_parts.append(f"📄 [ {filename} ](.{filename})")
    
    # Joindre avec des flèches
    return " > ".join(breadcrumb_parts)

def add_breadcrumb_to_file(file_path, root_path="/home/crilocom/accident-main"):
    """
    Ajoute ou met à jour le fil d'Ariane dans un fichier Markdown.
    
    Args:
        file_path: Chemin complet du fichier
        root_path: Chemin racine du projet
    
    Returns:
        bool: True si le fichier a été modifié, False sinon
    """
    breadcrumb = generate_breadcrumb(file_path, root_path)
    if not breadcrumb:
        return False
    
    # Lire le contenu actuel
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Erreur de lecture {file_path}: {e}")
        return False
    
    # Vérifier si le fil d'Ariane existe déjà
    breadcrumb_pattern = r'```\n🏠 \[Accueil\]\.*```'
    if re.search(breadcrumb_pattern, content, re.MULTILINE):
        # Remplacer le fil d'Ariane existant
        new_content = re.sub(
            breadcrumb_pattern,
            f'```\n{breadcrumb}\n```',
            content,
            flags=re.MULTILINE
        )
    else:
        # Ajouter le fil d'Ariane après le titre ou au début
        if content.startswith('# '):
            # Trouver la fin de la première ligne (titre)
            first_line_end = content.find('\n')
            if first_line_end != -1:
                new_content = ((
                    content[:first_line_end + 1] +  # Garder le titre
                    '\n\n```\n' + breadcrumb + '\n```\n' +  # Ajouter breadcrumb
                    content[first_line_end + 1:]  # Reste du contenu
                ))
            else:
                new_content = content + '\n\n```\n' + breadcrumb + '\n```\n'
        else:
            # Ajouter au début
            new_content = '```\n' + breadcrumb + '\n```\n\n' + content
    
    # Écrire le nouveau contenu
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Erreur d'écriture {file_path}: {e}")
        return False

def process_all_markdown_files(root_path="/home/crilocom/accident-main"):
    """
    Traite tous les fichiers Markdown dans le projet.
    
    Args:
        root_path: Chemin racine du projet
    
    Returns:
        dict: Statistiques de traitement
    """
    stats = {
        'total_files': 0,
        'modified_files': 0,
        'skipped_files': 0,
        'errors': 0
    }
    
    # Trouver tous les fichiers .md (en excluant .venv et .dev)
    md_files = []
    for root, dirs, files in os.walk(root_path):
        # Exclure les dossiers indésirables
        dirs[:] = [d for d in dirs if d not in ['.venv', '.dev', '__pycache__', '.git']]
        
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    stats['total_files'] = len(md_files)
    
    for file_path in md_files:
        try:
            if add_breadcrumb_to_file(file_path, root_path):
                stats['modified_files'] += 1
                print(f"✅ Mis à jour: {file_path}")
            else:
                stats['skipped_files'] += 1
        except Exception as e:
            stats['errors'] += 1
            print(f"❌ Erreur sur {file_path}: {e}")
    
    return stats

if __name__ == "__main__":
    print("🚀 Démarrage du script de génération de fils d'Ariane...")
    print("=" * 60)
    
    stats = process_all_markdown_files()
    
    print("\n" + "=" * 60)
    print("📊 STATISTIQUES:")
    print(f"  Fichiers traités: {stats['total_files']}")
    print(f"  Fichiers modifiés: {stats['modified_files']}")
    print(f"  Fichiers ignorés: {stats['skipped_files']}")
    print(f"  Erreurs: {stats['errors']}")
    print("=" * 60)
    print("✅ Script terminé!")