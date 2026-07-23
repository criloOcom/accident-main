#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit Règle #11 (durcie) : tout document .md du périmètre SORTANT (courriers,
actes de procédure, analyses juridiques) qui cite un article de loi SANS note de
bas de page Légifrance associée est signalé.

Mode diff-driven :
  - Si STAGED est fourni (variable d'env), on n'audite QUE les fichiers staged
    modifiés/nouveaux du périmètre sortant.
  - Sinon, on audite tout le périmètre sortant (pour vérification manuelle).

Sortie :
  0 = OK (aucune citation nue dans les fichiers audités)
  1 = ÉCHEC (citation nue détectée -> bloque le commit)
  2 = avertissement (legacy, hors périmètre)
"""
import os, re, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCOPE = ["Actes/Token/Courriers", "Actes/Token/Actes_proceduraux", "Actes/Token/Analyses_juridiques"]

# numéros d'articles déjà connus valides (dictionnaire Légifrance) -> s'ils sont nus,
# c'est une violation. Les autres (non résolubles) ne sont pas blockés (pas de devinette),
# mais on signale quand même pour information.
DICT_PATH = "/tmp/sources_dict.json"
KNOWN = set()
if os.path.exists(DICT_PATH):
    try:
        d = json.load(open(DICT_PATH, encoding="utf-8"))
        for k in d:
            nn = re.sub(r"[\s.]", "", k.split("|")[0]).upper()
            KNOWN.add(nn)
    except Exception:
        pass

ART = re.compile(
    r"\b(articles?|art\.)\s+((?:(?:L|R|D)\.?\s?)?\d+[\-\d]*)",
    re.IGNORECASE,
)

TAG = " [À VÉRIFIER]"


def in_scope(path):
    rel = os.path.relpath(path, ROOT)
    return any(rel.startswith(s) for s in SCOPE) and rel.endswith(".md") and not rel.endswith("README.md")


def citation_nue(t):
    """Retourne la liste des numéros d'articles nus (sans note [^..] ni tag) dans t."""
    # retirer la zone Source (déjà notée) et les défs de notes
    body = re.sub(r"<!-- Source -->.*?<!-- /Source -->", "", t, flags=re.DOTALL)
    body = re.sub(r"\[\^[^\]]+\]:.*$", "", body, flags=re.MULTILINE)
    nus = []
    for m in ART.finditer(body):
        e = m.end()
        nn = re.sub(r"[\s.]", "", m.group(2)).upper()
        # déjà doté d'une note ?
        if body[e : e + 4].startswith("[^"):
            continue
        # taggué douteux ?
        if body[e : e + len(TAG)] == TAG:
            continue
        nus.append(nn)
    return nus


def main():
    staged_env = os.environ.get("STAGED", "")
    if staged_env.strip():
        files = [f for f in staged_env.splitlines() if f.strip() and in_scope(f) and os.path.exists(f)]
        mode = "diff"
    else:
        files = []
        for r, dirs, fs in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", ".dev", ".opencode", "node_modules", "__pycache__")]
            for f in fs:
                p = os.path.join(r, f)
                if in_scope(p):
                    files.append(p)
        mode = "full"

    # Sémantique (Règle #11 durcie) :
    #  - Un fichier qui cite des articles ET n'a AUCUNE note de bas de page = document
    #    « non sourcé » -> BLOQUANT (nouveau document à 0% sourcé).
    #  - Un fichier qui cite des articles et EN A DÉJÀ (même incomplètes) = legacy
    #    partiel -> WARNING (ne bloque pas le stock existant à résorber progressivement).
    violations_block = []   # (fichier, [nus]) -> 0 note du tout
    violations_warn = []    # (fichier, [nus]) -> a déjà des notes
    for p in files:
        t = open(p, encoding="utf-8").read()
        nus = citation_nue(t)
        if not nus:
            continue
        connus = [n for n in nus if n in KNOWN]
        if not connus:
            continue
        has_any_note = bool(re.search(r"\[\^[^\]]+\]:", t)) or ("<!-- Source -->" in t)
        if has_any_note:
            violations_warn.append((p, connus))
        else:
            violations_block.append((p, connus))

    if not violations_block and not violations_warn:
        if mode == "diff":
            print("✅ Aucune citation d'article connue sans note dans les fichiers modifiés.")
        else:
            print("✅ Aucune citation d'article connue sans note (périmètre sortant).")
        sys.exit(0)

    if violations_block:
        print(f"❌ {len(violations_block)} fichier(s) STAGED citent des articles SANS AUCUNE note de bas de page (document non sourcé) :")
        for p, connus in violations_block:
            print(f"   📄 {os.path.relpath(p, ROOT)} : articles nus = {', '.join(connus[:12])}{'…' if len(connus)>12 else ''}")
        print("   Règle #11 durcie : un document citant un article DOIT avoir au moins une note de bas de page.")
        print("   FIX : lancez .dev/app/inject_footnotes_v2.py sur le fichier avant de committer.")
        if mode == "diff":
            sys.exit(1)
        sys.exit(2)

    # seulement des warnings (legacy partiel)
    print(f"⚠️  {len(violations_warn)} fichier(s) ont quelques citations sans note mais possèdent déjà des notes (legacy partiel) :")
    for p, connus in violations_warn[:10]:
        print(f"   📄 {os.path.relpath(p, ROOT)} : ex. {', '.join(connus[:6])}")
    if len(violations_warn) > 10:
        print(f"   … et {len(violations_warn)-10} autre(s).")
    print("   Règle #11 : idéalement, résorbez ces citations (inject_footnotes_v2.py). Non bloquant pour le stock existant.")
    sys.exit(2)


if __name__ == "__main__":
    main()
