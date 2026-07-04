import os
import re

ACTES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'actes')

YAML_MAP = {
    '01_Assignation_REFERE_PROVISION_FINAL.md': {
        'titre': 'Assignation en Référé-Provision et Demande d\'Expertise Médicale',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'procedure',
        'auteur': 'La Victime',
        'destinataire': 'Tribunal Judiciaire de la Ville de l\'Accident',
        'personnes': ['La Victime', 'L\'Exploitant du Commerce'],
        'tags': ['assignation', 'référé', 'provision', 'expertise médicale'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1ZIfWjszjl5VoxBxourQiDeRATbkckkWPzbU9tYmg5yg',
    },
    '02_ActionDirecte_AssureurRC.md': {
        'titre': 'Action Directe Assureur RC (Art. L.124-3)',
        'date': '2026-06-29',
        'type': 'acte',
        'categorie': 'procedure',
        'auteur': 'La Victime',
        'destinataire': 'Compagnie d\'Assurance de l\'Exploitant du Commerce',
        'personnes': ['La Victime', 'L\'Exploitant du Commerce'],
        'tags': ['action directe', 'assurance', 'mise en demeure', 'L.124-3'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1_tNTGHf1VGnx1zD0PvyrdvqHLAyYDBU_7wRibBwWlJY',
    },
    '03_Plainte_Complet_Defaut_Assurance.md': {
        'titre': 'Plainte Complément — Défaut d\'Assurance RC',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'penale',
        'auteur': 'La Victime',
        'destinataire': 'Procureur de la République',
        'personnes': ['La Victime', 'L\'Exploitant du Commerce'],
        'tags': ['plainte', 'défaut d\'assurance', 'pénal', 'L.211-26'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1TVN7SyAWgTLQtOvUzpWqqlfF7fyzT8H8yLziKLQhelc',
    },
    '04_Assignation_Refere_Provision_V1.md': {
        'titre': 'Projet d\'Assignation en Référé-Provision (V1 — 5000€)',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'procedure',
        'auteur': 'La Victime',
        'destinataire': 'Tribunal Judiciaire de la Ville de l\'Accident',
        'personnes': ['La Victime', 'L\'Exploitant du Commerce'],
        'tags': ['assignation', 'référé', 'provision', 'brouillon'],
        'statut': 'brouillon',
        'source': 'drive',
        'drive_id': '1L3lJuFQ3CmswKlBg8P5YF6whQQ1AV7QTCLQ_arWo39A',
    },
    '05_Constitution_Partie_Civile.md': {
        'titre': 'Constitution de Partie Civile',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'penale',
        'auteur': 'La Victime',
        'destinataire': 'Tribunal Correctionnel',
        'personnes': ['La Victime', 'L\'Exploitant du Commerce'],
        'tags': ['constitution', 'partie civile', 'pénal'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1tdFbDxNceGVjaABoYiHkUR1jxd8y0OaezWUOoV3ZDGc',
    },
    '06_Dossier_Presentation.md': {
        'titre': 'Dossier de Présentation destiné au Conseil Juridique',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'synthese',
        'auteur': 'La Victime',
        'destinataire': 'Conseil Juridique',
        'personnes': ['La Victime', 'L\'Exploitant du Commerce'],
        'tags': ['présentation', 'synthèse', 'avocat', 'dossier'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1DdpbOypghzt9XE09oxtzx46ngPdU4pnc4gayLQEZ_TU',
    },
    '07_ETUDE_Indemnisation_MAX.md': {
        'titre': 'Étude d\'Indemnisation Maximale (Nomenclature Dintilhac)',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'evaluation',
        'auteur': 'La Victime',
        'destinataire': None,
        'personnes': ['La Victime'],
        'tags': ['indemnisation', 'dintilhac', 'préjudice', 'évaluation'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1PiBFn1oA1DtkT61N-zvdPmsCYsmR0au9V4BA9IZzrH4',
    },
    '08_Index_EtatFinal_Dossier.md': {
        'titre': 'Index de l\'État Final du Dossier',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'inventaire',
        'auteur': 'La Victime',
        'destinataire': None,
        'personnes': ['La Victime', 'L\'Exploitant du Commerce'],
        'tags': ['index', 'inventaire', 'pièces', 'dossier'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1Zp-JK9kz0V0DTqNbA7QDDfHliWAqv7Ebyw4Yu3Li6lU',
    },
    '09_PlanAction_Chronologie.md': {
        'titre': 'Plan d\'Action et Chronologie de la Procédure',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'strategie',
        'auteur': 'La Victime',
        'destinataire': None,
        'personnes': ['La Victime'],
        'tags': ['plan', 'chronologie', 'procédure', 'stratégie'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '153cOANMpw-OoxZqq3jgo34NsWHPY_-cRXZntM_Ydf9s',
    },
    '10_Synthese_FAQ.md': {
        'titre': 'Synthèse Juridique et FAQ',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'synthese',
        'auteur': 'La Victime',
        'destinataire': None,
        'personnes': ['La Victime', 'L\'Exploitant du Commerce'],
        'tags': ['faq', 'synthèse', 'juridique', 'questions'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1eoOJ-bcHBNnLsKYo7_mVz7K1w0gFfhZE_NHdUj3CBoM',
    },
    '11_ANALYSE_correction_juridique.md': {
        'titre': 'Mémorandum Juridique — Audit Stratégique et Restructuration Contentieuse',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'analyse',
        'auteur': 'La Victime',
        'destinataire': None,
        'personnes': ['La Victime', 'L\'Exploitant du Commerce'],
        'tags': ['audit', 'correction', 'stratégie', 'juridique'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1Ikk9wlfyLuFlTofsyLiz6836bHM5g4_ejQhGuRdUkes',
    },
    '12_ANALYSE_Jurisprudence.md': {
        'titre': 'Rapport d\'Expertise Juridique — Analyse des Préjudices Corporels',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'analyse',
        'auteur': 'La Victime',
        'destinataire': None,
        'personnes': ['La Victime'],
        'tags': ['expertise', 'jurisprudence', 'préjudice', 'dintilhac'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1AO7GLNpbNGa9ChiUVa5rbbhLtmppzMTgOcg9qCIJBRU',
    },
    '13_ANALYSE_Plaidoirie_Dirigeants.md': {
        'titre': 'Mémorandum Juridique — Responsabilité des Dirigeants',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'analyse',
        'auteur': 'La Victime',
        'destinataire': None,
        'personnes': ['La Victime', 'Le Président de l\'Exploitation', 'La Directrice Générale de l\'Exploitation'],
        'tags': ['dirigeants', 'responsabilité', 'plaidoirie', 'sociétés'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1uHOesWZrUf16NVs7kC_dr15JtthOfaJnUNo6e3Z7W90',
    },
    '14_ANALYSE_Responsabilites_Legales.md': {
        'titre': 'Analyse des Fondements de la Responsabilité Juridique',
        'date': '2026-06-30',
        'type': 'acte',
        'categorie': 'analyse',
        'auteur': 'La Victime',
        'destinataire': None,
        'personnes': ['La Victime', 'L\'Exploitant du Commerce'],
        'tags': ['responsabilité', 'fondements', 'analyse', 'juridique'],
        'statut': 'final',
        'source': 'drive',
        'drive_id': '1lUKoGE8kozmE3KA4zErv9GYmJZ0yctOk9tn92O8KT34',
    },
}


def format_yaml(data: dict) -> str:
    lines = ['---']
    for key, value in data.items():
        if value is None:
            lines.append(f'{key}: null')
        elif isinstance(value, list):
            items = '\n'.join(f'  - {v}' for v in value)
            lines.append(f'{key}:\n{items}')
        elif isinstance(value, str) and (':' in value or '#' in value):
            lines.append(f'{key}: "{value}"')
        else:
            lines.append(f'{key}: {value}')
    lines.append('---')
    return '\n'.join(lines)


def main():
    for fname, yaml_data in YAML_MAP.items():
        fpath = os.path.join(ACTES_DIR, fname)
        if not os.path.exists(fpath):
            print(f'⚠ {fname} introuvable')
            continue

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove existing ---\n at start if present
        if content.startswith('---\n'):
            content = content[4:].lstrip('\n')

        yaml_block = format_yaml(yaml_data)
        new_content = yaml_block + '\n\n' + content

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f'✅ {fname}')


if __name__ == '__main__':
    main()
