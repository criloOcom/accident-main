#!/usr/bin/env python3
import re
import sys

# To fix the CWE-377 insecure temporary file vulnerability, we require the input
# file to be provided as an argument.
if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <input_file>", file=sys.stderr)
    sys.exit(1)

input_file = sys.argv[1]
with open(input_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Entity replacements (longest first to avoid partial overwrites)
replacements = [
    ("SAS HB BARBER", "[L'Exploitant du Commerce (La SAS)]"),
    ("HB BARBER", "[L'Exploitant du Commerce (La SAS)]"),
    ("22 Rue Lafaurie, 09000 Foix", "[L'Adresse de l'Exploitation]"),
    ("Madame Catherine ANDISSAC (née SORROCHE)", "[La Directrice Générale de l'Exploitation]"),
    ("104 103 262 00010", "[L'Identifiant de l'Exploitation]"),
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
text = re.sub(r'\b(La |la |Le |le |L\'|l\')(?=\[)', '', text)
text = re.sub(r'de la (?=\[L\'Exploitant)', 'de ', text)

text = re.sub(r'\(\d{2}\)', '', text)
text = re.sub(r'  +', ' ', text)

print(text)
