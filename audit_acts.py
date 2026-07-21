import os
import re
import yaml
from datetime import date, datetime

dirs_to_scan = [
    "/home/crilocom/accident-main/⚖️ Actes/🔑 Token/⚖️ Actes proceduraux",
    "/home/crilocom/accident-main/⚖️ Actes/🔑 Token/✉️ Courriers"
]

all_md_files = []
for d in dirs_to_scan:
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith('.md') and f != 'README.md':
                all_md_files.append(os.path.join(root, f))

REQUIRED_TAGS = [
    "<!-- Auteur -->",
    "<!-- Destinataire -->",
    "<!-- Date -->",
    "<!-- Objet -->",
    "<!-- LRAR -->",
    "<!-- Signature -->",
    "<!-- PJ -->",
    "<!-- Source -->"
]

def parse_frontmatter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                return fm, parts[1], parts[2]
            except:
                return None, None, content
    return None, None, content

def build_frontmatter(fm):
    return "---\n" + yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False) + "---\n"

renames = {}

for file_path in all_md_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    fm, fm_text, body = parse_frontmatter(content)
    
    if fm is None:
        fm = {}

    modified = False

    # 1. Check YAML frontmatter fields
    if 'auteur' not in fm:
        fm['auteur'] = 'Antoine'
        modified = True
    if 'destinataire' not in fm:
        fm['destinataire'] = 'Inconnu'
        modified = True
    if 'type' not in fm:
        fm['type'] = 'Courrier' if 'Courriers' in file_path else 'Acte'
        modified = True

    # 2. Check tags
    for tag in REQUIRED_TAGS:
        if tag not in body:
            # Just append missing tags at the end for simplicity, or ideally place them at the top.
            # Usually these tags are scattered or at the top. Let's prepend them if missing.
            body = f"{tag}\n" + body
            modified = True

    if modified:
        new_content = build_frontmatter(fm) + body
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    # 3. Naming convention
    destinataire = str(fm.get('destinataire', 'Inconnu')).lower()
    
    prefix = ""
    if "tribunal judiciaire" in destinataire or "tj foix" in destinataire:
        prefix = "TJ Foix - "
    elif "tribunal de commerce" in destinataire or "tc foix" in destinataire:
        prefix = "TC Foix - "
    elif "juge" in destinataire and "instruction" in destinataire:
        prefix = "DJI Foix - "
    elif "procureur" in destinataire or "parquet" in destinataire:
        prefix = "Parquet Foix - "
    elif "cpam" in destinataire:
        prefix = "CPAM - "
    elif "mairie" in destinataire:
        prefix = "Mairie Foix - "
    elif "inspection du travail" in destinataire or "ddets" in destinataire:
        prefix = "DDETS - "
    elif "urssaf" in destinataire:
        prefix = "URSSAF - "
    elif "sas" in destinataire or "salon" in destinataire:
        prefix = "SAS HB BARBER - "
    elif "propriétaire" in destinataire or "proprietaire" in destinataire:
        prefix = "Propriétaire - "
    elif "inpi" in destinataire:
        prefix = "INPI - "
    elif "cada" in destinataire:
        prefix = "CADA - "
    elif "chiva" in destinataire:
        prefix = "CHIVA - "
    elif "fgti" in destinataire:
        prefix = "FGTI - "
    elif "médecin" in destinataire or "medecin" in destinataire:
        prefix = "Médecin - "
    elif "codaf" in destinataire:
        prefix = "CODAF - "

    base_name = os.path.basename(file_path)
    base_name_no_ext = os.path.splitext(base_name)[0]
    
    # Strip existing prefix if it already has one to avoid duplication
    # e.g., "TJ Foix - Conclusions.md"
    clean_base = base_name_no_ext
    # very naive: if it starts with the prefix, don't add it
    if prefix and clean_base.startswith(prefix):
        prefix_to_add = ""
    elif prefix:
        # Check if there's a different prefix like "Parquet - " and we want "Parquet Foix - "
        if prefix == "Parquet Foix - " and clean_base.startswith("Parquet - "):
            clean_base = clean_base.replace("Parquet - ", "", 1)
        if prefix == "TJ Foix - " and clean_base.startswith("TJ - "):
            clean_base = clean_base.replace("TJ - ", "", 1)
        prefix_to_add = prefix
    else:
        prefix_to_add = ""

    new_base_name = prefix_to_add + clean_base + ".md"
    
    if new_base_name != base_name:
        new_path = os.path.join(os.path.dirname(file_path), new_base_name)
        renames[file_path] = new_path

# Execute renames
for old_path, new_path in renames.items():
    if not os.path.exists(new_path):
        os.rename(old_path, new_path)

# Update internal links
# We need to find all .md files in the entire repo and replace old_base_name with new_base_name
all_repo_md = []
for root, _, files in os.walk("/home/crilocom/accident-main"):
    for f in files:
        if f.endswith('.md'):
            all_repo_md.append(os.path.join(root, f))

for file_path in all_repo_md:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for old_path, new_path in renames.items():
        old_name = os.path.splitext(os.path.basename(old_path))[0]
        new_name = os.path.splitext(os.path.basename(new_path))[0]
        
        # simple replace for markdown links [[Old Name]] -> [[New Name]]
        new_content = new_content.replace(f"[[{old_name}]]", f"[[{new_name}]]")
        # and standard links [text](Old Name.md)
        new_content = new_content.replace(f"]({old_name}.md)", f"]({new_name}.md)")
        new_content = new_content.replace(f"]({old_name})", f"]({new_name})")

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

print(f"Renamed {len(renames)} files and updated tags/YAML fields.")
