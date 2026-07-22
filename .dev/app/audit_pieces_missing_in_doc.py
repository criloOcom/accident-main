#!/usr/bin/env python3
"""
audit_pieces_missing_in_doc.py — Détecte, dans tous les bordereaux .md du dépôt,
les pièces citées qui ne sont PAS encore présentes dans le Google Doc
« Pj & Chronologie WIP » (ID: 1LQCFXEyGj7VWD92ccdh6JRwFQgKl2THT131YbrnemoE).

Produit un tableau Markdown (Memory/PIECES_A_AJOUTER_DOC.md) :
| Pièce | Nom de la pièce (lien local) | ID Google Drive (si connu) | Dans le Doc ? |

Clé de jointure : le NOM DE FICHIER. Un bordereau .md pointe vers
  ../../Preuves officielles/20260529_DrJARDON/20260529-1630 SITUATION DrJulieJARDON.md
et le Google Doc contient un fichier Drive nommé
  « 20260529-1630 SITUATION DrJulieJARDON Doc_1.pdf ».
On normalise les noms et on cherche la correspondance.

Usage :
    python3 .dev/app/audit_pieces_missing_in_doc.py [--report]
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


def fetch_doc_drive_map():
    """Renvoie {nom_normalisé: (nom_brut, id_drive)} des fichiers Drive du Doc."""
    from googleapiclient.discovery import build
    creds = _creds()
    drive = build("drive", "v3", credentials=creds)
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
    result = {}
    for i in ids:
        try:
            meta = drive.files().get(fileId=i, fields="name").execute()
            result[normalize(meta.get("name", ""))] = (meta.get("name", ""), i)
        except Exception:
            pass
    return result


def normalize(s):
    """Normalise un nom de fichier pour la comparaison (alphabet numérique seul, minuscules)."""
    s = s.lower()
    s = re.sub(r"\.(pdf|md|docx?|png|jpg|jpeg)$", "", s)
    s = re.sub(r"[^a-z0-9]", "", s)
    return s


def find_local_links(md_text, base_dir):
    """
    Dans un bordereau .md, suit le numéro de pièce courant (titre 'PIÈCE N° X'
    ou '**Pièce n°X**') et capte les liens locaux vers les PREUVES OFFICIELLES
    qui suivent jusqu'à la pièce suivante. Renvoie une liste de dicts :
      {numero, nom_normalise, nom_brut, lien_relatif}
    """
    rows = []
    current_num = None
    lines = md_text.splitlines()
    for line in lines:
        mnum = re.search(r'PI[eè]CE\s*N[°o]?\s*(\d+[a-bA-B]?)', line, re.IGNORECASE)
        if mnum:
            current_num = mnum.group(1)
            continue
        for lm in re.finditer(r'\]\(([^)]+)\)', line):
            target = lm.group(1).strip()
            if target.startswith("http") or target.startswith("#"):
                continue
            # On ne garde QUE les liens vers Preuves officielles (vraies pièces)
            if "Preuves%20officielles" not in target and "Preuves officielles" not in target:
                continue
            seg = target.split("/")[-1]
            seg_decoded = seg.replace("%20", " ").replace("%F0%9F%86%98", " ")
            rows.append({
                "numero": current_num or "?",
                "nom_normalise": normalize(seg_decoded),
                "nom_brut": seg_decoded,
                "lien_relatif": target,
            })
    return rows


def main():
    log("Analyse des bordereaux .md vs Google Doc...")
    doc_map = fetch_doc_drive_map()
    log(f"Google Doc : {len(doc_map)} fichiers Drive indexés (ID + noms).")

    # Correction : assouplir la correspondance nom local <-> nom Drive
    def match_drive(nom_norm, doc_map):
        """Retourne (in_doc, drive_id) en tolérant .md/.pdf et suffixes 'Doc_1'."""
        if nom_norm in doc_map:
            return True, doc_map[nom_norm][1]
        # le nom local sans extension
        base = re.sub(r'\.md$', '', nom_norm)
        # chercher un fichier Drive qui contient le nom local (ou inversement)
        for dn, (_, did) in doc_map.items():
            dn_base = re.sub(r'\.pdf$', '', dn)
            if base and (base in dn_base or dn_base in base):
                return True, did
        return False, ""

    rows = []  # dicts enrichis
    total_pieces = 0
    scanned = 0
    seen_keys = set()
    for base in SCAN_DIRS:
        full = os.path.join(PROJECT_ROOT, base)
        if not os.path.isdir(full):
            continue
        for root, _, files in os.walk(full):
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                if fn.upper() == "README.md":
                    continue
                path = os.path.join(root, fn)
                try:
                    text = open(path, "r", encoding="utf-8").read()
                except Exception:
                    continue
                if not re.search(r'#\s*BORDEREAU', text, re.IGNORECASE) and \
                   "Bordereau" not in text:
                    continue
                scanned += 1
                local_rows = find_local_links(text, path)
                rel_md = os.path.relpath(path, PROJECT_ROOT)
                for r in local_rows:
                    total_pieces += 1
                    in_doc, drive_id = match_drive(r["nom_normalise"], doc_map)
                    key = (rel_md, r["numero"], r["nom_normalise"])
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)
                    rows.append({
                        "bordereau": rel_md,
                        "numero": r["numero"],
                        "nom": r["nom_brut"],
                        "lien": r["lien_relatif"],
                        "drive_id": drive_id,
                        "in_doc": in_doc,
                    })
    log(f"Bordereaux scannés : {scanned} | pièces citées (liens) : {total_pieces}")
    missing = [r for r in rows if not r["in_doc"]]
    present = [r for r in rows if r["in_doc"]]
    log(f"Déjà dans le Doc : {len(present)} | À ajouter : {len(missing)}")

    if "--report" in sys.argv:
        _write_report(rows, missing, present, scanned, total_pieces)

    print("\n=== RÉSUMÉ ===")
    print(f"À AJOUTER dans le Google Doc : {len(missing)} pièce(s)")
    print(f"Déjà présentes : {len(present)}")
    return 0


def _write_report(rows, missing, present, scanned, total_pieces):
    out = os.path.join(PROJECT_ROOT, "Memory", "PIECES_A_AJOUTER_DOC.md")
    lines = []
    lines.append("---")
    lines.append('title: "Pièces à ajouter dans le Google Doc (Pj & Chronologie WIP)"')
    lines.append('description: "Tableau auto-généré des pièces citées dans les bordereaux .md vs Google Doc. Case à cocher si présente dans le Doc."')
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
    lines.append(f"> Bordereaux scannés : **{scanned}** | Liens de pièces cités : **{total_pieces}** | Déjà dans le Doc : **{len(present)}** | À ajouter : **{len(missing)}**.")
    lines.append("")
    lines.append("> **Mode d'emploi :** pour chaque ligne non cochée, ouvrez le Google Doc et ajoutez la pièce (coller l'ID Drive en tête de page + activer le footer « Pièce n° »). La colonne « Nom de la pièce » est un lien cliquable vers le fichier local de référence. La colonne « ID Google Drive » est pré-remplie si l'ID est déjà connu du dépôt (sinon à compléter).")
    lines.append("")
    lines.append("| # | Bordereau | Pièce n° | Nom de la pièce (lien local) | ID Google Drive (si connu) | Dans le Google Doc ? |")
    lines.append("|---|-----------|----------|-------------------------------|--------------------------|----------------------|")
    # Trier : d'abord les manquantes, par bordereau puis numéro
    ordered = sorted(missing, key=lambda r: (r["bordereau"], r["numero"])) + \
              sorted(present, key=lambda r: (r["bordereau"], r["numero"]))
    for i, r in enumerate(ordered, 1):
        bord = r["bordereau"]
        num = r["numero"]
        nom = r["nom"]
        lien = r["lien"]
        # lien cliquable markdown vers le fichier local (relatif au dépôt), décodé pour lisibilité
        lien_decod = lien.replace("%20", " ").replace("%F0%9F%86%98", " ")
        nom_cell = f"[{nom}](../../{lien_decod})" if lien else nom
        did = r["drive_id"] or "—"
        check = "✅ oui" if r["in_doc"] else "☐ non"
        lines.append(f"| {i} | {bord} | {num} | {nom_cell} | {did} | {check} |")
        lines.append("")  # Règle #24 : ligne vide après chaque ligne de tableau (séparation visuelle)
    lines.append("")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n[RAPPORT] Écrit : {out}")


if __name__ == "__main__":
    sys.exit(main())
