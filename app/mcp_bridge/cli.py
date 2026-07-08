#!/usr/bin/env python3
import argparse
import json
import os
import sys


def cmd_judilibre_search(args):
    from .judilibre import JudilibreClient
    client = JudilibreClient()
    result = client.search(
        query=args.query,
        page=args.page,
        page_size=args.page_size,
        chamber=args.chamber,
        solution=args.solution,
        jurisdiction=args.jurisdiction,
        publication=args.publication,
        date_from=args.date_from,
        date_to=args.date_to,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_judilibre_decision(args):
    from .judilibre import JudilibreClient
    from .zones import extract_zones
    client = JudilibreClient()
    result = client.get_decision(args.decision_id)
    if "zones" in result and result.get("text"):
        result["zones_extracted"] = extract_zones(result)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_judilibre_ecli(args):
    from .judilibre import JudilibreClient
    client = JudilibreClient()
    result = client.search(args.ecli, page_size=5)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_legifrance_search(args):
    from .legifrance import LegifranceClient
    client = LegifranceClient()
    result = client.search(args.query, args.fond, args.page_size, args.page_number)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_legifrance_article(args):
    from .legifrance import LegifranceClient
    client = LegifranceClient()
    result = client.consulte_article(args.text_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_legifrance_decision(args):
    from .legifrance import LegifranceClient
    client = LegifranceClient()
    result = client.consulte_decision(args.text_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_legifrance_texte(args):
    from .legifrance import LegifranceClient
    client = LegifranceClient()
    result = client.consulte_texte(args.text_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_check(args):
    has_piste_env = bool(os.environ.get("PISTE_CREDENTIALS"))
    has_piste_file = os.path.exists(".piste-credentials.json")
    has_drive_env = all(
        os.environ.get(v) for v in
        ["GOOGLE_DRIVE_CLIENT_ID", "GOOGLE_DRIVE_CLIENT_SECRET", "GOOGLE_DRIVE_REFRESH_TOKEN"]
    )
    has_drive_file = os.path.exists(".drive-token.json")
    env = os.environ.get("PISTE_ENV", "non défini")
    print(json.dumps({
        "PISTE_CREDENTIALS (env)": "OK" if has_piste_env else "MANQUANT",
        "PISTE_CREDENTIALS (file)": "OK" if has_piste_file else "MANQUANT",
        "GOOGLE_DRIVE (env)": "OK" if has_drive_env else "MANQUANT",
        "GOOGLE_DRIVE (file)": "OK" if has_drive_file else "MANQUANT",
        "PISTE_ENV": env,
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Bridge juridique pour Jules")
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="Vérifier la configuration MCP")
    p_check.set_defaults(func=cmd_check)

    p_js = sub.add_parser("judilibre-search", help="Rechercher dans Judilibre")
    p_js.add_argument("query")
    p_js.add_argument("--page", type=int, default=1)
    p_js.add_argument("--page-size", type=int, default=10)
    p_js.add_argument("--chamber")
    p_js.add_argument("--solution")
    p_js.add_argument("--jurisdiction")
    p_js.add_argument("--publication")
    p_js.add_argument("--date-from")
    p_js.add_argument("--date-to")
    p_js.set_defaults(func=cmd_judilibre_search)

    p_jd = sub.add_parser("judilibre-decision", help="Consulter une décision Judilibre")
    p_jd.add_argument("decision_id")
    p_jd.set_defaults(func=cmd_judilibre_decision)

    p_je = sub.add_parser("judilibre-ecli", help="Rechercher par ECLI")
    p_je.add_argument("ecli")
    p_je.set_defaults(func=cmd_judilibre_ecli)

    p_ls = sub.add_parser("legifrance-search", help="Rechercher dans Légifrance")
    p_ls.add_argument("query")
    p_ls.add_argument("--fond", default="JURI", help="JURI, CODE, LODA, KALI")
    p_ls.add_argument("--page-size", type=int, default=5)
    p_ls.add_argument("--page-number", type=int, default=1)
    p_ls.set_defaults(func=cmd_legifrance_search)

    p_la = sub.add_parser("legifrance-article", help="Consulter un article de code")
    p_la.add_argument("text_id")
    p_la.set_defaults(func=cmd_legifrance_article)

    p_ld = sub.add_parser("legifrance-decision", help="Consulter une décision Légifrance")
    p_ld.add_argument("text_id")
    p_ld.set_defaults(func=cmd_legifrance_decision)

    p_lt = sub.add_parser("legifrance-texte", help="Consulter un texte légal")
    p_lt.add_argument("text_id")
    p_lt.set_defaults(func=cmd_legifrance_texte)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
