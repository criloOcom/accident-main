import os
import re

directories_to_scan = ["Actes/Token", "Rapports"]
output_file = "Rapports/AUDIT_VARIABLES_TOKEN.md"

def find_inconsistencies(filepath):
    if filepath == output_file:
        return []

    inconsistencies = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # Check Profession (Victime = Informaticien)
                # Look for "coiffeur" associated with "victime" or "profession"
                if re.search(r'(?i)coiffeur', line) and "pas coiffeur" not in line.lower() and "erreur" not in line.lower() and "non coiffeur" not in line.lower():
                     if re.search(r'(?i)profession.*?coiffeur', line) or re.search(r'(?i)victime.*?coiffeur', line) or re.search(r'(?i)coiffeur.*?victime', line):
                         if not "préposé" in line.lower() and not "tiers" in line.lower() and not "impliqué" in line.lower() and not "coiffeur est le tiers" in line.lower() and not "confusion" in line.lower():
                            inconsistencies.append((i+1, "Profession erronée (victime qualifiée de 'coiffeur')", line.strip(), "Remplacer par 'informaticien indépendant'."))
                if re.search(r'(?i)développeur salarié', line):
                     inconsistencies.append((i+1, "Profession erronée ('développeur salarié' au lieu d'informaticien indépendant)", line.strip(), "Remplacer par 'informaticien indépendant'."))

                # Check DFP (25 200 €)
                if "DFP" in line and "€" in line and filepath.startswith("Rapports"):
                    if "25 200" not in line and "SUPERSEDED" not in line and "25 000" not in line:
                         # Ensure it's a DFP amount line for the final amount
                         if "20 000" in line or "30 000" in line or "15 000" in line or "31 200" in line:
                             if "prudent" not in line.lower() and "médian" not in line.lower() and "initiale" not in line.lower() and "préconise" not in line.lower():
                                 inconsistencies.append((i+1, "Montant DFP erroné (25 200 € attendu)", line.strip(), "Mettre à jour à 25 200 €."))

                # Check SE (14 000 €)
                if "Souffrances" in line and ("15 000" in line or "12 000" in line or "24 000" in line or "3/7" in line or "3,5/7" in line) and filepath.startswith("Rapports"):
                    if "14 000" not in line and "4/7" not in line and "SUPERSEDED" not in line and "obsolète" not in line.lower() and "initialement" not in line.lower():
                        inconsistencies.append((i+1, "Montant/Cotation SE erroné (14 000 € ou 4/7 attendu)", line.strip(), "Mettre à jour avec 14 000 € (cotation 4/7)."))
                elif "Souffrances endurées" in line and "4/7" in line and "14 000" not in line and filepath.startswith("Rapports"):
                    pass # could be just 4/7

                # Date accident (29 mai 2026)
                if ("31 mai 2026" in line or "29 juin 2026" in line) and "accident" in line.lower():
                    inconsistencies.append((i+1, "Date d'accident erronée (29 mai 2026 attendu)", line.strip(), "Corriger la date en '29 mai 2026'."))

                # Adresse
                if "22, RUE DE LA FAURIE" in line and "orthographe" not in line.lower():
                     if "PV police" not in line and "PV de police" not in line and "Constat" not in line:
                        inconsistencies.append((i+1, "Adresse mal orthographiée (22 Rue Lafaurie attendu)", line.strip(), "Remplacer par '22 Rue Lafaurie'."))

                # Doigt
                if "auriculaire" in line.lower() and not "pas auriculaire" in line.lower() and not "jamais auriculaire" in line.lower() and not "erreur" in line.lower():
                    inconsistencies.append((i+1, "Doigt blessé erroné (index attendu)", line.strip(), "Remplacer 'auriculaire' par 'index'."))
                if "5e doigt" in line.lower() and not "pas 5e doigt" in line.lower() and not "jamais 5e doigt" in line.lower() and not "erreur" in line.lower():
                    inconsistencies.append((i+1, "Doigt blessé erroné (index attendu)", line.strip(), "Remplacer '5e doigt' par 'index'."))

                # SAS name
                if "SAS" in line and "L'Exploitant du Commerce (La SAS)" not in line and "NOM_SAS" in line:
                     inconsistencies.append((i+1, "Nom SAS non tokenisé", line.strip(), "Remplacer 'NOM_SAS' par '**[L'Exploitant du Commerce (La SAS)]**'."))

    except Exception as e:
        pass
    return inconsistencies

all_inconsistencies = {}
for directory in directories_to_scan:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                res = find_inconsistencies(filepath)
                if res:
                    all_inconsistencies[filepath] = res

# Generate Report Markdown
if os.path.exists(output_file):
    os.remove(output_file)

with open(output_file, "w", encoding="utf-8") as f:
    f.write("---\n")
    f.write("title: \"Audit des variables STRICT_VARIABLES et Tokens\"\n")
    f.write("description: \"Rapport recensant les incohérences factuelles dans les actes et rapports par rapport aux STRICT_VARIABLES.\"\n")
    f.write("type: rapport\n")
    f.write("---\n\n")
    f.write("<!-- Breadcrumb -->\n")
    f.write("<a href=\"../README.md\">Retour</a>\n")
    f.write("<!-- /Breadcrumb -->\n\n")
    f.write("<hr>\n\n")
    f.write("# Audit des variables STRICT_VARIABLES et Tokens\n\n")
    f.write("Ce rapport liste les incohérences détectées dans les fichiers sous `Actes/Token/` et `Rapports/` par rapport aux règles définies dans `Memory/STRICT_VARIABLES.md`.\n\n")

    f.write("<hr><hr>\n\n")
    f.write("## I — INCOHÉRENCES DÉTECTÉES\n\n")

    if not all_inconsistencies:
        f.write("Aucune incohérence détectée.\n\n")
    else:
        for filepath, inc_list in sorted(all_inconsistencies.items()):
            f.write(f"### A. Fichier : `{filepath}`\n\n")
            for i, error, value, correction in inc_list:
                f.write(f"- **Ligne {i}** : {error}\n")
                f.write(f"  - **Valeur erronée** : `{value}`\n")
                f.write(f"  - **Correction suggérée** : {correction}\n\n")

print("Report successfully generated!")
