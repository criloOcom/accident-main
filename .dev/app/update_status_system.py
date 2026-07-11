#!/usr/bin/env python3
"""
Script unique pour :
1. Ajouter reel_path/token_path dans les YAML (liens croisés)
2. Standardiser les statuts (draft→brouillon)
3. Ajouter statut: brouillon aux fichiers sans YAML/statut
4. Créer le dossier /status/ avec index par statut
"""

import os
import re
import glob
from collections import defaultdict

BASE = '/home/crilocom/accident-main'
TOKEN_BASE = os.path.join(BASE, '⚖️ Actes', '🔑 Token')
REAL_BASE = os.path.join(BASE, '⚖️ Actes', '👤 Reel')
STATUS_DIR = os.path.join(BASE, 'status')

STATUT_NORMALIZE = {
    'draft': 'brouillon',
    'DRAFT': 'brouillon',
    'Draft': 'brouillon',
}

def extract_yaml(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return match.group(1), match.end()
    return None, 0

def parse_yaml_lines(yaml_text):
    """Parse simple YAML key: value pairs."""
    result = {}
    for line in yaml_text.split('\n'):
        m = re.match(r'^(\w[\w_-]*)\s*:\s*(.*)', line)
        if m:
            result[m.group(1)] = m.group(2).strip()
    return result

def _find_key_block(yaml_lines, key):
    """Find the line range [start, end) for a key (including multi-line values).
    Returns (start_idx, end_idx) or None."""
    for i, line in enumerate(yaml_lines):
        m = re.match(r'^(\w[\w_-]*)\s*:', line)
        if m and m.group(1) == key:
            end = i + 1
            while end < len(yaml_lines):
                # Continuation lines start with space
                if yaml_lines[end].startswith(' ') or yaml_lines[end].startswith('-'):
                    end += 1
                else:
                    break
            return (i, end)
    return None

def update_yaml_in_content(content, updates):
    """Add or update fields in YAML front matter preserving structure."""
    yaml_text, end = extract_yaml(content)
    if yaml_text is None:
        new_yaml = '---\n'
        for k, v in updates.items():
            new_yaml += f'{k}: {v}\n'
        new_yaml += '---\n\n'
        return new_yaml + content.lstrip()
    
    yaml_lines = yaml_text.split('\n')
    
    # Build set of existing keys
    existing_keys = set()
    for line in yaml_lines:
        m = re.match(r'^(\w[\w_-]*)\s*:', line)
        if m:
            existing_keys.add(m.group(1))
    
    new_lines = list(yaml_lines)
    
    for key, value in updates.items():
        block = _find_key_block(new_lines, key)
        if block:
            idx_start, idx_end = block
            # Replace the first line (idx_start) with the new value
            new_lines[idx_start] = f'{key}: {value}'
        else:
            # Insert before the closing --- (last non-empty non-comment block)
            # Find last meaningful line (not empty, not just ---)
            insert_pos = len(new_lines)
            while insert_pos > 0 and (new_lines[insert_pos - 1].strip() == '' or new_lines[insert_pos - 1].strip() == '---'):
                insert_pos -= 1
            new_lines.insert(insert_pos, f'{key}: {value}')
    
    new_yaml = '\n'.join(new_lines)
    return f'---\n{new_yaml}\n---\n' + content[end:]

def get_statut(yaml_dict):
    """Extract and normalize statut from YAML dict."""
    raw = yaml_dict.get('statut', '')
    if not raw:
        return 'brouillon'
    raw = raw.strip().strip('"').strip("'")
    return STATUT_NORMALIZE.get(raw, raw)

def collect_files():
    """Collect all token and real files with their YAML."""
    
    def scan(base_dir, kind):
        """Scan a directory tree for .md files with YAML."""
        files = []
        for subdir in sorted(os.listdir(base_dir)):
            subdir_path = os.path.join(base_dir, subdir)
            if not os.path.isdir(subdir_path):
                continue
            for fpath in sorted(glob.glob(os.path.join(subdir_path, '*.md'))):
                fname = os.path.basename(fpath)
                if fname in ('README.md', 'INDEX.md'):
                    continue
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                yaml_text, _ = extract_yaml(content)
                yaml_dict = parse_yaml_lines(yaml_text) if yaml_text else {}
                files.append({
                    'kind': kind,
                    'subdir': subdir,
                    'fname': fname,
                    'path': fpath,
                    'content': content,
                    'yaml': yaml_dict,
                    'statut': get_statut(yaml_dict),
                })
        return files
    
    token_files = scan(TOKEN_BASE, 'token')
    real_files = scan(REAL_BASE, 'reel')
    return token_files, real_files

def make_relative_path(from_file, to_file):
    """Create a relative path from from_file to to_file, both absolute."""
    from_dir = os.path.dirname(from_file)
    rel = os.path.relpath(to_file, from_dir)
    return rel

def main():
    print("=== Phase 1: Collecte des fichiers ===")
    token_files, real_files = collect_files()
    print(f"  Token files: {len(token_files)}")
    print(f"  Real files:  {len(real_files)}")
    
    # Build lookup maps: (subdir, fname) -> file
    token_map = {(f['subdir'], f['fname']): f for f in token_files}
    real_map = {(f['subdir'], f['fname']): f for f in real_files}
    
    stats = {
        'added_reel_path': 0,
        'added_token_path': 0,
        'statut_standardized': 0,
        'statut_added': 0,
    }
    
    print("\n=== Phase 2: Mise à jour des YAML (liens croisés + statuts) ===")
    
    # Update token files
    for f in token_files:
        updates = {}
        
        # Add reel_path if counterpart exists
        if (f['subdir'], f['fname']) in real_map:
            real_path = real_map[(f['subdir'], f['fname'])]['path']
            rel = make_relative_path(f['path'], real_path)
            updates['reel_path'] = rel
            stats['added_reel_path'] += 1
        
        # Standardize statut
        raw_statut = f['yaml'].get('statut', '')
        normalized = STATUT_NORMALIZE.get(raw_statut.strip().strip('"').strip("'"))
        if normalized:
            updates['statut'] = normalized
            stats['statut_standardized'] += 1
        
        # Ensure statut field exists
        if 'statut' not in f['yaml']:
            updates['statut'] = 'brouillon'
            stats['statut_added'] += 1
        
        if updates:
            new_content = update_yaml_in_content(f['content'], updates)
            with open(f['path'], 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            # Update in-memory
            f['content'] = new_content
            yaml_text, _ = extract_yaml(new_content)
            f['yaml'] = parse_yaml_lines(yaml_text)
            f['statut'] = get_statut(f['yaml'])
    
    # Update real files
    for f in real_files:
        updates = {}
        
        # Add token_path if counterpart exists
        if (f['subdir'], f['fname']) in token_map:
            token_path = token_map[(f['subdir'], f['fname'])]['path']
            rel = make_relative_path(f['path'], token_path)
            updates['token_path'] = rel
            stats['added_token_path'] += 1
        
        # Standardize statut
        raw_statut = f['yaml'].get('statut', '')
        normalized = STATUT_NORMALIZE.get(raw_statut.strip().strip('"').strip("'"))
        if normalized:
            updates['statut'] = normalized
            # Don't double-count, already counted in token phase
            pass
        
        # Ensure statut field exists
        if 'statut' not in f['yaml']:
            updates['statut'] = 'brouillon'
            # Don't double-count
        
        if updates:
            new_content = update_yaml_in_content(f['content'], updates)
            with open(f['path'], 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            f['content'] = new_content
            yaml_text, _ = extract_yaml(new_content)
            f['yaml'] = parse_yaml_lines(yaml_text)
            f['statut'] = get_statut(f['yaml'])
    
    print(f"  reel_path ajoutés: {stats['added_reel_path']}")
    print(f"  token_path ajoutés: {stats['added_token_path']}")
    print(f"  statuts standardisés: {stats['statut_standardized']}")
    print(f"  statuts ajoutés (manquants): {stats['statut_added']}")
    
    print("\n=== Phase 3: Création du dossier /status/ ===")
    os.makedirs(STATUS_DIR, exist_ok=True)
    
    # Group all files by statut
    all_files = token_files + real_files
    by_statut = defaultdict(list)
    for f in all_files:
        by_statut[f['statut']].append(f)
    
    print(f"  Statuts trouvés: {sorted(by_statut.keys())}")
    
    # Create index file per statut
    for statut in sorted(by_statut.keys()):
        files = by_statut[statut]
        label = statut.capitalize()
        safe_name = statut.replace('é', 'e').replace('è', 'e').replace(' ', '_').replace('-', '_')
        index_path = os.path.join(STATUS_DIR, f'{safe_name}.md')
        
        # Count by kind
        token_count = sum(1 for f in files if f['kind'] == 'token')
        reel_count = sum(1 for f in files if f['kind'] == 'reel')
        
        lines = [
            f'# Statut : {statut}',
            f'',
            f'**{len(files)} documents** ({token_count} token, {reel_count} reel)',
            f'',
            f'## Documents tokenisés (🔑)',
            f'',
        ]
        
        token_files_by_statut = [f for f in files if f['kind'] == 'token']
        reel_files_by_statut = [f for f in files if f['kind'] == 'reel']
        
        if token_files_by_statut:
            for f in token_files_by_statut:
                rel_path = os.path.relpath(f['path'], BASE)
                rp = f['yaml'].get('reel_path', '')
                link_suffix = f' → [👤 reel]({rp})' if rp else ''
                lines.append(f'- [`{rel_path}`](/{rel_path}){link_suffix}')
        else:
            lines.append('  _(aucun)_')
        
        lines.extend(['', '## Versions réelles (👤)', ''])
        
        if reel_files_by_statut:
            for f in reel_files_by_statut:
                rel_path = os.path.relpath(f['path'], BASE)
                tp = f['yaml'].get('token_path', '')
                link_suffix = f' → [🔑 token]({tp})' if tp else ''
                lines.append(f'- [`{rel_path}`](/{rel_path}){link_suffix}')
        else:
            lines.append('  _(aucun)_')
        
        lines.append('')
        
        with open(index_path, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines))
        
        print(f"  ✓ {safe_name}.md ({len(files)} fichiers)")
    
    # Create a README for the status dir
    readme_path = os.path.join(STATUS_DIR, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as fh:
        fh.write("""# 📊 Index des statuts

Ce dossier contient un fichier par statut, listant tous les documents concernés avec leurs liens croisés.

## Index

""")
        for statut in sorted(by_statut.keys()):
            safe_name = statut.replace('é', 'e').replace('è', 'e').replace(' ', '_').replace('-', '_')
            count = len(by_statut[statut])
            fh.write(f'- [{statut} ({count})]({safe_name}.md)\n')
        
        fh.write("""
## Convention des statuts

| Statut | Signification |
|--------|---------------|
| `final` | Document finalisé, envoyé ou prêt à l'emploi |
| `brouillon` | En cours de rédaction ou d'édition |
| `projet` | Version projet, en attente de relecture/validation |
| `preparation` | En préparation (checklists, plannings) |
| `fusionne` | Fusionné dans un autre document |
| `archive` | Document historique conservé pour référence |
""")
    
    print(f"  ✓ README.md créé")
    print(f"\n=== Terminé ===")
    print(f"Dossier /status/ créé avec {len(by_statut)} index de statuts")
    print(f"Total fichiers mis à jour: {stats['added_reel_path'] + stats['added_token_path']}")

if __name__ == '__main__':
    main()
