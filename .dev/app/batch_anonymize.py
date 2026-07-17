#!/usr/bin/env python3
import re, sys

# ============================================================
# MASTER REPLACEMENT TABLE
# ============================================================
REPLACEMENTS = [
    # --- Addresses (full address FIRST to avoid partial match) ---
    ("10 Avenue de Purpan, 31700 Blagnac", "[L'Adresse de la Victime]"),
    ("10 Avenue de Purpan", "[L'Adresse de la Victime]"),
    ("31700 Blagnac", "[L'Adresse de la Victime]"),
    ("22 Rue Lafaurie, 09000 Foix", "[L'Adresse de l'Exploitation]"),
    ("22 Rue Lafaurie", "[L'Adresse de l'Exploitation]"),
    ("108 Avenue Paul Bert, 09000 Foix", "[L'Adresse du Président]"),
    ("14 Boulevard du Sud \u2014 BP 50078", ""),  # court address
    ("09008 Foix Cedex", ""),
    ("Foix Cedex", ""),

    # --- Victim (name variants, longest first) ---
    ("Monsieur Sébastien GRAZIDE", "[La Victime]"),
    ("Sébastien GRAZIDE", "[La Victime]"),
    ("Sébastien Grazide", "[La Victime]"),
    ("Monsieur GRAZIDE", "[La Victime]"),
    ("Monsieur Grazide", "[La Victime]"),
    ("Grazide", "[La Victime]"),
    ("GRAZIDE", "[La Victime]"),

    # --- Victim identifiers ---
    ("sebastien.grazide@gmail.com", "[L'Email de la Victime]"),
    ("SIREN : 500 474 457", "[L'Identifiant Professionnel de la Victime]"),
    ("SIREN 500 474 457", "[L'Identifiant Professionnel de la Victime]"),
    ("500 474 457", "[L'Identifiant Professionnel de la Victime]"),

    # --- Salon / Company (LMG — ancien exploitant) ---
    ("La SAS LES MAUVAIS GARCONS", "[L'Exploitant du Commerce (La SAS)]"),
    ("SAS LES MAUVAIS GARCONS", "[L'Exploitant du Commerce (La SAS)]"),
    ("SAS LES MAUVAIS GARÇONS", "[L'Exploitant du Commerce (La SAS)]"),
    ("LES MAUVAIS GARCONS", "[L'Exploitant du Commerce (La SAS)]"),
    ("LES MAUVAIS GARÇONS", "[L'Exploitant du Commerce (La SAS)]"),
    ("la SAS LES MAUVAIS GARCONS", "[L'Exploitant du Commerce (La SAS)]"),

    # --- Salon / Company (HB BARBER — nouvel exploitant) ---
    # NOTE: "HB BARBER" AVANT "SAS HB BARBER" pour éviter le double-wrap
    # (le token contient "HB BARBER" en sous-chaîne)
    ("HB BARBER", "[Le Nouvel Exploitant (HB BARBER)]"),
    ("SAS HB BARBER", "[Le Nouvel Exploitant (HB BARBER)]"),

    # --- Company identifier (LMG) ---
    ("938 033 222 00010", "[L'Identifiant de l'Exploitation]"),

    # --- Company identifier (HB BARBER) ---
    ("104 103 262 00010", "[Identifiant du Nouvel Exploitant]"),

    # --- Directors / Officers (LMG) ---
    ("Madame Catherine ANDISSAC (née SORROCHE)", "[La Directrice Générale de l'Exploitation]"),
    ("Catherine ANDISSAC", "[La Directrice Générale de l'Exploitation]"),
    ("Catherine Andissac", "[La Directrice Générale de l'Exploitation]"),
    ("Catherine SORROCHE (épouse ANDISSAC)", "[La Directrice Générale de l'Exploitation]"),
    ("Catherine SORROCHE", "[La Directrice Générale de l'Exploitation]"),
    ("ANDISSAC", "[La Directrice Générale de l'Exploitation]"),
    ("Andissac", "[La Directrice Générale de l'Exploitation]"),
    ("SORROCHE", "[La Directrice Générale de l'Exploitation]"),
    ("Monsieur Mountasser SABIR", "[Le Président de l'Exploitation]"),
    ("Mountasser SABIR", "[Le Président de l'Exploitation]"),
    ("Mountasser Sabir", "[Le Président de l'Exploitation]"),
    ("Monsieur SABIR", "[Le Président de l'Exploitation]"),
    ("SABIR", "[Le Président de l'Exploitation]"),
    ("Sabir", "[Le Président de l'Exploitation]"),
    ("Sabir MOUNTASSER", "[Le Président de l'Exploitation]"),
    ("Sabir Mountasser", "[Le Président de l'Exploitation]"),
    ("Monsieur Sabir MOUNTASSER", "[Le Président de l'Exploitation]"),
    ("MOUNTASSER", "[Le Président de l'Exploitation]"),
    ("Mountasser", "[Le Président de l'Exploitation]"),

    # --- Mairie contacts ---
    ("Bernard TAVELLA", "[L'Adjoint au Maire de la Commune]"),
    ("Bernard TAVELA", "[L'Adjoint au Maire de la Commune]"),
    ("M. Bernard TAVELLA", "[L'Adjoint au Maire de la Commune]"),
    ("M. TAVELLA", "[L'Adjoint au Maire de la Commune]"),
    ("TAVELLA", "[L'Adjoint au Maire de la Commune]"),
    ("btavella@mairie-foix.fr", "[L'Email de l'Adjoint au Maire]"),
    ("secretariat@mairie-foix.fr", "[L'Email du Secrétariat de la Mairie]"),
    ("mairie@mairie-foix.fr", "[L'Email du Secrétariat de la Mairie]"),

    # --- References (police, CPAM) ---
    ("CPAM de Haute-Garonne", "CPAM"),
    ("dossier n° 31727387", "[ ... ]"),
    ("31727387", "[ ... ]"),
    ("PV n° 2026/015967", "[ ... ]"),
    ("Procès-Verbal de police n° 2026/015967", "[ ... ]"),
    ("n° 2026/015967", "[ ... ]"),
    ("2026/015967", "[ ... ]"),

    # --- Employees ---
    ("Monsieur Ayoub Bennourine", "[Le Préposé de l'Exploitation]"),
    ("Ayoub Bennourine", "[Le Préposé de l'Exploitation]"),
    ("Ayoub BENNOURINE", "[Le Préposé de l'Exploitation]"),
    ("Monsieur BENNOURINE", "[Le Préposé de l'Exploitation]"),
    ("BENNOURINE", "[Le Préposé de l'Exploitation]"),

    # --- Medical ---
    ("Dr Iskander Djerbi", "[Le Chirurgien SOS Main]"),
    ("Dr Iskander DJERBI", "[Le Chirurgien SOS Main]"),
    ("Docteur Iskander DJERBI", "[Le Chirurgien SOS Main]"),
    ("le Docteur Iskander DJERBI", "[Le Chirurgien SOS Main]"),
    ("le Docteur Djerbi", "[Le Chirurgien SOS Main]"),
    ("Dr DJERBI", "[Le Chirurgien SOS Main]"),
    ("le Dr Djerbi", "[Le Chirurgien SOS Main]"),
    ("Docteur DJERBI", "[Le Chirurgien SOS Main]"),
    ("DJERBI", "[Le Chirurgien SOS Main]"),
    ("Dr Julie Jardon", "[Le Médecin en Urgence]"),
    ("Dr Julie JARDON", "[Le Médecin en Urgence]"),
    ("Docteur Julie JARDON", "[Le Médecin en Urgence]"),
    ("le Docteur Julie JARDON", "[Le Médecin en Urgence]"),
    ("Dr JARDON", "[Le Médecin en Urgence]"),
    ("le Dr JARDON", "[Le Médecin en Urgence]"),
    ("JARDON", "[Le Médecin en Urgence]"),
    ("Dr Oxybel", "[Le Médecin Généraliste]"),
    ("le Dr Oxybel", "[Le Médecin Généraliste]"),
    ("Oxybel", "[Le Médecin Généraliste]"),

    # --- Medical institutions ---
    ("SOS Main de la Clinique de l'Union", "SOS Main de [L'Établissement SOS Main]"),
    ("Clinique de l'Union", "[L'Établissement SOS Main]"),

    # --- CPAM contact ---
    ("Sigrid DESBOIS", "[La Gestionnaire CPAM]"),
    ("Sigrid Desbois", "[La Gestionnaire CPAM]"),
    ("DESBOIS", "[La Gestionnaire CPAM]"),

    # --- Property owner ---
    ("Monsieur Romain DELRIEU", "[Le Propriétaire des Murs]"),
    ("Romain DELRIEU", "[Le Propriétaire des Murs]"),
    ("Romain Delrieu", "[Le Propriétaire des Murs]"),

    # --- Directors / Officers (HB BARBER — nouvel exploitant) ---
    ("Hamza El Hachemi BERGUIGA", "[Le Président du Nouvel Exploitant]"),
    ("BERGUIGA", "[Le Président du Nouvel Exploitant]"),
    ("104 103 262", "[SIREN du Nouvel Exploitant]"),
    ("1 000 €", "[Capital du Nouvel Exploitant]"),

    # --- Cities ---
    ("FOIX", "[La Ville de l'Accident]"),
    ("Foix", "[La Ville de l'Accident]"),
    ("Blagnac", "[La Ville de Résidence de la Victime]"),
    ("Toulouse (31)", "[La Métropole Régionale]"),
    ("Toulouse", "[La Métropole Régionale]"),
    ("Saint-Jean (31)", "[La Ville de l'Établissement SOS Main]"),
    ("Saint-Jean", "[La Ville de l'Établissement SOS Main]"),

    # --- Lawyer (placeholder — add real name when known) ---
    ("Nom Prénom de l'Avocat", "[Nom de l'Avocat de la Victime]"),

    # --- Department numbers ---
    ("(31)", ""),
    ("(09)", ""),
]

def anonymize_text(text):
    """Apply all replacements to text, longest first for safety."""
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)

    # Remove civility prefixes before bracket tokens (safe: removes Monsieur/Madame/Dr before [token])
    text = re.sub(r'\b(Monsieur|Madame|M\.|Mme|Dr|Docteur|Maître)\s+(?=\[)', '', text)
    # Clean articles before [L'Exploitant... → "[L'Exploitant..."
    text = re.sub(r'\b(de la|la |Le |le |L\'|l\')(?=\[L\'Exploitant)', '', text)

    # Remove orphan department numbers
    text = re.sub(r'\(\d{2}\)', '', text)
    # Fix double spaces
    text = re.sub(r'  +', ' ', text)

    # Entourer les tokens d'identité de ** (convention double strate du projet).
    # Capture [X] sans espace après '[' (exclut les réserves [ ... ]) et déjà **[X]**.
    # Skip si déjà entouré de ** (évite le double-wrap).
    text = re.sub(r'(?<!\*)(?<!\[)(\[[^\]\s][^\]]*\])(?!\])(?!\*)', r'**\1**', text)

    # Fix nested token replacements (HB BARBER inside its own token name)
    text = text.replace('[Le Nouvel Exploitant ([Le Nouvel Exploitant (HB BARBER)])]', '[Le Nouvel Exploitant (HB BARBER)]')
    text = text.replace('[Le Nouvel Exploitant ([Le Nouvel Exploitant (HB BARBER)]]', '[Le Nouvel Exploitant (HB BARBER)]')

    return text

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: batch_anonymize.py <input_file> [output_file]")
        sys.exit(1)

    input_path = sys.argv[1]
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except OSError as e:
        print(f"ERREUR lecture {input_path} (ligne {e.__traceback__.tb_lineno if e.__traceback__ else '?'}): {e}", file=sys.stderr)
        sys.exit(2)

    result = anonymize_text(text)

    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Written to {out_path}")
        except OSError as e:
            print(f"ERREUR écriture {out_path} (ligne {e.__traceback__.tb_lineno if e.__traceback__ else '?'}): {e}", file=sys.stderr)
            sys.exit(3)
    else:
        print(result)
