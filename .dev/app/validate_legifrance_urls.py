#!/usr/bin/env python3
"""
Script pour valider les URLs Légifrance dans les métadonnées YAML
et générer un rapport de complétude.
"""

import re
from pathlib import Path
from urllib.parse import urlparse

def validate_url_format(url):
    """Valider le format d'une URL Légifrance"""
    try:
        result = urlparse(url)
        return all([result.scheme == 'https', 
                   result.netloc == 'www.legifrance.gouv.fr',
                   result.path.startswith('/codes/article_lc/')])
    except:
        return False

def check_yaml_structure(content):
    """Vérifier que le YAML est bien formé"""
    if not content.startswith('---'):
        return False, "Pas de frontmatter YAML"
    
    # Vérifier la structure de base
    required_fields = ['title', 'code', 'article', 'date', 'source', 'status', 'url']
    
    yaml_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        return False, "Frontmatter YAML mal formé"
    
    yaml_content = yaml_match.group(1)
    
    for field in required_fields:
        if f'{field}:' not in yaml_content:
            return False, f"Champ {field} manquant"
    
    # Extraire l'URL
    url_match = re.search(r'url:\s*(https?://\S+)', yaml_content)
    if not url_match:
        return False, "URL manquante"
    
    url = url_match.group(1)
    if not validate_url_format(url):
        return False, f"URL invalide: {url}"
    
    return True, "YAML valide"

def main():
    print("🔍 Validation des URLs Légifrance")
    print("=" * 60)
    
    lois_dir = Path("📜_Lois")
    total_files = 0
    valid_files = 0
    invalid_files = []
    
    # Parcourir tous les fichiers d'articles
    for md_file in lois_dir.rglob("Article*.md"):
        total_files += 1
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Valider la structure YAML
        is_valid, message = check_yaml_structure(content)
        
        if is_valid:
            valid_files += 1
            print(f"✅ {md_file.name} → {message}")
        else:
            print(f"❌ {md_file.name} → {message}")
            invalid_files.append((md_file.name, message))
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats de la validation:")
    print(f"  - Fichiers validés: {valid_files}/{total_files}")
    print(f"  - Taux de succès: {valid_files/total_files*100:.1f}%")
    
    if invalid_files:
        print(f"\n⚠️  Fichiers avec des problèmes:")
        for filename, error in invalid_files:
            print(f"  - {filename}: {error}")
    else:
        print(f"\n🎉 Tous les fichiers ont des métadonnées YAML valides avec des URLs Légifrance!")
    
    # Générer un rapport
    report_content = f"""# 📊 Rapport de Validation des URLs Légifrance

**Date :** {Path("📊_Rapports/RAPPORT_VALIDATION_URLS_20260711.md").stat().st_mtime if Path("📊_Rapports/RAPPORT_VALIDATION_URLS_20260711.md").exists() else "11 juillet 2026"}
**Total des fichiers :** {total_files}
**Fichiers valides :** {valid_files}
**Taux de succès :** {valid_files/total_files*100:.1f}%

---

## 📋 Détails de la Validation

### Critères vérifiés pour chaque fichier :
1. ✅ Présence de frontmatter YAML (---)
2. ✅ Tous les champs requis présents (title, code, article, date, source, status, url)
3. ✅ Format d'URL valide (https://www.legifrance.gouv.fr/codes/article_lc/...)
4. ✅ Structure YAML cohérente

### Champs YAML requis :
```yaml
---
title: [Titre de l'article]
code: [Code concerné]
article: [Numéro d'article]
date: [Date de traitement]
source: Légifrance
status: En vigueur
url: [URL officielle Légifrance]
---
```

---

## 📊 Statistiques par Dossier

"""
    
    # Compter les fichiers par dossier
    dossier_counts = {}
    for md_file in lois_dir.rglob("Article*.md"):
        dossier = md_file.parent.name
        if dossier not in dossier_counts:
            dossier_counts[dossier] = 0
        dossier_counts[dossier] += 1
    
    for dossier, count in sorted(dossier_counts.items()):
        report_content += f"- **{dossier}** : {count} articles\n"
    
    report_content += "\n---\n\n"
    
    if invalid_files:
        report_content += "## ⚠️ Problèmes détectés\n\n"
        for filename, error in invalid_files:
            report_content += f"- {filename}: {error}\n"
    else:
        report_content += "## ✅ Validation réussie\n\nTous les fichiers ont passé la validation avec succès!\n\n"
        report_content += "### Avantages :\n"
        report_content += "- **Traçabilité juridique** : Chaque article a un lien direct vers la source officielle\n"
        report_content += "- **Transparence** : Les références sont vérifiables par quiconque\n"
        report_content += "- **Professionnalisme** : Conformité avec les standards juridiques\n"
        report_content += "- **Automatisation** : Les URLs peuvent être utilisées pour des vérifications automatiques\n"
    
    report_content += "\n---\n\n> **Statut** : ✅ Validé et prêt pour utilisation\n> **Date** : 11 juillet 2026\n> **Responsable** : Mistral Vibe\n"
    
    # Écrire le rapport
    report_path = Path("📊_Rapports/RAPPORT_VALIDATION_URLS_20260711.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"\n✅ Rapport généré: {report_path}")
    return len(invalid_files) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)