#!/usr/bin/env python3
import re, sys

with open('/tmp/original_assignation.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Entity replacements (longest first to avoid partial overwrites)
replacements = [
    ("La SAS LES MAUVAIS GARCONS", "[L'Exploitant du Salon]"),
    ("SAS LES MAUVAIS GARCONS", "[L'Exploitant du Salon]"),
    ("22 Rue Lafaurie, 09000 Foix", "[L'Adresse de l'Exploitation]"),
    ("Madame Catherine ANDISSAC (née SORROCHE)", "[La Directrice Générale de l'Exploitation]"),
    ("938 033 222 00010", "[L'Identifiant de l'Exploitation]"),
    ("Monsieur Sébastien GRAZIDE", "[La Victime]"),
    ("Monsieur Sébastien Grazide", "[La Victime]"),
    ("Monsieur GRAZIDE", "[La Victime]"),
    ("Monsieur Grazide", "[La Victime]"),
    ("Monsieur Ayoub Bennourine", "[Le Préposé / Coiffeur]"),
    ("Dr Iskander Djerbi", "[Le Chirurgien SOS Main]"),
    ("Dr Julie Jardon", "[Le Médecin en Urgence]"),
    ("SOS Main de la Clinique de l'Union", "SOS Main de [L'Établissement SOS Main]"),
    ("Clinique de l'Union", "[L'Établissement SOS Main]"),
    ("FOIX", "[LA VILLE DE L'ACCIDENT]"),
    ("Foix", "[La Ville de l'Accident]"),
    ("(31)", ""),
    ("(09)", ""),
]

for old, new in replacements:
    text = text.replace(old, new)

# Remove civility prefixes and articles before tokens
text = re.sub(r'\b(Monsieur|Madame|M\.|Mme|Dr|Docteur|Maître)\s+(?=\[)', '', text)
# Remove "La " / "la " / "Le " / "le " if directly before a bracket (they duplicate the token)
text = re.sub(r'\b(La |la |Le |le |L\'|l\')(?=\[)', '', text)
# Handle "de la" before [L'Exploitant:
text = re.sub(r'de la (?=\[L\'Exploitant)', 'de ', text)

# Remove leftover "(31)" or "(09)"
text = re.sub(r'\(\d{2}\)', '', text)
# Fix double spaces
text = re.sub(r'  +', ' ', text)

print(text)
