import os
import re

PIECES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pieces')
TEXTS_DIR = '/tmp/opencode/ocr_txt'

PIECE_YAML = {
    '20260529-1630 SITUATION DrJulieJARDON': {
        'titre': 'Compte Rendu de Situation — Docteur Julie JARDON',
        'date': '2026-05-29',
        'categorie': 'medical',
        'emetteur': 'Dr Julie JARDON',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['compte rendu', 'situation', 'main'],
        'drive_id': '1WzTk0Mlm2BKgA51eBzYhSKBvpAiTiuVf',
        'ocr': False,
        'pages': 1,
    },
    '20260530 CROpératoire RapportInterventionMainDroite': {
        'titre': 'Compte Rendu Opératoire — Rapport d\'Intervention Main Droite',
        'date': '2026-05-30',
        'categorie': 'medical',
        'emetteur': 'Dr Julie JARDON',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['compte rendu opératoire', 'intervention', 'main droite'],
        'drive_id': '1lwmms_NV6HY2pR4wGA1CIdu4LIQC-nD9',
        'ocr': False,
        'pages': 3,
    },
    '20260601 DossierPlainte PlainteOfficiellePV n°2026-015967': {
        'titre': 'Dossier de Plainte — Plainte Officielle PV n°2026-015967',
        'date': '2026-06-01',
        'categorie': 'penal',
        'emetteur': 'Commissariat de Police de la Ville de l\'Accident',
        'destinataire': 'Procureur de la République',
        'personnes': ['Sébastien GRAZIDE', 'L\'Exploitant du Commerce'],
        'tags': ['plainte', 'procès-verbal', 'PV', 'police'],
        'drive_id': '1estaaOWMphbrt5VXhy6MsTfHqBGIdj22',
        'ocr': False,
        'pages': 6,
    },
    '20260601-1105 NOTE DrOXYBEL': {
        'titre': 'Note Médicale — Docteur OXYBEL',
        'date': '2026-06-01',
        'categorie': 'medical',
        'emetteur': 'Dr Yogan OXYBEL',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['note médicale', 'consultation'],
        'drive_id': '1hmgc2NFUc9Iq9UPxwymVOqECq4KRF79Y',
        'ocr': False,
        'pages': 1,
    },
    '20260601-1115 CERTIFICATmedical DrOXYBEL': {
        'titre': 'Certificat Médical Initial — Docteur OXYBEL',
        'date': '2026-06-01',
        'categorie': 'medical',
        'emetteur': 'Dr Yogan OXYBEL',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['certificat médical initial', 'ITT'],
        'drive_id': '1SIcpCYIIJp84_6TY9dVbyMMr8Rlxbeda',
        'ocr': True,
        'pages': 1,
    },
    '20260602 PVPolice PV n°2026-015967 AccidentSalonCoiffure': {
        'titre': 'Procès-Verbal de Police n°2026-015967 — Accident Salon de Coiffure',
        'date': '2026-06-02',
        'categorie': 'penal',
        'emetteur': 'Commissariat de Police de la Ville de l\'Accident',
        'personnes': ['Sébastien GRAZIDE', 'L\'Exploitant du Commerce'],
        'tags': ['procès-verbal', 'PV', 'police', 'accident', 'salon de coiffure'],
        'drive_id': '1YXaJE81FFPTKcrcShg9DI5jUZ82T988V',
        'ocr': True,
        'pages': 12,
    },
    '20260603-2046 DOSSIER 31727387 AttestationDepot': {
        'titre': 'Attestation de Dépôt de Plainte DOSSIER n°31727387',
        'date': '2026-06-03',
        'categorie': 'penal',
        'emetteur': 'Commissariat de Police de la Ville de l\'Accident',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['attestation', 'dépôt', 'plainte', 'DOSSIER'],
        'drive_id': '1wyKSNyNvbJ4HygvQ4N-J_3jx88ItXYzR',
        'ocr': False,
        'pages': 1,
    },
    '20260612-1207 SituationMain': {
        'titre': 'Situation Main — Consultation de Suivi',
        'date': '2026-06-12',
        'categorie': 'medical',
        'emetteur': 'Dr Julie JARDON',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['suivi', 'main', 'consultation'],
        'drive_id': '1gezULqgCQwUWSAJXePpLpTxUQ3A9u6bm',
        'ocr': False,
        'pages': 2,
    },
    '20260618-1406 DOC AssuranceMaladie DemandeDeRenseignement': {
        'titre': 'Document Assurance Maladie — Demande de Renseignement',
        'date': '2026-06-18',
        'categorie': 'administratif',
        'emetteur': 'Caisse Primaire d\'Assurance Maladie (CPAM)',
        'destinataire': 'Dr Julie JARDON',
        'personnes': ['Sébastien GRAZIDE', 'Dr Julie JARDON'],
        'tags': ['assurance maladie', 'CPAM', 'demande', 'renseignement'],
        'drive_id': '1XtFxLG3IsVBtTlF4bN7YeWxB3KZAEqBn',
        'ocr': False,
        'pages': 3,
    },
    '20260619-1528 MAIL DrDjerbi': {
        'titre': 'Courriel du Docteur DJERBI',
        'date': '2026-06-19',
        'categorie': 'medical',
        'emetteur': 'Dr DJERBI',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['courriel', 'mail', 'Dr DJERBI'],
        'drive_id': '1nT3r6nh6GnOeAOZiHD2km4h9qFUXMac4',
        'ocr': False,
        'pages': 2,
    },
    '20260623-1730 DrDJERBI Bilan': {
        'titre': 'Bilan — Docteur DJERBI',
        'date': '2026-06-23',
        'categorie': 'medical',
        'emetteur': 'Dr DJERBI',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['bilan', 'Dr DJERBI'],
        'drive_id': '1Xaz3iA_-40WtHRkOe_db1NcO-tBxAENQ',
        'ocr': True,
        'pages': 2,
    },
    '20260623-1731 DrDJERBI Ordonnance Kinesitherapeute': {
        'titre': 'Ordonnance de Kinésithérapie — Docteur DJERBI',
        'date': '2026-06-23',
        'categorie': 'medical',
        'emetteur': 'Dr DJERBI',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['ordonnance', 'kinésithérapie', 'Dr DJERBI'],
        'drive_id': '1t-DHwIZUyJgWwQGOAFHtNvNC2xVtMozp',
        'ocr': True,
        'pages': 2,
    },
    '20260623-1811 CompteRendu DrDJERBI MonEspaceSanté PJ1': {
        'titre': 'Compte Rendu — Docteur DJERBI MonEspaceSanté (PJ1)',
        'date': '2026-06-23',
        'categorie': 'medical',
        'emetteur': 'Dr DJERBI',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['compte rendu', 'MonEspaceSanté', 'Dr DJERBI'],
        'drive_id': '1WMUNB4CIElU9s6SV86iIVJAP4Nn8FfEP',
        'ocr': False,
        'pages': 2,
    },
    '20260623-1811 CompteRendu DrDJERBI MonEspaceSanté PJ2': {
        'titre': 'Compte Rendu — Docteur DJERBI MonEspaceSanté (PJ2)',
        'date': '2026-06-23',
        'categorie': 'medical',
        'emetteur': 'Dr DJERBI',
        'personnes': ['Sébastien GRAZIDE'],
        'tags': ['compte rendu', 'MonEspaceSanté', 'Dr DJERBI'],
        'drive_id': '1HaQVZh_Dsj2sbebvp6zHnps_6q791duR',
        'ocr': False,
        'pages': 2,
    },
    '20260629 ✉️ LR MiseEnDemeure Bailleur MrDELRIEU': {
        'titre': 'Lettre Recommandée — Mise en Demeure Bailleur Monsieur DELRIEU',
        'date': '2026-06-29',
        'categorie': 'juridique',
        'emetteur': 'Sébastien GRAZIDE',
        'destinataire': 'Monsieur DELRIEU (Bailleur)',
        'personnes': ['Sébastien GRAZIDE', 'Monsieur DELRIEU'],
        'tags': ['LR', 'mise en demeure', 'bailleur'],
        'drive_id': '114JeqDjs9-0PRC_PHQrBxH1CZ3PoZgIv',
        'ocr': False,
        'pages': 1,
    },
    '20260629 ✉️ LR MiseEnDemeure SAS LesMauvaisGarcons': {
        'titre': 'Lettre Recommandée — Mise en Demeure SAS Les Mauvais Garçons',
        'date': '2026-06-29',
        'categorie': 'juridique',
        'emetteur': 'Sébastien GRAZIDE',
        'destinataire': 'SAS Les Mauvais Garçons',
        'personnes': ['Sébastien GRAZIDE', 'SAS Les Mauvais Garçons'],
        'tags': ['LR', 'mise en demeure', 'SAS'],
        'drive_id': '1ig96EJZFO5yqZcYnkJl7g2urAuTxkZLn',
        'ocr': False,
        'pages': 1,
    },
    '20260629 ✉️ LR MiseEnDemeure SAS MmeANDISSAC': {
        'titre': 'Lettre Recommandée — Mise en Demeure SAS Madame ANDISSAC',
        'date': '2026-06-29',
        'categorie': 'juridique',
        'emetteur': 'Sébastien GRAZIDE',
        'destinataire': 'SAS ANDISSAC',
        'personnes': ['Sébastien GRAZIDE', 'SAS ANDISSAC'],
        'tags': ['LR', 'mise en demeure', 'SAS'],
        'drive_id': '1EcEmT59OVPSiVTf9pK9gKwCYcBHSJ_93',
        'ocr': False,
        'pages': 1,
    },
    '20260629 ✉️ LR MiseEnDemeure SAS President MrSABIR': {
        'titre': 'Lettre Recommandée — Mise en Demeure SAS Président Monsieur SABIR',
        'date': '2026-06-29',
        'categorie': 'juridique',
        'emetteur': 'Sébastien GRAZIDE',
        'destinataire': 'Monsieur SABIR (Président SAS)',
        'personnes': ['Sébastien GRAZIDE', 'Monsieur SABIR'],
        'tags': ['LR', 'mise en demeure', 'président', 'SAS'],
        'drive_id': '117sFmGu7yFbYzd0VrKYNSCK_tDYHugrL',
        'ocr': False,
        'pages': 1,
    },
    '20260629 ✉️ LR Transmission TribunalFOIX ProcureurDeLaRépublique': {
        'titre': 'Lettre Recommandée — Transmission Tribunal de FOIX au Procureur de la République',
        'date': '2026-06-29',
        'categorie': 'juridique',
        'emetteur': 'Sébastien GRAZIDE',
        'destinataire': 'Procureur de la République près le Tribunal Judiciaire de FOIX',
        'personnes': ['Sébastien GRAZIDE', 'Procureur de la République'],
        'tags': ['LR', 'transmission', 'tribunal', 'FOIX', 'procureur'],
        'drive_id': '1wpqT0wnHd5uwwKDJb65w576jG9H9wYzm',
        'ocr': False,
        'pages': 1,
    },
}

YAML_KEYS_ORDER = [
    'titre', 'date', 'type', 'categorie', 'emetteur', 'destinataire',
    'personnes', 'tags', 'statut', 'source', 'drive_id', 'drive_url', 'ocr', 'pages',
    'verifie',
]

IMMUTABILITY_BANNER = """

> **🔒 PIÈCE ORIGINALE — NE PAS MODIFIER**
> Ce fichier est une copie textuelle exacte de la pièce originale (PDF).
> Toute modification du contenu textuel est interdite.
> En cas d'erreur, corriger le PDF source et ré-exporter.
> drive_id: {drive_id}
> drive_url: {drive_url}

"""


def format_yaml(data: dict) -> str:
    lines = ['---']
    for key in YAML_KEYS_ORDER:
        if key not in data:
            continue
        value = data[key]
        if value is None:
            lines.append(f'{key}: null')
        elif isinstance(value, bool):
            lines.append(f'{key}: {str(value).lower()}')
        elif isinstance(value, int):
            lines.append(f'{key}: {value}')
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
    os.makedirs(PIECES_DIR, exist_ok=True)

    for base_name, yaml_data in PIECE_YAML.items():
        txt_path = os.path.join(TEXTS_DIR, f'{base_name}.txt')
        if not os.path.exists(txt_path):
            print(f'⚠ Fichier txt introuvable: {txt_path}')
            continue

        with open(txt_path, 'r', encoding='utf-8') as f:
            text_content = f.read()

        # Build YAML
        yaml_base = {
            'type': 'piece',
            'statut': 'original',
            'source': 'drive',
            'verifie': False,
        }
        yaml_base.update(yaml_data)

        drive_id = yaml_data['drive_id']
        yaml_base['drive_url'] = f'https://drive.google.com/file/d/{drive_id}/view'

        yaml_block = format_yaml(yaml_base)
        banner = IMMUTABILITY_BANNER.format(drive_id=drive_id, drive_url=yaml_base['drive_url'])

        md_content = yaml_block + banner + text_content

        # Clean OCR page markers for readability
        md_content = re.sub(r'^=== PIECE:.*?\n', '', md_content, flags=re.MULTILINE)
        md_content = re.sub(r'^--- PAGE (\d+) ---\n?', r'\n\n--- Page \1 ---\n\n', md_content, flags=re.MULTILINE)

        md_path = os.path.join(PIECES_DIR, f'{base_name}.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f'✅ {base_name}.md')


if __name__ == '__main__':
    main()
