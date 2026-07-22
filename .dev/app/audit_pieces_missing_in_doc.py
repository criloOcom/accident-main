#!/usr/bin/env python3
"""
audit_pieces_missing_in_doc.py — Détecte, dans tous les bordereaux .md du dépôt,
les pièces citées qui ne sont PAS encore présentes dans le Google Doc
« Pj & Chronologie WIP » (ID: 1LQCFXEyGj7VWD92ccdh6JRwFQgKl2THT131YbrnemoE).

But : donner à l'utilisateur la liste des pièces à ajouter (ID Drive + footer)
dans le Google Doc, sans rien modifier.

Clé de jointure : le NOM DE FICHIER. Un bordereau .md pointe souvent vers
  ../../Preuves officielles/20260529_DrJARDON/20260529-1630 SITUATION DrJulieJARDON.md
et le Google Doc contient un fichier Drive nommé
  « 20260529-1630 SITUATION DrJulieJARDON Doc_1.pdf ».
On normalise les noms (minuscules, alphanum seul) et on cherche si un fichier
Drive du Doc « contient » le nom local (ou inversement).

Usage :
    python3 .dev/app/audit_pieces_missing_in_doc.py
"""

import os
import re
import sys

PROJECT_ROOT = "/home/crilocom/accident-main"
DOC_ID = "1LQCFXEyGj7VWD92ccdh6JRwFQgKl2THT131YbrnemoE"

# Dossiers scannés pour les bordereaux
SCAN_DIRS = ["Actes/Token", "Actes/Reel"]

ID_RE = re.compile(r'\b1[A-Za-z0-9_-]{20,}\b')


def log(msg):
    print(f"[AUDIT_PIECES] {msg}")


def _creds():
    sys.path.insert(0, os.path.expanduser("~/.opencode"))
    from souverain import get_credentials
    creds = get_credentials()
    if not creds.valid:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
    return creds


def fetch_doc_drive_names():
    """Renvoie le set des noms de fichiers Drive (normalisés) présents dans le Doc."""
    from googleapiclient.discovery import build
    creds = _creds()
    drive = build("drive", "v3", credentials=creds)
    # On récupère les ID du Doc via API Docs, puis les noms via Drive
    from googleapiclient.discovery import build as bd
    docs = bd("docs", "v1", credentials=creds)
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
    names = set()
    for i in ids:
        try:
            meta = drive.files().get(fileId=i, fields="name").execute()
            names.add(normalize(meta.get("name", "")))
        except Exception:
            pass
    return names


def normalize(s):
    """Normalise un nom de fichier pour la comparaison (alphabet numérique seul, minuscules)."""
    s = s.lower()
    s = re.sub(r"\.(pdf|md|docx?|png|jpg|jpeg)$", "", s)
    s = re.sub(r"[^a-z0-9]", "", s)
    return s


def find_local_piece_files(md_text):
    """
    Dans un bordereau .md, trouve les liens vers des fichiers 'Preuves officielles'
    et renvoie le nom de fichier local normalisé.
    """
    files = set()
    for m in re.finditer(r'\]\(([^)]*Preuves%20officielles[^)]*)\)', md_text):
        path = m.group(1)
        # extraire le dernier segment
        seg = path.split("/")[-1]
        seg = seg.replace("%20", " ").replace("%F0%9F%86%98", " ")
        files.add(normalize(seg))
    return files


def find_piece_numbers(md_text):
    """Renvoie la liste des numéros de pièce cités (PIÈCE N° X ou **Pièce n°X**)."""
    nums = set()
    for m in re.finditer(r'PI[eè]CE\s*N[°o]?\s*(\d+[a-bA-B]?)', md_text, re.IGNORECASE):
        nums.add(m.group(1))
    return nums


def main():
    log("Analyse des bordereaux .md vs Google Doc...")
    doc_names = fetch_doc_drive_names()
    log(f"Google Doc : {len(doc_names)} noms de fichiers Drive indexés.")

    missing = []  # (fichier .md, numéro pièce, nom fichier local)
    total_pieces = 0
    scanned = 0
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
                    text = open(path, "r", encoding="utf-8").read()
                except Exception:
                    continue
                # Détecter si c'est un bordereau
                if not re.search(r'#\s*BORDEREAU', text, re.IGNORECASE) and \
                   "Bordereau" not in text:
                    continue
                scanned += 1
                nums = find_piece_numbers(text)
                local_files = find_local_piece_files(text)
                total_pieces += len(nums)
                for lf in local_files:
                    # une pièce est 'présente dans le Doc' si un fichier Drive contient ce nom
                    # (ou si le nom local contient un fichier Drive)
                    present = any(lf and (lf in dn or dn and lf[:15] in dn) for dn in doc_names)
                    if not present:
                        # retrouver le numéro associé (heuristique : proche dans le texte)
                        missing.append((os.path.relpath(path, PROJECT_ROOT), lf))
    log(f"Bordereaux scannés : {scanned} | pièces citées : {total_pieces}")
    log(f"Pièces dont le fichier n'est PAS trouvé dans le Google Doc : {len(missing)}")
    if missing:
        print("\n=== PIÈCES À AJOUTER DANS LE GOOGLE DOC ===")
        for rel, lf in sorted(set(missing)):
            print(f"  • {rel}\n      fichier : {lf}")
        # Génération d'un rapport .md (option --report)
        if "--report" in sys.argv:
            _write_report(missing, total_pieces, scanned, doc_names)
    else:
        print("✅ Toutes les pièces citées pointent vers un fichier présent dans le Google Doc.")
    return 0


def _write_report(missing, total_pieces, scanned, doc_names):
    out = os.path.join(PROJECT_ROOT, "Memory", "PIECES_A_AJOUTER_DOC.md")
    # Grouper par fichier .md source
    by_file = {}
    for rel, lf in missing:
        by_file.setdefault(rel, []).append(lf)
    lines = []
    lines.append("---")
    lines.append('title: "Pièces à ajouter dans le Google Doc (Pj & Chronologie WIP)"')
    lines.append('description: "Liste auto-générée des pièces citées dans les bordereaux .md mais absentes du Google Doc. À compléter par l\'utilisateur (coller ID Drive + footer)."')
    lines.append('type: readme')
    lines.append('date: "2026-07-22"')
    lines.append('auteur: Agent de synchronisation')
    lines.append('source_doc: "1LQCFXEyGj7VWD92ccdh6JRwFQgKl2THT131YbrnemoE"')
    lines.append("---")
    lines.append("")
    lines.append("*[🏠](../../README.md) › [🧠 Memory](./README.md)*")
    lines.append("<hr>")
    lines.append("")
    lines.append("# PIÈCES À AJOUTER DANS LE GOOGLE DOC")
    lines.append("")
    lines.append(f"> Rapport généré le 22/07/2026 par `audit_pieces_missing_in_doc.py`.")
    lines.append(f"> Bordereaux scannés : **{scanned}** | Pièces citées : **{total_pieces}** | Pièces absentes du Doc : **{len(missing)}**.")
    lines.append("")
    lines.append("> **Mode d'emploi :** pour chaque fichier ci-dessous, ouvrez le Google Doc et ajoutez la pièce (coller l'ID Drive en tête de page + activer le footer « Pièce n° »). Le nom de fichier indiqué est la clé de jointure avec le Doc.")
    lines.append("")
    lines.append("## Par bordereau")
    lines.append("")
    for rel in sorted(by_file):
        lines.append(f"### {rel}")
        lines.append("")
        for lf in sorted(set(by_file[rel])):
            lines.append(f"- {lf}")
            lines.append("")  # Règle #24 : liste loose
        lines.append("")
    lines.append("## Par nom de fichier (dedoublonné)")
    lines.append("")
    for lf in sorted(set(lf for _, lf in missing)):
        lines.append(f"- {lf}")
        lines.append("")  # Règle #24 : liste loose
    lines.append("")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n[RAPPORT] Écrit : {out}")


if __name__ == "__main__":
    sys.exit(main())
