import os
import re
import glob
import yaml

def load_tokens_map():
    tokens_map = {}
    
    # 1. Parse all Memory/Tokens/*.md YAML frontmatter
    for p in glob.glob('Memory/Tokens/*.md'):
        try:
            with open(p, 'r', encoding='utf-8') as f:
                c = f.read()
                if c.startswith('---'):
                    parts = c.split('---', 2)
                    if len(parts) >= 3:
                        y = yaml.safe_load(parts[1])
                        if isinstance(y, dict):
                            t_name = y.get('token')
                            r_val = y.get('real_value')
                            if t_name and r_val:
                                clean_t = str(t_name).strip().lstrip('[').rstrip(']')
                                tokens_map[clean_t] = str(r_val).strip()
        except Exception:
            pass

    # 2. Comprehensive fallbacks & alias mapping (including multiline variants)
    fallbacks = {
        "La Victime": "Sébastien GRAZIDE",
        "L'Adresse de la Victime": "10 Avenue de Purpan, 31700 Blagnac",
        "L'Email de la Victime": "sebastien.grazide@gmail.com",
        "Le Téléphone de la Victime": "06 30 51 67 75",
        "Téléphone de la Victime": "06 30 51 67 75",
        "Date de Naissance de la Victime": "18 janvier 1982",
        "L'Identifiant Professionnel de la Victime": "500 474 457",
        "L'Adresse de l'Exploitation": "22 Rue Lafaurie, 09000 Foix",
        "Adresse du Commerce": "22 Rue Lafaurie, 09000 Foix",
        "La Ville de l'Accident": "Foix",
        "LA VILLE DE L'ACCIDENT": "Foix",
        "Code Postal de l'Accident": "09000",
        "Code Postal Accident": "09000",
        "La Métropole Régionale": "Toulouse",
        "La Ville de Résidence de la Victime": "Blagnac",
        "La Ville de Residence de la Victime": "Blagnac",
        "L'Exploitant du Commerce (La SAS)": "SAS LES MAUVAIS GARCONS",
        "L'Exploitant\n  du Commerce (La SAS)": "SAS LES MAUVAIS GARCONS",
        "L'Exploitant du Commerce": "SAS LES MAUVAIS GARCONS",
        "L'EXPLOITANT DU COMMERCE": "SAS LES MAUVAIS GARCONS",
        "L'Exploitant": "SAS LES MAUVAIS GARCONS",
        "Le Commerce de l'Exploitation": "SAS LES MAUVAIS GARCONS",
        "Nom Commercial de l'Exploitation": "HB BARBER",
        "SIREN de l'Exploitation": "938 033 222",
        "SIRET de l'Exploitation": "938 033 222 00010",
        "L'Identifiant de l'Exploitation": "938 033 222 00010",
        "Capital Social de l'Exploitation": "1 000 €",
        "Capital Exploitant": "1 000 €",

        # Former exploitation
        "L'Ancien Exploitant du Commerce": "SAS LES MAUVAIS GARCONS",
        "L'Ancien Identifiant de l'Exploitation": "938 033 222 00010",
        "SIREN de l'Ancien Exploitant": "938 033 222",
        "L'Ancien Président de l'Exploitation": "Sabir MOUNTASSER",
        "L'Ancienne Directrice Générale de l'Exploitation": "Catherine ANDISSAC",

        # People
        "Le Président de l'Exploitation": "Hamza El Hachemi BERGUIGA",
        "Le President de l'Exploitation": "Hamza El Hachemi BERGUIGA",
        "L'Adresse du Président": "115 avenue Fernand Loubet, 09200 Saint-Girons",
        "L'Adresse du President": "115 avenue Fernand Loubet, 09200 Saint-Girons",
        "La Directrice Générale de l'Exploitation": "Catherine SORROCHE, dite ANDISSAC",
        "La Directrice Generale de l'Exploitation": "Catherine SORROCHE, dite ANDISSAC",
        "L'Adresse de la Directrice Générale": "351 route Impériale, 34670 Baillargues",
        "Le Préposé de l'Exploitation": "Ayoub BENNOURINE",
        "Le Prepose de l'Exploitation": "Ayoub BENNOURINE",
        "Le Telephone du Prepose": "07 58 40 12 87",
        "Le Téléphone du Préposé": "07 58 40 12 87",
        "Le Prénom du Préposé": "Ayoub",
        "Le Propriétaire des Murs": "Romain DELRIEU",
        "Le Proprietaire des Murs": "Romain DELRIEU",
        "Adresse du Propriétaire des Murs": "17 rue de la Baïse, 31120 Roquettes",
        "L'Adresse du Propriétaire des Murs": "17 rue de la Baïse, 31120 Roquettes",
        "L'Email du Propriétaire des Murs": "romain.delrieu@live.fr",
        "Le Chirurgien SOS Main": "Dr Iskander DJERBI",
        "RPPS Chirurgien SOS Main": "10101234567",
        "Le Médecin en Urgence": "Dr Julie JARDON",
        "Le Medecin en Urgence": "Dr Julie JARDON",
        "RPPS Médecin Urgence": "10107654321",
        "Le RPPS du Médecin en Urgence": "10107654321",
        "Le Médecin Généraliste": "Dr Oxybel",
        "Le Médecin de Suivi": "Dr Prisca AKUÉ",
        "Le Medecin de Suivi": "Dr Prisca AKUÉ",
        "Le Medecin Generaliste": "Dr Oxybel",
        "Le Médecin Traitant": "Dr Oxybel",
        "RPPS Médecin Traitant": "10109876543",
        "La Gestionnaire CPAM": "Sigrid DESBOIS",
        "L'Adjoint au Maire de la Commune": "Monsieur TAVELLA",
        "L'Adjoint au Maire\n  de la Commune": "Monsieur TAVELLA",
        "L'Adjoint au Maire": "Monsieur TAVELLA",
        "L'Email de l'Adjoint au Maire": "b.tavella@mairie-foix.fr",
        "L''Email de l''Adjoint au Maire": "b.tavella@mairie-foix.fr",
        "L'Email du Secrétariat de la Mairie": "secretariat.maire@mairie-foix.fr",
        "Email Secrétariat Mairie": "secretariat.maire@mairie-foix.fr",
        "Email Adjoint au Maire": "b.tavella@mairie-foix.fr",
        "La Secrétaire Générale de la Mairie": "Secrétariat Général de la Mairie de Foix",
        "L'Adresse de la Mairie de la Commune": "Cour de l'Hôtel de Ville, 09000 Foix",
        "Agent PJ, dépôt de plainte": "Jordy RODRIGUEZ CAPARROS",
        "L'Agent de Police Judiciaire": "Jordy RODRIGUEZ CAPARROS",
        "Centre de soins immédiats": "Centre Ariégeois de Soins Immédiats",
        "L'Adresse du Centre de soins immédiats": "Foix",
        "SMUR local": "SMUR 09",
        "L'Hôpital de Purpan (CHU Toulouse)": "CHU de Toulouse Purpan",
        "Le Témoin Mathieu": "Mathieu FRÉDÉRICK",
        "Le Témoin Clé Mathieu": "Mathieu FRÉDÉRICK",

        # Dates & Refs
        "N° PV Police": "2026/015967",
        "N° Dossier CPAM": "31727387",
        "N° Dossier CPAM Victime": "31727387",
        "J+0 Accident": "29 mai 2026",
        "Date de l'Accident": "29 mai 2026",
        "J+1 Chirurgie": "30 mai 2026",
        "J+2 Sortie": "31 mai 2026",
        "J+3 Premiers arrêts": "1 juin 2026",
        "J+4 Dépôt de plainte": "2 juin 2026",
        "J+5 Ouverture CPAM": "3 juin 2026",
        "J+12 Facture": "10 juin 2026",
        "J+18 Incohérence CPAM": "16 juin 2026",
        "J+21 Contrôle chirurgical": "19 juin 2026",
        "J+25 Première kiné": "23 juin 2026",
        "J+27 Confirmation kiné": "25 juin 2026",
        "J+31 Mises en demeure": "29 juin 2026",
        "J+32 Assignation référé": "30 juin 2026",
        "J+33 Plainte complémentaire": "1 juillet 2026",
        "J+35 AR propriétaire": "3 juillet 2026",
        "J+36 Lettre consolidation": "4 juillet 2026",
        "J+37 Assignation 145": "5 juillet 2026",
        "J+38 Constitution PC": "6 juillet 2026",
        "J+38 Mise à jour": "6 juillet 2026",
        "J+40 Consultation suivi": "8 juillet 2026",
        "J+41 Requete Constat 145": "9 juillet 2026",
        "J+46 Échéance amiable": "14 juillet 2026",
        "J+53 Demande attestation préposé": "21 juillet 2026",
        "J+53 Demande attestation président": "21 juillet 2026",
        "J+55 Fin d'ITT": "23 juillet 2026",
        "J+167 Expertise UMJ": "12 novembre 2026",
        "DATE RELANCE V2": "8 juillet 2026",
        "DATE REOUVERTURE BOUTIQUE": "6 juillet 2026",

        # LRAR Numbers
        "N° LRAR Exploitant": "87001424863012T",
        "N° LRAR Président": "87001424862879J",
        "N° LRAR Directrice": "87001424721856G",
        "N° LRAR DG": "87001424721856G",
        "N° LRAR Propriétaire": "87001424862462Y",
        "N° LRAR Parquet": "87001424923505I",
        "N° LRAR CHIVA": "87001424998811A",
        "N° LRAR Ancienne Directrice": "87001424721856G",
        "N° LRAR Ancien Président": "87001424862879J",
        "N° LRAR HB BARBER Société": "87001424863012T",
        "N° LRAR HB BARBER DG": "87001424721856G",
        "N° LRAR HB BARBER Président": "87001424862879J",
        "N° LRAR Propriétaire Relance 3": "87001424862462Y",

        # Finances
        "Finance Provision Référé": "15 000 €",
        "Finance Article 700": "3 000 €",
        "Finance Astreinte 145": "150 €",
        "Finance Article 700 Référé 145": "1 500 €",
        "Finance Article 475-1": "3 000 €",
        "Finance PGPA": "1 380 €",
        "Finance DFP": "25 000 €",
        "Finance Souffrances Endurées": "15 000 €",
        "Finance Incidence Professionnelle": "30 000 €",
        "Finance Préjudice Agrément": "5 000 €",
        "Finance Préjudice Esthétique": "3 000 €",
        "Finance Dévalorisation Pro": "3 000 €",
        "Finance Frais Divers": "3 000 €",
        "Finance Facture Chirurgie": "790,23 €",
        "Finance Prestation Salon": "15,00 €",
        "Finance Evaluation Initiale": "85 000 €",
    }

    for k, v in fallbacks.items():
        if k not in tokens_map:
            tokens_map[k] = v

    return tokens_map

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

def find_md_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for f in sorted(filenames):
            if f.endswith('.md') and f not in ('INDEX.md', 'README.md'):
                yield os.path.join(dirpath, f)

def main():
    tokens_map = load_tokens_map()
    input_base = 'Actes/Token'
    output_base = 'Actes/Reel'

    generated = []
    sorted_tokens = sorted(tokens_map.items(), key=lambda x: -len(x[0]))

    for filepath in find_md_files(input_base):
        rel_path = os.path.relpath(filepath, input_base)
        outpath = os.path.join(output_base, rel_path)
        os.makedirs(os.path.dirname(outpath), exist_ok=True)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        content = update_yaml_frontmatter(content)
        content = replace_header_block(content)

        # 1. First pass: strip Markdown link target wrappers around tokens
        content = re.sub(r'\[(\*\*\[[^\]]+\]\*\*|\[[^\]]+\])\]\([^)]*Memory/Tokens/[^)]*\)', r'\1', content)
        content = re.sub(r'(\*\*\[[^\]]+\]\*\*|\[[^\]]+\])\([^)]*Memory/Tokens/[^)]*\)', r'\1', content)
        content = re.sub(r'\[([^\]]+)\]\([^)]*Memory/Tokens/[^)]*\)', r'\1', content)

        # 2. Adapt Actes/Token/ relative links to Actes/Reel/
        content = content.replace('/Actes/Token/', '/Actes/Reel/')

        # 2b. Fix redundant '/Reel/' segment in relative links.
        # Token files legitimately link to '../../../Reel/Courriers/X.md' (the real mirror).
        # In the Reel mirror, that same relative path would resolve to 'Actes/Reel/Reel/Courriers/X.md'
        # (broken). Since the mirror is already under Actes/Reel, drop the redundant '/Reel/' segment.
        content = re.sub(r'(\.\./)+Reel/', lambda m: m.group(0).replace('Reel/', '', 1), content)

        # 3. Second pass: Replace token strings with real values
        for token_name, real_val in sorted_tokens:
            content = content.replace(f'**[{token_name}]**', real_val)
            content = content.replace(f'[{token_name}]', real_val)

        content = content.replace("**[Adresse à compléter]**", "[À compléter]")
        content = content.replace("**[À compléter]**", "[À compléter]")

        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(content)

        generated.append(outpath)
        print(f"  {outpath}")

    total = len(generated)
    print(f"\n--- {total} fichiers générés dans {output_base}/ ---")

if __name__ == '__main__':
    main()

def deduplicate_lrar_numbers(content):
    content = re.sub(r'(LRAR n° \[[0-9a-zA-Z]+\]\([^)]+\))\s*—\s*`[0-9a-zA-Z]+`', r'\1', content)
    content = re.sub(r'\(LRAR n° ([0-9a-zA-Z]+)\s*—\s*[0-9a-zA-Z]+\)', r'(LRAR n° \1)', content)
    content = re.sub(r'LRAR n° ([0-9a-zA-Z]+)\s*—\s*[0-9a-zA-Z]+', r'LRAR n° \1', content)
    content = re.sub(r'LRAR n° <([0-9a-zA-Z]+)>\s*—\s*[0-9a-zA-Z]+', r'LRAR n° <\1>', content)
    return content

def preprocess_nested_bracket_tokens(content):
    content = re.sub(r'\[\*\*\[N° \[Dossier CPAM\]\([^)]+\)\]\*\*\]\([^)]+\)', '31727387', content)
    content = re.sub(r'\*\*\[N° \[Dossier CPAM\]\([^)]+\)\]\*\*', '31727387', content)
    content = re.sub(r'\[\*\*\[N° \[Dossier CPAM erroné\]\([^)]+\)\]\*\*\]\([^)]+\)', '2631103960', content)
    content = re.sub(r'\*\*\[N° \[Dossier CPAM erroné\]\([^)]+\)\]\*\*', '2631103960', content)
    return content
