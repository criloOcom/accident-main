import os
import re
import yaml
import urllib.parse

actes_dir = "⚖️ Actes"
token_dir = os.path.join(actes_dir, "🔑 Token")
reel_dir = os.path.join(actes_dir, "👤 Reel")

report = []

def add_issue(filepath, issue, gravity, correction):
    report.append({"Fichier": filepath, "Problème": issue, "Gravité": gravity, "Correction": correction})

def check_naming(filename):
    if filename == "README.md" or filename == ".gitkeep":
        return True
    return bool(re.match(r'^\d+[a-zA-Z\+]* .+\.md$', filename)) or bool(re.match(r'^\d+ \S+ .+\.md$', filename))

# Read token map to get list of tokens
tokens = []
try:
    with open("🧠 Memory/TOKEN MAP.md", "r", encoding="utf-8") as f:
        content = f.read()
        # extract all tokens in backticks
        raw_tokens = re.findall(r'`([^`]+)`', content)
        for t in raw_tokens:
            if t.startswith("**[") and t.endswith("]**"):
                tokens.append(t)
            elif t.startswith("[") and t.endswith("]"):
                tokens.append(t)
except Exception as e:
    print("Error reading token map:", e)

# Collect files
token_files = {}
for root, _, files in os.walk(token_dir):
    for file in files:
        if file.endswith(".md"):
            rel_path = os.path.relpath(os.path.join(root, file), token_dir)
            token_files[rel_path] = os.path.join(root, file)

reel_files = {}
for root, _, files in os.walk(reel_dir):
    for file in files:
        if file.endswith(".md"):
            rel_path = os.path.relpath(os.path.join(root, file), reel_dir)
            reel_files[rel_path] = os.path.join(root, file)

all_rel_paths = set(token_files.keys()).union(set(reel_files.keys()))

for rel_path in all_rel_paths:
    t_file = token_files.get(rel_path)
    r_file = reel_files.get(rel_path)

    filename = os.path.basename(rel_path)
    if filename in ["README.md", "00 📇 Index.md"]:
        pass

    # 1. Naming
    if not bool(re.match(r'^\d+[a-zA-Z\+]*\s+[^\s]+\s+.*\.md$', filename)):
        if filename != "README.md":
            add_issue(rel_path, "Non-respect de la convention de nommage [NUMÉRO] [TYPE] [DESCRIPTION].md", "🟡", f"Renommer selon la convention")

    # 4. Orphans
    if not t_file:
        add_issue(rel_path, "Fichier orphelin: présent dans Reel/ mais absent de Token/", "🔴", "Supprimer de Reel/ ou créer dans Token/")
        continue # Skip other checks for reel only if we only want to audit token logic? We'll check both.
    if not r_file:
        add_issue(rel_path, "Fichier orphelin: présent dans Token/ mais absent de Reel/", "🔴", "Générer la version Reel/")
        continue

    # Read files
    try:
        with open(t_file, "r", encoding="utf-8") as f:
            t_content = f.read()
    except Exception as e:
        t_content = ""
    try:
        with open(r_file, "r", encoding="utf-8") as f:
            r_content = f.read()
    except Exception as e:
        r_content = ""

    # 2. Frontmatter YAML
    yaml_match = re.search(r'^---\n(.*?)\n---', t_content, re.DOTALL)
    if not yaml_match:
        if filename != "README.md":
            add_issue(rel_path, "Frontmatter YAML manquant", "🔴", "Ajouter le bloc YAML")
    else:
        try:
            fm = yaml.safe_load(yaml_match.group(1))
            missing = []
            for key in ["date", "statut", "type", "destinataire"]:
                if key not in fm or fm[key] is None:
                    missing.append(key)
            if missing:
                add_issue(rel_path, f"Frontmatter incomplet, champs manquants: {', '.join(missing)}", "🟡", f"Compléter le YAML")
        except Exception as e:
            add_issue(rel_path, "Erreur de parsing YAML", "🔴", "Corriger la syntaxe YAML")

    # 3. Duplicates
    if t_content == r_content and filename != "README.md":
        add_issue(rel_path, "Fichiers Token/ et Reel/ identiques (pas d'anonymisation / génération effectuée ?)", "🟡", "Vérifier la nécessité des tokens ou regénérer")

    # 5. Dead links
    # regex for md links [text](link)
    links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', t_content)
    for link in links:
        if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
            continue

        unquoted_link = urllib.parse.unquote(link)
        # handle file:/// links gracefully if they are local
        if unquoted_link.startswith("file:///"):
            # try to extract relative part, but it's hard to know what the root is here
            if "⚖️ Actes" in unquoted_link:
                unquoted_link = unquoted_link.split("⚖️ Actes")[1].lstrip("/")
                link_path = os.path.join(actes_dir, unquoted_link)
                if not os.path.exists(link_path):
                    add_issue(rel_path, f"Lien mort trouvé: {link}", "🔴", "Corriger ou supprimer le lien")
            continue

        link_path = os.path.join(os.path.dirname(t_file), unquoted_link)
        if not os.path.exists(link_path):
            add_issue(rel_path, f"Lien mort trouvé: {link}", "🔴", "Corriger ou supprimer le lien")

    # 6. Coherence Token/Reel
    # Also check if Reel has `**[` or `]**`
    token_found = False
    if "**[" in r_content and "]**" in r_content:
        token_found = True
    else:
        # Check against tokens list
        for token in tokens:
            if token in r_content:
                token_found = True
                break

    if token_found:
        add_issue(rel_path, "Tokens restants dans Reel/", "🔴", "Mettre à jour le script de génération pour remplacer les tokens")

# Output table
print("| Fichier | Problème | Gravité (🔴/🟡/🟢) | Correction |")
print("|---|---|---|---|")
for row in sorted(report, key=lambda x: x["Fichier"]):
    print(f"| {row['Fichier']} | {row['Problème']} | {row['Gravité']} | {row['Correction']} |")
