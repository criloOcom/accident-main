import json
from datetime import datetime
import sys

def parse_date(date_str):
    if not date_str:
        return datetime.min
    try:
        return datetime.strptime(date_str, '%d/%m/%Y %H:%M')
    except ValueError:
        pass
    try:
        return datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        return datetime.min

def main():
    try:
        with open('scratch_master_final.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        sys.exit(1)

    pieces_dict = {}
    for row in data:
        rp_field = row.get('RefPiece', '').strip()
        if not rp_field:
            continue
        # Handle comma separated
        for rp in [x.strip() for x in rp_field.split(',')]:
            if rp.isdigit():
                piece_num = int(rp)
                pieces_dict.setdefault(piece_num, []).append(row)

    markdown = """---
titre: Bordereau de pièces
date: 2026-07-15
type: acte
categorie: procedure
auteur: La Victime
destinataire: Tribunal Judiciaire de la Ville de l'Accident
personnes:
  - La Victime
  - L'Exploitant du Commerce
tags:
  - bordereau
  - pieces
  - référé
statut: final
format: Arial JUSTIFIED
---

# BORDEREAU DE PIÈCES

| Procédure : Référé Article 145 CPC | Demandeur : **[La Victime]** | Défendeur : **[L'Exploitant du Commerce]** |
|:---|:---|:---|

=== PAGE BREAK ===

"""

    for piece_num in sorted(pieces_dict.keys()):
        items = pieces_dict[piece_num]
        items.sort(key=lambda x: parse_date(x.get('DateHeure', '')))

        markdown += f"## Pièce n° {piece_num}\n\n"
        for item in items:
            date_str = item.get('DateHeure', 'Date inconnue')
            evt = item.get('Evt', 'Description manquante')
            desc = item.get('Desc', '')
            emetteur = item.get('Emetteur', '')
            drive = item.get('LienGDrive', '')

            line = f"- **{date_str}** — {evt}"
            if emetteur:
                line += f" ({emetteur})"
            if desc:
                line += f" : {desc}"
            if drive:
                line += f" [🔗 Voir]({drive})"
            markdown += f"{line}\n"
        markdown += "\n"

    with open('actes/01_Actes_proceduraux/04_Bordereau de pieces - V1.md', 'w') as f:
        f.write(markdown)
    print("Document successfully generated.")

if __name__ == "__main__":
    main()
