#!/usr/bin/env python3
import re, sys

# ============================================================
# MASTER REPLACEMENT TABLE
# ============================================================
REPLACEMENTS = [
    ("Sabir MOUNTASSER", "[L'Ancien Président de l'Exploitation]"),
    ("SABIR", "[Prénom de l'Ancien Président de l'Exploitation]"),
    ("Sabir", "[Prénom de l'Ancien Président de l'Exploitation]"),
    ("MOUNTASSER", "[Nom de l'Ancien Président de l'Exploitation]"),
    ("Mountasser", "[Nom de l'Ancien Président de l'Exploitation]"),
    ("SAS LES MAUVAIS GARÇONS", "[L'Ancien Exploitant du Commerce]"),
    ("SAS LES MAUVAIS GARCONS", "[L'Ancien Exploitant du Commerce]"),
    ("LES MAUVAIS GARÇONS", "[L'Ancien Exploitant du Commerce]"),
    ("LES MAUVAIS GARCONS", "[L'Ancien Exploitant du Commerce]"),
    # --- Addresses (full address FIRST to avoid partial match) ---
    # Geographic reference: complaint deposit location (must be BEFORE generic Toulouse)
    ("Service Local de Sécurité Publique de Toulouse Rive Droite (Hôtel de Police, 23 Boulevard de l'Embouchure, 31300 Toulouse)", "[Le Lieu du Dépôt de Plainte Initiale]"),
    ("Service Local de Sécurité Publique de Toulouse Rive Droite", "[Le Lieu du Dépôt de Plainte Initiale]"),
    ("Hôtel de Police, 23 Boulevard de l'Embouchure, 31300 Toulouse", "[Le Lieu du Dépôt de Plainte Initiale]"),
    ("23 Boulevard de l'Embouchure, 31300 Toulouse", "[Le Lieu du Dépôt de Plainte Initiale]"),
    ("23 Boulevard de l'Embouchure", "[Le Lieu du Dépôt de Plainte Initiale]"),
    ("Division Toulouse Rive Droite", "[Le Lieu du Dépôt de Plainte Initiale]"),
    ("Toulouse Rive Droite", "[Le Lieu du Dépôt de Plainte Initiale]"),
    ("10 Avenue de Purpan, 31700 Blagnac", "[L'Adresse de la Victime]"),
    ("10 Avenue de Purpan", "[L'Adresse de la Victime]"),
    ("31700 Blagnac", "[L'Adresse de la Victime]"),
    ("22 Rue Lafaurie, 09000 Foix", "[L'Adresse de l'Exploitation]"),
    ("22 Rue Lafaurie", "[L'Adresse de l'Exploitation]"),
    ("115 avenue Fernand Loubet, 09200 Saint-Girons", "[L'Adresse du Président]"),
    ("14 Boulevard du Sud \u2014 BP 50078", ""),  # court address
    ("09008 Foix Cedex", ""),
    ("Foix Cedex", ""),

    # --- Victim (name variants, longest first) ---
    ("Monsieur Sébastien GRAZIDE", "[La Victime]"),
    ("Sébastien GRAZIDE", "[La Victime]"),
    ("LES MAUVAIS GARCONS", "**[L'Ancien Exploitant]**"),
    ("MAUVAIS GARCONS", "**[L'Ancien Exploitant]**"),
    ("SABIR", "**[L'Ancien Président de l'Exploitation]**"),
    ("Sabir", "**[L'Ancien Président de l'Exploitation]**"),
    ("Sébastien Grazide", "[La Victime]"),
    ("Monsieur GRAZIDE", "[La Victime]"),
    ("Monsieur Grazide", "[La Victime]"),
    ("Grazide", "[La Victime]"),
    ("GRAZIDE", "[La Victime]"),

    # --- Exploitation ---
    ("SAS LES MAUVAIS GARCONS", "[L'Exploitant du Commerce (La SAS)]"),
    ("SAS LES MAUVAIS GARÇONS", "[L'Exploitant du Commerce (La SAS)]"),
    ("LES MAUVAIS GARCONS", "[L'Exploitant du Commerce (La SAS)]"),
    ("LES MAUVAIS GARÇONS", "[L'Exploitant du Commerce (La SAS)]"),
    ("Mountasser SABIR", "[Le Président de la SAS]"),
    ("Mountasser Sabir", "[Le Président de la SAS]"),
    ("SABIR", "[Le Président de la SAS]"),
    ("Sabir", "[Le Président de la SAS]"),
    ("Catherine ANDISSAC", "[La Directrice Générale de la SAS]"),
    ("Catherine Andissac", "[La Directrice Générale de la SAS]"),
    ("ANDISSAC", "[La Directrice Générale de la SAS]"),
    ("Andissac", "[La Directrice Générale de la SAS]"),

    # --- Victim identifiers ---
    ("sebastien.grazide@gmail.com", "[L'Email de la Victime]"),
    ("SIREN : 500 474 457", "[L'Identifiant Professionnel de la Victime]"),
    ("SIREN 500 474 457", "[L'Identifiant Professionnel de la Victime]"),
    ("500 474 457", "[L'Identifiant Professionnel de la Victime]"),

    # --- Admin / Civil status (LMG — ancien exploitant, conservé en clair pour narration historique, Cas A) ---

    # --- Salon / Company (HB BARBER — exploitant réel au 29/05/2026) ---
    ("HB BARBER", "[L'Exploitant du Commerce (La SAS)]"),
    ("SAS HB BARBER", "[L'Exploitant du Commerce (La SAS)]"),

    # --- Company identifier (HB BARBER) ---
    ("104 103 262 00010", "[L'Identifiant de l'Exploitation]"),

    # --- Directors / Officers (HB BARBER) ---
    ("Madame Catherine ANDISSAC (née SORROCHE)", "[La Directrice Générale de l'Exploitation]"),
    ("Catherine ANDISSAC", "[La Directrice Générale de l'Exploitation]"),
    ("Catherine Andissac", "[La Directrice Générale de l'Exploitation]"),
    ("Catherine SORROCHE (épouse ANDISSAC)", "[La Directrice Générale de l'Exploitation]"),
    ("Catherine SORROCHE", "[La Directrice Générale de l'Exploitation]"),
    ("ANDISSAC", "[La Directrice Générale de l'Exploitation]"),
    ("Andissac", "[La Directrice Générale de l'Exploitation]"),
    ("SORROCHE", "[La Directrice Générale de l'Exploitation]"),
    ("Hamza El Hachemi BERGUIGA", "[Le Président de l'Exploitation]"),
    ("BERGUIGA", "[Le Président de l'Exploitation]"),

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
    ("« Ayoub »", "[**[Le Prénom du Préposé]**]"),
    ("Ayoub", "[Le Préposé de l'Exploitation]"),
    ("Monsieur BENNOURINE", "[Le Préposé de l'Exploitation]"),
    ("BENNOURINE", "[Le Préposé de l'Exploitation]"),
    ("07 58 40 12 87", "[Le Téléphone du Préposé]"),
    ("+33 7 58 40 12 87", "[Le Téléphone du Préposé]"),

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
    ("Dr Prisca AKUÉ", "[Le Médecin de Suivi]"),
    ("Dr Prisca AKUE", "[Le Médecin de Suivi]"),
    ("le Dr AKUÉ", "[Le Médecin de Suivi]"),
    ("Dr AKUÉ", "[Le Médecin de Suivi]"),
    ("AKUÉ", "[Le Médecin de Suivi]"),
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

    # --- Directors / Officers (HB BARBER — exploitant réel) ---
    ("104 103 262", "[SIREN de l'Exploitation]"),
    ("1 000 €", "[Capital Social de l'Exploitation]"),

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

    # --- Identity tokens (Prénom, Âge, Date naissance) ---
    ("18 janvier 1982", "**[Date de naissance de la victime]**"),
    ("44 ans", "**[Âge de la Victime]**"),
    # "200 €" conservé en clair (capital ancien exploitant LMG — Cas A narration historique)
    ("09000", "**[Code Postal de l'Accident]**"),
    ("Sébastien", "**[Prénom de la Victime]**"),  # NB: risque faux positif si autre Sébastien dans un doc

    # --- Finance tokens (montants uniques uniquement) ---
    # ATTENTION: "15 000 €" et "3 000 €" sont exclus car chaque valeur correspond
    # à plusieurs tokens distincts (ex: 15k€ = Provision Référé + Souffrances Endurées).
    # Ces remplacements doivent être faits manuellement ou doc par doc.
    ("59 600 €", "**[Finance Evaluation Globale]**"),
    ("30 000 €", "**[Finance Incidence Professionnelle]**"),
    ("25 000 €", "**[Finance DFP]**"),
    ("5 000 €", "**[Finance Préjudice Agrément]**"),
    ("1 500 €", "**[Finance Article 700 Référé 145]**"),
    ("1 380 €", "**[Finance PGPA]**"),
    ("790,23 €", "**[Finance Facture Chirurgie]**"),
    ("150 €", "**[Finance Astreinte 145]**"),
    ("15,00 €", "**[Finance Prestation Salon]**"),
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

    # Fix nested token replacement (HB BARBER" inside its own token name)
    text = text.replace('[L\'Exploitant du Commerce (La SAS) ([L\'Exploitant du Commerce (La SAS)])]', "[L'Exploitant du Commerce (La SAS)]")

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
