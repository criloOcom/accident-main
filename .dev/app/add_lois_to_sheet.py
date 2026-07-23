#!/usr/bin/env python3
"""Ajoute les 81 fichiers Lois/ manquants dans le Google Sheet des sources
juridiques (colonnes coherentes avec l'existant). Souverain via 'souverain'."""
import os, re, sys
sys.path.insert(0, os.path.expanduser("~/.opencode"))
from souverain import get_credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = "14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ"
REPO = "/home/crilocom/accident-main"

# 1) recompute la liste des 81 manquantes (meme logique que compare_lois_sheet.py)
def pourvoi(s):
    m = re.search(r"(\d{2})[-.](\d{2})\.(\d{3})", s)
    return m.group(1) + m.group(2) + m.group(3) if m else None

def article_key(s):
    s = s.lower().replace(" ", "_")
    m = re.search(r"([a-z]?\d{1,4}[-_]\d{1,4})", s)
    if m:
        return m.group(1).replace("_", "-")
    m = re.search(r"(\d{3,4})", s)
    return m.group(1) if m else s.lower()

meta = {"README.md", "CHANGELOG_JURIDIQUE.md", "EXEMPLES_REQUETES_MCP.md",
        "RAPPORT_ORGANISATION_20260711.md", "RGPD_Articles7_9_82.md"}
lois_paths = []
for root, _, files in os.walk(os.path.join(REPO, "Lois")):
    for fn in files:
        if not fn.endswith(".md") or fn.upper() == "README.md":
            continue
        rel = os.path.relpath(os.path.join(root, fn), os.path.join(REPO, "Lois"))
        if os.path.basename(rel) in meta:
            continue
        lois_paths.append("Lois/" + rel)

# lire le Sheet pour connaitre ce qui est deja present
creds = get_credentials()
if not creds.valid:
    creds.refresh(Request())
svc = build("sheets", "v4", credentials=creds)
rows = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range="A1:Z1000").execute().get("values", [])
sheet_refs = set()
for r in rows[2:]:
    if not r:
        continue
    v = (r[4] if len(r) > 4 else "").strip() or (r[0] if r else "").strip()
    if v:
        sheet_refs.add(v.lower())

lois_pourvois = {pourvoi(os.path.basename(p)): p for p in lois_paths if pourvoi(os.path.basename(p))}
lois_arts = {article_key(os.path.basename(p)): p for p in lois_paths}

def is_in_sheet(p):
    b = os.path.basename(p)
    pv = pourvoi(b)
    if pv:
        for s in sheet_refs:
            if pv in s.replace(" ", ""):
                return True
    ak = article_key(b)
    if ak in ("263", "121-1", "143-2"):
        for s in sheet_refs:
            if ak in s.replace(" ", ""):
                return True
    for s in sheet_refs:
        if ak and ak in s.replace(" ", ""):
            return True
    return False

missing = [p for p in lois_paths if not is_in_sheet(p)]
print(f"Manquantes a ajouter: {len(missing)}")

# 2) construire les lignes (21 colonnes, alignees sur le Sheet)
def type_source(p):
    if "Jurisprudence" in p:
        if "CEDH" in p: return "CEDH"
        if "CA" in p or "TJ" in p: return "Jurisprudence (fond CA/TJ)"
        return "Cour de Cassation"
    if "Code" in p:
        return "Code"
    return "Autre"

new_rows = []
for p in sorted(missing):
    b = os.path.basename(p).replace(".md", "")
    # extraire la reference lisible
    ref = re.sub(r"_(Code|Codesassurances|CodePenal|Legifrance|CodeProcedureCivile|CodeProcedurePenale|Codeproc|Codecommerce|Codeconsommation|Codeconstructionhabitation|CodeGeneralCollectivitesTerritoriales|CodeTravail|Code_Legifrance|LivreProceduresFiscales|CRPA|LegiFrance|_CourCassation).*$", "", b, flags=re.I)
    ref = ref.replace("_", " ").strip()
    num = ref[:40]
    typ = type_source(p)
    # 21 colonnes
    row = [""] * 21
    row[0] = num                      # N° Référence
    row[1] = typ                      # Type de Source
    row[4] = ref                      # Référence de la Loi / Arrêt
    new_rows.append(row)

# 3) append dans le Sheet (apres la derniere ligne)
body = {"values": new_rows}
r = svc.spreadsheets().values().append(
    spreadsheetId=SHEET_ID, range="A1",
    valueInputOption="RAW", body=body).execute()
print(f"Lignes ajoutees: {r.get('updates', {}).get('updatedRows', 0)}")
print(f"URL: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
