#!/usr/bin/env python3
"""Vérification cross-document : liens, tokens, LEGIARTI, cohérence frontmatter.

Usage :
    python3 app/check_consistency.py

Retourne un code non-nul si au moins une anomalie est détectée.
"""

import argparse
import os
import re
import sys
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ACTES = REPO / "actes"
ANNEXES = REPO / "actes" / "token" / "06_Archives" / "annexes"
MEMORY = REPO / "memory"
APP = REPO / "app"

errors = []
warnings = []


def err(msg: str) -> None:
    errors.append(f"  ERROR   {msg}")


def warn(msg: str) -> None:
    warnings.append(f"  WARN    {msg}")


def all_acte_md() -> list[Path]:
    return sorted(ACTES.rglob("*.md"))


# ── 1. Liens internes ──────────────────────────────────────────────────
def check_internal_links() -> None:
    acte_files = all_acte_md()
    all_md = {f.name for f in acte_files}
    all_md.update({f.name for f in ANNEXES.glob("*.md")})
    all_md.update({f.name for f in MEMORY.glob("*.md")})
    all_md.add("AGENTS.md")
    all_md.add("JULES.md")
    all_md.add("GEMINI.md")
    all_md.add("README.md")

    link_pattern = re.compile(r'\(([^)]+\.md)\)')
    for f in acte_files:
        text = f.read_text(encoding="utf-8")
        for m in link_pattern.finditer(text):
            target = m.group(1)
            if target.startswith("http") or target.startswith("#"):
                continue
            target_decoded = urllib.parse.unquote(target)
            target_name = Path(target_decoded).name
            if target_name not in all_md:
                err(f"{f.name} → lien mort : {target}")


# ── 2. Tokens connus ──────────────────────────────────────────────────
def check_tokens() -> None:
    annexe_a = Path("actes/token/06_Archives/annexes") / "📚 ANNEXE A Lexique Tokens.md"
    if not annexe_a.exists():
        err("ANNEXE_A introuvable — impossible de vérifier les tokens")
        return

    token_lines = annexe_a.read_text(encoding="utf-8").splitlines()
    known_tokens = set()
    for line in token_lines:
        m = re.match(r'.*\[([^\]]+)\]\s*=', line)
        if m:
            known_tokens.add(m.group(1))

    acte_files = all_acte_md()
    token_usage = re.compile(r'\[([^\]]+)\](?!\s*\()')
    for f in acte_files:
        text = f.read_text(encoding="utf-8")
        for m in token_usage.finditer(text):
            token = m.group(1)
            if token in ("🔗 Drive", "NOM À COMMUNIQUER", "DATE", "cliquez ici", "À compléter"):
                continue
            if token.startswith("http") or token.startswith("#"):
                continue
            # Skip Table des matières links (e.g. [Conclusion](#conclusion))
            if re.match(r'^[A-Z][a-zà-ü].*\]\(#[a-z]', line.strip()):
                continue
            if token in ("L. 124-3", "L. 223-22", "L. 225-251", "L. 237-2",
                         "L. 421-3", "R. 123-2", "223-1"):
                continue
            if not re.match(r'^[A-ZÀ-Ü][a-zà-ü\s\-\'\]]+$', token):
                continue
            if len(token) < 4:
                continue
            if token not in known_tokens and token not in (
                "La Ville de l'Accident", "L'Adresse de la Victime",
                "L'Adresse de l'Exploitation", "L'Adresse du Président",
                "La Ville de Résidence de la Victime", "La Métropole Régionale",
                "La Ville de l'Établissement SOS Main", "L'Email de la Victime",
                "L'Identifiant Professionnel de la Victime",
                "L'Identifiant de l'Exploitation",
                "Adresse à compléter", "Centre de soins immédiats",
            ):
                warn(f"{f.name} → token potentiel non documenté : [{token}]")


# ── 3. Légifrance / Judilibre ─────────────────────────────────────────
def check_external_links() -> None:
    acte_files = all_acte_md()
    legi_pattern = re.compile(r'LEGIARTI\d+')
    juri_pattern = re.compile(r'JURITEXT\d+')
    
    # 1. Charger les IDs définis localement dans le code du projet
    local_ids = set()
    
    app_dir = str(REPO / "app")
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)
    mcp_dir = "/home/crilocom/.opencode/mcp-legifrance"
    if mcp_dir not in sys.path:
        sys.path.insert(0, mcp_dir)
    
    # Import depuis extract_legal_refs
    try:
        import extract_legal_refs
        for ref_data in extract_legal_refs.LEGAL_REFS.values():
            url = ref_data.get("url", "")
            m = re.search(r'(LEGIARTI[A-Z0-9]+|JURITEXT\d+)', url)
            if m:
                local_ids.add(m.group(1))
    except Exception as e:
        warn(f"Impossible d'importer extract_legal_refs : {e}")
        
    # Import depuis batch_link_legifrance
    try:
        import batch_link_legifrance
        local_ids.update(batch_link_legifrance.LEGIARTI.values())
    except Exception as e:
        warn(f"Impossible d'importer batch_link_legifrance : {e}")
        
    known_ids = local_ids
    
    # 2. Tenter de lire l'Annuaire sur Google Sheet pour une vérification en temps réel
    try:
        import drive_auth
        from googleapiclient import discovery
        
        service = drive_auth.get_drive_service()
        sheets = discovery.build("sheets", "v4", credentials=service._http.credentials)
        result = sheets.spreadsheets().values().get(
            spreadsheetId="14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ", range="A2:P1000"
        ).execute()
        rows = result.get("values", [])
        
        sheet_ids = set()
        for r in rows:
            if len(r) > 10:
                val = r[10].strip()
                if val:
                    sheet_ids.add(val)
                    
        if sheet_ids:
            # Union des IDs du sheet et des locaux pour éviter les faux-positifs
            known_ids = local_ids.union(sheet_ids)
    except Exception:
        # Fallback silencieux sur les IDs locaux si pas de connexion/credentials
        pass

    for f in acte_files:
        text = f.read_text(encoding="utf-8")
        for m in legi_pattern.finditer(text):
            val = m.group()
            if val not in known_ids:
                err(f"{f.name} → LEGIARTI non déclaré dans l'Annuaire ou le code local : {val}")
            else:
                # Vérifier l'existence réelle du LEGIARTI via le module local ou l'API si disponible
                try:
                    import os
                    if "PISTE_CREDENTIALS" not in os.environ:
                        sys.path.insert(0, "/home/crilocom/.opencode")
                        from souverain import get_secret
                        os.environ["PISTE_CREDENTIALS"] = get_secret("PISTE_CREDENTIALS")
                    import server
                    client = server.LegifranceClient()
                    res = client.consulte_article(val)
                    if not res or not res.get("article"):
                        err(f"{f.name} → LEGIARTI inexistant sur Légifrance : {val}")
                except Exception as ex:
                    # Fallback silencieux en cas d'absence de module, d'auth ou de réseau
                    pass
        for m in juri_pattern.finditer(text):
            val = m.group()
            if val not in known_ids:
                err(f"{f.name} → JURITEXT non déclaré dans l'Annuaire ou le code local : {val}")



# ── 4. Cohérence frontmatter ──────────────────────────────────────────
def check_frontmatter() -> None:
    acte_files = all_acte_md()
    date_pattern = re.compile(r'^date:\s*(\d{4}-\d{2}-\d{2})')
    for f in acte_files:
        text = f.read_text(encoding="utf-8")
        m = date_pattern.search(text)
        if m:
            d = m.group(1)
            if d < "2026-05-29":
                warn(f"{f.name} → date ({d}) antérieure à l'accident (2026-05-29)")


# ── 5. Annexe embarquée résiduelle ────────────────────────────────────
def check_residual_annexes() -> None:
    acte_files = all_acte_md()
    for f in acte_files:
        if "annexes" in f.parts:
            continue
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            if re.match(r'^#{1,3}\s+ANNEXE\s+[ABC]', line, re.IGNORECASE):
                err(f"{f.name}:{i} → Annexe {line.strip()} encore embarquée (doit être un lien vers annexes/)")


# ── 6. OpenLegi double-vérification ────────────────────────────────────
def check_openlegi() -> None:
    """Cross-check LEGIARTI references via OpenLegi for double verification."""
    app_dir = str(REPO / "app")
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)
    from openlegi_client import OpenLegiClient, health_check

    if not health_check():
        warn("OpenLegi indisponible — vérification ignorée")
        return

    # Collecter tous les LEGIARTI depuis les documents
    acte_files = all_acte_md()
    legi_pattern = re.compile(r'LEGIARTI\d+')
    all_legi = set()
    for f in acte_files:
        text = f.read_text(encoding="utf-8")
        for m in legi_pattern.finditer(text):
            all_legi.add(m.group())

    if not all_legi:
        return

    # Mapper LEGIARTI → (article_number, code_name) depuis les refs locales
    legi_to_ref = {}
    try:
        import extract_legal_refs
        for ref_name, ref_data in extract_legal_refs.LEGAL_REFS.items():
            url = ref_data.get("url", "")
            m = re.search(r'(LEGIARTI[A-Z0-9]+)', url)
            if m:
                ref_id = m.group(1)
                legi_to_ref[ref_id] = ref_name
    except Exception:
        pass

    try:
        import batch_link_legifrance
        for article_num, ref_id in batch_link_legifrance.LEGIARTI.items():
            legi_to_ref[ref_id] = article_num
    except Exception:
        pass

    verified = 0
    failed = 0
    renums = []

    # Map ref name patterns to (code_name, article_num_extractor)
    CODE_MAP = [
        (r"C\. civ\.", "Code civil", lambda r: r.split()[0]),
        (r"C\. pén\.", "Code pénal", lambda r: r.split()[0]),
        (r"C\. com\.", "Code de commerce", lambda r: r.split()[0]),
        (r"C\. trav\.", "Code du travail", lambda r: r.split()[0]),
        (r"C\. assur\.", "Code des assurances", lambda r: r.split()[0]),
        (r"CCH", "Code de la construction et de l'habitation", lambda r: r.split()[0]),
        (r"C\.séc\. soc\.", "Code de la sécurité sociale", lambda r: r.split()[0]),
        (r"CSP", "Code de la santé publique", lambda r: r.split()[0]),
        (r"CPP", "Code de procédure pénale", lambda r: r.split()[0]),
        (r"CPC", "Code de procédure civile", lambda r: r.split()[0]),
        (r"C\. urb\.", "Code de l'urbanisme", lambda r: r.split()[0]),
        (r"CSS", "Code de la sécurité sociale", lambda r: r.split()[0]),
    ]

    with OpenLegiClient() as ol:
        for legi_id in sorted(all_legi):
            ref_name = legi_to_ref.get(legi_id, "")

            # For known renumberings, flag them
            if legi_id == "LEGIARTI000006438819":
                renums.append(legi_id)
                warn(f"OpenLegi: {legi_id} (ex-Art.1382 C.civ.) → Art.1240 depuis 2016 — numéro réaffecté")
                continue

            if not ref_name:
                failed += 1
                warn(f"OpenLegi: {legi_id} → non vérifié (référence inconnue)")
                continue

            # Determine code and article number from ref name
            code_guess = "Code civil"
            article_num = ref_name

            for pattern, code_name, extractor in CODE_MAP:
                if re.search(pattern, ref_name):
                    code_guess = code_name
                    article_num = extractor(ref_name)
                    break
            else:
                # No code suffix detected — try to guess from prefix
                if re.match(r'^Art\.?L227\b', ref_name):
                    code_guess = "Code de commerce"
                if re.match(r'^Art\.?L421\b', ref_name):
                    code_guess = "Code de la consommation"

            # Normalize: strip "Art." prefix, remove dots in "L.227-8" -> "L227-8"
            article_num = re.sub(r'^Art\.?', '', article_num).strip()
            article_num = re.sub(r'\.(\d)', r'\1', article_num)

            try:
                result = ol._call("tools/call", {
                    "name": "rechercher_code",
                    "arguments": {
                        "search": article_num,
                        "code_name": code_guess,
                        "champ": "NUM_ARTICLE",
                        "page_size": 1,
                    },
                })
                content = result.get("content", [])
                text = " ".join(
                    item.get("text", "") for item in content if item.get("type") == "text"
                )
                if "VIGUEUR" in text:
                    verified += 1
                else:
                    failed += 1
                    warn(f"OpenLegi: {legi_id} ({ref_name}) → introuvable dans {code_guess} (cherché: {article_num})")
            except Exception as e:
                failed += 1
                warn(f"OpenLegi: {legi_id} ({ref_name}) → erreur: {e}")

    total = verified + failed
    if total:
        print(f"\n  OpenLegi double-vérification: {verified}/{total} OK, {failed} échec(s)")
        if renums:
            print(f"  Renumérotations détectées: {len(renums)}")


# ── Main ──────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(description="Vérification cross-document")
    parser.add_argument("--openlegi", action="store_true",
                        help="Activer la double-vérification via OpenLegi")
    args = parser.parse_args()
    print("=== VÉRIFICATION CROSS-DOCUMENT ===")
    print()

    check_internal_links()
    check_tokens()
    check_external_links()
    check_frontmatter()
    check_residual_annexes()

    if args.openlegi:
        check_openlegi()

    if not errors and not warnings:
        print("Rien à signaler — tout est cohérent.")
        return 0

    for e in errors:
        print(e)
    for w in warnings:
        print(w)

    print()
    print(f"{len(errors)} erreur(s), {len(warnings)} avertissement(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
