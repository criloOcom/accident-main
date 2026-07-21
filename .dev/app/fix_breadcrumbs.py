#!/usr/bin/env python3
"""
Script pour corriger les fils d'Ariane dans les fichiers Lois/
Selon le protocole : fil d'Ariane doit être en première ligne, suivi du titre, puis du contenu.
"""

from pathlib import Path
import re

def analyze_breadcrumb_problems():
    """Analyser les problèmes de fils d'Ariane"""
    lois_dir = Path("Lois")
    problems = {
        'fil_not_first_line': [],
        'title_before_fil': [],
        'duplicate_fil': [],
        'has_arrow_symbol': [],
        'broken_paths': []
    }
    
    for md_file in lois_dir.rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Vérifier si le fil d'Ariane est en première ligne
        if len(lines) > 0 and not lines[0].startswith('🏠'):
            problems['fil_not_first_line'].append(md_file.name)
        
        # Vérifier l'ordre titre/fil
        fil_line = -1
        title_line = -1
        for i, line in enumerate(lines):
            if line.startswith('🏠'):
                fil_line = i
            elif line.startswith('#'):
                title_line = i
                break
        
        if fil_line > title_line and title_line != -1:
            problems['title_before_fil'].append(md_file.name)
        
        # Vérifier les doublons de fil d'Ariane
        fil_count = sum(1 for line in lines if line.startswith('🏠'))
        if fil_count > 1:
            problems['duplicate_fil'].append(md_file.name)
        
        # Vérifier le symbole →
        content = ''.join(lines)
        if '→' in content:
            problems['has_arrow_symbol'].append(md_file.name)
        
        # Vérifier les chemins cassés (simplifié)
        if '../README.md' not in content and '..README.md' in content:
            problems['broken_paths'].append(md_file.name)
    
    print("🔍 Analyse des problèmes de fils d'Ariane")
    print("=" * 60)
    for problem_type, files in problems.items():
        print(f"{problem_type}: {len(files)} fichiers")
    
    return problems

def fix_article_file(file_path):
    """Corriger un fichier d'article"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Trouver tous les fils d'Ariane (y compris ceux dans les code fences)
    fil_lines = []
    in_code_fence = False
    for i, line in enumerate(lines):
        if line.startswith('```'):
            in_code_fence = not in_code_fence
        elif line.startswith('🏠') and not in_code_fence:
            fil_lines.append(i)
    
    if not fil_lines:
        return False, "Pas de fil d'Ariane trouvé"
    
    # Garder seulement le premier fil d'Ariane
    fil = lines[fil_lines[0]]
    
    # Trouver le titre
    title_line_idx = -1
    for i, line in enumerate(lines):
        if line.startswith('#') and not line.startswith('##'):
            title_line_idx = i
            break
    
    # Trouver le YAML frontmatter
    yaml_start = -1
    yaml_end = -1
    for i, line in enumerate(lines):
        if line.startswith('---'):
            if yaml_start == -1:
                yaml_start = i
            else:
                yaml_end = i
                break
    
    # Reconstruire le contenu dans le bon ordre
    new_lines = []
    
    # 1. Fil d'Ariane en première ligne
    new_lines.append(fil)
    
    # 2. Titre en deuxième ligne (s'il existe)
    if title_line_idx != -1:
        new_lines.append(lines[title_line_idx])
    
    # 3. YAML frontmatter (s'il existe)
    if yaml_start != -1 and yaml_end != -1:
        new_lines.extend(lines[yaml_start:yaml_end+1])
    
    # 4. Reste du contenu (sans les doublons de fil et les code fences vides)
    in_code_fence = False
    skip_next_empty_fence = False
    lines_to_skip = set(fil_lines[1:])  # Skip all duplicate breadcrumbs
    
    for i, line in enumerate(lines):
        # Skip title and YAML lines (already added)
        if i == title_line_idx or (yaml_start != -1 and yaml_end != -1 and yaml_start <= i <= yaml_end):
            continue
        
        # Skip all breadcrumbs (we already added the first one)
        if i in fil_lines:
            continue
        
        # Handle code fences
        if line.startswith('```'):
            if in_code_fence:
                # Closing fence - check if we should skip it
                if skip_next_empty_fence:
                    skip_next_empty_fence = False
                    continue
                in_code_fence = False
            else:
                # Opening fence - check if next line is a breadcrumb
                if i + 1 < len(lines) and lines[i + 1].startswith('🏠'):
                    skip_next_empty_fence = True
                    continue
                in_code_fence = True
            new_lines.append(line)
        elif not in_code_fence:
            new_lines.append(line)
    
    # Rejoindre et écrire
    new_content = '\n'.join(new_lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, "Corrigé"

def fix_readme_file(file_path):
    """Corriger un fichier README"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corriger les problèmes cosmétiques
    corrections = [
        ('→', '>'),  # Remplacer → par >
        ('(..README.md)', '(../README.md)'),  # Corriger les chemins
        ('(....README.md)', '(../../README.md)'),
    ]
    
    for old, new in corrections:
        content = content.replace(old, new)
    
    # Corriger les chemins cassés spécifiques
    content = re.sub(
        r'\[📁 (crilocom|home)\]\(\.\./README\.md\)',
        '[📁 Accueil](../README.md)',
        content
    )
    
    # S'assurer que le fil d'Ariane est en première ligne et supprimer les doublons
    lines = content.split('\n')
    fil_indices = []
    in_code_fence = False
    
    for i, line in enumerate(lines):
        if line.startswith('```'):
            in_code_fence = not in_code_fence
        elif line.startswith('🏠') and not in_code_fence:
            fil_indices.append(i)
    
    if fil_indices:
        # Garder seulement le premier fil d'Ariane
        fil = lines[fil_indices[0]]
        # Supprimer tous les fils d'Ariane sauf le premier
        lines = [line for i, line in enumerate(lines) if i not in fil_indices[1:] or i == fil_indices[0]]
        # Si le premier fil n'est pas en première ligne, le déplacer
        if fil_indices[0] > 0:
            lines = [line for i, line in enumerate(lines) if i != fil_indices[0]]
            lines.insert(0, fil)
        else:
            # Le premier fil est déjà en première ligne, s'assurer qu'il n'y a pas de doublons
            lines = [line for i, line in enumerate(lines) if not (i > 0 and line.startswith('🏠'))]
        
        content = '\n'.join(lines)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, "Corrigé"

def validate_file(file_path):
    """Valider qu'un fichier est correct"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 1. Fil d'Ariane doit être en première ligne
    if not lines or not lines[0].startswith('🏠'):
        return False, "Fil d'Ariane pas en première ligne"
    
    # 2. Pas de doublons de fil d'Ariane
    fil_count = sum(1 for line in lines if line.startswith('🏠'))
    if fil_count > 1:
        return False, f"Fil d'Ariane dupliqué ({fil_count} fois)"
    
    # 3. Pas de symbole →
    if '→' in ''.join(lines):
        return False, "Symbole → présent"
    
    # 4. Chemins relatifs corrects (vérification basique)
    if '..README.md' in ''.join(lines) and '../README.md' not in ''.join(lines):
        return False, "Chemins relatifs problématiques"
    
    return True, "Valide"

def main():
    print("🔧 Correction des fils d'Ariane dans Lois/")
    print("=" * 60)
    
    # Étape 1: Analyser les problèmes
    problems = analyze_breadcrumb_problems()
    
    # Étape 2: Corriger les fichiers
    lois_dir = Path("Lois")
    total_files = 0
    fixed_files = 0
    validation_issues = []
    
    for md_file in lois_dir.rglob("*.md"):
        total_files += 1
        
        if md_file.name.startswith("Article") or "Jurisprudence" in md_file.parts:
            # Fichier d'article
            success, msg = fix_article_file(md_file)
        else:
            # Fichier README
            success, msg = fix_readme_file(md_file)
        
        if success:
            fixed_files += 1
            print(f"✅ {md_file.name} → {msg}")
        else:
            print(f"❌ {md_file.name} → {msg}")
    
    # Étape 3: Validation
    print("\n" + "=" * 60)
    print("📊 Validation des corrections:")
    
    valid_files = 0
    for md_file in lois_dir.rglob("*.md"):
        is_valid, msg = validate_file(md_file)
        if is_valid:
            valid_files += 1
        else:
            validation_issues.append((md_file.name, msg))
    
    print(f"Fichiers valides: {valid_files}/{total_files}")
    
    if validation_issues:
        print("\n⚠️ Problèmes restants:")
        for filename, issue in validation_issues:
            print(f"  - {filename}: {issue}")
    else:
        print("\n🎉 Tous les fichiers ont été corrigés avec succès!")
    
    # Générer un rapport
    report_content = f"""# 📊 Rapport de Correction des Fils d'Ariane

**Date :** 11 juillet 2026
**Dossier :** Lois/
**Fichiers traités :** {total_files}
**Fichiers corrigés :** {fixed_files}
**Taux de succès :** {valid_files}/{total_files} ({valid_files/total_files*100:.1f}%)

---

## 📋 Problèmes Initiaux

"""
    
    for problem_type, files in problems.items():
        report_content += f"- **{problem_type}** : {len(files)} fichiers\n"
    
    report_content += "\n---\n\n"
    
    if validation_issues:
        report_content += "## ⚠️ Problèmes Restants\n\n"
        
        for filename, issue in validation_issues:
            report_content += f"- {filename}: {issue}\n"
    else:
        report_content += "## ✅ Tous les Fichiers Corrigés\n\n"
        report_content += "### Corrections appliquées :\n"
        report_content += "1. **Position** : Fil d'Ariane déplacé en première ligne\n"
        report_content += "2. **Ordre** : Titre placé après le fil d'Ariane\n"
        report_content += "3. **Doublons** : Fils d'Ariane dupliqués supprimés\n"
        report_content += "4. **Chemins** : Chemins relatifs corrigés\n"
        report_content += "5. **Format** : Symbole → remplacé par >\n"
        report_content += "\n### Structure standardisée :\n"
        report_content += "```\n"
        report_content += "🏠 [Accueil](../README.md) > 📁 [Dossier](../README.md) > 📄 [Fichier](./README.md)\n"
        report_content += "# Titre du fichier\n"
        report_content += "---\n"
        report_content += "Contenu...\n"
        report_content += "```\n"
    
    report_content += "\n---\n\n> **Statut** : ✅ Correction terminée\n> **Date** : 11 juillet 2026\n> **Responsable** : Mistral Vibe\n"
    
    report_path = Path("Rapports/RAPPORT_CORRECTION_BREADCRUMBS_20260711.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n✅ Rapport généré: {report_path}")
    return len(validation_issues) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)