import os
import re
import glob

REVERSE_MAP = {
    "**[La Victime]**": "Sébastien GRAZIDE",
    "**[Le Président de l'Exploitation]**": "Mountasser SABIR",
    "**[Le President de l'Exploitation]**": "Mountasser SABIR",
    "**[La Directrice Générale de l'Exploitation]**": "Catherine ANDISSAC",
    "**[La Directrice Generale de l'Exploitation]**": "Catherine ANDISSAC",
    "**[Le Préposé de l'Exploitation]**": "Ayoub BENNOURINE",
    "**[Le Prepose de l'Exploitation]**": "Ayoub BENNOURINE",
    "[Le Prepose de l'Exploitation]": "Ayoub BENNOURINE",
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
    "**[L'Adjoint au Maire de la Commune]**": "Monsieur TAVELLA",
}

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
    input_base = 'actes/token'
    output_base = 'actes/reel'

    generated = []

    for subdir in sorted(os.listdir(input_base)):
        input_dir = os.path.join(input_base, subdir)
        if not os.path.isdir(input_dir):
            continue

        output_dir = os.path.join(output_base, subdir)
        os.makedirs(output_dir, exist_ok=True)

        sub_generated = []
        for filepath in sorted(glob.glob(os.path.join(input_dir, '*.md'))):
            filename = os.path.basename(filepath)
            if filename in ('INDEX.md', 'README.md'):
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            content = update_yaml_frontmatter(content)
            content = replace_header_block(content)
            for token, real_val in REVERSE_MAP.items():
                content = content.replace(token, real_val)
            content = content.replace("**[Adresse à compléter]**", "[À compléter]")
            content = content.replace("**[À compléter]**", "[À compléter]")

            outpath = os.path.join(output_dir, filename)
            with open(outpath, 'w', encoding='utf-8') as f:
                f.write(content)

            sub_generated.append(filename)
            print(f"  {outpath}")

        if sub_generated:
            idx_path = os.path.join(output_dir, 'README.md')
            with open(idx_path, 'w', encoding='utf-8') as f:
                f.write(f"# Index — {subdir} (Versions Réelles)\n\n")
                for fn in sorted(sub_generated):
                    f.write(f"- [{fn}]({fn})\n")
            print(f"  {idx_path}")
            generated.append((subdir, sub_generated))

    total = sum(len(files) for _, files in generated)
    print(f"\n--- {total} fichiers générés dans {output_base}/ ---")

if __name__ == '__main__':
    main()
