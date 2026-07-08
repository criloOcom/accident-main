#!/usr/bin/env python3
import json
import re
import sys
import os
from googleapiclient import discovery

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive_auth import get_drive_service

# 1. Charger les données sources
with open('data/scratch/scratch_dest_rows.json') as f:
    dest_rows = json.load(f)
with open('data/scratch/scratch_final_new_rows.json') as f:
    new_rows = json.load(f)

# On commence par charger la destination existante pour préserver ses IDs (EVT-01, COR-01, etc.)
final_list = []
seen_keys = set() # (date_key, evt_key) pour dédoublonner

# 2. Variable strictes pour filtrage strict (autre affaire M. U)
EXCLUDE_KEYWORDS = [
    'prothèse', 'amputation', 'jambe', 'm. u', 'domofrance', 'matmut', 'civi', 
    'basse-terre', 'pointe-à-pitre', 'fauteuil roulant', 'logement adapté'
]

# Les dates en DD/MM/YYYY HH:MM ou YYYY-MM-DD
def parse_date(date_str):
    date_str = date_str.strip()
    if not date_str:
        return ""
    
    # 5. Normaliser les dates non standard
    if "non précisée dans la source" in date_str.lower() or "non précisé" in date_str.lower():
        return "Non précisé"
    if "d'ici le 05/06/2026" in date_str.lower() or "05/06/2026 (date butoir)" in date_str.lower():
        return "05/06/2026"
    if "avant le 12/06/2026" in date_str.lower():
        return "12/06/2026"
    if "mai 2026" in date_str.lower():
        return "01/05/2026"
        
    # Si format ISO AAAA-MM-JJ HH:MM ou AAAA-MM-JJ
    m_iso = re.match(r'^(\d{4})-(\d{2})-(\d{2})(?:\s+(\d{2}):(\d{2}))?', date_str)
    if m_iso:
        year, month, day = m_iso.group(1), m_iso.group(2), m_iso.group(3)
        hour = m_iso.group(4) if m_iso.group(4) else None
        minute = m_iso.group(5) if m_iso.group(5) else None
        if hour and minute:
            return f"{day}/{month}/{year} {hour}:{minute}"
        return f"{day}/{month}/{year}"
    
    # Si format standard JJ/MM/AAAA HH:MM ou JJ/MM/AAAA
    m_std = re.match(r'^(\d{2})/(\d{2})/(\d{4})(?:\s+(\d{2})[h:](\d{2}))?', date_str)
    if m_std:
        day, month, year = m_std.group(1), m_std.group(2), m_std.group(3)
        hour = m_std.group(4) if m_std.group(4) else None
        minute = m_std.group(5) if m_std.group(5) else None
        if hour and minute:
            return f"{day}/{month}/{year} {hour}:{minute}"
        return f"{day}/{month}/{year}"
    
    return date_str

def is_other_case(text):
    text_lower = text.lower()
    if any(kw in text_lower for kw in EXCLUDE_KEYWORDS):
        return True
    m_money = re.findall(r'(\d[\d\s]*)(?:€|eur)', text_lower)
    for m in m_money:
        val = int(m.replace(' ', ''))
        if val > 100000:
            return True
    return False

# Dictionnaire d'anonymisation des tokens (ordonné et exempt de double-remplacement)
tokens_anonyme = {
    "Sébastien GRAZIDE": "**[La Victime]**",
    "Sébastien Grazide": "**[La Victime]**",
    "GRAZIDE": "**[La Victime]**",
    "Grazide": "**[La Victime]**",
    "Sébastien": "**[La Victime]**",
    "Mountasser SABIR": "**[Le Président de l'Exploitation]**",
    "Mountasser Sabir": "**[Le Président de l'Exploitation]**",
    "SABIR": "**[Le Président de l'Exploitation]**",
    "Sabir": "**[Le Président de l'Exploitation]**",
    "Sabir MOUNTASSER": "**[Le Président de l'Exploitation]**",
    "Sabir Mountasser": "**[Le Président de l'Exploitation]**",
    "MOUNTASSER": "**[Le Président de l'Exploitation]**",
    "Mountasser": "**[Le Président de l'Exploitation]**",
    "Catherine ANDISSAC": "**[La Directrice Générale de l'Exploitation]**",
    "Catherine Andissac": "**[La Directrice Générale de l'Exploitation]**",
    "ANDISSAC": "**[La Directrice Générale de l'Exploitation]**",
    "Andissac": "**[La Directrice Générale de l'Exploitation]**",
    "ADUSSAC": "**[La Directrice Générale de l'Exploitation]**", 
    "Adussac": "**[La Directrice Générale de l'Exploitation]**",
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
    "Dr Yogan OXYBEL": "**[Le Médecin Généraliste]**",
    "Dr Yogan Oxybel": "**[Le Médecin Généraliste]**",
    "Dr Oxybel": "**[Le Médecin Généraliste]**",
    "Oxybel": "**[Le Médecin Généraliste]**",
    "OXYBEL": "**[Le Médecin Généraliste]**",
    "Yogan": "**[Le Médecin Généraliste]**",
    "Dr Roland GAU": "**[L'Anesthésiste de l'Établissement]**",
    "Dr Roland Gau": "**[L'Anesthésiste de l'Établissement]**",
    "Roland GAU": "**[L'Anesthésiste de l'Établissement]**",
    "Roland Gau": "**[L'Anesthésiste de l'Établissement]**",
    "Sigrid DESBOIS": "**[La Gestionnaire CPAM]**",
    "Sigrid Desbois": "**[La Gestionnaire CPAM]**",
    "DESBOIS": "**[La Gestionnaire CPAM]**",
    "Desbois": "**[La Gestionnaire CPAM]**",
    "SAS LES MAUVAIS GARCONS": "**[L'Exploitant du Commerce (La SAS)]**",
    "SAS LES MAUVAIS GARÇONS": "**[L'Exploitant du Commerce (La SAS)]**",
    "LES MAUVAIS GARÇONS": "**[L'Exploitant du Commerce (La SAS)]**",
    "LES MAUVAIS GARCONS": "**[L'Exploitant du Commerce (La SAS)]**",
    "Salon Les Mauvais Garçons": "**[L'Exploitant du Commerce (La SAS)]**",
    "Salon Les Mauvais Garcons": "**[L'Exploitant du Commerce (La SAS)]**",
    "Les Mauvais Garçons": "**[L'Exploitant du Commerce (La SAS)]**",
    "Les Mauvais Garcons": "**[L'Exploitant du Commerce (La SAS)]**",
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
    "J. Milas": "**[L'Officier de Police Judiciaire]**", 
    "Milas": "**[L'Officier de Police Judiciaire]**",
}

def clean_and_anonymize(val):
    if not isinstance(val, str):
        return val
    # Remplacer "Arr9t" par "Arrêt"
    val = val.replace("Arr9t", "Arrêt")
    
    # Remplacements ciblés
    for old in sorted(tokens_anonyme.keys(), key=len, reverse=True):
        val = re.sub(r'\b' + re.escape(old) + r'\b', tokens_anonyme[old], val)
        val = val.replace(old, tokens_anonyme[old])
    val = re.sub(r'\b(Monsieur|Madame|M\.|Mme|Dr|Docteur|Maître)\s+(?=\*\*\[)', '', val)
    val = val.replace('****', '**')
    
    # Correction d'un double remplacement éventuel du médecin généraliste
    val = val.replace('**[Le Médecin Généraliste]** **[Le Médecin Généraliste]**', '**[Le Médecin Généraliste]**')
    val = val.replace('**[Le Médecin Généraliste]****[Le Médecin Généraliste]**', '**[Le Médecin Généraliste]**')
    return val

# Traiter les 25 lignes d'origine de dest_rows
deleted_other_case = 0
duplicates_removed = 0

for r in dest_rows:
    fields_to_check = [r['Evt'], r['Desc'], r['Emetteur'], r['Destinataire'], r['Portee'], r['Montant']]
    if any(is_other_case(f) for f in fields_to_check) or '2010' in r['DateHeure']:
        deleted_other_case += 1
        continue
    
    parsed_dt = parse_date(r['DateHeure'])
    
    cat = r['Cat']
    # Correction stricte de la catégorie de jurisprudence
    if 'arrêt (jurisprudence)' in r['Evt'].lower():
        cat = "Jurisprudence"
        
    r_clean = {
        'Id': r['Id'],
        'DateHeure': parsed_dt,
        'Evt': clean_and_anonymize(r['Evt']),
        'Cat': cat,
        'Emetteur': clean_and_anonymize(r['Emetteur']),
        'Destinataire': clean_and_anonymize(r['Destinataire']),
        'Desc': clean_and_anonymize(r['Desc']),
        'Montant': clean_and_anonymize(r['Montant']),
        'ITT': r['ITT'],
        'RefPiece': clean_and_anonymize(r['RefPiece']),
        'Portee': clean_and_anonymize(r['Portee']),
        'LienGDrive': r['LienGDrive'],
        'Statut': r['Statut']
    }
    
    date_day = parsed_dt.split(' ')[0]
    seen_key = (date_day, r_clean['Evt'].lower())
    seen_keys.add(seen_key)
    final_list.append(r_clean)

# Traiter les nouvelles lignes de new_rows
max_evt = max([int(r['Id'].split('-')[1]) for r in final_list if r['Id'].startswith('EVT-')])
max_cor = max([int(r['Id'].split('-')[1]) for r in final_list if r['Id'].startswith('COR-')])

new_added = 0
for r in new_rows:
    fields_to_check = [r['Evt'], r['Desc'], r['Emetteur'], r['Destinataire'], r['Portee'], r['Montant']]
    if any(is_other_case(f) for f in fields_to_check) or '2010' in r['DateHeure'] or '2012' in r['DateHeure'] or '2013' in r['DateHeure'] or '2016' in r['DateHeure'] or '2019' in r['DateHeure'] or '2022' in r['DateHeure']:
        deleted_other_case += 1
        continue
    
    parsed_dt = parse_date(r['DateHeure'])
    
    cat = r['Cat']
    # Correction stricte de la catégorie de jurisprudence
    is_juris = 'arrêt (jurisprudence)' in r['Evt'].lower() or 'arr9t' in r['Evt'].lower() or cat == 'Jurisprudence'
    if is_juris:
        cat = "Jurisprudence"
        
    r_clean = {
        'Id': r.get('Id', ''),
        'DateHeure': parsed_dt,
        'Evt': clean_and_anonymize(r['Evt']),
        'Cat': cat,
        'Emetteur': clean_and_anonymize(r['Emetteur']),
        'Destinataire': clean_and_anonymize(r['Destinataire']),
        'Desc': clean_and_anonymize(r['Desc']),
        'Montant': clean_and_anonymize(r['Montant']),
        'ITT': r['ITT'],
        'RefPiece': clean_and_anonymize(r['RefPiece']),
        'Portee': clean_and_anonymize(r['Portee']),
        'LienGDrive': r['LienGDrive'],
        'Statut': r['Statut']
    }
    
    if not is_juris and '2026' not in r_clean['DateHeure'] and r_clean['DateHeure'] != 'Non précisé':
        deleted_other_case += 1
        continue
        
    date_day = parsed_dt.split(' ')[0]
    
    # Stratégie de dédoublonnement renforcée
    is_dup = False
    for u in final_list:
        u_day = u['DateHeure'].split(' ')[0]
        if u_day == date_day:
            if u['Evt'].lower() == r_clean['Evt'].lower() or r_clean['Evt'].lower() in u['Evt'].lower() or u['Evt'].lower() in r_clean['Evt'].lower():
                is_dup = True
                break
            if ('wero' in r_clean['Evt'].lower() or 'remboursement' in r_clean['Evt'].lower()) and ('wero' in u['Evt'].lower() or 'remboursement' in u['Evt'].lower()):
                is_dup = True
                break
            if ('accident' in r_clean['Evt'].lower()) and ('accident' in u['Evt'].lower()):
                is_dup = True
                break
            if ('urgence' in r_clean['Evt'].lower()) and ('urgence' in u['Evt'].lower() or 'jardon' in u['Desc'].lower()):
                is_dup = True
                break
            if ('chirurg' in r_clean['Evt'].lower() or 'bloc' in r_clean['Evt'].lower()) and ('chirurg' in u['Evt'].lower() or 'bloc' in u['Evt'].lower()):
                is_dup = True
                break
            if ('consultation' in r_clean['Evt'].lower() or 'anesthésie' in r_clean['Evt'].lower()) and ('consultation' in u['Evt'].lower() or 'anesthésie' in u['Evt'].lower() or 'gau' in u['Emetteur'].lower() or 'oxybel' in u['Emetteur'].lower()):
                is_dup = True
                break
            if ('frais' in r_clean['Evt'].lower() or 'séjour' in r_clean['Evt'].lower() or 'versements' in r_clean['Evt'].lower()) and ('séjour' in u['Evt'].lower() or 'prestations' in u['Evt'].lower()):
                is_dup = True
                break
            if ('plainte' in r_clean['Evt'].lower()) and ('plainte' in u['Evt'].lower()):
                is_dup = True
                break
            if ('recours' in r_clean['Evt'].lower() or 'sinistre' in r_clean['Evt'].lower()) and ('recours' in u['Evt'].lower() or 'sinistre' in u['Evt'].lower() or 'déclaration d\'accident' in u['Evt'].lower()):
                is_dup = True
                break
            if ('arrêt de travail' in r_clean['Evt'].lower()) and ('arrêt' in u['Evt'].lower() or 'itt' in u['Evt'].lower()):
                is_dup = True
                break
            if ('rééducation' in r_clean['Evt'].lower() or 'kiné' in r_clean['Evt'].lower()) and ('rééducation' in u['Evt'].lower() or 'kiné' in u['Evt'].lower()):
                is_dup = True
                break
            if ('transmission' in r_clean['Evt'].lower() or 'envoi' in r_clean['Evt'].lower()) and ('transmission' in u['Evt'].lower() or 'envoi' in u['Evt'].lower() or 'email' in u['Evt'].lower()):
                is_dup = True
                break
            if ('expertise' in r_clean['Evt'].lower() or 'examen médical' in r_clean['Evt'].lower()) and ('expertise' in u['Evt'].lower() or 'examen médical' in u['Evt'].lower()):
                is_dup = True
                break
                
    if is_dup:
        duplicates_removed += 1
        continue
        
    is_cor = 'mise en demeure' in r_clean['Evt'].lower() or 'courrier' in r_clean['Evt'].lower() or 'transmission' in r_clean['Evt'].lower() or 'envoi' in r_clean['Evt'].lower() or 'action directe' in r_clean['Evt'].lower() or r_clean['Cat'] == 'Correspondance'
    if is_cor:
        max_cor += 1
        r_clean['Id'] = f"COR-{max_cor:02d}"
    else:
        max_evt += 1
        r_clean['Id'] = f"EVT-{max_evt:02d}"
        
    final_list.append(r_clean)
    new_added += 1

# Rétablir EVT-01 s'il a été écrasé ou supprimé par dédoublonnement
evt_01_exists = any(r['Id'] == 'EVT-01' for r in final_list)
if not evt_01_exists:
    print("EVT-01 manquant. Restauration d'EVT-01...")
    evt_01_orig = [r for r in dest_rows if r['Id'] == 'EVT-01'][0]
    evt_01_clean = {
        'Id': 'EVT-01',
        'DateHeure': parse_date(evt_01_orig['DateHeure']),
        'Evt': clean_and_anonymize(evt_01_orig['Evt']),
        'Cat': evt_01_orig['Cat'],
        'Emetteur': clean_and_anonymize(evt_01_orig['Emetteur']),
        'Destinataire': clean_and_anonymize(evt_01_orig['Destinataire']),
        'Desc': clean_and_anonymize(evt_01_orig['Desc']),
        'Montant': clean_and_anonymize(evt_01_orig['Montant']),
        'ITT': evt_01_orig['ITT'],
        'RefPiece': clean_and_anonymize(evt_01_orig['RefPiece']),
        'Portee': clean_and_anonymize(evt_01_orig['Portee']),
        'LienGDrive': evt_01_orig['LienGDrive'],
        'Statut': evt_01_orig['Statut']
    }
    final_list = [r for r in final_list if r['Id'] != 'EVT-19']
    final_list.append(evt_01_clean)

# Double vérification pour forcer les catégories non-jurisprudence sur les arrêts de travail, courriers, etc.
for r in final_list:
    is_real_juris = 'arrêt (jurisprudence)' in r['Evt'].lower() or r['Cat'] == 'Jurisprudence'
    if 'arrêt de travail' in r['Evt'].lower() or 'envoi' in r['Evt'].lower() or 'lrar' in r['Evt'].lower() or 'consultation' in r['Evt'].lower():
        is_real_juris = False
        
    if is_real_juris:
        r['Cat'] = "Jurisprudence"
    else:
        # Correction des résidus cosmétiques :
        # - EVT-26 (Information sur les droits des victimes) -> Procédure
        # - EVT-42 (Frais justice 475-1 / Condamnation) -> Procédure
        if r['Id'] in ['EVT-26', 'EVT-42'] or 'droits des victimes' in r['Evt'].lower() or 'indemnisation (frais de justice)' in r['Evt'].lower() or 'frais de justice' in r['Evt'].lower() or '475-1' in r['Desc'].lower():
            r['Cat'] = "Procédure"
        elif r['Id'] == 'EVT-28' or 'démarche administrative' in r['Evt'].lower():
            r['Cat'] = "Procédure"
        else:
            orig_cat = None
            for dr in dest_rows:
                if dr['Id'] == r['Id']:
                    orig_cat = dr['Cat']
                    break
            if orig_cat:
                r['Cat'] = orig_cat
            else:
                if 'lrar' in r['Evt'].lower() or 'envoi' in r['Evt'].lower() or 'courrier' in r['Evt'].lower() or r['Id'].startswith('COR-'):
                    r['Cat'] = "Correspondance"
                else:
                    r['Cat'] = "Médical" if r['Id'].startswith('EVT-') else "Procédure"

# Trier chronologiquement de façon stricte
def get_sort_key(r):
    dt_str = r['DateHeure'].strip()
    is_juris = r['Cat'] == "Jurisprudence"
    
    if dt_str == "Non précisé":
        return (0 if is_juris else 1, 9999, 12, 31, 23, 59)
        
    m = re.search(r'(\d{4})$', dt_str.split(' ')[0])
    year = int(m.group(1)) if m else 9999
    
    m2 = re.search(r'^(\d{2})/(\d{2})/', dt_str)
    day = int(m2.group(1)) if m2 else 1
    month = int(m2.group(2)) if m2 else 1
    
    hour = 0
    minute = 0
    m_time = re.search(r'\s+(\d{2}):(\d{2})', dt_str)
    if m_time:
        hour = int(m_time.group(1))
        minute = int(m_time.group(2))
        
    juris_val = 0 if is_juris else 1
    
    return (juris_val, year, month, day, hour, minute)

final_sorted = sorted(final_list, key=get_sort_key)

# 4. Écrire dans le Google Sheet cible via l'API Sheets
spreadsheet_id = "1q-7Ag9zEBR_h27yonvIqypJqqp58fow6GyHEUNBsVAc"
sheet_name = "@"

values = [
    [
        r['Id'],
        r['DateHeure'],
        r['Evt'],
        r['Cat'],
        r['Emetteur'],
        r['Destinataire'],
        r['Desc'],
        r['Montant'],
        r['ITT'],
        r['RefPiece'],
        r['Portee'],
        r['LienGDrive'],
        r['Statut']
    ] for r in final_sorted
]

header = [
    "N° Événement",
    "Date & Heure",
    "Événement / Acte",
    "Catégorie",
    "Émetteur",
    "Destinataire",
    "Description Détaillée / Synthèse",
    "Montant Financier (EUR)",
    "Période d'Arrêt (ITT)",
    "Numéro de Suivi / Réf. Pièce",
    "Portée Juridique & Application",
    "Lien GDrive",
    "Statut / Échéance"
]

body = {
    'values': [header] + values
}

service = get_drive_service()
sheets = discovery.build('sheets', 'v4', credentials=service._http.credentials)

print("Vidage de la feuille cible...")
sheets.spreadsheets().values().clear(
    spreadsheetId=spreadsheet_id,
    range=f"'{sheet_name}'!A1:M300"
).execute()

print(f"Écriture de {len(final_sorted)} lignes triées...")
sheets.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range=f"'{sheet_name}'!A1",
    valueInputOption="USER_ENTERED",
    body=body
).execute()

print(f"Lignes totales écrites: {len(final_sorted)}")
print(f"Lignes supprimées (autre affaire): {deleted_other_case}")
print(f"Doublons supprimés: {duplicates_removed}")

# Sauvegarder dans scratch_master_final.json
with open('data/scratch/scratch_master_final.json', 'w') as f:
    json.dump(final_sorted, f, indent=2)
