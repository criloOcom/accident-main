import os
import re
import glob
import urllib.parse

REVERSE_MAP = {
    "**[La Victime]**": "Sébastien GRAZIDE",
    "**[Le Président de l'Exploitation]**": "Sabir MOUNTASSER",
    "**[Le President de l'Exploitation]**": "Sabir MOUNTASSER",
    "**[La Directrice Générale de l'Exploitation]**": "Catherine SORROCHE, dite ANDISSAC",
    "**[La Directrice Generale de l'Exploitation]**": "Catherine SORROCHE, dite ANDISSAC",
    "**[Le Préposé de l'Exploitation]**": "Ayoub BENNOURINE",
    "**[Le Prepose de l'Exploitation]**": "Ayoub BENNOURINE",
    "[Le Prepose de l'Exploitation]": "Ayoub BENNOURINE",
    "**[Le Propriétaire des Murs]**": "Romain DELRIEU",
    "**[Le Chirurgien SOS Main]**": "Dr Iskander DJERBI",
    "**[Le Médecin en Urgence]**": "Dr Julie JARDON",
    "**[La Victime]**": "Sébastien GRAZIDE",
    "**[Le Président de l'Exploitation]**": "Sabir MOUNTASSER",
    "**[Le President de l'Exploitation]**": "Sabir MOUNTASSER",
    "**[La Directrice Générale de l'Exploitation]**": "Catherine SORROCHE, dite ANDISSAC",
    "**[La Directrice Generale de l'Exploitation]**": "Catherine SORROCHE, dite ANDISSAC",
    "**[Le Préposé de l'Exploitation]**": "Ayoub BENNOURINE",
    "**[Le Prepose de l'Exploitation]**": "Ayoub BENNOURINE",
    "[Le Prepose de l'Exploitation]": "Ayoub BENNOURINE",
    "**[Le Propriétaire des Murs]**": "Romain DELRIEU",
    "**[Le Proprietaire des Murs]**": "Romain DELRIEU",
    "**[Le Chirurgien SOS Main]**": "Dr Iskander DJERBI",
    "**[Le Medecin en Urgence]**": "Dr Julie JARDON",
    "**[Le Médecin Généraliste]**": "Dr Oxybel",
    "**[Le Medecin Generaliste]**": "Dr Oxybel",
    "**[La Gestionnaire CPAM]**": "Sigrid DESBOIS",
    "**[Nom de l'Avocat de la Victime]**": "Nom Prénom de l'Avocat",
    "**[L'Exploitant du Commerce (La SAS)]**": "SAS LES MAUVAIS GARCONS",
    "**[Le Commerce de l'Exploitation]**": "SAS LES MAUVAIS GARCONS",
    "**[L'Établissement SOS Main]**": "Clinique de l'Union",
    "**[L'Etablissement SOS Main]**": "Clinique de l'Union",
    "**[L'Adresse de la Victime]**": "10 Avenue de Purpan, 31700 Blagnac",
    "**[L'Adresse de l'Exploitation]**": "22 Rue Lafaurie, 09000 Foix",
    "**[Adresse du Commerce]**": "22 Rue Lafaurie, 09000 Foix",
    "**[L'Adresse du Président]**": "108 Avenue Paul Bert, 09000 Foix",
    "**[L'Adresse du President]**": "108 Avenue Paul Bert, 09000 Foix",
    "**[La Ville de l'Accident]**": "Foix",
    "**[La Ville de Résidence de la Victime]**": "Blagnac",
    "**[La Ville de Residence de la Victime]**": "Blagnac",
    "**[La Métropole Régionale]**": "Toulouse",
    "**[La Ville de l'Établissement SOS Main]**": "Saint-Jean",
    "**[La Ville de l'Etablissement SOS Main]**": "Saint-Jean",
    "**[L'Email de la Victime]**": "sebastien.grazide@gmail.com",
    "**[L'Identifiant Professionnel de la Victime]**": "500 474 457",
    "**[L'Identifiant de l'Exploitation]**": "938 033 222 00010",
    "**[L'Adjoint au Maire de la Commune]**": "Monsieur TAVELLA",
    "**[L'Email de l'Adjoint au Maire]**": "btavella@mairie-foix.fr",
    "**[L'Email du Secrétariat de la Mairie]**": "secretariat@mairie-foix.fr",
    "**[Centre de soins immédiats]**": "Centre Ariégeois de Soins Immédiats",
    "**[L'Adresse du Centre de soins immédiats]**": "4 Rue du Sénateur Paul Laffont, 09000 Foix",
    "**[Le RPPS du Médecin en Urgence]**": "10005156871",

    # Date tokens
    "**[J+0 Accident]**": "29 mai 2026",
    "**[J+1 Chirurgie]**": "30 mai 2026",
    "**[J+2 Sortie]**": "31 mai 2026",
    "**[J+3 Premiers arrêts]**": "1 juin 2026",
    "**[J+4 Dépôt de plainte]**": "2 juin 2026",
    "**[J+5 Ouverture CPAM]**": "3 juin 2026",
    "**[J+12 Facture]**": "10 juin 2026",
    "**[J+18 Incohérence CPAM]**": "16 juin 2026",
    "**[J+21 Contrôle chirurgical]**": "19 juin 2026",
    "**[J+25 Première kiné]**": "23 juin 2026",
    "**[J+31 Mises en demeure]**": "29 juin 2026",
    "**[J+32 Assignation référé]**": "30 juin 2026",
    "**[J+33 Plainte complémentaire]**": "1 juillet 2026",
    "**[J+35 AR propriétaire]**": "3 juillet 2026",
    "**[J+37 Assignation 145]**": "5 juillet 2026",
    "**[J+38 Constitution PC]**": "6 juillet 2026",
    "**[J+40 Consultation suivi]**": "8 juillet 2026",
    "**[J+46 Échéance amiable]**": "14 juillet 2026",
    "**[J+55 Fin d'ITT]**": "23 juillet 2026",
    "**[J+167 Expertise UMJ]**": "12 novembre 2026",

    # Relance V2 specific tokens
    "**[DATE RELANCE V2]**": "8 juillet 2026",
    "**[DATE REOUVERTURE BOUTIQUE]**": "6 juillet 2026",

    # Reference tokens
    "**[N° Dossier CPAM]**": "31727387",
    "**[N° Dossier CPAM erroné]**": "2631103960",
    "**[SIREN de l'Exploitation]**": "938 033 222",
    "**[SIRET de l'Exploitation]**": "938 033 222 00010",
    "**[SIREN du Nouvel Exploitant]**": "104 103 262",
    "**[Identifiant du Nouvel Exploitant]**": "104 103 262 00010",
    "**[Capital du Nouvel Exploitant]**": "1 000 €",
    "**[Le Nouvel Exploitant (HB BARBER)]**": "SAS HB BARBER",
    "**[Le Président du Nouvel Exploitant]**": "Hamza El Hachemi BERGUIGA",
    "**[Adresse du Président du Nouvel Exploitant]**": "115 avenue Fernand Loubet, 09200 Saint-Girons",
    "**[Adresse de la Directrice Générale du Nouvel Exploitant]**": "351 route Impériale, 34670 Baillargues",
    "**[N° LRAR Exploitant]**": "87001424863012T",
    "**[N° LRAR Président]**": "87001424862879J",
    "**[N° LRAR Directrice]**": "87001424721856G",
    "**[N° LRAR Propriétaire]**": "87001424862462Y",
    "**[N° LRAR Parquet]**": "87001424923505I",
    "**[N° Transaction Wero]**": "IPR000297029234",
    "**[N° PV Police]**": "2026/015967",
    "[N° PV Police]": "2026/015967",  # fallback for bare-bracket variants

    # Financial tokens
    "**[Finance Provision Référé]**": "15 000 €",
    "**[Finance Article 700]**": "3 000 €",
    "**[Finance Astreinte 145]**": "150 €",
    "**[Finance Article 700 Référé 145]**": "1 500 €",
    "**[Finance Article 475-1]**": "3 000 €",
    "**[Finance PGPA]**": "1 380 €",
    "**[Finance DFP]**": "25 000 €",
    "**[Finance Souffrances Endurées]**": "15 000 €",
    "**[Finance Incidence Professionnelle]**": "30 000 €",
    "**[Finance Préjudice Agrément]**": "5 000 €",
    "**[Finance Préjudice Esthétique]**": "3 000 €",
    "**[Finance Dévalorisation Pro]**": "3 000 €",
    "**[Finance Frais Divers]**": "3 000 €",
    "**[Finance Facture Chirurgie]**": "790,23 €",
    "**[Finance Prestation Salon]**": "15,00 €",
    "**[Finance Evaluation Initiale]**": "59 600 €",
    "**[Le Téléphone de la Victime]**": "06 30 51 67 75",
    "**[Le Téléphone du Préposé]**": "07 58 40 12 87",

    # Identity tokens (ajout Phase 1c)
    "**[Prénom de la Victime]**": "Sébastien",
    "**[Code Postal de l'Accident]**": "09000",
    "**[Date de naissance de la victime]**": "18 janvier 1982",
    "**[Âge de la Victime]**": "44 ans",
    "**[Age de la Victime]**": "44 ans",
    "**[Capital Social de l'Exploitation]**": "200 €",

    # Finance tokens (uniques — ajout Phase 1c, redondant pour les montants uniques déjà présents)
    "**[Finance Evaluation Globale]**": "59 600 €",
    "**[Finance Incidence Professionnelle]**": "30 000 €",
    "**[Finance DFP]**": "25 000 €",
    "**[Finance Préjudice Agrément]**": "5 000 €",
    "**[Finance Article 700 Référé 145]**": "1 500 €",
    "**[Finance PGPA]**": "1 380 €",
    "**[Finance Facture Chirurgie]**": "790,23 €",
    "**[Finance Astreinte 145]**": "150 €",
    "**[Finance Prestation Salon]**": "15,00 €",
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
    input_base = '⚖️ Actes/🔑 Token'
    output_base = '⚖️ Actes/👤 Reel'

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
            for token, real_val in REVERSE_MAP.items():
                content = content.replace(token, real_val)
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
