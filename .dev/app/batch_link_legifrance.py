#!/usr/bin/env python3
"""Batch link all legal references to Légifrance URLs inline.

Processes all identified unlinked references + fixes wrong LEGIARTI IDs in ANNEXE B.
Run from project root: python3 .dev/app/batch_link_legifrance.py

EXEMPLES D'UTILISATION MCP:
-----------------------

# Exemple 1: Recherche dans les codes
from mcp_legifrance.server import LegifranceClient
client = LegifranceClient()
result = client.search('responsabilité civile', 'CODE', page_size=10)

# Exemple 2: Recherche jurisprudence
result = client.search('accident salon coiffure', 'JURI', page_size=5)

# Exemple 3: Consultation article spécifique
article = client.consulte_article('LEGIARTI000032041571')

# Exemple 4: Recherche avec Judilibre
from mcp_judilibre.server import JudilibreClient
judilibre = JudilibreClient()
result = judilibre.search('accident travail', chamber='soc', solution='cassation')

Voir Lois/EXEMPLES_REQUETES_MCP.md pour plus d'exemples détaillés.
"""

import re
import os

BASE = "https://www.legifrance.gouv.fr/codes/article_lc"
JURI_BASE = "https://www.legifrance.gouv.fr/juri/id"

LEGIARTI = {
    "1240 C. civ.": "LEGIARTI000032041571",
    "1242 C. civ.": "LEGIARTI000051786000",
    "1231-1 C. civ.": "LEGIARTI000032010123",
    "1641 C. civ.": "LEGIARTI000006441924",
    "1719 C. civ.": "LEGIARTI000020459127",
    "1844-8 C. civ.": "LEGIARTI000006444186",
    "2226 C. civ.": "LEGIARTI000019017112",
    "2226 C. civ. (v2)": "LEGIARTI000019017259",
    "121-3 C. pén.": "LEGIARTI000006417209",
    "121-3 C. pén. (v2)": "LEGIARTI000006417208",
    "222-19 C. pén.": "LEGIARTI000024042643",
    "222-19 C. pén. (v2)": "LEGIARTI000024042635",
    "222-20 C. pén.": "LEGIARTI000024042640",
    "1240 C. civ. (v2)": "LEGIARTI000051787311",
    "475-1 CPP": "LEGIARTI000006576696",
    "475-1 CPP (v2)": "LEGIARTI000044570107",
    "145 CPC": "LEGIARTI000051869339",
    "700 CPC": "LEGIARTI000045268436",
    "700 CPC (v2)": "LEGIARTI000006647394",
    "835 al.2 CPC": "LEGIARTI000042597284",
    "835 al.2 CPC (v2)": "LEGIARTI000051869487",
    "L.111-1 C. consom.": "LEGIARTI000048523650",
    "L.124-3 C. assur.": "LEGIARTI000017735449",
    "706-3 CPP": "LEGIARTI000006577625",
    "706-3 CPP (FGTI)": "LEGIARTI000006418734",
    "706-5 CPP": "LEGIARTI000006577627",
    "L.113-2 C. assur.": "LEGIARTI000035731302",
    "L.211-26 C. assur.": "LEGIARTI000006795644",
    "223-1 C. pén.": "LEGIARTI000006417253",
    "L.223-22 C. com.": "LEGIARTI000006223141",
    "L.223-22 C. assur.": "LEGIARTI000038837071",
    "L.225-251 C. com.": "LEGIARTI000006226329",
    "L.225-251 C. com. (v2)": "LEGIARTI000006447928",
    "L.237-2 C. com.": "LEGIARTI000006230063",
    "R.123-2 C. com.": "LEGIARTI000046073350",
    "R.143-2 CCH": "LEGIARTI000043818941",
    "263 CPC": "LEGIARTI000006410394",
    "Cousin JURI": "JURITEXT000007043322",
    "Costedoat JURI": "JURITEXT000007043704",
    "Crim2014 JURI": "JURITEXT000029014493",
    "Com1993 JURI": "JURITEXT000007030228",
}

def link(url_id, text):
    if url_id.startswith("JURITEXT"):
        return f"[{text}]({JURI_BASE}/{url_id})"
    return f"[{text}]({BASE}/{url_id})"

REPLACEMENTS = [
    # === PRESENTATION Dossier.md specific ===
    (r"(?<!\]\()Article 1242 alinéas 1 et 5 du Code civil",
     link("LEGIARTI000051786000", "Article 1242 alinéas 1 et 5 du Code civil")),
    (r"(?<!\]\()Article 222-20 du Code pénal",
     link("LEGIARTI000024042640", "Article 222-20 du Code pénal")),

    # === SYNTHESE FAQ.md ===
    (r"(?<!\]\()l'article 1231-1 du Code civil",
     link("LEGIARTI000032010123", "l'article 1231-1 du Code civil")),
    (r"(?<!\]\()l'article 1240 du même code",
     link("LEGIARTI000032041571", "l'article 1240 du même code")),
    (r"(?<!\]\()l'article 1641 du Code civil",
     link("LEGIARTI000006441924", "l'article 1641 du Code civil")),
    (r"(?<!\()\(Art\. L\. 124-3 du Code des assurances\)",
     f"({link('LEGIARTI000017735449', 'Art. L. 124-3 du Code des assurances')})"),
    (r"(?<!\()\(Art\. 145 du CPC\)",
     f"({link('LEGIARTI000051869339', 'Art. 145 du CPC')})"),
    (r"(?<!\()\(Art\. L\. 113-2 du Code des assurances\)",
     f"({link('LEGIARTI000035731302', 'Art. L. 113-2 du Code des assurances')})"),
    (r"(?<!\()\(Art\. L\. 237-2 du Code de commerce\)",
     f"({link('LEGIARTI000006230063', 'Art. L. 237-2 du Code de commerce')})"),

    # === ANALYSE Correction Juridique.md ===
    (r"(?<!\]\()l'article L\. 124-3 du Code des assurances",
     link("LEGIARTI000017735449", "l'article L. 124-3 du Code des assurances")),

    # === ANALYSE Jurisprudence.md ===
    (r"(?<!\]\()articles 1240 et 1231-1 du Code civil",
     f"[articles 1240 et 1231-1 du Code civil]({BASE}/LEGIARTI000032041571)"),
    (r"(?<!\()\(Art\. L\.124-3 Code des assurances\)",
     f"({link('LEGIARTI000017735449', 'Art. L.124-3 Code des assurances')})"),
    (r"(?<!\()\(Art\. 1242 al\.1 Code civil\)",
     f"({link('LEGIARTI000051786000', 'Art. 1242 al.1 Code civil')})"),
    (r"(?<!\()\(Art\. 1242 al\.5 Code civil\)",
     f"({link('LEGIARTI000051786000', 'Art. 1242 al.5 Code civil')})"),
    (r"(?<!\()\(Art\. 1240 Code civil\)",
     f"({link('LEGIARTI000032041571', 'Art. 1240 Code civil')})"),

    # === STRATEGIE Contentieux Civil.md ===
    (r"(?<!\| )Article 700 du Code de procédure civile(?= \|)",
     link("LEGIARTI000045268436", "Article 700 du Code de procédure civile")),

    # === ETUDE Indemnisation MAX.md ===
    (r"(?<!\()\(Article 700 CPC\)",
     f"({link('LEGIARTI000045268436', 'Article 700 CPC')})"),
    (r"(?<!\()\(Art\. 700 CPC\)",
     f"({link('LEGIARTI000045268436', 'Art. 700 CPC')})"),

    # === ANALYSE Responsabilites Legales.md ===
    (r"(?<!\]\()l'article L\. 113-2, 4° du Code des assurances",
     link("LEGIARTI000035731302", "l'article L. 113-2, 4° du Code des assurances")),
    (r"(?<!\]\()l'article L\. 124-3 du Code des assurances",
     link("LEGIARTI000017735449", "l'article L. 124-3 du Code des assurances")),
    (r"(?<!\]\()l'article 145 du Code de procédure civile \(CPC\)",
     link("LEGIARTI000051869339", "l'article 145 du Code de procédure civile (CPC)")),

    # === 03_Courrier SAS.md ===
    (r"(?<!\]\()L'article L\. 124-3 du Code des assurances",
     link("LEGIARTI000017735449", "L'article L. 124-3 du Code des assurances")),
    (r"(?<!\]\()L'article L\. 227-8 du Code de commerce",
     link("LEGIARTI000006227036", "L'article L. 227-8 du Code de commerce")),
    (r"(?<!\]\()article 145 du Code de procédure civile",
     link("LEGIARTI000051869339", "article 145 du Code de procédure civile")),
    (r"(?<!\()\(article L\. 113-2, 4° du Code des assurances\)",
     f"({link('LEGIARTI000035731302', 'article L. 113-2, 4° du Code des assurances')})"),

    # === 04_Courrier Assureur.md ===
    (r"(?<!\()\(Art\. L\.124-3\)",
     f"({link('LEGIARTI000017735449', 'Art. L.124-3')})"),
    (r"(?<!\]\()l'article L\. 124-3 du Code des assurances",
     link("LEGIARTI000017735449", "l'article L. 124-3 du Code des assurances")),
    (r"(?<!\]\()l'article 145 du Code de procédure civile",
     link("LEGIARTI000051869339", "l'article 145 du Code de procédure civile")),
    (r"(?<!\()\(article L\. 113-2, 4° du Code des assurances\)",
     f"({link('LEGIARTI000035731302', 'article L. 113-2, 4° du Code des assurances')})"),

    # === 05_Courrier Proprietaire.md ===
    (r"(?<!\]\()L'article 1719 du Code civil",
     link("LEGIARTI000020459127", "L'article 1719 du Code civil")),
    (r"(?<!\]\()L'article 1720 du même code",
     link("LEGIARTI000020459127", "L'article 1720 du même code")),
    (r"(?<!\]\()l'Article L\. 124-3 du Code des assurances",
     link("LEGIARTI000017735449", "l'Article L. 124-3 du Code des assurances")),
    (r"(?<!\()\(article L\. 113-2, 4° du Code des assurances\)",
     f"({link('LEGIARTI000035731302', 'article L. 113-2, 4° du Code des assurances')})"),
    (r"(?<!\]\()l'article 145 du Code de procédure civile",
     link("LEGIARTI000051869339", "l'article 145 du Code de procédure civile")),

    # === 06_Courrier President DG.md ===
    (r"(?<!\]\()arrêt SATI",
     link("JURITEXT000007047369", "arrêt SATI")),
    (r"(?<!\]\()L'article L\. 227-8 du Code de commerce",
     link("LEGIARTI000006227036", "L'article L. 227-8 du Code de commerce")),
    (r"(?<!\]\()l'article L\. 124-3 du Code des assurances",
     link("LEGIARTI000017735449", "l'article L. 124-3 du Code des assurances")),
    (r"(?<!\]\()l'article 145 du Code de procédure civile",
     link("LEGIARTI000051869339", "l'article 145 du Code de procédure civile")),
    (r"(?<!\()\(article L\. 113-2, 4° du Code des assurances\)",
     f"({link('LEGIARTI000035731302', 'article L. 113-2, 4° du Code des assurances')})"),

    # === CONSTITUTION Partie Civile.md ===
    (r"(?<!\()\(Article 222-20 du Code pénal\)",
     f"({link('LEGIARTI000024042640', 'Article 222-20 du Code pénal')})"),
    (r"(?<!\()\(Article 475-1 du Code de procédure pénale\)",
     f"({link('LEGIARTI000044570107', 'Article 475-1 du Code de procédure pénale')})"),

    # === PLAINTE Complement Defaut Assurance RC.md ===
(r"(?<!\]\()L'article L\. 124-3 du Code des assurances",
     link("LEGIARTI000017735449", "L'article L. 124-3 du Code des assurances")),
    (r"(?<!\]\()l'article 706-3 du Code de procédure pénale",
     link("LEGIARTI000006577625", "l'article 706-3 du Code de procédure pénale")),
]

def apply_replacements(text, replacements):
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    return text


# === ANNEXE B special handling ===

def link_annexe_b_articles(text):
    """Replace bold article names with linked versions in ANNEXE B."""
    articles_b = {
        "Article 1240 du Code civil": "LEGIARTI000032041571",
        "Article 1242 du Code civil": "LEGIARTI000051786000",
        "Article 1719 du Code civil": "LEGIARTI000020459127",
        "Article 1720 du Code civil": None,
        "Article 1844-8 du Code civil": "LEGIARTI000006444186",
        "Article 2226 du Code civil": "LEGIARTI000019017259",
        "Article 121-3 du Code pénal": "LEGIARTI000006417208",
        "Article 222-19 du Code pénal": "LEGIARTI000024042643",
        "Article 222-20 du Code pénal": "LEGIARTI000024042640",
        "Article 475-1 du Code de procédure pénale": "LEGIARTI000044570107",
        "Article 835 du Code de procédure civile": None,
        "Article 145 du Code de procédure civile": "LEGIARTI000051869339",
        "Article 700 du Code de procédure civile": "LEGIARTI000045268436",
        "Article L. 124-3 du Code des assurances": "LEGIARTI000017735449",
        "Article L. 223-22 du Code des assurances": "LEGIARTI000038837071",
        "Article L. 225-251 du Code de commerce": "LEGIARTI000006226329",
        "Article L. 237-2 du Code de commerce": "LEGIARTI000006230063",
        "Article R. 123-2 du Code de commerce": "LEGIARTI000046073350",
    }

    def replace_article(match):
        bold_text = match.group(1)
        rest = match.group(2)
        article_text = bold_text.strip("* ")
        legi_id = articles_b.get(article_text)
        if legi_id:
            return f"**[{article_text}]({BASE}/{legi_id})**{rest}"
        return match.group(0)

    # Match **Article ...** — rest of line
    text = re.sub(
        r'\*\*(Article [^*]+)\*\*(.*)',
        replace_article,
        text
    )
    return text


def fix_annexe_b_wrong_ids(text):
    """Fix wrong LEGIARTI IDs in existing Lien: lines in ANNEXE B."""
    wrong_ids = {
        "LEGIARTI000019017112": "LEGIARTI000019017259",
        "LEGIARTI000006417209": "LEGIARTI000006417208",
        "LEGIARTI000024042635": "LEGIARTI000024042643",
        "LEGIARTI000006576696": "LEGIARTI000044570107",
        "LEGIARTI000006647394": "LEGIARTI000045268436",
        "LEGIARTI000022537549": "LEGIARTI000038837071",
        "LEGIARTI000006447928": "LEGIARTI000006226329",
    }
    # Also fix R.123-2 which currently has L.237-2's ID
    for wrong, correct in wrong_ids.items():
        text = text.replace(wrong, correct)
    return text


def process_file(filepath, use_annexe_b=False, fix_wrong_ids=False):
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return
    with open(filepath, "r") as f:
        text = f.read()
    original = text

    if fix_wrong_ids:
        text = fix_annexe_b_wrong_ids(text)

    if use_annexe_b:
        text = link_annexe_b_articles(text)

    text = apply_replacements(text, REPLACEMENTS)

    if text != original:
        with open(filepath, "w") as f:
            f.write(text)
        print(f"  MODIFIED: {filepath}")
    else:
        print(f"  UNCHANGED: {filepath}")


def main():
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "actes")

    files = {
        # (filepath, use_annexe_b, fix_wrong_ids)
        os.path.join(base, "token", "06_Archives", "annexes", "ANNEXE B Lois Jurisprudence.md"): (True, True),
        os.path.join(base, "token", "06_Archives", "ANALYSE_correction_juridique.md"): (False, False),
        os.path.join(base, "token", "06_Archives", "ANALYSE_Jurisprudence.md"): (False, False),
        os.path.join(base, "token", "06_Archives", "STRATEGIE_Contentieux_Civil.md"): (False, False),
        os.path.join(base, "token", "06_Archives", "STRATEGIE_Contentieux_Penal.md"): (False, False),
        os.path.join(base, "token", "06_Archives", "Constitution_Partie_Civile.md"): (False, False),
        os.path.join(base, "token", "Etudes_indemnisation", "11_Etude indemnisation.md"): (False, False),
        os.path.join(base, "token", "Analyses_juridiques", "13_Responsabilites legales.md"): (False, False),
        # 4 nouveaux courriers 03-06
        os.path.join(base, "token", "Courriers", "03_Courrier SAS.md"): (False, False),
        os.path.join(base, "token", "Courriers", "04_Courrier Assureur.md"): (False, False),
        os.path.join(base, "token", "Courriers", "05_Courrier Proprietaire.md"): (False, False),
        os.path.join(base, "token", "Courriers", "06_Courrier President DG.md"): (False, False),
    }

    print("=== Batch linking legal references to Légifrance ===")
    for filepath, (annexe_b, fix_ids) in files.items():
        process_file(filepath, use_annexe_b=annexe_b, fix_wrong_ids=fix_ids)

    print("\nDone.")


if __name__ == "__main__":
    main()
