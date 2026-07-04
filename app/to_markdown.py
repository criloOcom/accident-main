#!/usr/bin/env python3
import re

with open('/tmp/anonymized_assignation.txt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
result = []

for line in lines:
    stripped = line.strip()
    if stripped == '':
        result.append('')
        continue

    # Title
    if stripped == "ASSIGNATION EN RÉFÉRÉ-PROVISION ET DEMANDE D'EXPERTISE MÉDICALE":
        result.append(f"# {stripped}")
        continue

    # Subtitle
    if stripped.startswith("Devant le Président du Tribunal"):
        result.append(f"*{stripped}*")
        continue

    # Legal quotes: italic only, no blockquote
    if stripped.startswith('«'):
        result.append(f"*{stripped}*")
        continue

    if stripped == "PAR CES MOTIFS":
        result.append(f"## {stripped}")
        continue

    if re.match(r'^(I{1,3}|IV|V|VI)\.\s', stripped):
        result.append(f"## {stripped}")
        continue

    if re.match(r'^[A-Z]\.\s', stripped):
        result.append(f"### {stripped}")
        continue

    if stripped in ("POUR :", "CONTRE :"):
        result.append(f"## {stripped}")
        continue

    if stripped.startswith("PLAISE AU MONSIEUR LE PRÉSIDENT"):
        result.append(f"## {stripped}")
        continue

    if stripped.startswith('•'):
        content = stripped[1:].strip()
        result.append(f"- {content}")
        continue

    if re.match(r'^\d+\.\s', stripped):
        content = stripped.split('.', 1)[1].strip()
        result.append(f"1. {content}")
        continue

    result.append(stripped)

output = '\n'.join(result)
print(output)
