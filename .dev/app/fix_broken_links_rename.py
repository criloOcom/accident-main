#!/usr/bin/env python3
"""
Fix broken links from Courriers emoji removal and Contentieux renames.

Maps old filenames (with emojis or old prefixes) to new filenames.
"""

import os
import re
import urllib.parse

ROOT = '/home/crilocom/accident-main'

# Mapping: old filename patterns → new filename patterns
# Applied as substring replacements in link targets
LINK_FIXES = [
    # Courriers emoji removal: 📜 Police - → Police -
    ('📜 Police - Note Erratum Identité.md', 'Police - Note Erratum Identité.md'),
    ('📋 Police - Bordereau Pièces.md', 'Police - Bordereau Pièces.md'),
    ('📋 Note - Note - Note - Police - Note Frise Chronologique.md', 'Police - Note Frise Chronologique.md'),
    ('📋 Police - Note Personnelle.md', 'Police - Note Personnelle.md'),
    ('📋 Police - Note Projet Déclaration.md', 'Police - Note Projet Déclaration.md'),
    ('📋 Note - Police - Note Guide Plainte.md', 'Police - Note Guide Plainte.md'),
    ('📋 Note - Police - Note Guide Plainte Orale.md', 'Police - Note Guide Plainte Orale.md'),
    
    # Courriers emoji removal: ✉️ prefix on filenames
    ('✉️ SAS - Courrier.md', 'SAS - Courrier.md'),
    ('✉️ SAS - Assureur RC - Courrier.md', 'SAS - Assureur RC - Courrier.md'),
    ('✉️ SAS - Assureur RC - Courrier (copie Avocat).md', 'SAS - Assureur RC - Courrier (copie Avocat).md'),
    ('✉️ SAS - Dirigeants - Courrier - Relance.md', 'SAS - Dirigeants - Courrier - Relance.md'),
    ('✉️ SAS - Président - Courrier.md', 'SAS - Président - Courrier.md'),
    ('✉️ SAS - Directrice Générale - Courrier.md', 'SAS - Directrice Générale - Courrier.md'),
    ('✉️ Doyen des Juges - Saisine.md', 'DJI Foix - Doyen des Juges - Saisine.md'),
    ('✉️ Mairie - ERP Tavella - Courrier.md', 'Mairie - ERP Tavella - Courrier.md'),
    ('✉️ Mairie - Maire de Foix - Courrier.md', 'Mairie - Maire de Foix - Courrier.md'),
    ('✉️ Mairie - Tavella - Courrier - Relance.md', 'Mairie - Tavella - Courrier - Relance.md'),
    ('✉️ Propriétaire - Courrier.md', 'Propriétaire - Courrier.md'),
    ('✉️ Propriétaire - Courrier - Relance 3.md', 'Propriétaire - Courrier - Relance 3.md'),
    ('✉️ CPAM - Relance.md', 'CPAM - Relance.md'),
    ('✉️ CPAM - Recours Tiers - Saisine.md', 'CPAM - Recours Tiers - Saisine.md'),
    ('✉️ CPAM - Rectification Identité - Relance.md', 'CPAM - Rectification Identité - Relance.md'),
    ('✉️ DDETS - Signalement.md', 'DDETS - Signalement.md'),
    ('✉️ DDETS - Signalement - Relance.md', 'DDETS - Signalement - Relance.md'),
    ('✉️ CODAF - Signalement.md', 'CODAF - Signalement.md'),
    ('✉️ CODAF - Signalement - Relance.md', 'CODAF - Signalement - Relance.md'),
    ('✉️ CODAF - Préfecture - Signalement.md', 'CODAF - Préfecture - Signalement.md'),
    ('✉️ Préfecture - Signalement.md', 'CODAF - Préfecture - Signalement.md'),
    ('✉️ URSSAF - Signalement.md', 'URSSAF - Signalement.md'),
    ('✉️ SIE - Signalement.md', 'SIE - Signalement.md'),
    ('✉️ SIE URSSAF - Mutualisation - Courrier.md', 'SIE URSSAF - Mutualisation - Courrier.md'),
    ('✉️ INPI - Signalement.md', 'INPI - Signalement.md'),
    ('✉️ INPI - Immatriculation - Opposition.md', 'INPI - Immatriculation - Opposition.md'),
    ('✉️ SDIS - Signalement.md', 'SDIS - Signalement.md'),
    ('✉️ Conseil Départemental - Signalement.md', 'Conseil Départemental - Signalement.md'),
    ('✉️ FGTI - Saisine.md', 'FGTI - Saisine.md'),
    ('✉️ Consultation - Avocat Jimini.md', 'Consultation - Avocat Jimini.md'),
    ('✉️ TJ Foix - Courrier - Preuves Complémentaires.md', 'TJ Foix - Courrier - Preuves Complémentaires.md'),
    ('✉️ TJ Foix - Mémo - Audience 31-07-2026.md', 'TJ Foix - Mémo - Audience 31-07-2026.md'),
    ('✉️ TC Foix - Tribunal de Commerce - Opposition Radiation.md', 'TC Foix - Tribunal de Commerce - Opposition Radiation.md'),
    ('✉️ Médecin Traitant - Consolidation - Demande.md', 'Médecin Traitant - Consolidation - Demande.md'),
    ('✉️ Médecin Traitant - Consolidation - Relance.md', 'Médecin Traitant - Consolidation - Relance.md'),
    ('✉️ CHIVA - Dossier Médical - Demande.md', 'CHIVA - Dossier Médical - Demande.md'),
    ('✉️ Témoin Client - Attestation.md', 'Témoin Client - Attestation.md'),
    ('✉️ Pompier SAMU - Attestation.md', 'Pompier SAMU - Attestation.md'),
    ('✉️ Police - Vidéos - Relance.md', 'Police - Vidéos - Relance.md'),
    ('✉️ Police - Plainte Complémentaire.md', 'Police - Plainte Complémentaire.md'),
    ('✉️ BAJ - Demande AJ - Totale.md', 'BAJ - Demande AJ - Totale.md'),
    ('✉️ BAJ - Demande AJ - Guide.md', 'BAJ - Demande AJ - Guide.md'),
    ('✉️ Constat Huissier - Requête Archive.md', 'Requête - Constat Huissier Archive.md'),
    
    # Contentieux proceduraux renames: old prefix → new prefix
    ('Partie Civile - Constitution.md', 'DJI Foix - Partie Civile - Constitution.md'),
    ('Parquet - Réquisitoire Introductif.md', 'DJI Foix - Parquet - Réquisitoire Introductif.md'),
    ('Parquet - Plainte Complémentaire - Correction.md', 'Parquet Foix - Plainte Complémentaire - Correction.md'),
    ('Parquet - Plainte Complémentaire - PV Audition.md', 'Parquet Foix - Plainte Complémentaire - PV Audition.md'),
    ('Parquet - Plainte Complémentaire - PV Audition Foix.md', 'Parquet Foix - Plainte Complémentaire - PV Audition Foix.md'),
    ('Parquet - Assurance RC - Plainte Défaut.md', 'Parquet Foix - Assurance RC - Plainte Défaut.md'),
    ('Parquet - Signalement Fraude.md', 'Parquet Foix - Signalement Fraude.md'),
    
    # Contentieux civil renames: TJ Foix - TJ Foix - → TJ Foix -
    ('TJ Foix - TJ Foix - Bordereau Unifié.md', 'TJ Foix - Bordereau Unifié.md'),
    ('TJ Foix - TJ Foix - Référé Provision - Ordonnance Projet.md', 'TJ Foix - Référé Provision - Ordonnance Projet.md'),
    ('TJ Foix - TJ Foix - Mémo - Audience 31-07-2026.md', 'TJ Foix - Mémo - Audience 31-07-2026.md'),
    
    # Contentieux civil renames: old names → new names
    ('Référé Provision - Assignation.md', 'TJ Foix - Référé Provision - Assignation.md'),
    ('Référé Provision - Conclusions.md', 'TJ Foix - Référé Provision - Conclusions.md'),
    ('CPC 145 - Requête.md', 'TJ Foix - CPC 145 - Requête.md'),
    ('CPC 145 - Ordonnance sur Requête.md', 'TJ Foix - CPC 145 - Ordonnance sur Requête.md'),
    ('Mandataire Ad Hoc - Requête.md', 'TC Foix - Mandataire Ad Hoc - Requête.md'),
    
    # Archives renames
    ('33 ✉️ Constat Huissier - Requête 145 CPC.md', '33_Requête_-_Constat_Huissier_145_CPC.md'),
    ('Constat Huissier - Requête Archive.md', 'Requête - Constat Huissier Archive.md'),
    
    # Mail Attestation → correct name
    ('Mail Attestation.md', 'Email Attestation.md'),
    
    # Courriers emoji in URL-encoded paths (fix the ✉️ in directory paths)
    ('/%E2%9C%89%EF%B8%8F%20', '/'),
]


def fix_links_in_file(filepath):
    """Fix broken links in a file. Returns (content, changes_made)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    for old, new in LINK_FIXES:
        if old in content:
            content = content.replace(old, new)
            changes.append(f"  {old} → {new}")
    
    if content != original:
        return content, changes
    return content, []


def find_all_md_files():
    """Find all .md files in the project."""
    files = []
    for dp, _, fnames in os.walk(ROOT):
        if '.git' in dp or '__pycache__' in dp:
            continue
        for f in fnames:
            if f.endswith('.md'):
                files.append(os.path.join(dp, f))
    return sorted(files)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fix broken links from renames')
    parser.add_argument('--apply', action='store_true', help='Apply fixes')
    args = parser.parse_args()
    
    files = find_all_md_files()
    print(f"Scanning {len(files)} files...")
    
    total_fixed = 0
    total_changes = 0
    
    for fp in files:
        rel_path = os.path.relpath(fp, ROOT)
        fixed_content, changes = fix_links_in_file(fp)
        
        if changes:
            total_fixed += 1
            total_changes += len(changes)
            print(f"\n{rel_path}:")
            for change in changes:
                print(f"  {change}")
            
            if args.apply:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Files scanned: {len(files)}")
    print(f"Files with fixes: {total_fixed}")
    print(f"Total link fixes: {total_changes}")
    if not args.apply:
        print(f"\nRun with --apply to apply fixes")


if __name__ == '__main__':
    main()
