#!/usr/bin/env python3
"""
sync_reel_gdocs.py — Réciprocité totale strate Réelle ↔ Google Docs.

Pour CHAQUE fichier .md de Actes/Reel/ :
  1. Cherche `reel_drive_id` dans le YAML (Reel puis Token miroir).
  2. Si absent/invalide → crée le Google Doc (conversion markdown native Drive)
     dans le dossier Drive « Accident Main - Docs Reel/ » (arborescence miroir),
     puis écrit `reel_drive_id` dans le YAML du fichier TOKEN miroir (Token-first,
     Règle #22) ET du fichier Reel (même valeur, cohérence immédiate).
  3. Si présent → met à jour le contenu du Google Doc depuis le .md Réel.

Le champ `drive_id` existant (qui pointe vers le Google Docs TOKENISÉ) n'est
JAMAIS modifié. `generate_breadcrumbs.py` utilise `reel_drive_id` en priorité
pour l'émoji [📄] de la strate Réelle.

Usage :
  python3 .dev/app/sync_reel_gdocs.py            # dry-run
  python3 .dev/app/sync_reel_gdocs.py --apply    # crée/synchronise réellement
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.drive_auth import (  # noqa: E402
    get_credentials_from_adc,
    get_credentials_from_env,
    get_credentials_from_file,
    get_drive_service,
)
from googleapiclient.discovery import build  # noqa: E402
from googleapiclient.http import MediaIoBaseUpload  # noqa: E402

ROOT = "/home/crilocom/accident-main"
REEL_BASE = os.path.join(ROOT, "Actes", "Reel")
TOKEN_BASE = os.path.join(ROOT, "Actes", "Token")
DRIVE_ROOT_NAME = "Accident Main - Docs Reel"
VALID_ID = re.compile(r"^[A-Za-z0-9_-]{10,}$")
DOC_MIME = "application/vnd.google-apps.document"
FOLDER_MIME = "application/vnd.google-apps.folder"


def read_yaml_field(path, field):
    if not os.path.isfile(path):
        return None
    try:
        txt = open(path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", txt, re.DOTALL)
    if not m:
        return None
    fm = re.search(r"^" + re.escape(field) + r":\s*(.+?)\s*$", m.group(1), re.MULTILINE)
    return fm.group(1).strip().strip('"').strip("'") if fm else None


def set_yaml_field(path, field, value):
    """Ajoute/remplace un champ scalaire dans le frontmatter YAML. True si écrit."""
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?\n)---", txt, re.DOTALL)
    if not m:
        return False
    fm = m.group(1)
    line = f"{field}: {value}\n"
    if re.search(r"^" + re.escape(field) + r":", fm, re.MULTILINE):
        new_fm = re.sub(r"^" + re.escape(field) + r":.*$", line.rstrip("\n"), fm, flags=re.MULTILINE)
    else:
        new_fm = fm + line
    new_txt = txt[: m.start(1)] + new_fm + txt[m.end(1):]
    open(path, "w", encoding="utf-8").write(new_txt)
    return True


def find_or_create_folder(svc, name, parent_id, cache, dry):
    key = (parent_id, name)
    if key in cache:
        return cache[key]
    safe = name.replace("'", "\\'")
    q = f"name='{safe}' and mimeType='{FOLDER_MIME}' and trashed=false"
    if parent_id:
        q += f" and '{parent_id}' in parents"
    files = svc.files().list(q=q, fields="files(id)").execute().get("files", [])
    if files:
        cache[key] = files[0]["id"]
        return files[0]["id"]
    if dry:
        cache[key] = "DRY_RUN_FOLDER"
        return cache[key]
    body = {"name": name, "mimeType": FOLDER_MIME}
    if parent_id:
        body["parents"] = [parent_id]
    fid = svc.files().create(body=body, fields="id").execute()["id"]
    cache[key] = fid
    return fid


import time
from googleapiclient.errors import HttpError


def call_with_retry(fn, *args, max_retries=5, **kwargs):
    """Exécute une fonction d'API Google avec retry exponentiel en cas de rate limit (429)."""
    for attempt in range(max_retries):
        try:
            return fn(*args, **kwargs)
        except HttpError as e:
            if e.resp.status == 429 and attempt < max_retries - 1:
                wait_time = (2 ** attempt) + 1
                time.sleep(wait_time)
            else:
                raise


def extract_and_clean_footnotes(txt: str):
    """
    1. Extrait les définitions de footnotes [^nX]: ... du markdown source.
    2. Purge le bloc ## Sources Législation et les définitions de footnotes en bas de page.
    3. Remplace les appels [^nX] dans le corps par [[FOOTNOTE_key]].
    4. Nettoie le contenu des footnotes : enlève blockquotes (>), citations complètes,
       garde SEULEMENT le lien Légifrance cliquable "Titre — URL".
    Retourne (txt_clean, footnote_map).
    """
    footnote_map = {}
    
    # Pattern pour capturer le tag [^key]: et son contenu (jusqu'au prochain [^...] ou section # ou fin)
    fn_def_pattern = re.compile(r"^(?:<!--\s*Source\s*-->\s*)?\[\^([a-zA-Z0-9_-]+)\]:\s*(.*?)(?=\n\[\^|\n<!--|\n#|\Z)", re.MULTILINE | re.DOTALL)
    for m in fn_def_pattern.finditer(txt):
        key = m.group(1)
        content = m.group(2).strip()
        
        # Chercher TOUS les liens [Titre](URL) dans le contenu
        links = re.findall(r"\[(.*?)\]\((https?://.*?)\)", content)
        if links:
            # Garder SEULEMENT le premier lien Légifrance (le plus pertinent)
            # Filtrer pour legifrance.gouv.fr en priorité
            legifrance_links = [(t, u) for t, u in links if "legifrance.gouv.fr" in u]
            if legifrance_links:
                title, url = legifrance_links[0]
            else:
                title, url = links[0]
            # Nettoyer le titre : enlever le nom du code s'il est redondant
            # Ex: "Article L2212-2 du Code général des collectivités territoriales" -> "Article L2212-2"
            clean_title = re.sub(r"\s+du\s+Code\s+[^.]+$", "", title, flags=re.IGNORECASE)
            clean_text = f"{clean_title} — {url}"
        else:
            # Pas de lien : nettoyer le contenu brut (enlever blockquotes, guillemets, etc.)
            clean_content = re.sub(r"^\s*>\s*", "", content, flags=re.MULTILINE)  # enlever > en début de ligne
            clean_content = re.sub(r"[>#*«»]", "", clean_content)  # enlever caractères résiduels
            clean_content = re.sub(r"\s+", " ", clean_content).strip()
            clean_text = clean_content[:150]
            
        footnote_map[key] = clean_text

    # Purger la section ## Sources Législation et les définitions
    txt = re.sub(r"<!--\s*Source\s*-->.*?<!--\s*/Source\s*-->", "", txt, flags=re.DOTALL | re.IGNORECASE)
    txt = re.sub(r"<hr>\s*<hr>\s*##\s*SOURCES?\s*LÉGISLATION.*$", "", txt, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE)
    txt = re.sub(r"##\s*SOURCES?\s*LÉGISLATION.*$", "", txt, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE)
    txt = re.sub(r"^\[\^([a-zA-Z0-9_-]+)\]:\s*.*$", "", txt, flags=re.MULTILINE)

    # Remplacer les appels de footnotes dans le corps par [[FOOTNOTE_key]]
    for key in footnote_map.keys():
        txt = txt.replace(f"[^{key}]", f"[[FOOTNOTE_{key}]]")
        
    return txt, footnote_map


def clean_markdown_for_gdocs(txt: str, reel_path: str = None):
    """Purge le bloc YAML frontmatter, le fil d'Ariane, la section Sources Législation, les icônes 📚 et flèches ↩."""
    txt, fn_map = extract_and_clean_footnotes(txt)
    # 1. Purger le bloc YAML frontmatter au début (--- ... ---)
    txt = re.sub(r"^---\s*\n.*?\n---\s*\n?", "", txt, flags=re.DOTALL)
    # 2. Purger le bloc fil d'Ariane (<!-- Breadcrumb --> ... <!-- /Breadcrumb -->) et les <hr> éventuels qui suivent
    txt = re.sub(r"<!-- Breadcrumb -->.*?<!-- /Breadcrumb -->\s*(<hr>\s*)?", "", txt, flags=re.DOTALL)
    # 3. Purger toute ligne de fil d'Ariane Markdown non balisée (*[🏠...)
    txt = re.sub(r"^\*?\[?🏠.*?\n", "", txt, flags=re.MULTILINE)
    # 4. Purger les références de bibliothèque locale et flèches de retour ↩
    txt = re.sub(r"📚 Bibliothèque locale :.*?↩\n?", "", txt)
    txt = re.sub(r"\s*\[📚\]\(.*?\)", "", txt)
    txt = re.sub(r"↩", "", txt)
    # 4b. Purger le bloc Source Google Drive et le bloc d'exploitant obsolète
    txt = re.sub(r"^\s*>\s*🔗\s*Source\s*Google\s*Drive\s*:.*?\n", "", txt, flags=re.MULTILINE | re.IGNORECASE)
    txt = re.sub(r"^\s*>\s*\*\*Mise à jour — Identification du véritable exploitant :\*\*.*?\n\n?", "", txt, flags=re.MULTILINE | re.DOTALL)
    # 4b-bis. Masquer les mentions de pièce originale (🔒 PIÈCE ORIGINALE...)
    txt = re.sub(r"^\s*🔒\s*PIÈCE ORIGINALE.*$\n?", "", txt, flags=re.MULTILINE)
    # 4c. Transmutation des hyperliens Markdown : liens relatifs .md vers Drive/Docs ou texte brut
    def sanitize_link(m):
        text, url = m.group(1), m.group(2)
        if re.match(r"^(https?://(drive\.google\.com|www\.legifrance\.gouv\.fr|judilibre\.juridiction\.fr)|mailto:)", url, re.I):
            return f"[{text}]({url})"
        
        if reel_path and (".md" in url or "Actes/" in url or "Memory/" in url or "Preuves_officielles/" in url):
            base_dir = os.path.dirname(reel_path)
            clean_url_path = url.split("#")[0]
            target_abs = os.path.normpath(os.path.join(base_dir, clean_url_path))
            
            if os.path.isfile(target_abs):
                target_id = read_yaml_field(target_abs, "reel_drive_id") or read_yaml_field(target_abs, "drive_id")
                if target_id and VALID_ID.match(target_id):
                    if "Preuves_officielles" in target_abs:
                        return f"[{text}](https://drive.google.com/open?id={target_id})"
                    else:
                        return f"[{text}](https://docs.google.com/document/d/{target_id}/edit)"
        return text

    txt = re.sub(r"\[(.*?)\]\((.*?)\)", sanitize_link, txt)
    # 5. Convertir les sauts de page <hr><hr> en marqueur [[PAGE_BREAK]] pour l'API Docs
    txt = re.sub(r"<hr>\s*<hr>", "\n\n[[PAGE_BREAK]]\n\n", txt, flags=re.IGNORECASE)
    # 6. Convertir les intitulés de titres (#, ##, ###) en MAJUSCULES
    txt = re.sub(r'^(#{1,3}\s+)(.+)$', lambda m: m.group(1) + m.group(2).upper(), txt, flags=re.MULTILINE)
    # 7. Nettoyer les sauts de ligne initiaux
    txt = txt.lstrip("\n")
    return txt, fn_map


def md_media(path):
    raw_txt = open(path, encoding="utf-8").read()
    clean_txt, fn_map = clean_markdown_for_gdocs(raw_txt, reel_path=path)
    data = clean_txt.encode("utf-8")
    return MediaIoBaseUpload(io.BytesIO(data), mimetype="text/markdown", resumable=False), fn_map


def replace_page_break_markers(docs_svc, doc_id):
    """Post-traitement API Google Docs : remplace les marqueurs [[PAGE_BREAK]] par de vrais sauts de page (insertPageBreak)."""
    try:
        doc = call_with_retry(docs_svc.documents().get(documentId=doc_id).execute)
        content = doc.get("body", {}).get("content", [])
        markers = []
        for element in content:
            if "paragraph" in element:
                for pe in element["paragraph"].get("elements", []):
                    if "textRun" in pe:
                        text = pe["textRun"].get("content", "")
                        if "[[PAGE_BREAK]]" in text:
                            start_idx = pe.get("startIndex")
                            end_idx = pe.get("endIndex")
                            markers.append((start_idx, end_idx))
        if not markers:
            return
        # Remplacer chaque marqueur en partant de la fin pour ne pas invalider les index précédents
        for start_idx, end_idx in reversed(markers):
            try:
                requests = [
                    {"insertPageBreak": {"location": {"index": start_idx}}},
                    {"deleteContentRange": {"range": {"startIndex": start_idx + 1, "endIndex": end_idx + 1}}}
                ]
                call_with_retry(docs_svc.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute)
            except Exception:
                pass
    except Exception as e:
        print(f"    ⚠️ Erreur conversion saut de page sur {doc_id}: {e}")


def process_native_footnotes(docs_svc, doc_id, footnote_map):
    """
    Parcourt le corps du document Google Doc, trouve les marqueurs [[FOOTNOTE_key]],
    insère une Footnote native (createFootnote), remplit son segment avec le texte purifié
    et applique un formatage professionnel (8pt, JUSTIFIED, 0pt indentation).
    """
    if not footnote_map:
        return
        
    for key, note_text in footnote_map.items():
        marker_str = f"[[FOOTNOTE_{key}]]"
        try:
            doc = call_with_retry(docs_svc.documents().get(documentId=doc_id).execute)
            content = doc.get("body", {}).get("content", [])
            
            start_idx = None
            for element in content:
                if "paragraph" in element:
                    for pe in element["paragraph"].get("elements", []):
                        if "textRun" in pe and marker_str in pe["textRun"].get("content", ""):
                            t_content = pe["textRun"].get("content", "")
                            m_pos = t_content.find(marker_str)
                            start_idx = pe.get("startIndex") + m_pos
                            break
                if start_idx is not None:
                    break
                    
            if start_idx is None:
                continue
                
            req_create = {
                "requests": [
                    {"createFootnote": {"location": {"index": start_idx}}},
                    {"deleteContentRange": {"range": {"startIndex": start_idx + 1, "endIndex": start_idx + 1 + len(marker_str)}}}
                ]
            }
            res = call_with_retry(docs_svc.documents().batchUpdate(documentId=doc_id, body=req_create).execute)
            
            fn_id = None
            for reply in res.get("replies", []):
                if "createFootnote" in reply:
                    fn_id = reply["createFootnote"].get("footnoteId")
                    break
            if not fn_id:
                continue
                
            fn_url = None
            clean_note_text = note_text
            url_match = re.search(r"(https?://[^\s]+)", note_text)
            if url_match:
                fn_url = url_match.group(1)
                clean_note_text = re.sub(r"\s*—\s*https?://[^\s]+", "", note_text).strip()
                
            fn_reqs = [
                {"insertText": {"location": {"segmentId": fn_id, "index": 0}, "text": clean_note_text + "\n"}},
                {
                    "updateParagraphStyle": {
                        "range": {"segmentId": fn_id, "startIndex": 0, "endIndex": len(clean_note_text) + 1},
                        "paragraphStyle": {
                            "alignment": "START",
                            "indentStart": {"magnitude": 0, "unit": "PT"},
                            "indentFirstLine": {"magnitude": 0, "unit": "PT"},
                            "spaceAbove": {"magnitude": 2, "unit": "PT"},
                            "spaceBelow": {"magnitude": 2, "unit": "PT"}
                        },
                        "fields": "alignment,indentStart,indentFirstLine,spaceAbove,spaceBelow"
                    }
                },
                {
                    "updateTextStyle": {
                        "range": {"segmentId": fn_id, "startIndex": 0, "endIndex": len(clean_note_text)},
                        "textStyle": {
                            "fontSize": {"magnitude": 8, "unit": "PT"},
                            "foregroundColor": {"color": {"rgbColor": {"red": 0.1, "green": 0.3, "blue": 0.7}}} if fn_url else {"color": {"rgbColor": {"red": 0.2, "green": 0.2, "blue": 0.2}}},
                            "link": {"url": fn_url} if fn_url else {}
                        },
                        "fields": "fontSize,foregroundColor,link" if fn_url else "fontSize,foregroundColor"
                    }
                }
            ]
            call_with_retry(docs_svc.documents().batchUpdate(documentId=doc_id, body={"requests": fn_reqs}).execute)
        except Exception as ex:
            print(f"    ⚠️ Erreur insertion footnote {key} sur {doc_id}: {ex}")


def process_native_tables(docs_svc, doc_id, reel_path=None):
    """
    Détecte les tableaux Markdown originaux dans reel_path, localise leur équivalent
    texte brut dans le Google Doc via l'en-tête de colonne, puis le remplace par de vraies
    tables natives Google Docs (insertTable) avec cellules et liens Google Drive.
    """
    if not reel_path or not os.path.isfile(reel_path):
        return
        
    raw_md = open(reel_path, encoding="utf-8").read()
    
    md_tables = []
    lines = raw_md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and "|" in line[1:]:
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i].strip())
                i += 1
            if len(block) >= 2:
                rows = []
                for l in block:
                    if re.match(r"^\|[\s:-|-]+\|$", l):
                        continue
                    cells = [c.strip() for c in l.strip("|").split("|")]
                    if cells:
                        rows.append(cells)
                if rows:
                    md_tables.append(rows)
        else:
            i += 1
            
    if not md_tables:
        return

    try:
        doc = call_with_retry(docs_svc.documents().get(documentId=doc_id).execute)
        body_content = doc.get("body", {}).get("content", [])
        
        for raw_rows in md_tables:
            header_term = raw_rows[0][0] if raw_rows and raw_rows[0] else None
            if not header_term:
                continue
                
            clean_header_term = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", header_term)
            
            target_elem = None
            for elem in body_content:
                if "paragraph" in elem:
                    t = "".join(pe.get("textRun", {}).get("content", "") for pe in elem["paragraph"].get("elements", []))
                    if clean_header_term in t or "Pièce" in t or "DRIVE" in t or "CR opératoire" in t:
                        target_elem = elem
                        break
                        
            if not target_elem:
                continue
                
            start_idx = target_elem.get("startIndex")
            end_idx = target_elem.get("endIndex")
            
            num_rows = len(raw_rows)
            num_cols = max(len(r) for r in raw_rows)
            
            try:
                reqs = [
                    {"deleteContentRange": {"range": {"startIndex": start_idx, "endIndex": end_idx - 1}}},
                    {"insertTable": {"rows": num_rows, "columns": num_cols, "location": {"index": start_idx}}}
                ]
                call_with_retry(docs_svc.documents().batchUpdate(documentId=doc_id, body={"requests": reqs}).execute)
            except Exception:
                continue

            fresh_doc = call_with_retry(docs_svc.documents().get(documentId=doc_id).execute)
            fresh_body = fresh_doc.get("body", {}).get("content", [])
            
            target_table = None
            for fe in fresh_body:
                if "table" in fe and fe.get("startIndex") >= start_idx:
                    target_table = fe["table"]
                    break
                    
            if not target_table:
                continue
                
            fill_reqs = []
            for r_idx, row_data in enumerate(raw_rows):
                if r_idx < len(target_table.get("tableRows", [])):
                    g_row = target_table["tableRows"][r_idx]
                    for c_idx, cell_text in enumerate(row_data):
                        if c_idx < len(g_row.get("tableCells", [])):
                            cell_elem = g_row["tableCells"][c_idx]
                            c_start = cell_elem.get("startIndex") + 1
                            
                            clean_cell = cell_text
                            cell_link = None
                            link_m = re.search(r"\[(.*?)\]\((.*?)\)", cell_text)
                            if link_m:
                                clean_cell = link_m.group(1)
                                cell_link = link_m.group(2)
                                
                            fill_reqs.append({"insertText": {"location": {"index": c_start}, "text": clean_cell}})
                            
                            if r_idx == 0:
                                fill_reqs.append({
                                    "updateTextStyle": {
                                        "range": {"startIndex": c_start, "endIndex": c_start + len(clean_cell)},
                                        "textStyle": {"bold": True, "fontSize": {"magnitude": 10, "unit": "PT"}},
                                        "fields": "bold,fontSize"
                                    }
                                })
                            elif cell_link:
                                fill_reqs.append({
                                    "updateTextStyle": {
                                        "range": {"startIndex": c_start, "endIndex": c_start + len(clean_cell)},
                                        "textStyle": {"link": {"url": cell_link}, "foregroundColor": {"color": {"rgbColor": {"blue": 0.8, "green": 0.4, "red": 0.1}}}},
                                        "fields": "link,foregroundColor"
                                    }
                                })
            if fill_reqs:
                call_with_retry(docs_svc.documents().batchUpdate(documentId=doc_id, body={"requests": fill_reqs}).execute)

    except Exception as e:
        print(f"    ⚠️ Erreur conversion tables natives sur {doc_id}: {e}")


def apply_document_styles(docs_svc, doc_id):
    """Applique les marges globales (14pt header/footer), le texte JUSTIFIÉ et le formatage des titres en GRAS sur tout le document."""
    try:
        doc = call_with_retry(docs_svc.documents().get(documentId=doc_id).execute)
        body_content = doc.get("body", {}).get("content", [])
        reqs = [
            {
                "updateDocumentStyle": {
                    "documentStyle": {
                        "marginTop": {"magnitude": 72, "unit": "PT"},
                        "marginBottom": {"magnitude": 72, "unit": "PT"},
                        "marginHeader": {"magnitude": 14, "unit": "PT"},
                        "marginFooter": {"magnitude": 14, "unit": "PT"}
                    },
                    "fields": "marginTop,marginBottom,marginHeader,marginFooter"
                }
            }
        ]
        for element in body_content:
            if "paragraph" in element:
                para = element["paragraph"]
                style_name = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
                start_idx = element.get("startIndex")
                end_idx = element.get("endIndex")
                if not start_idx or not end_idx or start_idx >= end_idx:
                    continue
                
                # 1. Texte normal -> JUSTIFIÉ
                if style_name == "NORMAL_TEXT":
                    reqs.append({
                        "updateParagraphStyle": {
                            "range": {"startIndex": start_idx, "endIndex": end_idx},
                            "paragraphStyle": {"alignment": "JUSTIFIED"},
                            "fields": "alignment"
                        }
                    })
                # 2. Titres (HEADING_1, HEADING_2, etc.) -> GRAS + Taille
                elif "HEADING" in style_name:
                    font_size = 16 if style_name == "HEADING_1" else (14 if style_name == "HEADING_2" else 12)
                    reqs.append({
                        "updateTextStyle": {
                            "range": {"startIndex": start_idx, "endIndex": end_idx},
                            "textStyle": {
                                "bold": True,
                                "fontSize": {"magnitude": font_size, "unit": "PT"}
                            },
                            "fields": "bold,fontSize"
                        }
                    })
        if reqs:
            call_with_retry(docs_svc.documents().batchUpdate(documentId=doc_id, body={"requests": reqs}).execute)
    except Exception as e:
        print(f"    ⚠️ Erreur styles document sur {doc_id}: {e}")


def apply_header_footer(docs_svc, doc_id, rel_path, reel_path):
    """Ajoute des en-têtes et pieds de page discrets A4 uniquement sur les documents de type courrier."""
    if not (rel_path.startswith("Courriers/") or "/Courriers/" in rel_path):
        return

    try:
        doc = call_with_retry(docs_svc.documents().get(documentId=doc_id).execute)
        headers = doc.get("headers", {})
        footers = doc.get("footers", {})
        
        # 1. Obtenir / Créer Header et Footer de manière idempotente
        header_id = list(headers.keys())[0] if headers else None
        if not header_id:
            try:
                res_h = call_with_retry(docs_svc.documents().batchUpdate(
                    documentId=doc_id,
                    body={"requests": [{"createHeader": {"type": "DEFAULT"}}]}
                ).execute)
                header_id = res_h.get("replies", [{}])[0].get("createHeader", {}).get("headerId")
            except Exception:
                fresh_doc = call_with_retry(docs_svc.documents().get(documentId=doc_id).execute)
                h_map = fresh_doc.get("headers", {})
                if h_map:
                    header_id = list(h_map.keys())[0]

        footer_id = list(footers.keys())[0] if footers else None
        if not footer_id:
            try:
                res_f = call_with_retry(docs_svc.documents().batchUpdate(
                    documentId=doc_id,
                    body={"requests": [{"createFooter": {"type": "DEFAULT"}}]}
                ).execute)
                footer_id = res_f.get("replies", [{}])[0].get("createFooter", {}).get("footerId")
            except Exception:
                fresh_doc = call_with_retry(docs_svc.documents().get(documentId=doc_id).execute)
                f_map = fresh_doc.get("footers", {})
                if f_map:
                    footer_id = list(f_map.keys())[0]

        # 3. Écriture Header
        h_doc = call_with_retry(docs_svc.documents().get(documentId=doc_id).execute)
        h_content = h_doc.get("headers", {}).get(header_id, {}).get("content", [])
        h_text_len = sum(len(e.get("paragraph", {}).get("elements", [{}])[0].get("textRun", {}).get("content", "")) for e in h_content if "paragraph" in e)
        
        if h_text_len <= 1:
            raw_auteur = read_yaml_field(reel_path, "expediteur") or read_yaml_field(reel_path, "auteur") or read_yaml_field(reel_path, "redacteur") or "Sébastien GRAZIDE"
            clean_auteur = raw_auteur.strip().strip("[").strip("]")
            auteur = "Sébastien GRAZIDE" if clean_auteur in ("La Victime", "la victime", "LA VICTIME") else clean_auteur
            h_text = f"{auteur}\tAccident Main — Document confidentiel\n"
            h_reqs = [
                {"insertText": {"location": {"segmentId": header_id, "index": 0}, "text": h_text}},
                {
                    "updateParagraphStyle": {
                        "range": {"segmentId": header_id, "startIndex": 0, "endIndex": len(h_text)},
                        "paragraphStyle": {
                            "alignment": "START",
                            "borderBottom": {
                                "color": {"color": {"rgbColor": {"red": 0.8, "green": 0.8, "blue": 0.8}}},
                                "width": {"magnitude": 0.75, "unit": "PT"},
                                "padding": {"magnitude": 4, "unit": "PT"},
                                "dashStyle": "SOLID"
                            }
                        },
                        "fields": "alignment,borderBottom"
                    }
                },
                {"updateTextStyle": {"range": {"segmentId": header_id, "startIndex": 0, "endIndex": len(h_text)}, "textStyle": {"fontSize": {"magnitude": 8, "unit": "PT"}, "foregroundColor": {"color": {"rgbColor": {"red": 0.4, "green": 0.4, "blue": 0.4}}}}, "fields": "fontSize,foregroundColor"}}
            ]
            call_with_retry(docs_svc.documents().batchUpdate(documentId=doc_id, body={"requests": h_reqs}).execute)

        # 4. Écriture Footer avec numéro de page dynamique (\u0001) si vide
        f_doc = call_with_retry(docs_svc.documents().get(documentId=doc_id).execute)
        f_content = f_doc.get("footers", {}).get(footer_id, {}).get("content", [])
        f_text_len = sum(len(e.get("paragraph", {}).get("elements", [{}])[0].get("textRun", {}).get("content", "")) for e in f_content if "paragraph" in e)

        if f_text_len <= 1:
            f_text_static = "Accident de la Main — Document confidentiel — Page "
            f_text_dynamic = "\u0001"
            f_text = f"{f_text_static}{f_text_dynamic}\n"
            f_reqs = [
                {"insertText": {"location": {"segmentId": footer_id, "index": 0}, "text": f_text}},
                {
                    "updateParagraphStyle": {
                        "range": {"segmentId": footer_id, "startIndex": 0, "endIndex": len(f_text)},
                        "paragraphStyle": {
                            "alignment": "CENTER",
                            "borderTop": {
                                "color": {"color": {"rgbColor": {"red": 0.8, "green": 0.8, "blue": 0.8}}},
                                "width": {"magnitude": 0.75, "unit": "PT"},
                                "padding": {"magnitude": 4, "unit": "PT"},
                                "dashStyle": "SOLID"
                            }
                        },
                        "fields": "alignment,borderTop"
                    }
                },
                {"updateTextStyle": {"range": {"segmentId": footer_id, "startIndex": 0, "endIndex": len(f_text)}, "textStyle": {"fontSize": {"magnitude": 8, "unit": "PT"}, "foregroundColor": {"color": {"rgbColor": {"red": 0.4, "green": 0.4, "blue": 0.4}}}}, "fields": "fontSize,foregroundColor"}}
            ]
            call_with_retry(docs_svc.documents().batchUpdate(documentId=doc_id, body={"requests": f_reqs}).execute)

    except Exception as e:
        print(f"    ⚠️ Erreur header/footer sur {doc_id}: {e}")


def get_creds():
    return get_credentials_from_env() or get_credentials_from_file() or get_credentials_from_adc()


def main():
    import random
    dry = "--apply" not in sys.argv
    
    target_files = None
    if "--files" in sys.argv:
        idx = sys.argv.index("--files")
        target_files = [f for f in sys.argv[idx + 1:] if not f.startswith("--")]
    
    random_limit = None
    if "--random" in sys.argv:
        idx = sys.argv.index("--random")
        try:
            random_limit = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            random_limit = 20

    creds = get_creds()
    svc = build("drive", "v3", credentials=creds)
    docs_svc = build("docs", "v1", credentials=creds) if not dry else None
    cache = {}
    root_id = find_or_create_folder(svc, DRIVE_ROOT_NAME, None, cache, dry)

    # Collecter tous les fichiers .md éligibles
    file_list = []
    for dp, dn, fn in os.walk(REEL_BASE):
        dn.sort()
        for f in sorted(fn):
            if not f.endswith(".md") or f == "README.md":
                continue
            reel_path = os.path.join(dp, f)
            rel = os.path.relpath(reel_path, REEL_BASE)
            if target_files and rel not in target_files and f not in target_files:
                continue
            file_list.append((reel_path, rel, f))

    if random_limit and not target_files:
        file_list = random.sample(file_list, min(random_limit, len(file_list)))

    print(f"📌 Batch ciblé : {len(file_list)} document(s) à traiter.")
    for rp, rel, f in file_list:
        tp = os.path.join(TOKEN_BASE, rel)
        r_id = read_yaml_field(rp, "reel_drive_id") or read_yaml_field(rp, "drive_id") or read_yaml_field(tp, "reel_drive_id") or read_yaml_field(tp, "drive_id")
        print(f"  📄 SELECTED_FILE: {rel} | ID: https://docs.google.com/document/d/{r_id}/edit")

    created, updated, skipped, errors = 0, 0, 0, []
    for reel_path, rel, f in file_list:
        token_path = os.path.join(TOKEN_BASE, rel)
        rid = (
            read_yaml_field(reel_path, "reel_drive_id")
            or read_yaml_field(reel_path, "drive_id")
            or read_yaml_field(token_path, "reel_drive_id")
            or read_yaml_field(token_path, "drive_id")
        )
        if rid and not VALID_ID.match(rid):
            rid = None

        # Vérifie l'existence réelle du doc si ID connu
        if rid and not dry:
            try:
                meta = svc.files().get(fileId=rid, fields="id,trashed").execute()
                if meta.get("trashed"):
                    rid = None
            except Exception:
                rid = None

        try:
            media, fn_map = md_media(reel_path)
            if rid:
                if dry:
                    skipped += 1
                else:
                    call_with_retry(svc.files().update(fileId=rid, media_body=media).execute)
                    replace_page_break_markers(docs_svc, rid)
                    process_native_footnotes(docs_svc, rid, fn_map)
                    process_native_tables(docs_svc, rid, reel_path)
                    apply_document_styles(docs_svc, rid)
                    apply_header_footer(docs_svc, rid, rel, reel_path)
                    time.sleep(0.5)
                    updated += 1
            else:
                if dry:
                    print(f"[DRY] CREATE {rel}")
                    created += 1
                    continue
                # Dossier Drive miroir
                parent = root_id
                for seg in os.path.dirname(rel).split(os.sep):
                    if seg:
                        parent = find_or_create_folder(svc, seg, parent, cache, dry)
                body = {
                    "name": os.path.splitext(f)[0],
                    "mimeType": DOC_MIME,
                    "parents": [parent],
                }
                new_id = call_with_retry(svc.files().create(
                    body=body, media_body=media, fields="id"
                ).execute)["id"]
                replace_page_break_markers(docs_svc, new_id)
                process_native_footnotes(docs_svc, new_id, fn_map)
                apply_document_styles(docs_svc, new_id)
                apply_header_footer(docs_svc, new_id, rel, reel_path)
                time.sleep(0.5)
                # Token-first : écrire dans le Token miroir, puis refléter dans le Reel
                if os.path.isfile(token_path):
                    set_yaml_field(token_path, "reel_drive_id", new_id)
                    if not read_yaml_field(token_path, "drive_id"):
                        set_yaml_field(token_path, "drive_id", new_id)
                set_yaml_field(reel_path, "reel_drive_id", new_id)
                if not read_yaml_field(reel_path, "drive_id"):
                    set_yaml_field(reel_path, "drive_id", new_id)
                created += 1
                print(f"  + CREATE {rel} → {new_id}")
        except Exception as e:
            errors.append((rel, str(e)))
            print(f"  ✗ ERREUR {rel}: {e}")

    print(f"\nMODE: {'DRY-RUN' if dry else 'APPLY'}")
    print(f"créés: {created} | mis à jour: {updated} | inchangés (dry): {skipped} | erreurs: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

