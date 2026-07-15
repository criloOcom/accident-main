import os
import re

def parse_markdown(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            return content
    except Exception as e:
        return ""

def extract_narrative(content):
    # Try to find sections titled "Faits", "Rappel des faits", "Circonstances", "Mécanisme", "Faits et Procédure"
    match = re.search(r'(?i)#+\s*(?:(?:Rappel des\s*)?(?:Faits|Circonstances|Mécanisme|Exposé du litige)|Faits\s+et\s+procédure).*?(?=\n#+ |\Z)', content, re.DOTALL)
    if match:
        return match.group(0).strip()
    return None

def check_consistency(directory):
    files_with_facts = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md") and "README" not in file:
                path = os.path.join(root, file)
                content = parse_markdown(path)
                facts = extract_narrative(content)

                # Check for facts inconsistencies
                keywords = ["vasque", "téléviseur", "télévision", "glissade", "chute", "basculement", "cassure", "glissé", "effondrée", "effondrement"]
                found_keywords = {kw for kw in keywords if kw.lower() in content.lower()}

                # Extract date, location
                date_match = re.search(r'29\s*(?:mai|05|juin|06)\s*2026', content, re.IGNORECASE)
                date_found = date_match.group(0) if date_match else None

                if facts or found_keywords or date_found:
                    files_with_facts[path] = {
                        "facts": facts,
                        "keywords": list(found_keywords),
                        "date": date_found
                    }

    return files_with_facts

# Check all docs
all_docs = {}
directories = [
    "⚖️ Actes/🔑 Token/",
    "📊 Rapports/"
]

for d in directories:
    results = check_consistency(d)
    all_docs.update(results)

# Dump summary to analyze
with open("narrative_analysis.txt", "w", encoding="utf-8") as f:
    for path, data in all_docs.items():
        f.write(f"\n{'='*50}\nFILE: {path}\nKEYWORDS: {', '.join(data['keywords'])}\nDATE: {data['date']}\n")
        if data['facts']:
            f.write(f"FACTS SNIPPET (first 1000 chars):\n{data['facts'][:1000]}\n")

print(f"Analyzed {len(all_docs)} files with narrative content.")
