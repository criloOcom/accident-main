import os
import re
import glob

# Reverse mapping based on memory/TOKEN MAP.md and STRICT VARIABLES.md
REVERSE_MAP = {
    "**[La Victime]**": "Sébastien GRAZIDE",
    "**[Le Président de l'Exploitation]**": "Mountasser SABIR",
    "**[Le President de l'Exploitation]**": "Mountasser SABIR",
    "**[La Directrice Générale de l'Exploitation]**": "Catherine ANDISSAC",
    "**[La Directrice Generale de l'Exploitation]**": "Catherine ANDISSAC",
    "**[Le Préposé de l'Exploitation]**": "Ayoub BENNOURINE",
    "**[Le Prepose de l'Exploitation]**": "Ayoub BENNOURINE",
    "[Le Prepose de l'Exploitation]": "Ayoub BENNOURINE", # specifically added for line in Doc 12
    "**[Le Propriétaire des Murs]**": "Romain DELRIEU",
    "**[Le Chirurgien SOS Main]**": "Dr Iskander DJERBI",
    "**[Le Médecin en Urgence]**": "Dr Julie JARDON",
    "**[Le Médecin Généraliste]**": "Dr Oxybel",
    "**[Le Medecin Generaliste]**": "Dr Oxybel",
    "**[La Gestionnaire CPAM]**": "Sigrid DESBOIS",
    "**[Nom de l'Avocat de la Victime]**": "Nom Prénom de l'Avocat",
    "**[L'Exploitant du Commerce]**": "SAS LES MAUVAIS GARCONS",
    "**[Le Commerce de l'Exploitation]**": "SAS LES MAUVAIS GARCONS",
    "**[L'Établissement SOS Main]**": "Clinique de l'Union",
    "**[L'Adresse de la Victime]**": "10 Avenue de Purpan, 31700 Blagnac",
    "**[L'Adresse de l'Exploitation]**": "22 Rue Lafaurie, 09000 Foix",
    "**[Adresse du Commerce]**": "22 Rue Lafaurie, 09000 Foix",
    "**[L'Adresse du Président]**": "108 Avenue Paul Bert, 09000 Foix",
    "**[La Ville de l'Accident]**": "Foix",
    "**[La Ville de Résidence de la Victime]**": "Blagnac",
    "**[La Métropole Régionale]**": "Toulouse",
    "**[La Ville de l'Établissement SOS Main]**": "Saint-Jean",
    "**[L'Email de la Victime]**": "sebastien.grazide@gmail.com",
    "**[L'Identifiant Professionnel de la Victime]**": "500 474 457",
    "**[L'Identifiant de l'Exploitation]**": "938 033 222 00010",
    "**[L'Adjoint au Maire de la Commune]**": "Monsieur TAVELLA" # Given the context of 08_Courrier Suivi TAVELLA
}

# The address block mapping that removes the asterisks entirely for the victim's header
# We want to replace this exact string or similar block with the correct info, but we'll do this carefully.

def replace_header_block(content):
    # Search for the address block
    # Note: it's possible the block has empty lines
    # We'll use regex to match the block
    pattern = r"\*\*\[L'Adresse de la Victime\]\*\*\n\nCourriel : \*\*\[L'Email de la Victime\]\*\*"
    replacement = "Sébastien GRAZIDE\n10 Avenue de Purpan, 31700 Blagnac\nCourriel : sebastien.grazide@gmail.com"
    content = re.sub(pattern, replacement, content)
    return content

def update_yaml_frontmatter(content):
    # Add " - Version réelle" to the "titre:" field in the frontmatter
    def replacer(match):
        title_line = match.group(0)
        if " - Version réelle" not in title_line:
            return title_line + " - Version réelle"
        return title_line
    return re.sub(r'^titre:\s*.*$', replacer, content, flags=re.MULTILINE)

def main():
    input_dir = 'actes/02_Courriers'
    output_dir = 'actes/07_Reel'
    os.makedirs(output_dir, exist_ok=True)

    generated_files = []

    # Read all files in input_dir
    filepaths = glob.glob(os.path.join(input_dir, '*.md'))
    for filepath in filepaths:
        filename = os.path.basename(filepath)

        # Skip INDEX.md if it exists in there somehow
        if filename == 'INDEX.md':
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update YAML frontmatter
        content = update_yaml_frontmatter(content)

        # Replace header block specifically for the victim
        content = replace_header_block(content)

        # Replace tokens
        for token, real_val in REVERSE_MAP.items():
            content = content.replace(token, real_val)

        # Address to complete is a placeholder that wasn't previously a mapped token
        content = content.replace("**[Adresse à compléter]**", "[À compléter]")
        content = content.replace("**[À compléter]**", "[À compléter]")

        # Write out
        outpath = os.path.join(output_dir, filename)
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(content)

        generated_files.append(filename)
        print(f"Generated {outpath}")

    # Write INDEX.md
    index_path = os.path.join(output_dir, 'INDEX.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# Index des Courriers (Versions Réelles)\n\n")
        for filename in sorted(generated_files):
            f.write(f"- [{filename}]({filename})\n")

    print(f"Generated {index_path}")

if __name__ == '__main__':
    main()
