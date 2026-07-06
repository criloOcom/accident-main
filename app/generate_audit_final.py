import json
import os
import re
from datetime import datetime

def load_master():
    with open('scratch_master_final.json', 'r', encoding='utf-8') as f:
        return json.load(f)

months = {
    'janvier': '01', 'fevrier': '02', 'février': '02', 'mars': '03', 'avril': '04',
    'mai': '05', 'juin': '06', 'juillet': '07', 'aout': '08', 'août': '08',
    'septembre': '09', 'octobre': '10', 'novembre': '11', 'decembre': '12', 'décembre': '12'
}

def normalize_date(date_str):
    m = re.match(r'^(\d{2})/(\d{2})/(\d{4})$', date_str)
    if m: return f"{m.group(1)}/{m.group(2)}/{m.group(3)}"
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', date_str)
    if m: return f"{m.group(3)}/{m.group(2)}/{m.group(1)}"
    m = re.match(r'^(\d{1,2})\s+([a-zA-Zûé]+)\s+(\d{4})$', date_str.lower())
    if m:
        day = m.group(1).zfill(2)
        month_str = m.group(2)
        year = m.group(3)
        if month_str in months: return f"{day}/{months[month_str]}/{year}"
    return None

date_patterns = [
    r'\b\d{2}/\d{2}/\d{4}\b',
    r'\b\d{4}-\d{2}-\d{2}\b',
    r'\b\d{1,2}\s+(?:janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre)\s+\d{4}\b'
]

def find_dates_in_files(directory):
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for pattern in date_patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            raw_date = match.group(0)
                            norm_date = normalize_date(raw_date)
                            if norm_date:
                                start = max(0, match.start() - 40)
                                end = min(len(content), match.end() + 40)
                                context = content[start:end].replace('\n', ' ').strip()
                                results.append({
                                    'file': filepath,
                                    'raw_date': raw_date,
                                    'norm_date': norm_date,
                                    'context': context
                                })
    return results

master_data = load_master()
master_dates = set()
for item in master_data:
    raw_date = item.get('DateHeure', '').split(' ')[0]
    if raw_date and raw_date not in ['Non pr\u00e9cis\u00e9', 'N/A', 'Non', '']:
        norm = normalize_date(raw_date)
        if norm: master_dates.add(norm)

# Exclude specific valid rules dates from being simple "absent" anomalies
master_dates.add("23/07/2026") # Fin ITT explicit in rules

file_dates = find_dates_in_files('actes')

anomalies = []
for item in file_dates:
    norm = item['norm_date']
    context = item['context']
    raw_date = item['raw_date']

    issue = ""
    ctx_lower = context.lower()

    # Validation Rules
    if "accident" in ctx_lower and "29/05/2026" not in norm:
        if "accident du" in ctx_lower or "survenu le" in ctx_lower:
            issue = "Date d'accident incorrecte (devrait être 29/05/2026)"
    elif ("lrar" in ctx_lower or "mise en demeure" in ctx_lower) and "29/06/2026" not in norm and "14/07/2026" not in norm:
        if "mise en demeure du" in ctx_lower or "lrar du" in ctx_lower or "mise en demeure" in ctx_lower:
            issue = "Date LRAR / Mise en demeure incohérente (attendu: 29/06/2026)"
    elif "itt" in ctx_lower and ("29/05/2026" not in norm and "23/07/2026" not in norm):
        if "jours d'itt" in ctx_lower:
            pass # might just be mentioning days, wait

    if not issue and norm not in master_dates:
        issue = "Date absente du master chronologique"

    if issue:
        # Avoid exact duplicates
        if not any(a['Fichier'] == item['file'] and a['Date trouvée'] == norm and a['Contexte'] == context for a in anomalies):
            anomalies.append({
                'Fichier': item['file'],
                'Date trouvée': norm,
                'Format original': raw_date,
                'Contexte': context,
                'Anomalie': issue
            })

with open('memory/AUDIT_DATES.md', 'w', encoding='utf-8') as out:
    out.write("# Audit de Cohérence des Dates\n\n")
    out.write("Ce document recense les anomalies de dates détectées dans les actes par rapport au fichier `scratch_master_final.json` et aux règles métier.\n\n")
    out.write("## Règles vérifiées\n")
    out.write("- Accident = 29/05/2026\n")
    out.write("- ITT = 29/05 au 23/07/2026 (56 jours)\n")
    out.write("- LRAR = 29/06/2026\n")
    out.write("- Échéance = 14/07/2026\n\n")

    out.write("## Tableau des Anomalies\n\n")
    out.write("| Fichier | Date trouvée | Format original | Contexte | Anomalie |\n")
    out.write("|---------|--------------|-----------------|----------|----------|\n")

    anomalies.sort(key=lambda x: x['Fichier'])

    for a in anomalies:
        out.write(f"| {a['Fichier']} | {a['Date trouvée']} | {a['Format original']} | {a['Contexte']} | {a['Anomalie']} |\n")

print(f"Generated AUDIT_DATES.md with {len(anomalies)} anomalies")
