#!/usr/bin/env python3
"""Cree un onglet 'Lois_Manquantes' dans le Google Sheet et y ajoute les fichiers
Lois/ absents de l'onglet principal '@'. Travaille UNIQUEMENT sur le nouvel onglet
(aucune ecriture sur '@'). Souverain via 'souverain'."""
import os, re, sys
sys.path.insert(0, os.path.expanduser("~/.opencode"))
from souverain import get_credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SHEET_ID = "14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ"
REPO = "/home/crilocom/accident-main"
NEW_TAB = "Lois_Manquantes"
MAIN_TAB = "'@'"

creds = get_credentials()
if not creds.valid:
    creds.refresh(Request())
svc = build("sheets", "v4", credentials=creds)

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

def norm_ref(s):
    s = s.lower()
    s = re.sub(r"article", "", s)
    s = re.sub(r"[^a-z0-9]", "", s)
    # enlever les prefixes de code residuels
    s = s.replace("l", "").replace("r", "")  # ex: 'l2111' -> '2111', 'r1432' -> '1432'
    return s

# 1) lire l'onglet principal pour connaitre ce qui est deja present
main_rows = svc.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range=f"{MAIN_TAB}!A1:Z1000").execute().get("values", [])
main_refs = set()
for r in main_rows[2:]:
    if not r:
        continue
    v = (r[4] if len(r) > 4 else "").strip() or (r[0] if r else "").strip()
    if v:
        main_refs.add(norm_ref(v))
for r in main_rows[2:]:
    if r and r[0].strip():
        main_refs.add(norm_ref(r[0]))

# 2) lister Lois/ (hors README/meta)
meta = {"README.md", "CHANGELOG_JURIDIQUE.md", "EXEMPLES_REQUETES_MCP.md",
        "RAPPORT_ORGANISATION_20260711.md", "RGPD_Articles7_9_82.md"}
lois = []
for root, _, files in os.walk(os.path.join(REPO, "Lois")):
    for fn in files:
        if not fn.endswith(".md") or fn.upper() == "README.md":
            continue
        rel = os.path.relpath(os.path.join(root, fn), os.path.join(REPO, "Lois"))
        if os.path.basename(rel) in meta:
            continue
        lois.append("Lois/" + rel)

def is_in_main(p):
    b = os.path.basename(p)
    keys = set()
    pv = pourvoi(b)
    if pv:
        keys.add(norm_ref(pv))
    ak = article_key(b)
    keys.add(norm_ref(ak))
    ref = re.sub(r"_(Code|Codesassurances|CodePenal|Legifrance|CodeProcedureCivile|CodeProcedurePenale|Codeproc|Codecommerce|Codeconsommation|Codeconstructionhabitation|CodeGeneralCollectivitesTerritoriales|CodeTravail|Code_Legifrance|LivreProceduresFiscales|CRPA|LegiFrance|_CourCassation).*$", "", b.replace(".md",""), flags=re.I)
    ref = ref.replace("_", " ").strip()
    keys.add(norm_ref(ref))
    keys.add(norm_ref(ref.replace(" ", "")))
    return any(k in main_refs for k in keys if k)

missing = [p for p in sorted(lois) if not is_in_main(p)]
print(f"Fichiers Lois/ totaux: {len(lois)}")
print(f"Deja dans l'onglet principal '@': {len(lois)-len(missing)}")
print(f"A ajouter dans '{NEW_TAB}': {len(missing)}")

if "--apply" not in sys.argv:
    print("DRY-RUN: aucune ecriture (relance avec --apply pour ecrire).")
    sys.exit(0)

# 3) creer l'onglet s'il n'existe pas
md = svc.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
titles = [s["properties"]["title"] for s in md.get("sheets", [])]
if NEW_TAB not in titles:
    svc.spreadsheets().batchUpdate(
        spreadsheetId=SHEET_ID,
        body={"requests": [{"addSheet": {"properties": {"title": NEW_TAB}}}]}).execute()
    print(f"Onglet '{NEW_TAB}' cree.")

# 4) ecrire en-tetes (ligne1 vide reservee, ligne2 libelles) + donnees sur NEW_TAB
HEADER = ["N° Référence","Type de Source","Lien de partage Google Drive","Date En Vigueur",
          "Référence de la Loi / Arrêt","Citation","Citation (Format Markdown)","...",
          "Preuves à produire / Pièces du dossier","Arguments de la défense & Contre-attaques",
          "Poste de préjudice visé (Dintilhac)","Portée Juridique","Argument adverse","Contre-attaque",
          "Application","Identifiant Unique (LEGIARTI / JURITEXT)","Lien officiel LegiFrance.Gouv.fr",
          "Lien officiel CourDeCassation.fr","Textes connexes / Jurisprudence associée",
          "Niveau de force","Phase"]

def type_source(p):
    if "Jurisprudence" in p:
        if "CEDH" in p: return "CEDH"
        if "CA" in p or "TJ" in p: return "Jurisprudence (fond CA/TJ)"
        return "Cour de Cassation"
    if "Code" in p: return "Code"
    return "Autre"

out_rows = [[]]
out_rows.append(HEADER)
for p in missing:
    b = os.path.basename(p).replace(".md", "")
    ref = re.sub(r"_(Code|Codesassurances|CodePenal|Legifrance|CodeProcedureCivile|CodeProcedurePenale|Codeproc|Codecommerce|Codeconsommation|Codeconstructionhabitation|CodeGeneralCollectivitesTerritoriales|CodeTravail|Code_Legifrance|LivreProceduresFiscales|CRPA|LegiFrance|_CourCassation).*$", "", b, flags=re.I)
    ref = ref.replace("_", " ").strip()
    row = [""] * 21
    row[0] = ref[:40]
    row[1] = type_source(p)
    row[4] = ref
    out_rows.append(row)

body = {"values": out_rows}
svc.spreadsheets().values().update(
    spreadsheetId=SHEET_ID, range=f"{NEW_TAB}!A1",
    valueInputOption="RAW", body=body).execute()
print(f"Ecrit {len(out_rows)-2} lignes dans '{NEW_TAB}' (ligne1 reservee, ligne2 libelles).")
print(f"URL: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
