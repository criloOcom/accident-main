import os
import re

directories = ['actes', 'memory']
names_to_search = [
    'Sébastien', 'Grazide', 'GRAZIDE', 'Mountasser', 'SABIR', 'Sabir', 'Andissac', 'ANDISSAC',
    'Sorroche', 'Djerbi', 'DJERBI', 'Iskander', 'Jardon', 'JARDON', 'Julie', 'Oxybel',
    'Desbois', 'DESBOIS', 'Sigrid', 'Delrieu', 'DELRIEU', 'Romain', 'Bennourine',
    'BENNOURINE', 'Ayoub', 'Tavella', 'Rodriguez', 'Caparros'
]

pattern_str = r'\b(?:' + '|'.join(map(re.escape, names_to_search)) + r')\b'
name_pattern = re.compile(pattern_str)

token_pattern = re.compile(r'\*\*\[.*?\]\*\*')

results = []

for d in directories:
    if not os.path.exists(d):
        continue
    for root, dirs, files in os.walk(d):
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                if os.path.normpath(filepath) == os.path.normpath('memory/AUDIT_NOMS_RESIDUELS.md'):
                    continue
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    continue

                in_frontmatter = False
                if len(lines) > 0 and lines[0].strip() == '---':
                    in_frontmatter = True

                for i, line in enumerate(lines):
                    line_num = i + 1

                    if line_num == 1 and in_frontmatter:
                        continue

                    if in_frontmatter:
                        if line.strip() == '---':
                            in_frontmatter = False
                        continue

                    cleaned_line = token_pattern.sub('', line)

                    matches = name_pattern.findall(cleaned_line)
                    if matches:
                        results.append({
                            'file': filepath,
                            'line': line_num,
                            'context': line.strip(),
                            'matches': list(set(matches))
                        })

results.sort(key=lambda x: (x['file'], x['line']))

report_lines = ["# AUDIT NOMS RÉELS RÉSIDUELS\n"]

if not results:
    report_lines.append("Aucun nom réel résiduel n'a été trouvé.")
else:
    for res in results:
        report_lines.append(f"- **Fichier:** `{res['file']}` (Ligne {res['line']})")
        report_lines.append(f"  - **Nom(s) trouvé(s):** {', '.join(res['matches'])}")
        report_lines.append(f"  - **Contexte:** `{res['context']}`\n")

with open('memory/AUDIT_NOMS_RESIDUELS.md', 'w', encoding='utf-8') as out_f:
    out_f.write('\n'.join(report_lines))

print(f"Audit completed. Found {len(results)} issues.")
