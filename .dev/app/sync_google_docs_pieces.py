#!/usr/bin/env python3
"""
sync_google_docs_pieces.py — Synchronise le bordereau des pièces depuis le Google Doc
« Pj & Chronologie WIP » (ID: 1LQCFXEyGj7VWD92ccdh6JRwFQgKl2THT131YbrnemoE) vers
Memory/PIECES MAP.md, et audite les citations de pièces dans le dépôt.

Authentification : module `souverain` (identifiants souverains Google Cloud du projet).
Lecture du Doc   : API Google Docs (structure) + API Google Drive (export PDF pour les
                   numéros de page, et validation des ID Drive).

──── CONVENTION AUTOMATIQUE DANS LE GOOGLE DOC (aucune saisie manuelle requise) ────
Sur CHAQUE page de pièce, l'utilisateur colle en HAUT de page l'ID Google Drive de la
pièce (Google Docs l'affiche tel quel). Google Docs génère en BAS de page un footer
« Pièce n°N » (numéro de page automatique). Le script exporte le Doc en PDF et relie
automatiquement :  ID Drive (haut de page)  →  Pièce n°N (footer)  →  page physique N+2.

Usage :
    python3 .dev/app/sync_google_docs_pieces.py          # AUDIT (dry-run) : ne modifie rien
    python3 .dev/app/sync_google_docs_pieces.py --apply  # met à jour la section auto-générée de PIECES MAP.md
"""

import os
import re
import sys
import io
import shutil
import subprocess

PROJECT_ROOT = "/home/crilocom/accident-main"
DOC_ID = "1LQCFXEyGj7VWD92ccdh6JRwFQgKl2THT131YbrnemoE"
PIECES_MAP_PATH = os.path.join(PROJECT_ROOT, "Memory", "PIECES MAP.md")

AUTO_START = "<!-- AUTO-SYNC-GDOC-START -->"
AUTO_END = "<!-- AUTO-SYNC-GDOC-END -->"

DRY_RUN = "--apply" not in sys.argv
SCAN_DIRS = ["Actes", "Memory", "Rapports", "Lois"]

ID_RE = re.compile(r'\b1[A-Za-z0-9_-]{20,}\b')
PIECE_FOOTER_RE = re.compile(r'Pi[eè]ce\s*n[°o]?\s*(\d+)', re.IGNORECASE)
CITATION_RE = re.compile(r'Pi[eè]ce\s*n[°o]?\s*(\d+[a-bA-B]?)', re.IGNORECASE)

# Cache PDF pour éviter re-export à chaque appel
_PDF_BYTES = None


def log(msg):
    print(f"[SYNC_PIECES] {msg}")


def _creds():
    sys.path.insert(0, os.path.expanduser("~/.opencode"))
    from souverain import get_credentials
    creds = get_credentials()
    if not creds.valid:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
    return creds


def get_pdf_bytes():
    global _PDF_BYTES
    if _PDF_BYTES is None:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseDownload
        creds = _creds()
        drive = build("drive", "v3", credentials=creds)
        buf = io.BytesIO()
        dl = MediaIoBaseDownload(buf, drive.files().export(fileId=DOC_ID, mimeType="application/pdf"))
        done = False
        while not done:
            _, done = dl.next_chunk()
        _PDF_BYTES = buf.getvalue()
    return _PDF_BYTES


def pdf_to_text(pdf_bytes):
    import tempfile
    tmp = "/tmp/_gdoc_pj_chronologie.pdf"
    with open(tmp, "wb") as f:
        f.write(pdf_bytes)
    if shutil.which("pdftotext"):
        p = subprocess.run(["pdftotext", "-layout", tmp, "-"],
                           capture_output=True, text=True)
        out = p.stdout
    else:
        out = ""
    try:
        os.remove(tmp)
    except OSError:
        pass
    return out


def extract_page_pieces(pdf_text):
    """
    Renvoie une liste de dicts, une par page physique :
      {'page': N, 'piece_no': int|None, 'drive_id': str|None}
    Basée sur le footer 'Pièce n°X' et l'ID Drive en haut de page.
    """
    pages = pdf_text.split("\f")  # pdftotext sépare les pages par \f
    result = []
    for idx, block in enumerate(pages, start=1):
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        footer = PIECE_FOOTER_RE.search(block)
        piece_no = int(footer.group(1)) if footer else None
        # ID Drive : chercher sur les premières lignes (haut de page)
        drive_id = None
        for l in lines[:6]:
            m = ID_RE.search(l)
            if m:
                drive_id = m.group(0)
                break
        if drive_id is None:
            m = ID_RE.search(block)
            if m:
                drive_id = m.group(0)
        result.append({"page": idx, "piece_no": piece_no, "drive_id": drive_id})
    return result


def validate_drive_ids(ids):
    """Valide une liste d'ID via l'API Drive. Renvoie set des ID valides + dict nom."""
    from googleapiclient.discovery import build
    creds = _creds()
    drive = build("drive", "v3", credentials=creds)
    valid = set()
    names = {}
    invalid = []
    for i in ids:
        try:
            meta = drive.files().get(fileId=i, fields="id,name,trashed").execute()
            if not meta.get("trashed", False):
                valid.add(i)
                names[i] = meta.get("name", "?")
        except Exception:
            invalid.append(i)
    return valid, names, invalid


def fetch_doc_bordereau():
    """Bordereau textuel du Doc (numéro -> intitulé) via API Docs."""
    from googleapiclient.discovery import build
    creds = _creds()
    docs = build("docs", "v1", credentials=creds)
    doc = docs.documents().get(documentId=DOC_ID).execute()

    def text_of(el):
        t = ""
        if "paragraph" in el:
            for pe in el["paragraph"].get("elements", []):
                if "textRun" in pe:
                    t += pe["textRun"].get("content", "")
        return t

    parts = []
    for el in doc["body"]["content"]:
        if "paragraph" in el:
            parts.append(text_of(el))
        elif "table" in el:
            for row in el["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    for ce in cell.get("content", []):
                        parts.append(text_of(ce))
    full = "\n".join(parts)
    m = re.search(r"INVENTAIRE DES PI[eè]CES JUSTIFICATIVES", full, re.IGNORECASE)
    pieces = {}
    if m:
        body = full[m.start():]
        for num, title in re.findall(r"Pi[eè]ce\s*n[°o]?\s*(\d+[a-bA-B]?)\s*:\s*(.+?)(?=\n|●|\Z)", body, re.DOTALL):
            if num.upper() not in pieces:
                pieces[num.upper()] = re.sub(r"\s+", " ", title).strip()
    return pieces


def fetch_doc_drive_ids():
    """
    Liste FIABLE des ID Google Drive présents dans le Doc, via l'API Docs
    (et non le PDF, dont l'OCR/extraction peut tronquer les ID).
    Renvoie une liste ordonnée des ID uniques tels que collés dans le Doc.
    """
    from googleapiclient.discovery import build
    creds = _creds()
    docs = build("docs", "v1", credentials=creds)
    doc = docs.documents().get(documentId=DOC_ID).execute()

    def text_of(el):
        t = ""
        if "paragraph" in el:
            for pe in el["paragraph"].get("elements", []):
                if "textRun" in pe:
                    t += pe["textRun"].get("content", "")
        return t

    ids = []
    seen = set()
    for el in doc["body"]["content"]:
        chunks = []
        if "paragraph" in el:
            chunks = [text_of(el)]
        elif "table" in el:
            for row in el["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    for ce in cell.get("content", []):
                        chunks.append(text_of(ce))
        for ch in chunks:
            for m in ID_RE.finditer(ch):
                if m.group(0) not in seen:
                    seen.add(m.group(0))
                    ids.append(m.group(0))
    return ids


def scan_citations():
    found = {}
    for base in SCAN_DIRS:
        full = os.path.join(PROJECT_ROOT, base)
        if not os.path.isdir(full):
            continue
        for root, _, files in os.walk(full):
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                path = os.path.join(root, fn)
                try:
                    content = open(path, "r", encoding="utf-8").read()
                except Exception:
                    continue
                nums = CITATION_RE.findall(content)
                if nums:
                    rel = os.path.relpath(path, PROJECT_ROOT)
                    found[rel] = [n.upper() for n in nums]
    return found


def build_auto_section(mapping, names, invalid_ids):
    lines = [AUTO_START, ""]
    lines.append("## 🔄 Bordereau synchronisé depuis le Google Doc (Pj & Chronologie WIP)")
    lines.append("")
    lines.append(f"_Source de vérité visuelle : Document ID `{DOC_ID}`. "
                 "Mapping automatique via export PDF (footer « Pièce n°N » + ID Drive en tête de page)._")
    lines.append("")
    if not mapping:
        lines.append("> ⚠️ Aucune page de pièce détectée (footer « Pièce n°N » + ID Drive en tête). "
                     "Vérifiez que le Document a bien un footer de numéro de pièce.")
        lines.append("")
    else:
        lines.append("| Pièce | Page PDF | ID Google Drive | Nom du fichier Drive |")
        lines.append("|-------|----------|----------------|----------------------|")
        for no in sorted(mapping):
            info = mapping[no]
            lines.append(f"| {no} | {info['page']} | `{info['drive_id']}` | {info['name']} |")
        lines.append("")
        lines.append(f"_Total : {len(mapping)} pièces reliées (ID ↔ numéro ↔ page)._")
        lines.append("")
    if invalid_ids:
        lines.append("> ⚠️ ID Drive INVALIDES (non trouvés sur Drive) : " + ", ".join(f"`{i}`" for i in invalid_ids))
        lines.append("")
    lines.append(AUTO_END)
    return "\n".join(lines)


def update_pieces_map(text_auto):
    content = open(PIECES_MAP_PATH, "r", encoding="utf-8").read()
    if AUTO_START in content and AUTO_END in content:
        pre = content[:content.index(AUTO_START)]
        post = content[content.index(AUTO_END) + len(AUTO_END):]
        new_content = pre + text_auto + post
    else:
        new_content = content.rstrip() + "\n\n" + text_auto + "\n"
    open(PIECES_MAP_PATH, "w", encoding="utf-8").write(new_content)


def main():
    log("Démarrage sync pièces (Google Doc PDF -> dépôt)...")
    if DRY_RUN:
        log("Mode AUDIT (dry-run) : aucune écriture. Ajouter --apply pour mettre à jour PIECES MAP.md.")

    # 1. Export PDF + extraction page/piece (footers)
    log("Export PDF du Google Doc...")
    try:
        pdf = get_pdf_bytes()
    except Exception as e:
        log(f"⚠️ Export PDF impossible ({e}). Audit annulé (avertissement, commit non bloqué).")
        return 2
    log(f"PDF : {len(pdf)} octets.")
    text = pdf_to_text(pdf)
    page_pieces = extract_page_pieces(text)
    pages_with_footer = [p for p in page_pieces if p["piece_no"] is not None]
    log(f"Pages : {len(page_pieces)} | footer 'Pièce n°' sur {len(pages_with_footer)} pages.")

    # 1b. ID Drive FIABLES extraits du Doc (API Docs), pas du PDF
    doc_ids = fetch_doc_drive_ids()
    valid, names, invalid = validate_drive_ids(doc_ids)
    log(f"ID Drive du Doc : {len(doc_ids)} | validés sur Drive : {len(valid)} "
        f"| invalides : {len(invalid)}.")

    # 2. Mapping pièce <-> ID <-> page (depuis le PDF : footer + ID en tête)
    #    On ne garde qu'un ID par page ; en cas de doublon d'ID sur plusieurs pages,
    #    on conserve la PREMIÈRE page (ordre du Doc).
    id_to_first_page = {}
    for pp in page_pieces:
        if pp["drive_id"] and pp["drive_id"] not in id_to_first_page:
            id_to_first_page[pp["drive_id"]] = pp["page"]
    mapping = {}
    for pp in page_pieces:
        no = pp["piece_no"]
        did = pp["drive_id"]
        if no is None or not did or did not in names:
            continue
        mapping[no] = {"drive_id": did, "page": pp["page"], "name": names.get(did, "?")}
    log(f"Mapping pièces reliées : {len(mapping)} (ID valide + footer + page).")
    if invalid:
        log("⚠️ ID INVALIDES (non trouvés sur Drive) : " + ", ".join(invalid))

    # 4. Audit citations du dépôt
    citations = scan_citations()
    total_cited = sum(len(v) for v in citations.values())
    log(f"Scan de {len(citations)} fichiers .md citant des pièces ({total_cited} mentions).")
    cited_nums = set()
    for v in citations.values():
        cited_nums.update(int(re.sub(r'[^0-9]', '', n)) for n in v if re.sub(r'[^0-9]', '', n))
    mapped_nums = set(mapping.keys())
    missing = sorted(cited_nums - mapped_nums)
    if missing:
        log(f"⚠️ {len(missing)} numéro(s) cités ABSENTS du bordereau PDF du Doc : " + ", ".join(map(str, missing)))
    else:
        log("✅ Tous les numéros cités existent dans le bordereau du Doc.")

    # 5. Mise à jour PIECES MAP.md
    text_auto = build_auto_section(mapping, names, invalid)
    if not DRY_RUN:
        try:
            update_pieces_map(text_auto)
            log(f"PIECES MAP.md mis à jour ({len(mapping)} pièces reliées).")
        except Exception as e:
            log(f"❌ Échec mise à jour PIECES MAP.md : {e}")
            return 1
    else:
        log("Aperçu (dry-run) :")
        for ln in text_auto.splitlines()[:14]:
            print("    " + ln)

    # 6. Bilan honnête
    desync = len(missing)
    if invalid:
        rc = 2
        log(f"BILAN : {len(invalid)} ID Drive INVALIDE(S) détecté(s) — corrige le collage dans le Doc.")
    elif desync:
        rc = 2
        log(f"BILAN : {desync} désynchronisation(s) RÉELLE(S) (numéro cité absent du bordereau du Doc).")
    else:
        rc = 0
        log("BILAN : aucune désynchronisation détectée (audit réel).")
    return rc


if __name__ == "__main__":
    sys.exit(main())
