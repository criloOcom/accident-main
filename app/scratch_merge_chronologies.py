import json
import re
import sys
import os
from googleapiclient import discovery

# Insérer le dossier 'app' dans le sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drive_auth import get_drive_service

def main():
    print("Début de la synchronisation de la chronologie unifiée...")
    
    # 1. Charger les fichiers sources intermédiaires
    with open('data/scratch/scratch_dest_rows.json') as f:
        dest_rows = json.load(f)
    with open('data/scratch/scratch_final_new_rows.json') as f:
        new_rows = json.load(f)

    # 2. Re-déduire les doublons avec logique renforcée
    final_list = []
    for r in dest_rows:
        final_list.append({
            'DateHeure': r['DateHeure'].strip(),
            'Evt': r['Evt'].strip(),
            'Cat': r['Cat'].strip(),
            'Emetteur': r['Emetteur'].strip(),
            'Destinataire': r['Destinataire'].strip(),
            'Desc': r['Desc'].strip(),
            'Montant': r['Montant'].strip(),
            'ITT': r['ITT'].strip(),
            'RefPiece': r['RefPiece'].strip(),
            'Portee': r['Portee'].strip(),
            'LienGDrive': r['LienGDrive'].strip(),
            'Statut': r['Statut'].strip()
        })

    def normalize_date_to_key(dt):
        dt = dt.strip()
        m_yyyy = re.search(r'^(\d{4})-(\d{2})-(\d{2})', dt)
        if m_yyyy:
            return f"{m_yyyy.group(1)}-{m_yyyy.group(2)}-{m_yyyy.group(3)}"
        m_std = re.search(r'(\d{2})[/-](\d{2})[/-](\d{4})', dt)
        if m_std:
            return f"{m_std.group(3)}-{m_std.group(2)}-{m_std.group(1)}"
        return dt

    added_rows = []
    for idx, r in enumerate(new_rows):
        dt = r['DateHeure'].strip()
        evt = r['Evt'].strip()
        desc = r['Desc'].strip()
        norm_date_r = normalize_date_to_key(dt)
        
        is_duplicate = False
        
        # Filtrer l'accident de jambe de M. U (2010-2024)
        if 'prothèse' in desc.lower() or 'jambe' in desc.lower() or 'amputation' in desc.lower() or 'rente' in desc.lower() or 'logement adapté' in desc.lower() or 'fauteuil' in desc.lower():
            is_duplicate = True
        if '2010' in dt or '2012' in dt or '2013' in dt or '2014' in dt or '2016' in dt or '2019' in dt or '2021' in dt or '2022' in dt or '2024' in dt:
            if 'arrêt' not in evt.lower() and 'arr9t' not in evt.lower() and 'jurisprudence' not in evt.lower():
                is_duplicate = True
        if 'm. u' in desc.lower() or 'm. u' in evt.lower() or 'domofrance' in desc.lower():
            is_duplicate = True
        if 'arrêt de la cour de cassation' in evt.lower() or 'arrêt de la cour d\'appel' in evt.lower() or 'arrêt de cour d\'appel' in evt.lower():
            is_duplicate = True

        # Filtrer sur les dates critiques pour éviter les doublons redondants avec la destination existante
        critical_dates = ['2026-05-29', '2026-05-30', '2026-06-01', '2026-06-02', '2026-06-03', '2026-06-12', '2026-06-23', '2026-06-24',
                          '29/05/2026', '30/05/2026', '01/06/2026', '02/06/2026', '03/06/2026', '12/06/2026', '23/06/2026', '24/06/2026']
        
        if not is_duplicate and any(cd in dt or cd in norm_date_r for cd in critical_dates):
            for u in final_list:
                u_dt = u['DateHeure'].strip()
                u_evt = u['Evt'].strip()
                u_desc = u['Desc'].strip()
                norm_date_u = normalize_date_to_key(u_dt)
                
                if norm_date_r[:10] == norm_date_u[:10]:
                    if ('chirurg' in evt.lower() or 'bloc' in evt.lower()) and ('chirurg' in u_evt.lower() or 'bloc' in u_evt.lower()):
                        is_duplicate = True
                        break
                    if ('accident' in evt.lower() or 'blessure' in evt.lower()) and ('accident' in u_evt.lower() or 'blessure' in u_evt.lower()):
                        is_duplicate = True
                        break
                    if ('wero' in evt.lower() or 'remboursement' in evt.lower()) and ('wero' in u_evt.lower() or 'remboursement' in u_evt.lower()):
                        is_duplicate = True
                        break
                    if 'plainte' in evt.lower() and 'plainte' in u_evt.lower():
                        is_duplicate = True
                        break
                    if ('arrêt' in evt.lower() or 'itt' in evt.lower()) and ('arrêt' in u_evt.lower() or 'itt' in u_evt.lower()):
                        is_duplicate = True
                        break
                    if ('cpam' in evt.lower() or 'recours' in evt.lower()) and ('cpam' in u_evt.lower() or 'recours' in u_evt.lower()):
                        is_duplicate = True
                        break
                    if ('urgence' in evt.lower() or 'jardon' in evt.lower()) and ('urgence' in u_evt.lower() or 'jardon' in u_evt.lower()):
                        is_duplicate = True
                        break
                    if 'kiné' in evt.lower() and 'kiné' in u_evt.lower():
                        is_duplicate = True
                        break
                        
        if not is_duplicate:
            for u in final_list:
                u_dt = u['DateHeure'].strip()
                u_evt = u['Evt'].strip()
                u_desc = u['Desc'].strip()
                norm_date_u = normalize_date_to_key(u_dt)
                
                if norm_date_r == norm_date_u or (len(norm_date_r) >= 10 and len(norm_date_u) >= 10 and norm_date_r[:10] == norm_date_u[:10]):
                    if u_evt.lower() == evt.lower() or evt.lower() in u_evt.lower() or u_evt.lower() in evt.lower():
                        is_duplicate = True
                        break
                    if u_desc[:30].lower() == desc[:30].lower() or desc[:20].lower() in u_desc.lower():
                        is_duplicate = True
                        break

        if not is_duplicate:
            final_list.append(r)
            added_rows.append(r)

    # 3. Re-générer la chronologie triée et ré-indexée
    combined_rows = []
    for r in dest_rows:
        combined_rows.append({
            'Id': r['Id'],
            'DateHeure': r['DateHeure'].strip(),
            'Evt': r['Evt'].strip(),
            'Cat': r['Cat'].strip(),
            'Emetteur': r['Emetteur'].strip(),
            'Destinataire': r['Destinataire'].strip(),
            'Desc': r['Desc'].strip(),
            'Montant': r['Montant'].strip(),
            'ITT': r['ITT'].strip(),
            'RefPiece': r['RefPiece'].strip(),
            'Portee': r['Portee'].strip(),
            'LienGDrive': r['LienGDrive'].strip(),
            'Statut': r['Statut'].strip()
        })

    for idx, r in enumerate(added_rows):
        combined_rows.append({
            'Id': f"NEW-{idx+1:03d}",
            'DateHeure': r['DateHeure'].strip(),
            'Evt': r['Evt'].strip(),
            'Cat': r['Cat'].strip(),
            'Emetteur': r['Emetteur'].strip(),
            'Destinataire': r['Destinataire'].strip(),
            'Desc': r['Desc'].strip(),
            'Montant': r['Montant'].strip(),
            'ITT': r['ITT'].strip(),
            'RefPiece': r['RefPiece'].strip(),
            'Portee': r['Portee'].strip(),
            'LienGDrive': r['LienGDrive'].strip(),
            'Statut': r['Statut'].strip()
        })

    months_fr = {
        'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
        'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
        'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
    }

    def get_sort_key_combined(r):
        dt_str = r['DateHeure'].strip()
        if not dt_str or 'non précisé' in dt_str.lower() or 'non spécifié' in dt_str.lower() or 'à l\'audience' in dt_str.lower() or 'non précisée' in dt_str.lower():
            return (9999, 12, 31, 23, 59)
        m_yyyy = re.search(r'^(\d{4})-(\d{2})-(\d{2})', dt_str)
        if m_yyyy:
            year = int(m_yyyy.group(1))
            month = int(m_yyyy.group(2))
            day = int(m_yyyy.group(3))
            hour = 0
            minute = 0
            m_time = re.search(r'(\d{2}):(\d{2})', dt_str)
            if m_time:
                hour = int(m_time.group(1))
                minute = int(m_time.group(2))
            return (year, month, day, hour, minute)
        m_std = re.search(r'(\d{2})[/-](\d{2})[/-](\d{4})', dt_str)
        if m_std:
            day = int(m_std.group(1))
            month = int(m_std.group(2))
            year = int(m_std.group(3))
            hour = 0
            minute = 0
            m_time = re.search(r'(\d{2})[h:](\d{2})', dt_str)
            if m_time:
                hour = int(m_time.group(1))
                minute = int(m_time.group(2))
            priority = 1
            if 'préalablement' in dt_str.lower():
                priority = 0
            elif 'avant' in dt_str.lower():
                priority = 0.5
            return (year, month, day, hour, minute, priority)
        m_month_str = re.search(r'(\d{1,2})?\s*([a-zéûâô]+)\s*(\d{4})', dt_str.lower())
        if m_month_str:
            day = int(m_month_str.group(1)) if m_month_str.group(1) else 1
            month_name = m_month_str.group(2)
            year = int(m_month_str.group(3))
            month = 1
            for m_fr, m_num in months_fr.items():
                if m_fr in month_name:
                    month = int(m_num)
                    break
            return (year, month, day, 0, 0, 1)
        m_year = re.search(r'(\d{4})', dt_str)
        if m_year:
            return (int(m_year.group(1)), 1, 1, 0, 0, 2)
        return (9999, 12, 31, 23, 59, 3)

    sorted_combined = sorted(combined_rows, key=get_sort_key_combined)

    evt_counter = 1
    cor_counter = 1
    final_sorted_rows = []
    for r in sorted_combined:
        is_cor = 'mise en demeure' in r['Evt'].lower() or 'courrier' in r['Evt'].lower() or 'transmission' in r['Evt'].lower() or 'envoi' in r['Evt'].lower() or 'action directe' in r['Evt'].lower() or r['Cat'] == 'Correspondance'
        
        if is_cor:
            r['Id'] = f"COR-{cor_counter:02d}"
            cor_counter += 1
        else:
            r['Id'] = f"EVT-{evt_counter:02d}"
            evt_counter += 1
        final_sorted_rows.append(r)

    # 4. Écrire dans le Google Sheet cible via l'API Sheets
    spreadsheet_id = "1q-7Ag9zEBR_h27yonvIqypJqqp58fow6GyHEUNBsVAc"
    sheet_name = "@"
    
    # Préparer la structure matricielle des valeurs pour l'insertion
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
        ] for r in final_sorted_rows
    ]
    
    # L'en-tête de la table de destination
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
    
    # Vider le contenu précédent de l'onglet @
    print("Vidage de la feuille cible...")
    sheets.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A1:M300"
    ).execute()
    
    # Écrire les nouvelles valeurs consolidées
    print(f"Écriture de {len(final_sorted_rows)} lignes triées...")
    sheets.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_name}'!A1",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

    print("Consolidation terminée avec succès !")

if __name__ == '__main__':
    main()
