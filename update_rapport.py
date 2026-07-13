import re

with open("📊 Rapports/RAPPORT_STABILITE_TECHNIQUE_2026-07-14.md", "r") as f:
    content = f.read()

content = content.replace('"Grazide Sébastien" ou "sébastien grazide"', '"Prénom Nom" ou "prénom nom"')
content = content.replace('- La vérification', '  - La vérification')
content = content.replace('- Le script ne vérifie pas', '  - Le script ne vérifie pas')

with open("📊 Rapports/RAPPORT_STABILITE_TECHNIQUE_2026-07-14.md", "w") as f:
    f.write(content)
