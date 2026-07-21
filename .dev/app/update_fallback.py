import re

EXTRA_FALLBACKS = {
    "L'Exploitant du Commerce": "SAS HB BARBER",
    "L'EXPLOITANT DU COMMERCE (LA SAS)": "SAS HB BARBER",
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
}

with open(".dev/app/generate_real_versions.py", "r") as f:
    content = f.read()

# insert EXTRA_FALLBACKS into FALLBACK_MAP
dict_str = ""
for k, v in EXTRA_FALLBACKS.items():
    dict_str += f'    "{k}": "{v}",\n'

content = content.replace("FALLBACK_MAP = {", "FALLBACK_MAP = {\n" + dict_str)

with open(".dev/app/generate_real_versions.py", "w") as f:
    f.write(content)

