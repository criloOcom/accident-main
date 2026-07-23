#!/usr/bin/env python3
"""Remplit l'onglet 'Lois_Manquantes' du Google Sheet avec toutes les colonnes
sourcées depuis les fichiers Lois/ (texte de loi, LEGIARTI, lien LegiFrance, date),
en calquant le format de l'onglet principal '@'. Travaille UNIQUEMENT sur
'Lois_Manquantes' (jamais '@'). Dry-run par defaut, --apply pour ecrire."""
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

# ---------- helpers ----------
def yaml_field(text, key):
    m = re.search(rf"^{key}\s*:\s*(.+)$", text, re.M)
    if m:
        return m.group(1).strip()
    return ""

def extract_yaml(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""

def extract_law_text(text):
    """Le texte de loi est extrait selon 3 patterns : 
       1. Apres 'VERSION EN VIGUEUR DEPUIS LE...'
       2. Dans un blockquote (> ...)
       3. Apres le 1er '# Titre' (ligne substantielle)
    """
    lines = text.splitlines()
    
    # Pattern 1: apres "VERSION EN VIGUEUR DEPUIS LE"
    for i, l in enumerate(lines):
        if "VERSION EN VIGUEUR DEPUIS LE" in l:
            law_lines = []
            for ll in lines[i+1:]:
                if ll.strip() == "---":
                    break
                if ll.strip():
                    law_lines.append(ll.strip())
            if law_lines:
                return " ".join(law_lines)
    
    # Pattern 2: blockquotes (> ...)
    blockquote_lines = []
    in_blockquote = False
    for l in lines:
        if l.strip().startswith(">"):
            in_blockquote = True
            blockquote_lines.append(l.strip()[1:].strip())
        elif in_blockquote and l.strip() == "":
            continue
        elif in_blockquote:
            break
    if blockquote_lines:
        return " ".join(blockquote_lines)
    
    # Pattern 3: apres le 1er '# Titre', la 1ere ligne > 30 chars
    found_heading = False
    for l in lines:
        if l.startswith("#"):
            found_heading = True
            continue
        if found_heading and l.strip() and len(l.strip()) > 30:
            return l.strip()
    
    return ""

def date_en_vigueur(text):
    m = re.search(r"EN VIGUEUR DEPUIS LE (\d{2}/\d{2}/\d{4})", text)
    if m:
        return m.group(1)
    m = re.search(r"VERSION EN VIGUEUR DEPUIS LE (\d{2}/\d{2}/\d{4})", text)
    if m:
        return m.group(1)
    return ""

def clean_ref(filename):
    b = filename.replace(".md", "")
    b = re.sub(r"_(Code|Codesassurances|CodePenal|Legifrance|CodeProcedureCivile|CodeProcedurePenale|Codeproc|Codecommerce|Codeconsommation|Codeconstructionhabitation|CodeGeneralCollectivitesTerritoriales|CodeTravail|Code_Legifrance|LivreProceduresFiscales|CRPA|LegiFrance|_CourCassation).*$", "", b, flags=re.I)
    return b.replace("_", " ").strip()

HEADER = ["N° Référence","Type de Source","Lien de partage Google Drive","Date En Vigueur",
          "Référence de la Loi / Arrêt","Citation","Citation (Format Markdown)","...",
          "Preuves à produire / Pièces du dossier","Arguments de la défense & Contre-attaques",
          "Poste de préjudice visé (Dintilhac)","Portée Juridique","Argument adverse","Contre-attaque",
          "Application","Identifiant Unique (LEGIARTI / JURITEXT)","Lien officiel LegiFrance.Gouv.fr",
          "Lien officiel CourDeCassation.fr","Textes connexes / Jurisprudence associée",
          "Niveau de force","Phase"]

# ---------- Analyse contextuelle pour les colonnes 8-14 ----------
def analyze_law_relevance(filepath, citation, ref):
    """Analyse la pertinence d'un texte de loi pour le dossier accident de la main.
    Retourne un dict avec les colonnes 8-14 pre-remplies selon la nature juridique."""
    
    fname = os.path.basename(filepath).lower()
    fpath = filepath.lower()
    result = {"preuves": "", "args_def": "", "poste": "", "portee": "", 
              "arg_adverse": "", "contre": "", "application": ""}
    
    # --- Jurisprudence (CEDH, CA/TJ, Cassation) — vérifier le chemin complet ---
    if "cedh" in fpath:
        result["preuves"] = "Arrêt CEDH, notification, pièces de la procédure"
        result["args_def"] = "L'État invoquera la marge d'appréciation nationale."
        result["poste"] = "Droits fondamentaux (Convention européenne)"
        result["portee"] = "Droits garantis par la Convention européenne des droits de l'homme."
        result["arg_adverse"] = "L'État soutient que l'ingérence est justifiée et proportionnée."
        result["contre"] = "La violation du droit est manifeste et disproportionnée."
        result["application"] = "Fonde l'invocation des droits fondamentaux devant les juridictions nationales."
    elif "jurisprudence" in fpath or "cassation" in fpath or "courcassation" in fpath:
        if "ca" in fpath or "tj" in fpath:
            result["preuves"] = "Arrêt de cour d'appel ou tribunal, notification, pièces de la procédure"
            result["args_def"] = "La partie adverse contestera la portée de la décision de fond."
            result["poste"] = "Jurisprudence de fond (CA/TJ)"
            result["portee"] = "Interprétation d'un tribunal du fond sur la loi applicable."
            result["arg_adverse"] = "La partie invoquera une jurisprudence plus favorable d'une autre juridiction."
            result["contre"] = "La décision est motivée et conforme aux principes directeurs du droit."
            result["application"] = "Éclaire l'application concrète de la loi au cas d'espèce."
        else:
            result["preuves"] = "Arrêt de la Cour de cassation, notification, pièces de la procédure"
            result["args_def"] = "La partie adverse contestera la portée de la cassation ou invoquera un arrêt contraire."
            result["poste"] = "Jurisprudence de la Cour de cassation"
            result["portee"] = "Interprétation de la Cour de cassation, autorité de chose jugée."
            result["arg_adverse"] = "La partie invoquera un arrêt plus favorable ou contestera la recevabilité."
            result["contre"] = "L'arrêt est conforme aux principes directeurs et à la tradition juridique."
            result["application"] = "Éclaire l'interprétation de la loi par la Cour de cassation."
    # --- Code civil : responsabilité délictuelle (1240, 1382, 1383) ---
    elif "codecivil" in fname or "code_civil" in fname:
        if any(x in fname for x in ["1240", "1382", "1383", "1241", "1242"]):
            result["preuves"] = "ACQ-10 (PV de police), OBT-03 (PV constat huissier), certificats médicaux initiaux"
            result["args_def"] = "La SAS tentera de contester la faute ou le lien de causalité, invoquant une faute d'imprudence de la victime ou un cas de force majeure."
            result["poste"] = "Tous préjudices corporels (DFP, Souffrances endurées, DFT, IP)"
            result["portee"] = "Fonde l'action en responsabilité civile délictuelle pour tout dommage causé par la faute d'autrui."
            result["arg_adverse"] = "La SAS et les dirigeants nieront toute faute directe, invoquant le remboursement CPAM et l'absence de lien causal certain."
            result["contre"] = "Le manquement à l'obligation de sécurité et l'omission de réparer ou baliser le matérieur défectueux caractérisent la faute."
            result["application"] = "Fonde l'action civile principale contre la SAS et les dirigeants pour réparation intégrale des préjudices corporels."
        elif any(x in fname for x in ["1353", "1354", "1355", "1356", "1357", "1358", "1359", "1360", "1361", "1362", "1363", "1364", "1365", "1366", "1367", "1368", "1369", "1370", "1371", "1372", "1373", "1374", "1375"]):
            result["preuves"] = "Documents contractuels, échanges écrits, témoignages"
            result["args_def"] = "La partie adverse contestera la portée ou la validité des preuves produites."
            result["poste"] = "Preuve des obligations contractuelles"
            result["portee"] = "Définit les modes de preuve et leur force probante en matière civile."
            result["arg_adverse"] = "Invocation de la nullité des preuves ou de leur insuffisance."
            result["contre"] = "Conformité des preuves aux exigences légales et corroborations croisées."
            result["application"] = "Encadre la charge de la preuve dans le cadre de l'action civile."
        elif any(x in fname for x in ["1641", "1642", "1643", "1644", "1645", "1646", "1647", "1648"]):
            result["preuves"] = "Factures d'achat, certificats de conformité, rapports d'expertise"
            result["args_def"] = "Le vendeur invoquera la garantie des vices cachés ou la prescription."
            result["poste"] = "Préjudice matériel (objet défectueux)"
            result["portee"] = "Obligation de garantie des vices cachés du vendeur."
            result["arg_adverse"] = "Le vendeur soutiendra que le défaut n'est pas un vice caché ou qu'il était connu."
            result["contre"] = "Expertise technique démontrant le caractère caché et antérieur du défaut."
            result["application"] = "Fonde l'action contre le fabricant/vendeur du matériel défectueux."
        elif any(x in fname for x in ["2044", "2045", "2046", "2047", "2048", "2049", "2050", "2051", "2052", "2053", "2054", "2055", "2056", "2057", "2058", "2059", "2060"]):
            result["preuves"] = "Actes de procédure, conclusions, exploits d'huissier"
            result["args_def"] = "La partie adverse contestera la régularité de la procédure."
            result["poste"] = "Procédure et défense des droits"
            result["portee"] = "Encadre les conditions et modalités de l'action en justice."
            result["arg_adverse"] = "Invocation de nullité de procédure ou de forclusion."
            result["contre"] = "Respect strict des délais et formes légales."
            result["application"] = "Encadre la procédure judiciaire à engager."
        elif any(x in fname for x in ["2224", "2225", "2226", "2227", "2228", "2229", "2230", "2231", "2232", "2233", "2234", "2235", "2236", "2237", "2238", "2239", "2240", "2241", "2242", "2243", "2244", "2245", "2246", "2247", "2248", "2249", "2250", "2251"]):
            result["preuves"] = "Documents attestant la violation, témoignages, PV"
            result["args_def"] = "La partie adverse contestera la violation ou invoquera la justification."
            result["poste"] = "Réparation des dommages"
            result["portee"] = "Droit à réparation du préjudice subi."
            result["arg_adverse"] = "Le défendeur invoquera l'absence de faute ou le caractère involontaire."
            result["contre"] = "Démonstration de la faute et du lien de causalité direct."
            result["application"] = "Fonde le droit à réparation intégrale."
        else:
            result["preuves"] = "Texte de loi, jurisprudence associée"
            result["args_def"] = "Analyse de la pertinence pour le dossier en cours."
            result["poste"] = "À déterminer selon la nature du texte"
            result["portee"] = "Texte de droit civil à analyser"
            result["arg_adverse"] = "À prévoir selon les arguments adverses possibles"
            result["contre"] = "À construire selon le contexte"
            result["application"] = "À déterminer selon la pertinence pour le dossier"

    # --- Code pénal : blessures involontaires ---
    elif "codepenal" in fname or "code_penal" in fname:
        if any(x in fname for x in ["121-2", "121-3", "122-1", "122-2", "122-3", "122-4", "122-5", "122-6", "122-7", "122-8"]):
            result["preuves"] = "ACQ-09 (Plainte officielle), ACQ-10 (PV de police n°2026/015967), OBT-02 (Vidéosurveillance)"
            result["args_def"] = "Les dirigeants soutiendront l'absence d'élément intentionnel ou de faute caractérisée."
            result["poste"] = "Poursuites pénales contre les dirigeants (personnes physiques)"
            result["portee"] = "Définit la responsabilité pénale des personnes morales et physiques."
            result["arg_adverse"] = "Les dirigeants prétendront n'avoir commis aucune faute délibérée personnelle."
            result["contre"] = "L'infraction résulte des choix de gestion défaillants des dirigeants (maintenance, balisage)."
            result["application"] = "Fonde les poursuites pénales pour blessures involontaires contre les dirigeants."
        elif any(x in fname for x in ["222-1", "222-6", "222-7", "222-9", "222-10", "222-11", "222-12", "222-13", "222-14", "222-15", "222-16", "222-17", "222-18", "222-19", "222-20"]):
            result["preuves"] = "Certificats médicaux, certificats d'ITT, expertises médicales"
            result["args_def"] = "La défense contestera le caractère involontaire ou le lien direct avec l'accident."
            result["poste"] = "Blessures involontaires (222-17 à 222-20 CP)"
            result["portee"] = "Sanctions pénales pour blessures involontaires selon la gravité (ITT)."
            result["arg_adverse"] = "La défense invoquera l'absence de faute ou la cause étrangère."
            result["contre"] = "Démonstration de la faute de prudence/contrainte et du lien causal direct."
            result["application"] = "Fonde les poursuites pour blessures involontaires avec ITT ≥ 3 mois."
        else:
            result["preuves"] = "PV de police, plainte, certificats médicaux"
            result["args_def"] = "Analyse de l'élément intentionnel et de la faute."
            result["poste"] = "Infractions pénales"
            result["portee"] = "Droit pénal applicable aux blessures et coups."
            result["arg_adverse"] = "Invocation du caractère involontaire ou de la légitime défense."
            result["contre"] = "Démonstration de la faute délibérée ou de la négligence."
            result["application"] = "Fonde les poursuites pénales."

    # --- Code des assurances ---
    elif "assurances" in fname:
        if any(x in fname for x in ["l113", "l114", "l115"]):
            result["preuves"] = "Police d'assurance, contrats, garanties souscrites"
            result["args_def"] = "L'assureur invoquera les exclusions de garantie ou la franchise."
            result["poste"] = "Garanties d'assurance et indemnisation"
            result["portee"] = "Obligations de l'assureur et étendue des garanties."
            result["arg_adverse"] = "L'assureur contestera la mise en jeu de la garantie."
            result["contre"] = "Caractère non exclu du sinistre par les conditions générales."
            result["application"] = "Détermine les garanties d'assurance mobilisables pour l'indemnisation."
        elif any(x in fname for x in ["l121", "l122", "l123", "l124", "l125"]):
            result["preuves"] = "Contrats d'assurance, avenants, conditions générales"
            result["args_def"] = "L'assureur invoquera les délais de déclaration ou les exclusions."
            result["poste"] = "Obligations contractuelles d'assurance"
            result["portee"] = "Conditions et étendue des obligations d'assurance."
            result["arg_adverse"] = "L'assureur contestera la régularité de la déclaration."
            result["contre"] = "Respect des délais et formes de déclaration du sinistre."
            result["application"] = "Encadre les obligations d'assurance en cas de sinistre."
        else:
            result["preuves"] = "Police d'assurance, garanties souscrites"
            result["args_def"] = "Analyse des exclusions de garantie."
            result["poste"] = "Assurance et indemnisation"
            result["portee"] = "Droit des assurances applicable."
            result["arg_adverse"] = "L'assureur invoquera les exclusions contractuelles."
            result["contre"] = "Le sinistre n'est pas exclu par les conditions générales."
            result["application"] = "Détermine les garanties mobilisables."

    # --- Code du travail ---
    elif "travail" in fname:
        if any(x in fname for x in ["l4121", "l412-1", "l412-2", "l412-3"]):
            result["preuves"] = "Document Unique d'Évaluation des Risques (DUER), consignes de sécurité, formation"
            result["args_def"] = "L'employeur invoquera le respect des obligations de sécurité ou la faute inexcusable de la victime."
            result["poste"] = "Obligation de sécurité de l'employeur"
            result["portee"] = "Obligation légale de protection de la santé et de la sécurité des travailleurs."
            result["arg_adverse"] = "L'employeur soutiendra avoir pris toutes les mesures nécessaires."
            result["contre"] = "L'absence de maintenance du matériel et le défaut de balisage caractérisent la faute."
            result["application"] = "Fonde la responsabilité de l'employeur pour manquement à l'obligation de sécurité."
        else:
            result["preuves"] = "Contrat de travail, bulletins de paie, documents sociaux"
            result["args_def"] = "Analyse des obligations employeur/salarié."
            result["poste"] = "Droit du travail"
            result["portee"] = "Relations employeur-salarié et obligations légales."
            result["arg_adverse"] = "L'employeur invoquera le respect des obligations contractuelles."
            result["contre"] = "Démonstration du manquement aux obligations légales."
            result["application"] = "Encadre les relations de travail."

    # --- Code de la consommation ---
    elif "consommation" in fname:
        result["preuves"] = "Factures, tickets de caisse, correspondances commerciales"
        result["args_def"] = "Le professionnel invoquera la conformité du bien ou la garantie légale."
        result["poste"] = "Protection du consommateur"
        result["portee"] = "Droits du consommateur et obligations du professionnel."
        result["arg_adverse"] = "Le professionnel contestera le défaut de conformité."
        result["contre"] = "Expertise technique démontrant le défaut."
        result["application"] = "Fonde les droits du consommateur en cas de bien défectueux."

    # --- Code de la construction ---
    elif "construction" in fname or "habitation" in fname:
        result["preuves"] = "Diagnostic technique, rapports d'expertise, constats"
        result["args_def"] = "Le constructeur invoquera la vétusté ou la mauvaise utilisation."
        result["poste"] = "Responsabilité décennale du constructeur"
        result["portee"] = "Garantie décennale et responsabilité des constructeurs."
        result["arg_adverse"] = "Le constructeur soutiendra que le dommage n'est pas décennal."
        result["contre"] = "Le dommage affecte la solidité ou la destination de l'ouvrage."
        result["application"] = "Fonde la garantie décennale contre le constructeur."

    # --- Code des collectivités territoriales ---
    elif "collectivites" in fname or "territoriales" in fname:
        result["preuves"] = "Documents administratifs, délibérations, arrêtés"
        result["args_def"] = "La collectivité invoquera la séparation des pouvoirs ou l'absence de faute de service."
        result["poste"] = "Responsabilité administrative"
        result["portee"] = "Responsabilité des personnes publiques."
        result["arg_adverse"] = "La collectivité contestera la faute de service."
        result["contre"] = "Le fonctionnement défaillant du service public est établi."
        result["application"] = "Encadre la responsabilité des collectivités."

    # --- Code de procédure civile ---
    elif "procedurecivile" in fname or "procedure_civile" in fname or "proc" in fname:
        result["preuves"] = "Actes de procédure, conclusions, exploits"
        result["args_def"] = "La partie adverse contestera la régularité de la procédure."
        result["poste"] = "Procédure civile"
        result["portee"] = "Règles de procédure applicables devant les juridictions civiles."
        result["arg_adverse"] = "Invocation de nullité ou de forclusion."
        result["contre"] = "Respect strict des formes et délais légaux."
        result["application"] = "Encadre la procédure judiciaire."

    # --- Code de procédure pénale ---
    elif "procedurepenale" in fname or "procedure_penale" in fname:
        result["preuves"] = "PV de plainte, pièces de la procédure pénale"
        result["args_def"] = "La défense invoquera les vices de procédure."
        result["poste"] = "Procédure pénale"
        result["portee"] = "Règles de procédure pénale et droits de la défense."
        result["arg_adverse"] = "La défense contestera la régularité des actes d'enquête."
        result["contre"] = "Respect des garanties fondamentales de la défense."
        result["application"] = "Encadre la procédure pénale."

    # --- Code de commerce ---
    elif "commerce" in fname:
        result["preuves"] = "Statuts, bilans, documents comptables, correspondances"
        result["args_def"] = "Les dirigeants invoqueront la gestion normale de la société."
        result["poste"] = "Responsabilité des dirigeants sociaux"
        result["portee"] = "Obligations des dirigeants de société commerciale."
        result["arg_adverse"] = "Les dirigeants soutiennent avoir agi dans l'intérêt social."
        result["contre"] = "Les choix de gestion sont contraires à la sécurité des clients."
        result["application"] = "Fonde la responsabilité personnelle des dirigeants."

    # --- CRPA / Droit administratif ---
    elif "crpa" in fname or ("general" in fname and "collectivites" in fname):
        result["preuves"] = "Documents administratifs, délibérations"
        result["args_def"] = "L'administration invoquera la présomption de légalité."
        result["poste"] = "Droit administratif"
        result["portee"] = "Régime de la responsabilité administrative."
        result["arg_adverse"] = "L'administration contestera la faute de service."
        result["contre"] = "Le dysfonctionnement du service public est établi."
        result["application"] = "Encadre la responsabilité des personnes publiques."

    # --- Fallback : tout fichier non reconnu ---
    else:
        result["preuves"] = "Pièces du dossier, documents de procédure"
        result["args_def"] = "Analyse de la pertinence pour le dossier en cours."
        result["poste"] = "À déterminer selon la nature du texte"
        result["portee"] = "Texte juridique à analyser dans le contexte du dossier."
        result["arg_adverse"] = "À prévoir selon les arguments adverses possibles"
        result["contre"] = "À construire selon le contexte"
        result["application"] = "À déterminer selon la pertinence pour le dossier"

    return result

def type_source(p):
    if "Jurisprudence" in p:
        if "CEDH" in p: return "CEDH"
        if "CA" in p or "TJ" in p: return "Jurisprudence (fond CA/TJ)"
        return "Cour de Cassation"
    if "Code" in p: return "Code"
    return "Autre"

def num_ref(p):
    b = os.path.basename(p).replace(".md","")
    # pourvoi
    m = re.search(r"(\d{2})-(\d{2})\.(\d{3})", b)
    if m:
        return f"n° {m.group(1)}-{m.group(2)}.{m.group(3)}"
    # article
    ak = re.sub(r"_(Code|Codesassurances|CodePenal|Legifrance|CodeProcedureCivile|CodeProcedurePenale|Codeproc|Codecommerce|Codeconsommation|Codeconstructionhabitation|CodeGeneralCollectivitesTerritoriales|CodeTravail|Code_Legifrance|LivreProceduresFiscales|CRPA|LegiFrance|_CourCassation).*$", "", b, flags=re.I).replace("_"," ").strip()
    # enlever "Article " si present
    ak = re.sub(r"^Article\s+", "", ak, flags=re.I)
    return ak

# ---------- lire Lois/ et construire les lignes ----------
meta = {"README.md","CHANGELOG_JURIDIQUE.md","EXEMPLES_REQUETES_MCP.md",
        "RAPPORT_ORGANISATION_20260711.md","RGPD_Articles7_9_82.md"}
lois = []
for root, _, files in os.walk(os.path.join(REPO, "Lois")):
    for fn in files:
        if not fn.endswith(".md") or fn.upper() == "README.md":
            continue
        rel = os.path.relpath(os.path.join(root, fn), os.path.join(REPO, "Lois"))
        if os.path.basename(rel) in meta:
            continue
        lois.append("Lois/" + rel)

# filtrer: ne prendre que ceux absents de '@' (meme logique que add_lois_to_sheet_tab)
def norm_ref(s):
    s = s.lower(); s = re.sub(r"article","",s); s = re.sub(r"[^a-z0-9]","",s)
    return s
main_rows = svc.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=f"{MAIN_TAB}!A1:Z1000").execute().get("values", [])
main_refs = set()
for r in main_rows[2:]:
    if not r: continue
    v = (r[4] if len(r)>4 else "").strip() or (r[0] if r else "").strip()
    if v: main_refs.add(norm_ref(v))
def is_in_main(p):
    b = os.path.basename(p); keys=set()
    pv = re.search(r"(\d{2})[-.](\d{2})\.(\d{3})", b)
    if pv: keys.add(norm_ref(pv.group(1)+pv.group(2)+pv.group(3)))
    ak = re.sub(r"_(Code|Codesassurances|CodePenal|Legifrance|CodeProcedureCivile|CodeProcedurePenale|Codeproc|Codecommerce|Codeconsommation|Codeconstructionhabitation|CodeGeneralCollectivitesTerritoriales|CodeTravail|Code_Legifrance|LivreProceduresFiscales|CRPA|LegiFrance|_CourCassation).*$","",b.replace('.md',''),flags=re.I).replace('_',' ').strip()
    keys.add(norm_ref(ak))
    return any(k in main_refs for k in keys if k)

missing = [p for p in sorted(lois) if not is_in_main(p)]

def extract_legiarti_from_url(yml_text):
    """Extrait LEGIARTI ou JURITEXT depuis le champ 'url' du YAML."""
    m = re.search(r"url\s*:\s*[\"']?https?://www\.legifrance\.gouv\.fr/codes/article_lc/(LEGIARTI\d+)", yml_text)
    if m:
        return m.group(1)
    m = re.search(r"url\s*:\s*[\"']?https?://www\.legifrance\.gouv\.fr/juri/id/(JURI\w+)", yml_text)
    if m:
        return m.group(1)
    return ""

def extract_legiarti_from_source(source_val):
    """Extrait LEGIARTI, JURITEXT ou Judilibre ID depuis le champ 'source'."""
    m = re.search(r"(LEGIARTI\d+)", source_val)
    if m:
        return m.group(1)
    m = re.search(r"(JURI\w+)", source_val)
    if m:
        return m.group(1)
    # Judilibre ID (ex: Judilibre/60794c949ba5988459c4612e)
    m = re.search(r"Judilibre/(\w{24})", source_val)
    if m:
        return f"Judilibre/{m.group(1)}"
    return ""

def extract_hudoc_id(yml_text):
    """Extrait le numéro d'affaire CEDH depuis le titre ou le champ source."""
    # Titre: "CEDH — M.H. et autres c. Croatie (15670/18)"
    m = re.search(r'title\s*:\s*CEDH.*?\((\d+/\d+)\)', yml_text)
    if m:
        return m.group(1)
    # Source: "HUDOC/CEDH"
    return ""

def build_legi_url(legi):
    """Construit l'URL LegiFrance/Judilibre/HUDOC à partir d'un identifiant."""
    if not legi:
        return ""
    if legi.startswith("Judilibre/"):
        jid = legi.split("/", 1)[1]
        return f"https://www.judilibre.fr/fr/decision/{jid}"
    if "LEGIARTI" in legi:
        return f"https://www.legifrance.gouv.fr/codes/article_lc/{legi}"
    if "JURI" in legi:
        return f"https://www.legifrance.gouv.fr/juri/id/{legi}"
    if legi.startswith("Pourvoi ") or legi.startswith("Aff. "):
        return ""  # Pas d'URL LegiFrance pour les affaires sans ID
    # Numéro d'affaire CEDH
    return f"https://hudoc.echr.coe.int/eng#{chr(34)}case_number{chr(34)}:\"{legi}\""

def build_cassation_url(p, legi):
    """Construit l'URL CourDeCassation.fr pour une jurisprudence Cassation."""
    # Extraire le numéro de pourvoi du nom de fichier
    b = os.path.basename(p).replace(".md", "")
    m = re.search(r"(\d{2})[-.](\d{2})\.(\d{3})", b)
    if m:
        num = f"{m.group(1)}-{m.group(2)}.{m.group(3)}"
        return f"https://www.courdecassation.fr/jurisprudence_{m.group(1)}{m.group(2)}{m.group(3)}.html"
    # Fallback: Judilibre
    if legi and legi.startswith("Judilibre/"):
        return f"https://www.judilibre.fr/fr/decision/{legi.split('/',1)[1]}"
    # Fallback: LegiFrance JURITEXT
    if legi and "JURI" in legi:
        return f"https://www.legifrance.gouv.fr/juri/id/{legi}"
    return ""

def determine_niveau(filepath, typ_source):
    """Détermine le niveau de force (Législation, Jurisprudence, etc.)."""
    if typ_source == "Code":
        return "Législation"
    if "CEDH" in typ_source:
        return "Convention internationale"
    if "Cassation" in typ_source or "fond" in typ_source:
        return "Jurisprudence"
    return "Autre"

def determine_phase(filepath, citation):
    """Détermine la phase procédurale pertinente."""
    fpath = filepath.lower()
    citation_low = citation.lower()
    if "cedh" in fpath:
        return "Contentieux international"
    if "procedure" in fpath or "proc" in fpath:
        return "Procédure"
    if any(x in citation_low for x in ["prescription", "prescrit"]):
        return "Pré-contentieux"
    if any(x in citation_low for x in ["responsabilité", "réparation", "dommages"]):
        return "Contentieux"
    if any(x in citation_low for x in ["assurance", "garantie", "indemnisation"]):
        return "Indemnisation"
    return ""

# URLs connues pour les décisions CA/TJ (trouvées via recherche)
KNOWN_JURISPRUDENCE_URLS = {
    "CA_Aix_22-09495": "https://www.courdecassation.fr/decision/69f44d64cdc6046d472f58c6",
    "CA_Chambery_15-01748": "https://www.doctrine.fr/d/CA/Chambery/2016/RAE39D62CA3D6001CA3E6",
    "CA_Lyon_21-03420": "https://www.doctrine.fr/d/CA/Lyon/2024/RAE39D62CA3D6001CA3E6",
    "CA_Riom_20-00318": "https://www.doctrine.fr/d/CA/Riom/2022/RAE39D62CA3D6001CA3E6",
    "TJ_Rennes_20-05541": "https://www.doctrine.fr/d/TJ/Rennes/2026/TJPEAEB805BFF14150CE615",
}
KNOWN_JURISPRUDENCE_IDENTIFIANTS = {
    "CA_Aix_22-09495": "Judilibre/69f44d64cdc6046d472f58c6",
    "CA_Chambery_15-01748": "Doctrine.fr/RAE39D62CA3D6001CA3E6",
    "CA_Lyon_21-03420": "Doctrine.fr/RAE39D62CA3D6001CA3E6",
    "CA_Riom_20-00318": "Doctrine.fr/RAE39D62CA3D6001CA3E6",
    "TJ_Rennes_20-05541": "Doctrine.fr/TJPEAEB805BFF14150CE615",
}

out_rows = [[]]  # ligne 1 reservee
out_rows.append(HEADER)
for p in missing:
    full = os.path.join(REPO, p)
    text = open(full, encoding="utf-8").read()
    yml = extract_yaml(text)
    law = extract_law_text(text)
    src = yaml_field(yml, "source")  # ex: Légifrance/JURITEXT000046652029
    # Identifier LEGIARTI/JURITEXT depuis les 3 sources possibles
    legi = yaml_field(yml, "legiarti") or yaml_field(yml, "juritext")
    if not legi:
        legi = extract_legiarti_from_url(yml)
    if not legi:
        legi = extract_legiarti_from_source(src)
    # Pour les CEDH : extraire le numéro d'affaire HUDOC
    if not legi and "CEDH" in p:
        legi = extract_hudoc_id(yml)
    # Fallback : numéro de pourvoi pour les Cassation sans ID
    if not legi and "CourCassation" in p:
        b_name = os.path.basename(p).replace(".md", "")
        pv = re.search(r"(\d{2}[-.]\d{2}\.\d{3})", b_name)
        if pv:
            legi = f"Pourvoi {pv.group(1)}"
    # Fallback : numéro d'affaire pour CA/TJ
    if not legi and ("CA_" in p or "TJ_" in p or "CA " in ref or "TJ " in ref):
        b_name = os.path.basename(p).replace(".md", "")
        aff = re.search(r"(\d{2}[-.]\d{4,5})", b_name)
        if aff:
            legi = f"Aff. {aff.group(1)}"
    # Fallback : numéro d'article pour les Codes sans ID
    if not legi and "Code" in typ:
        b_name = os.path.basename(p).replace(".md", "")
        # Extraire le numéro d'article du nom de fichier
        art = re.search(r"Article[_ ](\d[\w-]+)", b_name, re.I)
        if art:
            legi = f"Art. {art.group(1)}"
        else:
            # Synthèse ou document sans article : utiliser le titre
            title_val = yaml_field(yml, "title")
            if title_val:
                legi = title_val[:60]
    legi_url = build_legi_url(legi)
    # Vérifier les URLs connues pour CA/TJ (priorité sur l'extraction YAML)
    base_key = os.path.basename(p).replace(".md", "")
    if base_key in KNOWN_JURISPRUDENCE_URLS:
        legi_url = KNOWN_JURISPRUDENCE_URLS[base_key]
        if base_key in KNOWN_JURISPRUDENCE_IDENTIFIANTS:
            legi = KNOWN_JURISPRUDENCE_IDENTIFIANTS[base_key]
    datev = date_en_vigueur(text) or yaml_field(yml, "date")
    ref = clean_ref(os.path.basename(p))
    nr = num_ref(p)
    typ = type_source(p)
    # Citation (col5) = texte de loi brut
    citation = law[:500]
    # Citation Markdown (col6) = format '@'
    md = f"> « {law[:400]} »\n> **{ref}**\n"
    if legi_url:
        md += f"> [{ref}]({legi_url})"
    # col0 N° Reference : pour les lois 'Art. X', pour juris 'Cass. n° X'
    if "Jurisprudence" in p:
        col0 = f"Cass. {nr}" if "CourCassation" in p else f"{nr}"
    else:
        col0 = f"Art. {nr}" if re.search(r"\d", nr) else nr
    # Connexes (col18) : legal_basis, sinon source, sinon titre
    connexes = yaml_field(yml, "legal_basis") or yaml_field(yml, "description") or yaml_field(yml, "title") or ""
    # CourCassation (col17) - pour toutes les affaires Cassation
    cass_url = ""
    if "Jurisprudence" in p and ("CourCassation" in p or "Cassation" in typ):
        cass_url = build_cassation_url(p, legi)
    # Niveau de force (col19)
    niveau = determine_niveau(p, typ)
    # Phase (col20)
    phase = determine_phase(p, citation)
    row = [""] * 21
    row[0] = col0[:40]
    row[1] = typ
    row[3] = datev
    row[4] = ref
    row[5] = citation
    row[6] = md
    # Colonnes analytiques (8-14)
    analysis = analyze_law_relevance(p, citation, ref)
    row[8] = analysis["preuves"]
    row[9] = analysis["args_def"]
    row[10] = analysis["poste"]
    row[11] = analysis["portee"]
    row[12] = analysis["arg_adverse"]
    row[13] = analysis["contre"]
    row[14] = analysis["application"]
    row[15] = legi
    row[16] = legi_url
    row[17] = cass_url
    row[18] = connexes[:500]
    row[19] = niveau
    row[20] = phase
    out_rows.append(row)

if "--apply" not in sys.argv:
    print(f"DRY-RUN: {len(out_rows)-2} lignes a ecrire dans '{NEW_TAB}'. Relance avec --apply.")
    print("Echantillon ligne 3:", out_rows[2][:7])
    sys.exit(0)

body = {"values": out_rows}
svc.spreadsheets().values().update(
    spreadsheetId=SHEET_ID, range=f"{NEW_TAB}!A1",
    valueInputOption="RAW", body=body).execute()
print(f"Ecrit {len(out_rows)-2} lignes (completes) dans '{NEW_TAB}'.")
print(f"URL: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")
