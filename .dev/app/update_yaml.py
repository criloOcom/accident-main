import os
import re
import glob

# Current REVERSE_MAP to populate the YAMLs
REVERSE_MAP = {
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
    "Le Téléphone de la Victime": "06 30 51 67 75",
    "Le Téléphone du Préposé": "07 58 40 12 87",
    "Prénom de la Victime": "Sébastien",
    "Code Postal de l'Accident": "09000",
    "Date de naissance de la victime": "18 janvier 1982",
    "Âge de la Victime": "44 ans",
    "Age de la Victime": "44 ans",
    "Capital Social de l'Exploitation": "1 000 €",
}

for root, _, files in os.walk('Memory/Tokens'):
    for f in files:
        if not f.endswith('.md') or f in ('README.md', 'INDEX.md'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # match description: "Token :** `**[Token_Name]**`"
        m = re.search(r'description:\s*"[^`]*`\*\*\[(.*?)\]\*\*`"', content)
        if m:
            token_name = m.group(1)
            real_val = REVERSE_MAP.get(token_name)
            if real_val and "real_value:" not in content:
                # inject real_value just after description
                content = content.replace(m.group(0), m.group(0) + f'\nreal_value: "{real_val}"')
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated {path} with {real_val}")
