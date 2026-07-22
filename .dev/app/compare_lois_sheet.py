#!/usr/bin/env python3
"""Compare le dossier Lois/ avec le Google Sheet des sources juridiques et
genere Rapports/COMPARAISON_LOIS_vs_SHEET.md (ce qui manque dans le Sheet)."""
import re, os, sys, datetime

sys.path.insert(0, os.path.expanduser("~/.opencode"))
from souverain import get_credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = "14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ"
REPO = "/home/crilocom/accident-main"
OUT = os.path.join(REPO, "Rapports", "COMPARAISON_LOIS_vs_SHEET.md")

# 1) lire le Sheet
creds = get_credentials()
if not creds.valid:
    creds.refresh(Request())
svc = build("sheets", "v4", credentials=creds)
rows = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range="A1:Z1000").execute().get("values", [])
sheet_raw = []
for r in rows[2:]:
    if not r:
        continue
    ref = (r[4] if len(r) > 4 else "").strip()
    num = (r[0] if r else "").strip()
    v = ref or num
    if v:
        sheet_raw.append(v)

# 2) lister Lois/ (hors README/meta)
meta = {"README.md", "CHANGELOG_JURIDIQUE.md", "EXEMPLES_REQUETES_MCP.md",
        "RAPPORT_ORGANISATION_20260711.md", "RGPD_Articles7_9_82.md"}
lois_paths = []
for root, _, files in os.walk(os.path.join(REPO, "Lois")):
    for fn in files:
        if not fn.endswith(".md"):
            continue
        if fn.upper() == "README.md":
            continue
        rel = os.path.relpath(os.path.join(root, fn), os.path.join(REPO, "Lois"))
        lois_paths.append("Lois/" + rel)
# on retire les meta non-juridiques
lois_paths = [p for p in lois_paths if os.path.basename(p) not in meta]

def pourvoi(s):
    m = re.search(r"(\d{2})[-.](\d{2})\.(\d{3})", s)
    if m:
        return m.group(1) + m.group(2) + m.group(3)
    return None

def article_key(s):
    s = s.lower().replace(" ", "_")
    m = re.search(r"([a-z]?\d{1,4}[-_]\d{1,4})", s)
    if m:
        return m.group(1).replace("_", "-")
    m = re.search(r"(\d{3,4})", s)
    return m.group(1) if m else s.lower()

lois_pourvois = {pourvoi(os.path.basename(p)): p for p in lois_paths if pourvoi(os.path.basename(p))}
lois_arts = {article_key(os.path.basename(p)): p for p in lois_paths}

matched_lois = set()
for s in sheet_raw:
    pv = pourvoi(s)
    if pv and pv in lois_pourvois:
        matched_lois.add(lois_pourvois[pv]); continue
    ak = article_key(s)
    if ak in lois_arts:
        matched_lois.add(lois_arts[ak]); continue
    if ak in ("263", "121-1", "143-2"):  # variantes etendues deja partielles
        # marquer le fichier de base comme present
        base = {"263": "263", "121-1": "121-1", "143-2": "143-2"}[ak]
        if base in lois_arts:
            matched_lois.add(lois_arts[base])

missing = [p for p in lois_paths if p not in matched_lois]

# dans le Sheet mais absentes de Lois/
really_missing_in_lois = []
for s in sheet_raw:
    pv = pourvoi(s); ak = article_key(s)
    if pv and pv in lois_pourvois: continue
    if ak in lois_arts: continue
    if ak in ("263", "121-1", "143-2"): continue
    really_missing_in_lois.append(s)

# 3) rapport
L = []
L.append("---")
L.append(f'title: "Comparaison Lois/ vs Google Sheet (sources juridiques)"')
L.append(f'date: "{datetime.date.today().isoformat()}"')
L.append('type: rapport')
L.append("---")
L.append("")
L.append("# Comparaison : dossier `Lois/` vs Google Sheet des sources juridiques")
L.append("")
L.append(f"Sheet analysé : https://docs.google.com/spreadsheets/d/{SHEET_ID}")
L.append("")
L.append(f"- **Sheet** : {len(sheet_raw)} références (lignes 3+ du Sheet).")
L.append(f"- **Dossier `Lois/`** : {len(lois_paths)} fichiers juridiques pertinents (hors README/méta/compta).")
L.append(f"- **Présentes dans les deux** : {len(matched_lois)}.")
L.append(f"- **Dans `Lois/` mais ABSENTES du Sheet (à ajouter)** : **{len(missing)}**.")
L.append("")
L.append("## Ce qui manque dans le Sheet (fichiers `Lois/` à ajouter)")
L.append("")
for p in sorted(missing):
    L.append(f"- {p}")
L.append("")
L.append("## Dans le Sheet mais absentes de `Lois/` (à créer dans `Lois/`)")
L.append("")
for s in really_missing_in_lois:
    L.append(f"- {s}")
L.append("")
open(OUT, "w", encoding="utf-8").write("\n".join(L))
print(f"Sheet refs: {len(sheet_raw)}")
print(f"Lois pertinents: {len(lois_paths)}")
print(f"Dans les deux: {len(matched_lois)}")
print(f"MANQUANTS dans Sheet (Lois->ajouter): {len(missing)}")
print(f"Dans Sheet mais absentes de Lois: {len(really_missing_in_lois)}")
print(f"Rapport: {OUT}")
