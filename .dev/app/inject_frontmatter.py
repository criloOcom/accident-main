#!/usr/bin/env python3
import os
import re

LOIS_DIR = "/home/crilocom/accident-main/Lois"

# Law articles: filename -> (title, code, article, legiarti, status)
LAW_ARTICLES = {
    "Article1240_CodeCivil.md": ("Article 1240 — Code civil", "Code civil", "1240", "LEGIARTI000032041571", "en_vigueur"),
    "Article1242_CodeCivil.md": ("Article 1242 — Code civil", "Code civil", "1242", "LEGIARTI000051786000", "en_vigueur"),
    "Article_145_CodeDeProcédureCivile_Legifrance.md": ("Article 145 — Code de procédure civile", "Code de procédure civile", "145", "LEGIARTI000051869339", "en_vigueur"),
    "Article835_CodeDeProcedureCivile_LegiFrance.md": ("Article 835 — Code de procédure civile", "Code de procédure civile", "835", "LEGIARTI000042597284", "en_vigueur"),
    "Article_700_Codeproc_Legifrance.md": ("Article 700 — Code de procédure civile", "Code de procédure civile", "700", "LEGIARTI000045268436", "en_vigueur"),
    "Article_263_Codeproc_Legifrance.md": ("Article 263 — Code de procédure civile", "Code de procédure civile", "263", "LEGIARTI000006410394", "en_vigueur"),
    "Article_L124-3_Codesassurances_Legifrance.md": ("Article L124-3 — Code des assurances", "Code des assurances", "L124-3", "LEGIARTI000017735449", "en_vigueur"),
    "Article_L113-2_Codesassurances_Legifrance.md": ("Article L113-2 — Code des assurances", "Code des assurances", "L113-2", "LEGIARTI000035731302", "en_vigueur"),
    "Article_2226_Code_Legifrance.md": ("Article 2226 — Code civil", "Code civil", "2226", "LEGIARTI000019017259", "en_vigueur"),
    "Article_1844-8_Code_Legifrance.md": ("Article 1844-8 — Code civil", "Code civil", "1844-8", "LEGIARTI000006444186", "en_vigueur"),
    "Article_222-19_CodePenal_Legifrance.md": ("Article 222-19 — Code pénal", "Code pénal", "222-19", "LEGIARTI000024042643", "en_vigueur"),
    "Article222-20_CodePenal_LegiFrance.md": ("Article 222-20 — Code pénal", "Code pénal", "222-20", "LEGIARTI000024042640", "en_vigueur"),
    "Article_121-3_Code_Legifrance.md": ("Article 121-3 — Code pénal", "Code pénal", "121-3", "LEGIARTI000006417208", "en_vigueur"),
    "Article1719_CodeCivil_LegiFrance.md": ("Article 1719 — Code civil", "Code civil", "1719", "LEGIARTI000020459127", "en_vigueur"),
    "Article1720_CodeCivil_LegiFrance.md": ("Article 1720 — Code civil", "Code civil", "1720", "LEGIARTI000006442784", "en_vigueur"),
    "Article_L210-6_Codecommerce_Legifrance.md": ("Article L210-6 — Code de commerce", "Code de commerce", "L210-6", "LEGIARTI000006222358", "en_vigueur"),
    "Article_L223-22_Codecommerce_Legifrance.md": ("Article L223-22 — Code de commerce", "Code de commerce", "L223-22", "LEGIARTI000006223141", "en_vigueur"),
    "Article_L225-251_Codecommerce_Legifrance.md": ("Article L225-251 — Code de commerce", "Code de commerce", "L225-251", "LEGIARTI000006226329", "en_vigueur"),
    "Article_L227-8_Codecommerce_Legifrance.md": ("Article L227-8 — Code de commerce", "Code de commerce", "L227-8", "LEGIARTI000006227036", "en_vigueur"),
    "Article_L237-2_Codecommerce_Legifrance.md": ("Article L237-2 — Code de commerce", "Code de commerce", "L237-2", "LEGIARTI000006230063", "en_vigueur"),
    "Article_L421-3_Codeconsommation_Legifrance.md": ("Article L421-3 — Code de la consommation", "Code de la consommation", "L421-3", "LEGIARTI000049464053", "en_vigueur"),
    "Article_R143-2_Codeconstructionhabitation_Legifrance.md": ("Article R143-2 — Code de la construction et de l'habitation", "Code de la construction et de l'habitation", "R143-2", "LEGIARTI000043818941", "en_vigueur"),
    "Article475-1_CodeProcedurePenale.md": ("Article 475-1 — Code de procédure pénale", "Code de procédure pénale", "475-1", "LEGIARTI000044570107", "abroge_differe_2029"),
    "Article_121-1a121-7_CodePenal_Legifrance.md": ("Articles 121-1 à 121-7 — Code pénal", "Code pénal", "121-1 à 121-7", "LEGIARTI000006417206", "en_vigueur"),
}

JURISPRUDENCES = {
    "00-82.066_CourCassation.md": ("Arrêt Cousin — Ass. Plén., n° 00-82.066", "Cour de cassation — Assemblée plénière", "00-82.066", "JURITEXT000007071351", "publié"),
    "11-15.699_CourCassation.md": ("Cass. Soc., n° 11-15.699", "Cour de cassation — Chambre sociale", "11-15.699", "JURITEXT000026515553", "publié"),
    "13-80.849_CourCassation.md": ("Crim., n° 13-80.849", "Cour de cassation — Chambre criminelle", "13-80.849", "JURITEXT000029014493", "publié"),
    "14-15.326_CourCassation.md": ("Civ. 3e, n° 14-15.326", "Cour de cassation — Troisième chambre civile", "14-15.326", "JURITEXT000032194983", "publié"),
    "16-24.631_CourCassation.md": ("Civ. 2e, n° 16-24.631", "Cour de cassation — Deuxième chambre civile", "16-24.631", "NON TROUVÉ SUR LÉGIFRANCE", "rnsm_non_indexe"),
    "18-17.868_CourCassation.md": ("Civ. 2e, n° 18-17.868", "Cour de cassation — Deuxième chambre civile", "18-17.868", "JURITEXT000041585779", "publié"),
    "19-15.659_CourCassation.md": ("Civ. 2e, n° 19-15.659", "Cour de cassation — Deuxième chambre civile", "19-15.659", "NON TROUVÉ SUR LÉGIFRANCE", "rnsm_non_indexe"),
    "19-23.173_CourCassation.md": ("Civ. 2e, n° 19-23.173", "Cour de cassation — Deuxième chambre civile", "19-23.173", "JURITEXT000043489943", "publié"),
    "20-15.106_CourCassation.md": ("Civ. 2e, n° 20-15.106", "Cour de cassation — Deuxième chambre civile", "20-15.106", "JURITEXT000043782126", "publié"),
    "20-16.463_CourCassation.md": ("Civ. 1re, n° 20-16.463", "Cour de cassation — Première chambre civile", "20-16.463", "JURITEXT000044482848", "publié"),
    "21-14.197_CourCassation.md": ("Civ. 2e, n° 21-14.197", "Cour de cassation — Deuxième chambre civile", "21-14.197", "JURITEXT000047700832", "publié"),
    "22-19.307_CourCassation.md": ("Civ. 2e, n° 22-19.307", "Cour de cassation — Deuxième chambre civile", "22-19.307", "JURITEXT000049418278", "publié"),
    "23-12.369_CourCassation.md": ("Civ. 2e, n° 23-12.369", "Cour de cassation — Deuxième chambre civile", "23-12.369", "JURITEXT000050509897", "publié"),
    "24-21.702_CourCassation.md": ("Civ. 2e, n° 24-21.702", "Cour de cassation — Deuxième chambre civile", "24-21.702", "JURITEXT000054167506", "publié"),
    "70-12.124_CourCassation.md": ("Arrêt Leroy — Civ. 2e, n° 70-12.124", "Cour de cassation — Deuxième chambre civile", "70-12.124", "JURITEXT000006987399", "publié"),
    "74-10.466_CourCassation.md": ("Civ. 2e, n° 74-10.466", "Cour de cassation — Deuxième chambre civile", "74-10.466", "JURITEXT000006993485", "publié"),
    "80-14.994_CourCassation.md": ("Arrêt Gabillet — Ass. Plén., n° 80-14.994", "Cour de cassation — Assemblée plénière", "80-14.994", "JURITEXT000007013792", "publié"),
    "89-18.422_CourCassation.md": ("Civ. 2e, n° 89-18.422", "Cour de cassation — Deuxième chambre civile", "89-18.422", "JURITEXT000007026411", "publié"),
    "91-13.580_CourCassation.md": ("Civ. 2e, n° 91-13.580", "Cour de cassation — Deuxième chambre civile", "91-13.580", "JURITEXT000007029806", "publié"),
    "91-15.035_CourCassation.md": ("Civ. 2e, n° 91-15.035", "Cour de cassation — Deuxième chambre civile", "91-15.035", "JURITEXT000007030324", "publié"),
    "97-17.378_CourCassation.md": ("Arrêt Costedoat — Ass. Plén., n° 97-17.378", "Cour de cassation — Assemblée plénière", "97-17.378", "JURITEXT000007043704", "publié"),
    "99-17.092_CourCassation.md": ("Com., n° 99-17.092", "Cour de cassation — Chambre commerciale", "99-17.092", "JURITEXT000007047369", "publié"),
}

def make_yaml(data, is_law):
    lines = ["---"]
    lines.append(f"title: \"{data[0]}\"")
    lines.append(f"type: {'law_article' if is_law else 'jurisprudence'}")
    if is_law:
        lines.append(f"code: \"{data[1]}\"")
        lines.append(f"article: \"{data[2]}\"")
        lines.append(f"legiarti: {data[3]}")
    else:
        lines.append(f"jurisdiction: \"{data[1]}\"")
        lines.append(f"pourvoi: \"{data[2]}\"")
        lines.append(f"juritext: {data[3]}")
    lines.append(f"status: \"{data[4]}\"")
    lines.append(f"last_verified: \"2026-07-11\"")
    lines.append("---")
    return "\n".join(lines)

def strip_old_block(text):
    lines = text.split("\n")
    result = []
    skip_block = False
    for line in lines:
        if line.startswith("> **Nature**"):
            skip_block = True
            continue
        if skip_block:
            if line.strip() == "---":
                skip_block = False
                continue
            if line.startswith("> ") or line.strip() == "":
                continue
        if skip_block:
            continue
        result.append(line)
    return "\n".join(result)

def process_file(fname, data, is_law):
    path = os.path.join(LOIS_DIR, fname)
    with open(path, "r") as f:
        content = f.read()

    yaml_block = make_yaml(data, is_law)
    new_content = yaml_block + "\n\n" + strip_old_block(content)

    with open(path, "w") as f:
        f.write(new_content)

    print(f"  ✅ {fname}")

count = 0
for fname, data in LAW_ARTICLES.items():
    if os.path.exists(os.path.join(LOIS_DIR, fname)):
        process_file(fname, data, True)
        count += 1
    else:
        print(f"  ⚠️  NOT FOUND: {fname}")

for fname, data in JURISPRUDENCES.items():
    if os.path.exists(os.path.join(LOIS_DIR, fname)):
        process_file(fname, data, False)
        count += 1
    else:
        print(f"  ⚠️  NOT FOUND: {fname}")

print(f"\nDone: {count} files updated")
