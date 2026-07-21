#!/usr/bin/env python3
"""Migrate ✉️ Courriers from type-based to recipient-based structure."""

import os
import sys
import subprocess

ROOT = '/home/crilocom/accident-main'
BASE = os.path.join(ROOT, '⚖️ Actes/🔑 Token/✉️ Courriers')

# Mapping: old_path → new_path (relative to ✉️ Courriers/)
MAPPING = {}

def mv(old_sub, new_sub):
    MAPPING[old_sub] = new_sub

# ── 🏢 SAS & Salon (anciennes Mises en demeure SAS + Relance Dirigeants) ──
mv('📜 Mises en demeure/✉️📜 SAS Directrice.md',           '🏢 SAS & Salon/✉️📜 SAS Directrice.md')
mv('📜 Mises en demeure/✉️📜 SAS President.md',            '🏢 SAS & Salon/✉️📜 SAS President.md')
mv('📜 Mises en demeure/✉️📜 SAS.md',                      '🏢 SAS & Salon/✉️📜 SAS.md')
mv('📜 Mises en demeure/✉️📜 SAS Assureur RC.md',          '🏢 SAS & Salon/✉️📜 SAS Assureur RC.md')
mv('📜 Mises en demeure/✉️📜 SAS Assureur RC — Avocat.md', '🏢 SAS & Salon/✉️📜 SAS Assureur RC — Avocat.md')
mv('📜 Mises en demeure/✉️📜 SAS HB BARBER DG.md',         '🏢 SAS & Salon/✉️📜 SAS HB BARBER DG.md')
mv('📜 Mises en demeure/✉️📜 SAS HB BARBER President.md',  '🏢 SAS & Salon/✉️📜 SAS HB BARBER President.md')
mv('📜 Mises en demeure/✉️📜 SAS HB BARBER Societe.md',    '🏢 SAS & Salon/✉️📜 SAS HB BARBER Societe.md')
mv('🔄 Relances/✉️🔄 SAS Dirigeants.md',                   '🏢 SAS & Salon/✉️🔄 SAS Dirigeants.md')

# ── 🏠 Propriétaire ──
mv('📜 Mises en demeure/✉️📜 Proprietaire.md',             '🏠 Propriétaire/✉️📜 Proprietaire.md')
mv('📜 Mises en demeure/✉️📜 Proprietaire Relance 3.md',   '🏠 Propriétaire/✉️📜 Proprietaire Relance 3.md')

# ── 🏥 CPAM ──
mv('⚖️ Contentieux/✉️⚖️ CPAM Recours Tiers.md',           '🏥 CPAM/✉️⚖️ CPAM Recours Tiers.md')
mv('🔄 Relances/✉️🔄 CPAM Rectification Identite.md',     '🏥 CPAM/✉️🔄 CPAM Rectification Identite.md')
mv('🔄 Relances/🔄 CPAM.md',                               '🏥 CPAM/🔄 CPAM.md')

# ── 🏛️ Justice ──
mv('⚖️ Contentieux/✉️⚖️ Doyen Juges Instruction Saisine.md',  '🏛️ Justice/✉️⚖️ Doyen Juges Instruction Saisine.md')
mv('⚖️ Contentieux/✉️⚖️ FGTI Saisine.md',                     '🏛️ Justice/✉️⚖️ FGTI Saisine.md')
mv('⚖️ Contentieux/✉️⚖️ Procureur Foix Signalement Suites Mairie.md', '🏛️ Justice/✉️⚖️ Procureur Foix Signalement Suites Mairie.md')
mv('⚖️ Contentieux/✉️⚖️ TC Opposition Radiation.md',           '🏛️ Justice/✉️⚖️ TC Opposition Radiation.md')
mv('⚖️ Contentieux/✉️⚖️ TJ Foix Preuves Complementaires.md',  '🏛️ Justice/✉️⚖️ TJ Foix Preuves Complementaires.md')
mv('📝 Procédure/✉️📝 Avocat Consultation Jimini.md',          '🏛️ Justice/✉️📝 Avocat Consultation Jimini.md')

# ── 👮 Police ──
mv('⚖️ Contentieux/✉️⚖️ Commissariat Foix Plainte Complementaire.md', '👮 Police/✉️⚖️ Commissariat Foix Plainte Complementaire.md')
mv('🔄 Relances/🔄 Police Videos.md',                                   '👮 Police/🔄 Police Videos.md')

# ── 🏛️ Mairie ──
mv('📜 Mises en demeure/✉️📜 Maire Foix.md',          '🏛️ Mairie/✉️📜 Maire Foix.md')
mv('🔄 Relances/✉️🔄 Adjoint Maire Tavella.md',       '🏛️ Mairie/✉️🔄 Adjoint Maire Tavella.md')
mv('📝 Procédure/✉️📝 Mairie Tavella ERP.md',         '🏛️ Mairie/✉️📝 Mairie Tavella ERP.md')

# ── 🏛️ Administrations ──
mv('⚖️ Contentieux/✉️⚖️ INPI Opposition Immatriculation.md',  '🏛️ Administrations/✉️⚖️ INPI Opposition Immatriculation.md')
mv('📝 Procédure/✉️📝 CADA Saisine Formulaire.md',            '🏛️ Administrations/✉️📝 CADA Saisine Formulaire.md')
mv('📝 Procédure/✉️📝 CADA Saisine Modele.md',                '🏛️ Administrations/✉️📝 CADA Saisine Modele.md')
mv('📝 Procédure/✉️📝 SIE URSSAF Mutualisation.md',           '🏛️ Administrations/✉️📝 SIE URSSAF Mutualisation.md')
mv('🔄 Relances/✉️🔄 Inspection Travail.md',                  '🏛️ Administrations/✉️🔄 Inspection Travail.md')
mv('🔄 Relances/✉️🔄 Préfecture CODAF.md',                   '🏛️ Administrations/✉️🔄 Préfecture CODAF.md')
mv('🚨 Signalements/✉️🚨 CODAF.md',                          '🏛️ Administrations/✉️🚨 CODAF.md')
mv('🚨 Signalements/✉️🚨 Conseil Departemental.md',           '🏛️ Administrations/✉️🚨 Conseil Departemental.md')
mv('🚨 Signalements/✉️🚨 INPI.md',                            '🏛️ Administrations/✉️🚨 INPI.md')
mv('🚨 Signalements/✉️🚨 Inspection Travail.md',              '🏛️ Administrations/✉️🚨 Inspection Travail.md')
mv('🚨 Signalements/✉️🚨 Prefecture.md',                      '🏛️ Administrations/✉️🚨 Prefecture.md')
mv('🚨 Signalements/✉️🚨 SDIS.md',                            '🏛️ Administrations/✉️🚨 SDIS.md')
mv('🚨 Signalements/✉️🚨 SIE.md',                             '🏛️ Administrations/✉️🚨 SIE.md')
mv('🚨 Signalements/✉️🚨 URSSAF.md',                          '🏛️ Administrations/✉️🚨 URSSAF.md')

# ── 👥 Témoins ──
mv('📋 Attestations/📋 Témoin Client.md',         '👥 Témoins/📋 Témoin Client.md')
mv('📋 Attestations/📋 Témoin Client 📧Mail.md',  '👥 Témoins/📋 Témoin Client 📧Mail.md')
mv('📋 Attestations/📋 Employe.md',               '👥 Témoins/📋 Employe.md')
mv('📋 Attestations/📋 Employe 📧Mail.md',        '👥 Témoins/📋 Employe 📧Mail.md')
mv('📋 Attestations/📋 Pompier SAMU.md',           '👥 Témoins/📋 Pompier SAMU.md')
mv('📋 Attestations/📋 Pompier SAMU 📧Mail.md',    '👥 Témoins/📋 Pompier SAMU 📧Mail.md')

# ── ⚕️ Médical ──
mv('🔄 Relances/🔄 DrDJERBI Consolidation ✉️Mail.md', '⚕️ Médical/🔄 DrDJERBI Consolidation.md')

# ── 📋 Interne (docs non envoyés) ──
mv('📋 Personnel/📋 Antiseche Orale Plainte.md',      '📋 Interne/📋 Antiseche Orale Plainte.md')
mv('📋 Personnel/📋 Guide Dialogue Police.md',         '📋 Interne/📋 Guide Dialogue Police.md')
mv('📝 Procédure/📝 Demande AJ Totale.md',             '📋 Interne/📝 Demande AJ Totale.md')
mv('📝 Procédure/📝 Guide Demande AJ.md',              '📋 Interne/📝 Guide Demande AJ.md')

# ── 🗄️ Archivé (inchangé mais déplacé sous Courriers) ──
# Requete Constat Huissier stays in 🗄️ Archivé


def repo_rel(sub):
    """Convert relative path under BASE to repo-root-relative path."""
    full = os.path.join(BASE, sub)
    return os.path.relpath(full, ROOT)

def main():
    os.chdir(ROOT)
    
    # Step 1: Create new directories
    new_dirs = set(os.path.dirname(p) for p in MAPPING.values())
    for d in sorted(new_dirs):
        os.makedirs(os.path.join(BASE, d), exist_ok=True)
        print(f'📁 Created {d}/')
    
    # Step 2: git mv each file
    for old, new in sorted(MAPPING.items()):
        old_full = os.path.join(BASE, old)
        if not os.path.exists(old_full):
            print(f'❌ Source not found: {old}')
            continue
        subprocess.run(['git', 'mv', repo_rel(old), repo_rel(new)], check=True)
        print(f'  ✅ {old} → {new}')
    
    # Step 3: Remove empty old directories
    for old in sorted(set(os.path.dirname(p) for p in MAPPING), reverse=True):
        old_abs = os.path.join(BASE, old)
        if os.path.isdir(old_abs):
            remaining = [f for f in os.listdir(old_abs) if f.endswith('.md') and f != 'README.md']
            if not remaining:
                readme_path = os.path.join(old_abs, 'README.md')
                if os.path.exists(readme_path):
                    subprocess.run(['git', 'rm', repo_rel(readme_path)], check=True)
                    print(f'  🗑️ Removed {old}/README.md')
                print(f'  📭 {old}/ is now empty')
    
    print(f'\n✅ Migration done. {len(MAPPING)} files moved.')

if __name__ == '__main__':
    main()
