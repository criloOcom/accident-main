#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
legifrance_citation.py — Résolveur SOUVERAIN d'articles de loi via l'API PISTE/Légifrance.

Découverte clé (2026-07-11), confirmée par la doc officielle
(exemples-d-utilisation-de-l-api.docx, DILA V3 17/09/2025) :
  Workflow en 2 étapes pour récupérer le TEXTE INTÉGRAL d'un article de code :
    1. POST /search  (fond=CODE_DATE, filtre NOM_CODE + typeChamp NUM_ARTICLE EXACTE)
       -> renvoie le BON LEGIARTI (filtré sur le bon code, évite les homonymes
          type "202 CPC" vs "202 CPP").
    2. POST /consult/getArticle  {"id": "LEGIARTI..."}
       -> renvoie texte + contexte hiérarchique (context.titresTM).

  NB : le serveur MCP local mcp-legifrance/server.py utilisait à tort
  AccoConsultRequest / consult/code (accords) -> 500. Ne pas réutiliser cette voie.

Usage :
  PYTHONPATH=/home/crilocom/.opencode PISTE_ENV=production \
    python3 legifrance_citation.py "Code de procédure civile" 202
  -> imprime le bloc de citation au format projet (blockquote 3 lignes).

  Import :
    from legifrance_citation import get_client, resolve_legiarti, get_article, build_block
"""
import os
import sys
import json

PISTE_PATH = "/home/crilocom/.opencode"
if PISTE_PATH not in sys.path:
    sys.path.insert(0, PISTE_PATH)

_OAUTH = {
    "sandbox": "https://sandbox-oauth.piste.gouv.fr/api/oauth/token",
    "production": "https://oauth.piste.gouv.fr/api/oauth/token",
}
_API = {
    "sandbox": "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app/",
    "production": "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app/",
}


def _today_ms():
    """Timestamp epoch-ms de minuit aujourd'hui (facette DATE_VERSION Légifrance)."""
    import datetime
    d = datetime.date.today()
    return int(datetime.datetime(d.year, d.month, d.day).timestamp() * 1000)


def get_client(env=None):
    """Construit un LegifranceClient authentifié depuis le secret PISTE_CREDENTIALS."""
    from souverain import get_secret
    from pylegifrance import LegifranceClient, ApiConfig

    env = env or os.environ.get("PISTE_ENV", "production")
    creds = json.loads(get_secret("PISTE_CREDENTIALS"))["piste"][env]
    return LegifranceClient(
        ApiConfig(
            client_id=creds["client_id"],
            client_secret=creds["client_secret"],
            token_url=_OAUTH[env],
            api_url=_API[env],
        )
    )


def resolve_legiarti(client, code_nom, num):
    """Renvoie (legiarti, section_title, article_num) pour `num` dans le code `code_nom`.

    code_nom : nom EXACT du code (facette NOM_CODE), ex. "Code de procédure civile".
    num      : numéro d'article, ex. "202", "L376-1", "R4323-58".
    Lève ValueError si aucun match exact du numéro dans ce code.
    """
    payload = {
        "recherche": {
            "champs": [
                {
                    "typeChamp": "NUM_ARTICLE",
                    "criteres": [
                        {"typeRecherche": "EXACTE", "valeur": num, "operateur": "ET"}
                    ],
                    "operateur": "ET",
                }
            ],
            "filtres": [
                {"facette": "NOM_CODE", "valeurs": [code_nom]},
                {"facette": "DATE_VERSION", "singleDate": _today_ms()},
            ],
            "pageNumber": 1,
            "pageSize": 10,
            "operateur": "ET",
            "sort": "PERTINENCE",
            "typePagination": "ARTICLE",
        },
        "fond": "CODE_DATE",
    }
    data = client.call_api("search", payload).json()
    want = num.replace(" ", "").replace(".", "").upper()
    candidates = []  # (is_vigueur, ex, section_title)
    for res in data.get("results", []):
        for sec in res.get("sections", []):
            for ex in sec.get("extracts", []):
                got = (ex.get("num") or "").replace(" ", "").replace(".", "").upper()
                if got == want:
                    is_vig = (ex.get("legalStatus") == "VIGUEUR")
                    candidates.append((is_vig, ex, sec.get("title")))
    if not candidates:
        raise ValueError(f"Article {num} introuvable (exact) dans {code_nom!r}")
    # Priorité absolue à la version EN VIGUEUR (évite les textes historiques périmés).
    candidates.sort(key=lambda c: (0 if c[0] else 1))
    _, ex, sec_title = candidates[0]
    return ex.get("id"), sec_title, ex.get("num")


def get_article(client, legiarti):
    """Renvoie (texte, chemin_hierarchique, num, etat) via /consult/getArticle."""
    data = client.call_api("consult/getArticle", {"id": legiarti}).json()
    art = data.get("article", {}) or {}
    texte = (art.get("texte") or "").strip()
    ctx = art.get("context", {}) or {}
    titres = ctx.get("titresTM") or []
    chemin = " > ".join(t.get("titre", "").strip() for t in titres if t.get("titre"))
    return texte, chemin, art.get("num"), art.get("etat")


def build_block(code_nom, num, texte, chemin, legiarti):
    """Construit le bloc de citation au format projet (blockquote 3 lignes)."""
    url = f"https://www.legifrance.gouv.fr/codes/article_lc/{legiarti}"
    # Ligne 2 : "Code > Section" — on garde le dernier niveau significatif si chemin long
    filiation = f"{code_nom}"
    if chemin:
        # dernier segment hiérarchique le plus précis
        last = chemin.split(" > ")[-1].strip()
        filiation = f"{code_nom} > {last}"
    filiation = filiation.rstrip(".")  # évite le double point (chemin finissant déjà par '.')
    # texte : normaliser espaces internes, un seul espace, pas de retour ligne
    texte = " ".join(texte.split())
    return (
        f"> « {texte} » <br>\n"
        f"> **{filiation}.** <br>\n"
        f"> [Article {num} du {code_nom}]({url})"
    )


def cite(code_nom, num, env=None):
    """Chaîne complète : résout + consulte + construit le bloc. Renvoie dict."""
    client = get_client(env)
    legiarti, section, anum = resolve_legiarti(client, code_nom, num)
    texte, chemin, rnum, etat = get_article(client, legiarti)
    block = build_block(code_nom, rnum or num, texte, chemin, legiarti)
    return {
        "code": code_nom,
        "num": rnum or num,
        "legiarti": legiarti,
        "etat": etat,
        "chemin": chemin,
        "texte": texte,
        "url": f"https://www.legifrance.gouv.fr/codes/article_lc/{legiarti}",
        "block": block,
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: legifrance_citation.py \"<Nom du code>\" <num>", file=sys.stderr)
        sys.exit(2)
    code_nom = sys.argv[1]
    num = sys.argv[2]
    r = cite(code_nom, num)
    print(f"# {r['code']} — Article {r['num']}  (LEGIARTI={r['legiarti']}, état={r['etat']})")
    print(f"# Chemin: {r['chemin']}")
    print()
    print(r["block"])
