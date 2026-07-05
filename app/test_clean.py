import json
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from batch_anonymize import anonymize_text

# On va charger TOKEN MAP ou utiliser batch_anonymize qui est complet.
# Faisons des tests d'anonymisation pour voir si Sébastien GRAZIDE est bien remplacé par **[La Victime]** (en gras comme spécifié: **[La Victime]**).
# Ah, batch_anonymize.py produit [La Victime] sans les astérisques.
# La consigne dit: "Sébastien GRAZIDE → **[La Victime]**, Ayoub Bennourine → **[Le Préposé de l'Exploitation]**, etc."
# Donc on doit ajouter les ** ** autour des jetons s'ils n'en ont pas déjà.
# Faisons un dictionnaire de remplacement propre pour les chaînes.

tokens_anonyme = {
    "Sébastien GRAZIDE": "**[La Victime]**",
    "Sébastien Grazide": "**[La Victime]**",
    "GRAZIDE": "**[La Victime]**",
    "Grazide": "**[La Victime]**",
    "Mountasser SABIR": "**[Le Président de l'Exploitation]**",
    "Mountasser Sabir": "**[Le Président de l'Exploitation]**",
    "SABIR": "**[Le Président de l'Exploitation]**",
    "Sabir": "**[Le Président de l'Exploitation]**",
    "Catherine ANDISSAC": "**[La Directrice Générale de l'Exploitation]**",
    "Catherine Andissac": "**[La Directrice Générale de l'Exploitation]**",
    "ANDISSAC": "**[La Directrice Générale de l'Exploitation]**",
    "Andissac": "**[La Directrice Générale de l'Exploitation]**",
    "Ayoub Bennourine": "**[Le Préposé de l'Exploitation]**",
    "Ayoub BENNOURINE": "**[Le Préposé de l'Exploitation]**",
    "BENNOURINE": "**[Le Préposé de l'Exploitation]**",
    "Bennourine": "**[Le Préposé de l'Exploitation]**",
    "Ayoub": "**[Le Préposé de l'Exploitation]**",
    "Romain DELRIEU": "**[Le Propriétaire des Murs]**",
    "Romain Delrieu": "**[Le Propriétaire des Murs]**",
    "DELRIEU": "**[Le Propriétaire des Murs]**",
    "Delrieu": "**[Le Propriétaire des Murs]**",
    "Dr Iskander Djerbi": "**[Le Chirurgien SOS Main]**",
    "Iskander DJERBI": "**[Le Chirurgien SOS Main]**",
    "DJERBI": "**[Le Chirurgien SOS Main]**",
    "Djerbi": "**[Le Chirurgien SOS Main]**",
    "Dr Julie Jardon": "**[Le Médecin en Urgence]**",
    "Julie JARDON": "**[Le Médecin en Urgence]**",
    "JARDON": "**[Le Médecin en Urgence]**",
    "Jardon": "**[Le Médecin en Urgence]**",
    "Dr Oxybel": "**[Le Médecin Généraliste]**",
    "Oxybel": "**[Le Médecin Généraliste]**",
    "Sigrid DESBOIS": "**[La Gestionnaire CPAM]**",
    "Sigrid Desbois": "**[La Gestionnaire CPAM]**",
    "DESBOIS": "**[La Gestionnaire CPAM]**",
    "Desbois": "**[La Gestionnaire CPAM]**",
    "SAS LES MAUVAIS GARCONS": "**[L'Exploitant du Commerce]**",
    "SAS LES MAUVAIS GARÇONS": "**[L'Exploitant du Commerce]**",
    "LES MAUVAIS GARÇONS": "**[L'Exploitant du Commerce]**",
    "LES MAUVAIS GARCONS": "**[L'Exploitant du Commerce]**",
    "Clinique de l'Union": "**[L'Établissement SOS Main]**",
    "10 Avenue de Purpan, 31700 Blagnac": "**[L'Adresse de la Victime]**",
    "10 Avenue de Purpan": "**[L'Adresse de la Victime]**",
    "22 Rue Lafaurie, 09000 Foix": "**[L'Adresse de l'Exploitation]**",
    "22 Rue Lafaurie": "**[L'Adresse de l'Exploitation]**",
    "108 Avenue Paul Bert, 09000 Foix": "**[L'Adresse du Président]**",
    "Foix": "**[La Ville de l'Accident]**",
    "Blagnac": "**[La Ville de Résidence de la Victime]**",
    "Toulouse": "**[La Métropole Régionale]**",
    "Saint-Jean": "**[La Ville de l'Établissement SOS Main]**",
    "sebastien.grazide@gmail.com": "**[L'Email de la Victime]**",
    "500 474 457": "**[L'Identifiant Professionnel de la Victime]**",
    "938 033 222 00010": "**[L'Identifiant de l'Exploitation]**",
}

def clean_and_anonymize(val):
    if not isinstance(val, str):
        return val
    # Appliquer les remplacements du TOKEN MAP (longest keys first)
    for old in sorted(tokens_anonyme.keys(), key=len, reverse=True):
        # Utiliser un regex pour remplacer le mot exact ou la phrase exacte
        val = re.sub(r'\b' + re.escape(old) + r'\b', tokens_anonyme[old], val)
        # Remplacement direct au cas où les limites de mots posent problème avec les accents/lettres françaises
        val = val.replace(old, tokens_anonyme[old])
    
    # Nettoyer les civilités devant les tokens
    val = re.sub(r'\b(Monsieur|Madame|M\.|Mme|Dr|Docteur|Maître)\s+(?=\*\*\[)', '', val)
    # Nettoyer les doublons d'astérisques
    val = val.replace('****', '**')
    return val

print("Test anonymisation:")
print(clean_and_anonymize("Monsieur Sébastien GRAZIDE a rencontré Dr Julie Jardon à Foix"))
