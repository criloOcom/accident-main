import os
import re
import glob
import urllib.parse
import yaml

# Hardcoded fallback for items not in tokens or strict variables easily parseable
FALLBACK_MAP = {
    "N° LRAR Exploitant": "87001424863012T",
    "N° LRAR Président": "87001424862879J",
    "N° LRAR Directrice": "87001424721856G",
    "N° LRAR Propriétaire": "87001424862462Y",
    "N° LRAR Parquet": "87001424923505I",
    "N° LRAR HB BARBER Société": "87500152771696F",
    "N° LRAR HB BARBER Président": "875001528942001",
    "N° LRAR HB BARBER DG": "875001528942010",
    "N° LRAR CHIVA": "87500152888336B",
    "N° LRAR Propriétaire Relance 3": "87500152910287Q",
    "N° Dossier CPAM": "31727387",
    "N° Dossier CPAM erroné": "2631103960",
    "N° Transaction Wero": "IPR000297029234",
    "N° PV Police": "2026/015967",
    "Le Prepose de l'Exploitation": "Ayoub BENNOURINE",
    "Le Medecin en Urgence": "Dr Julie JARDON",
    "Le Medecin Generaliste": "Dr Oxybel",
    "L'Etablissement SOS Main": "Clinique de l'Union",
    "L'Adresse du President": "115 avenue Fernand Loubet, 09200 Saint-Girons",
    "La Ville de Residence de la Victime": "Blagnac",
    "La Ville de l'Etablissement SOS Main": "Saint-Jean",
    "Age de la Victime": "44 ans",
    "Le President de l'Exploitation": "Hamza El Hachemi BERGUIGA",
    "La Directrice Generale de l'Exploitation": "Catherine SORROCHE, dite ANDISSAC",
    "Adresse du Commerce": "22 Rue Lafaurie, 09000 Foix",
    "Centre de soins immédiats": "Centre Ariégeois de Soins Immédiats",
    "L'Adresse du Centre de soins immédiats": "4 Rue du Sénateur Paul Laffont, 09000 Foix",
    "Le RPPS du Médecin en Urgence": "10005156871",
}

def extract_tokens_from_yaml(tokens_dir):
    token_map = {}
    for root, _, files in os.walk(tokens_dir):
        for f in files:
            if not f.endswith('.md') or f in ('README.md', 'INDEX.md'):
                continue
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Extract yaml block
            m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if m:
                yaml_content = m.group(1)
                try:
                    data = yaml.safe_load(yaml_content)
                    if data and 'description' in data and 'real_value' in data:
                        desc = data['description']
                        real_val = data['real_value']
                        # desc: "Token :** `**[Token_Name]**`"
                        m2 = re.search(r'`\*\*\[(.*?)\]\*\*`', desc)
                        if m2:
                            token_map[m2.group(1)] = real_val
                except Exception as e:
                    pass
    return token_map

def extract_strict_variables(path):
    token_map = {}
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Match the financial/LRAR tables: | `[Token_Name]` | Variable | Value |
    matches = re.findall(r'\|\s*`\[([^\]]+)\]`\s*\|\s*[^|]+\|\s*([^|]+?)\s*\|', content)
    for token_name, value in matches:
        token_map[token_name] = value.strip()
    return token_map

def build_reverse_map():
    map = FALLBACK_MAP.copy()
    
    # 1. Extract from yaml
    map.update(extract_tokens_from_yaml('Memory/Tokens'))
    
    # 2. Extract from STRICT VARIABLES
    map.update(extract_strict_variables('Memory/STRICT VARIABLES.md'))
    
    # Make sure we add bracket-less keys for all
    return map

def replace_header_block(content):
    pattern = r"\*\*\[L'Adresse de la Victime\]\*\*\n\nCourriel : \*\*\[L'Email de la Victime\]\*\*"
    replacement = "Sébastien GRAZIDE\n10 Avenue de Purpan, 31700 Blagnac\nCourriel : sebastien.grazide@gmail.com"
    return re.sub(pattern, replacement, content)

def update_yaml_frontmatter(content):
    def replacer(match):
        title_line = match.group(0)
        if " - Version réelle" not in title_line:
            return title_line + " - Version réelle"
        return title_line
    return re.sub(r'^titre:\s*.*$', replacer, content, flags=re.MULTILINE)

def main():
    input_base = 'Actes/Token'
    output_base = 'Actes/Reel'

    token_map = build_reverse_map()
    # Sort keys by length descending to prevent partial replacements (e.g. Finance DFP vs Finance DFP initial)
    sorted_keys = sorted(token_map.keys(), key=len, reverse=True)

    generated = []

    for root, dirs, files in os.walk(input_base):
        rel_path = os.path.relpath(root, input_base)
        if rel_path == '.':
            continue

        dirs.sort()
        output_dir = os.path.join(output_base, rel_path)
        os.makedirs(output_dir, exist_ok=True)

        sub_generated = []
        for filepath in sorted(glob.glob(os.path.join(root, '*.md'))):
            filename = os.path.basename(filepath)
            if filename in ('INDEX.md', 'README.md'):
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            content = update_yaml_frontmatter(content)
            content = replace_header_block(content)
            
            for token_name in sorted_keys:
                real_val = token_map[token_name]
                escaped_name = re.escape(token_name)
                
                # Replace markdown link tokens: **[Token](path)**, [Token](path), etc.
                # Regex matches optional asterisks, then [, the token name, ], then (anything not parenthesis)
                link_pattern = r'\*?\*?\[\s*' + escaped_name + r'\s*\]\([^)]+\)\*?\*?'
                content = re.sub(link_pattern, real_val, content)
                
                # Replace plain tokens: **[Token]**, [Token]
                plain_pattern = r'\*?\*?\[\s*' + escaped_name + r'\s*\]\*?\*?'
                content = re.sub(plain_pattern, real_val, content)
                
            content = content.replace("**[Adresse à compléter]**", "[À compléter]")
            content = content.replace("**[À compléter]**", "[À compléter]")
            content = content.replace(" ↩", "")

            outpath = os.path.join(output_dir, filename)
            with open(outpath, 'w', encoding='utf-8') as f:
                f.write(content)

            sub_generated.append(filename)
            print(f"  {outpath}")

        if sub_generated:
            idx_path = os.path.join(output_dir, 'README.md')
            with open(idx_path, 'w', encoding='utf-8') as f:
                f.write(f"# Index — {rel_path} (Versions Réelles)\n\n")
                for fn in sorted(sub_generated):
                    f.write(f"- [{fn}]({urllib.parse.quote(fn)})\n")
            print(f"  {idx_path}")
            generated.append((rel_path, sub_generated))

    total = sum(len(files) for _, files in generated)
    print(f"\n--- {total} fichiers générés dans {output_base}/ ---")

if __name__ == '__main__':
    main()
