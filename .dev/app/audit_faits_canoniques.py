#!/usr/bin/env python3
"""
Audit factuel ciblé du dépôt Actes/Token.

But : détecter les ÉCARTS FACTUELS par rapport à la Source Unique de Vérité
(Memory/STRICT VARIABLES.md). PAS de faux positifs (contrairement à
l'audit bruité précédent qui traitait les liens [🏠] et les vrais LRAR
de « hallucinations »).

On ne remonte QUE des écarts factuels avérés vs les valeurs canoniques.
"""
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TOKEN = ROOT / "Actes/Token"
STRICT = ROOT / "Memory/STRICT VARIABLES.md"

# --- Patterns d'écarts factuels INTERDITS (valeurs fausses connues) ---
# Chaque règle : (regex, explication, fichiers à exclure si nécessaire)
RULES = [
    # Dates fausses
    (r"31\s*mai\s*2026", "Date chirurgie erronée : '31 mai 2026' (réel : 30 mai 2026). Le 31/05 est la date du compte-rendu, pas de la chirurgie."),
    (r"29\s*juin\s*2026", "Date accident erronée : '29 juin 2026' (réel : 29 mai 2026). Certains certificats ont cette erreur matérielle."),
    (r"12\s*mai\s*2026", "Date accident erronée : '12 mai' (réel : 29 mai 2026)."),
    (r"12\s*mars\s*1982", "Date naissance erronée : '12 mars 1982' (réel : 18 janvier 1982)."),
    # Doigt atteint
    (r"5[ée]\s*doigt", "Référence à '5e doigt' (auriculaire) — ERREUR : seule la main droite / index droit est atteint(e)."),
    (r"auriculaire", "Référence à 'auriculaire' — ERREUR : seule la main droite / index droit est atteint(e)."),
    # Numéros de dossier CPAM
    (r"31713398", "Numéro CPAM obsolète '31713398' (réel : 31727387)."),
    # Numéros LRAR — on vérifie que les vrais sont présents et qu'aucun faux n'apparait
]

# Numéros LRAR RÉELS (doivent apparaître tels quels dans la strate Réelle, et comme tokens dans Token)
LRAR_REELS = [
    "87001424863012T", "87001424721856G", "87001424862879J",
    "87001424862462Y", "87001424923505I", "87001421903907I", "870014282662911",
]
# Numéros LRAR FACTICES jamais valides (à signaler s'ils apparaissent)
LRAR_FACTICES_SUSPECTS = [
    r"8700142\d{7}[A-Z]",  # forme générale La Poste à 15 chars + lettre
]

# Tokens LRAR autorisés dans Token (ils résolvent vers les réels en strate Réelle)
LRAR_TOKENS_OK = ["[N° LRAR Exploitant]", "[N° LRAR Directrice]", "[N° LRAR Président]",
                  "[N° LRAR Proprietaire]", "[N° LRAR Président]", "[Numéro LRAR]",
                  "[N° LRAR Bailleur]"]

def scan_file(path: Path):
    rel = path.relative_to(ROOT)
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return []
    hits = []
    # Règles d'écarts factuels
    for pat, expl in RULES:
        for m in re.finditer(pat, text, re.IGNORECASE):
            line_no = text[:m.start()].count("\n") + 1
            snippet = text.splitlines()[line_no-1].strip()[:160]
            hits.append((rel, line_no, "ÉCART DATE/DOIGT/CPAM", expl, snippet))
    # LRAR : alerter si un numéro complet 15-car La Poste apparaît dans un fichier Token
    # (dans Token on attend des TOKENS, pas les vrais numéros — sauf dans certains cas)
    for m in re.finditer(r"8700142\d{7}[A-Z]", text):
        line_no = text[:m.start()].count("\n") + 1
        num = m.group(0)
        if num not in LRAR_REELS:
            hits.append((rel, line_no, "LRAR SUSPECT", f"Numéro LRAR '{num}' non référencé comme réel.", text.splitlines()[line_no-1].strip()[:160]))
        # sinon (réel) : toléré dans les mémo internes Personnel/Organisation (pas destinés à tiers)
        else:
            if "Reel" not in str(rel) and "Personnel" not in str(rel) and "Organisation" not in str(rel):
                hits.append((rel, line_no, "LRAR BRUT DANS TOKEN", f"Le vrai numéro '{num}' apparaît en clair dans un fichier Token (devrait être tokenisé).", text.splitlines()[line_no-1].strip()[:160]))
    return hits

def main():
    all_hits = []
    for p in TOKEN.rglob("*.md"):
        if p.name.upper() == "README.md":
            continue
        all_hits.extend(scan_file(p))
    # Rapport
    out = ROOT / "Rapports/audit" / "20260713_audit_faits_canoniques.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---",
             'title: "AUDIT FAITS CANONIQUES — Écarts vs STRICT VARIABLES.md"',
             'description: "Audit ciblé des écarts factuels (dates, doigts, CPAM, LRAR) dans Actes/Token."',
             "type: rapport", "date: 2026-07-13", "---", "", "# Audit faits canoniques", "",
             f"Fichiers scannés : {len(list(TOKEN.rglob('*.md')))}",
             f"Écarts détectés : {len(all_hits)}", ""]
    if not all_hits:
        lines.append("✅ Aucun écart factuel détecté vs STRICT VARIABLES.md.")
    else:
        cur = None
        for rel, ln, cat, expl, snip in all_hits:
            lines.append(f"\n## {rel} (ligne {ln}) — {cat}")
            lines.append(f"- {expl}")
            lines.append(f"- Extrait : `{snip}`")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Écarts détectés : {len(all_hits)}")
    for h in all_hits[:40]:
        print(f"  [{h[2]}] {h[0]}:{h[1]} — {h[3][:70]}")
    print(f"\nRapport écrit : {out}")

if __name__ == "__main__":
    main()
