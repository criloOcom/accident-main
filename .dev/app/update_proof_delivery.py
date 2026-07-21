#!/usr/bin/env python3
"""
Marque les 5 courriers avec preuve d'envoi : statut: envoye + proof_delivery.
Le reste des final sans preuve reste inchangé.
"""
import os, re

BASE = '/home/crilocom/accident-main'

SENT_FILES = {
    # (subdir, filename) -> proof value
    ('Courriers', '03 ✉️ Courrier SAS.md'): 'LRAR 87001424863012T',
    ('Courriers', '05 ✉️ Courrier Proprietaire.md'): 'AR signé par bailleur (M. Romain Delrieu)',
    ('Courriers', '06 ✉️ Courrier President DG.md'): 'LRAR 87001424721856G + 87001424862879J',
    ('Courriers', '06 V2 ✉️ Relance Dirigeants.md'): 'LRAR 870014282662911 + facture Z0132713629',
    ('Courriers', '10 ✉️ Courrier Doyen Juges Instruction.md'): 'Déposé au TJ Foix le 06/07/2026',
}

def update_file(filepath, updates):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        print(f"  ✗ PAS DE YAML: {filepath}")
        return False
    
    yaml_text = match.group(1)
    yaml_lines = yaml_text.split('\n')
    
    # Find existing keys and their line indices
    existing = {}
    multi_line_keys = {}
    current_key = None
    
    for i, line in enumerate(yaml_lines):
        m = re.match(r'^(\w[\w_-]*)\s*:', line)
        if m:
            current_key = m.group(1)
            existing[current_key] = (i, i + 1)
            multi_line_keys[current_key] = [i]
        elif current_key and (line.startswith(' ') or line.startswith('-')):
            multi_line_keys[current_key].append(i)
            existing[current_key] = (existing[current_key][0], i + 1)
        else:
            current_key = None
    
    new_lines = list(yaml_lines)
    
    for key, value in updates.items():
        if key in existing:
            start, _ = existing[key]
            new_lines[start] = f'{key}: {value}'
        else:
            # Insert before last meaningful line
            insert_pos = len(new_lines)
            while insert_pos > 0 and (new_lines[insert_pos - 1].strip() == '' or new_lines[insert_pos - 1].strip() == '---'):
                insert_pos -= 1
            new_lines.insert(insert_pos, f'{key}: {value}')
    
    new_yaml = '\n'.join(new_lines)
    new_content = f'---\n{new_yaml}\n---\n' + content[match.end():]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    for (subdir, fname), proof in SENT_FILES.items():
        for kind in ['Token', 'Reel']:
            filepath = os.path.join(BASE, 'Actes', kind, subdir, fname)
            if not os.path.exists(filepath):
                print(f"  ~ INTROUVABLE: {filepath}")
                continue
            updates = {'statut': 'envoye', 'proof_delivery': f'"{proof}"'}
            if update_file(filepath, updates):
                print(f"  ✓ {kind}/{subdir}/{fname} → envoye")

if __name__ == '__main__':
    main()
