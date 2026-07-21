import os
import re
import glob
import urllib.parse
import yaml

FALLBACK_MAP = {
    "L'Exploitant du Commerce": "SAS HB BARBER",
    "L'EXPLOITANT DU COMMERCE (LA SAS)": "SAS HB BARBER",
    "L'Ancien Exploitant du Commerce": "SAS LES MAUVAIS GARÇONS",
    "L'Assureur RC": "[Assurance RC Inconnue]",
    "L''Adresse de la Victime": "10 Avenue de Purpan, 31700 Blagnac",
    "L'Email du Propriétaire des Murs": "[Email du Propriétaire]",
    "L'Avocat de la Victime": "Nom Prénom de l'Avocat",
    "L'Exploitant": "SAS HB BARBER",
    "Capital Exploitant": "1 000 €",
    "RCS Ville Exploitant": "Foix",
    "Siret Exploitant": "104 103 262 00010",
    "Adresse Exploitant": "22 Rue Lafaurie, 09000 Foix",
    "Date de l'Accident": "29 mai 2026",
    "Assureur RC Exploitant": "[Assurance RC Inconnue]",
    "L'Adresse de la Mairie de la Commune": "Mairie de Foix",
    "L'Hôpital de Purpan (CHU Toulouse)": "Hôpital de Purpan (CHU Toulouse)",
    "La Victime": "Sébastien GRAZIDE",
    "Le Président de l'Exploitation": "Hamza El Hachemi BERGUIGA",
    "Le President de l'Exploitation": "Hamza El Hachemi BERGUIGA",
    "La Directrice Générale de l'Exploitation": "Catherine SORROCHE, dite ANDISSAC",
    "La Directrice Generale de l'Exploitation": "Catherine SORROCHE, dite ANDISSAC",
    "Le Préposé de l'Exploitation": "Ayoub BENNOURINE",
    "Le Prepose de l'Exploitation": "Ayoub BENNOURINE",
    "Le Propriétaire des Murs": "Romain DELRIEU",
    "Le Chirurgien SOS Main": "Dr Iskander DJERBI",
    "Le Médecin en Urgence": "Dr Julie JARDON",
    "Le Medecin en Urgence": "Dr Julie JARDON",
    "Le Médecin Généraliste": "Dr Oxybel",
    "Le Medecin Generaliste": "Dr Oxybel",
    "La Gestionnaire CPAM": "Sigrid DESBOIS",
    "Nom de l'Avocat de la Victime": "Nom Prénom de l'Avocat",
    "L'Exploitant du Commerce (La SAS)": "SAS HB BARBER",
    "Le Commerce de l'Exploitation": "SAS HB BARBER",
    "L'Établissement SOS Main": "Clinique de l'Union",
    "L'Etablissement SOS Main": "Clinique de l'Union",
    "L'Adresse de la Victime": "10 Avenue de Purpan, 31700 Blagnac",
    "Le Lieu du Dépôt de Plainte Initiale": "Service Local de Sécurité Publique de Toulouse Rive Droite (Hôtel de Police, 23 Boulevard de l'Embouchure, 31300 Toulouse)",
    "L'Adresse de l'Exploitation": "22 Rue Lafaurie, 09000 Foix",
    "Adresse du Commerce": "22 Rue Lafaurie, 09000 Foix",
    "L'Adresse du Président": "115 avenue Fernand Loubet, 09200 Saint-Girons",
    "L'Adresse du President": "115 avenue Fernand Loubet, 09200 Saint-Girons",
    "La Ville de l'Accident": "Foix",
    "La Ville de Résidence de la Victime": "Blagnac",
    "La Ville de Residence de la Victime": "Blagnac",
    "La Métropole Régionale": "Toulouse",
    "La Ville de l'Établissement SOS Main": "Saint-Jean",
    "La Ville de l'Etablissement SOS Main": "Saint-Jean",
    "L'Email de la Victime": "sebastien.grazide@gmail.com",
    "L'Identifiant Professionnel de la Victime": "500 474 457",
    "L'Identifiant de l'Exploitation": "104 103 262 00010",
    "L'Adjoint au Maire de la Commune": "Monsieur TAVELLA",
    "L'Email de l'Adjoint au Maire": "btavella@mairie-foix.fr",
    "L'Email du Secrétariat de la Mairie": "secretariat@mairie-foix.fr",
    "Centre de soins immédiats": "Centre Ariégeois de Soins Immédiats",
    "L'Adresse du Centre de soins immédiats": "4 Rue du Sénateur Paul Laffont, 09000 Foix",
    "Le RPPS du Médecin en Urgence": "10005156871",
    "J+0 Accident": "29 mai 2026",
    "J+1 Chirurgie": "30 mai 2026",
    "J+2 Sortie": "31 mai 2026",
    "J+3 Premiers arrêts": "1 juin 2026",
    "J+4 Dépôt de plainte": "2 juin 2026",
    "J+5 Ouverture CPAM": "3 juin 2026",
    "J+12 Facture": "10 juin 2026",
    "J+18 Incohérence CPAM": "16 juin 2026",
    "J+21 Contrôle chirurgical": "19 juin 2026",
    "J+25 Première kiné": "23 juin 2026",
    "J+31 Mises en demeure": "29 juin 2026",
    "J+32 Assignation référé": "30 juin 2026",
    "J+33 Plainte complémentaire": "1 juillet 2026",
    "J+35 AR propriétaire": "3 juillet 2026",
    "J+37 Assignation 145": "5 juillet 2026",
    "J+38 Constitution PC": "6 juillet 2026",
    "J+40 Consultation suivi": "8 juillet 2026",
    "J+46 Échéance amiable": "14 juillet 2026",
    "J+55 Fin d'ITT": "23 juillet 2026",
    "J+167 Expertise UMJ": "12 novembre 2026",
    "DATE RELANCE V2": "8 juillet 2026",
    "DATE REOUVERTURE BOUTIQUE": "6 juillet 2026",
    "N° Dossier CPAM": "31727387",
    "N° Dossier CPAM erroné": "2631103960",
    "SIREN de l'Exploitation": "104 103 262",
    "SIRET de l'Exploitation": "104 103 262 00010",
    "L'Adresse de la Directrice Générale": "351 route Impériale, 34670 Baillargues",
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
    "N° Transaction Wero": "IPR000297029234",
    "N° PV Police": "2026/015967",
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
    "Finance Evaluation Initiale": "59 600 €",
    "Le Téléphone de la Victime": "06 30 51 67 75",
    "Le Téléphone du Préposé": "07 58 40 12 87",
    "Le Telephone du Prepose": "07 58 40 12 87",
    "Le Prénom du Préposé": "Ayoub",
    "Le Prenom du Prepose": "Ayoub",
    "Prénom de la Victime": "Sébastien",
    "Code Postal de l'Accident": "09000",
    "Date de naissance de la victime": "18 janvier 1982",
    "Âge de la Victime": "44 ans",
    "Age de la Victime": "44 ans",
    "Capital Social de l'Exploitation": "1 000 €",
    "Finance Evaluation Globale": "59 600 €",
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

            m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            if m:
                yaml_content = m.group(1)
                try:
                    data = yaml.safe_load(yaml_content)
                    if data and 'description' in data and 'real_value' in data:
                        desc = data['description']
                        real_val = str(data['real_value']).strip()
                        m2 = re.search(r'`\*\*\[(.*?)\]\*\*`', desc)
                        if m2:
                            token_map[m2.group(1)] = real_val
                except Exception:
                    pass
    return token_map


def extract_strict_variables(path):
    token_map = {}
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'\|\s*`\[([^\]]+)\]`\s*\|\s*[^|]+\|\s*([^|]+?)\s*\|', content)
    for token_name, value in matches:
        token_map[token_name] = value.strip()
    return token_map


def build_reverse_map():
    map_dict = FALLBACK_MAP.copy()
    map_dict.update(extract_tokens_from_yaml('🧠 Memory/🗂️ Tokens'))
    map_dict.update(extract_strict_variables('🧠 Memory/STRICT VARIABLES.md'))
    return map_dict


def deduplicate_lrar_numbers(content):
    """Remove duplicate LRAR tracking numbers (e.g. LRAR n° [NUM](link) — NUM → LRAR n° [NUM](link))"""
    # Pattern A: LRAR n° [NUMBER](link) — NUMBER (with optional backticks) → LRAR n° [NUMBER](link)
    content = re.sub(r'(LRAR\s+n°\s+\[[^\]]+\]\([^)]+\))\s*[—–-]\s*`?(\d{13,15}[A-Z]?)`?', r'\1', content)
    # Pattern B: (LRAR n° NUMBER — NUMBER) → (LRAR n° NUMBER)
    content = re.sub(r'\(LRAR\s+n°\s+(\d{13,15}[A-Z]?)\s*[—–-]\s*\1\)', r'(LRAR n° \1)', content)
    # Pattern C: LRAR n° NUMBER — NUMBER (without parens, standalone)
    content = re.sub(r'(LRAR\s+n°\s+)(\d{13,15}[A-Z]?)\s*[—–-]\s*\2', r'\1\2', content)
    # Pattern D: LRAR n° <NUMBER> — NUMBER → LRAR n° <NUMBER>
    content = re.sub(r'(LRAR\s+n°\s+<\d{13,15}[A-Z]?>)\s*[—–-]\s*(\d{13,15}[A-Z]?)', r'\1', content)
    return content


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


def preprocess_nested_bracket_tokens(content):
    """Handle tokens with square brackets in their name (e.g. N° [Dossier CPAM])
    which appear with nested markdown links in the text."""
    rules = [
        # N° [Dossier CPAM] → 31727387 (with outer link)
        (
            r'\[(?:\*\*)?\[N°\s*\[Dossier\s+CPAM\]\([^)]+\)\](?:\*\*)?\](?:\([^)]+\))?',
            '31727387'
        ),
        # N° [Dossier CPAM] → 31727387 (bare bold)
        (
            r'\*\*\[N°\s*\[Dossier\s+CPAM\]\([^)]+\)\]\*\*',
            '31727387'
        ),
        # N° [Dossier CPAM erroné] → 2631103960 (with outer link)
        (
            r'\[(?:\*\*)?\[N°\s*\[Dossier\s+CPAM\s+erroné\]\([^)]+\)\](?:\*\*)?\](?:\([^)]+\))?',
            '2631103960'
        ),
        # N° [Dossier CPAM erroné] → 2631103960 (bare bold)
        (
            r'\*\*\[N°\s*\[Dossier\s+CPAM\s+erroné\]\([^)]+\)\]\*\*',
            '2631103960'
        ),
    ]
    for pattern, replacement in rules:
        content = re.sub(pattern, replacement, content)
    return content


def main():
    input_base = '⚖️ Actes/🔑 Token'
    output_base = '⚖️ Actes/👤 Reel'

    token_map = build_reverse_map()
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

            # Pre-process bracket-containing tokens before generic replacement
            content = preprocess_nested_bracket_tokens(content)

            for token_name in sorted_keys:
                real_val = token_map[token_name]
                escaped_name = re.escape(token_name)

                # Pattern A: markdown link [**[Token]**](url) or [Token](url)
                # Captures the URL part so we preserve the link
                link_pat = r'\[' + r'(?:\*\*)?' + escaped_name + r'(?:\*\*)?' + r'\]\(([^)]+)\)'

                def link_replacer(m, val=real_val):
                    return f'[{val}]({m.group(1)})'

                content = re.sub(link_pat, link_replacer, content)

                # Pattern B: bare brackets **[Token]** or [**[Token]**] or [Token]
                bare_pat = r'(?:\*\*)?\[' + r'(?:\*\*)?' + escaped_name + r'(?:\*\*)?' + r'\](?:\*\*)?'

                content = re.sub(bare_pat, real_val, content)

            # Post-processing: fix double SAS from "la SAS [**[Exploitant SAS]**]" → "la SAS HB BARBER"
            content = re.sub(r'SAS\s+SAS\s+(HB\s+BARBER|LES\s+MAUVAIS\s+GARÇONS)', r'SAS \1', content)

            # Post-processing: deduplicate LRAR tracking numbers
            content = deduplicate_lrar_numbers(content)

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
