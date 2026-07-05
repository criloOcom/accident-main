#!/usr/bin/env python3
"""Vérification cross-document : liens, tokens, LEGIARTI, cohérence frontmatter.

Usage :
    python3 app/check_consistency.py

Retourne un code non-nul si au moins une anomalie est détectée.
"""

import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ACTES = REPO / "actes"
ANNEXES = REPO / "actes" / "archives" / "annexes"
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
            target_name = Path(target).name
            if target_name not in all_md:
                err(f"{f.name} → lien mort : {target}")


# ── 2. Tokens connus ──────────────────────────────────────────────────
def check_tokens() -> None:
    annexe_a = Path("actes/06_Archives/annexes/ANNEXE A Lexique Tokens.md")
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
            if token in ("🔗 Drive", "NOM À COMMUNIQUER", "DATE", "cliquez ici"):
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
                "L'Identifiant Professionnel de la Victime",                 "L'Identifiant de l'Exploitation",
                "Adresse à compléter",
            ):
                warn(f"{f.name} → token potentiel non documenté : [{token}]")


# ── 3. Légifrance / Judilibre ─────────────────────────────────────────
def check_external_links() -> None:
    acte_files = all_acte_md()
    legi_pattern = re.compile(r'LEGIARTI[0-9]{13}')
    juri_pattern = re.compile(r'JURITEXT[0-9]{12}')
    known_ids = {
        "LEGIARTI000032041571", "LEGIARTI000051786000",
        "LEGIARTI000020459127", "LEGIARTI000006442784",
        "LEGIARTI000006444186", "LEGIARTI000019017112",
        "LEGIARTI000006417209", "LEGIARTI000024042635",
        "LEGIARTI000024042640", "LEGIARTI000006576696",
        "LEGIARTI000042597284", "LEGIARTI000051869339",
        "LEGIARTI000006647394", "LEGIARTI000017735449",
        "LEGIARTI000022537549", "LEGIARTI000006447928",
        "LEGIARTI000006230063", "LEGIARTI000049464053",
        "LEGIARTI000006896089", "LEGIARTI000045268436",
        "LEGIARTI000006792596",
        "JURITEXT000007047369", "JURITEXT000038340141",
        "JURITEXT000043489943", "JURITEXT000043782126",
        "JURITEXT000044482848", "JURITEXT000049418278",
        "JURITEXT000007043831", "JURITEXT000007043322",
        "JURITEXT000028994017",
    }
    for f in acte_files:
        text = f.read_text(encoding="utf-8")
        for m in legi_pattern.finditer(text):
            if m.group() not in known_ids:
                warn(f"{f.name} → LEGIARTI inconnu : {m.group()}")
        for m in juri_pattern.finditer(text):
            if m.group() not in known_ids:
                warn(f"{f.name} → JURITEXT inconnu : {m.group()}")


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


# ── Main ──────────────────────────────────────────────────────────────
def main() -> int:
    print("=== VÉRIFICATION CROSS-DOCUMENT ===")
    print()

    check_internal_links()
    check_tokens()
    check_external_links()
    check_frontmatter()
    check_residual_annexes()

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
