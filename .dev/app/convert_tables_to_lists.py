#!/usr/bin/env python3
"""
convert_tables_to_lists.py — Convertit les tableaux Markdown de TYPE "listing"
(colonne de numéros + liens vers des .md) en listes à puces lisibles.

Objectif : améliorer la lisibilité mobile et humaine (les tableaux à colonne
de numéros sont illisibles sur GitHub). Les tableaux de DONNÉES (dates,
montants, comparaisons) sont conservés.

Détection d'un tableau "listing" à convertir :
  - l'en-tête contient un jeton de numérotation (#, N°, N, Num) ET
  - une colonne avec un lien vers un fichier .md (ou un nom de document)
  - le corps a une colonne de numéros (01, 02, 1, 2...) en 1ère ou 2e colonne

Usage :
  python3 .dev/app/convert_tables_to_lists.py            # dry-run
  python3 .dev/app/convert_tables_to_lists.py --apply     # écrit
  python3 .dev/app/convert_tables_to_lists.py --path "⚖️_Actes"  # cible
"""
import os
import re
import sys
import argparse

ROOT = "/home/crilocom/accident-main"
SKIP_DIRS = {'.git', '.pytest_cache', '.venv', 'node_modules', '__pycache__', '.opencode'}

NUM_HEADER = re.compile(r'\b(#|n°|num|no)\b', re.IGNORECASE)
TABLE_ROW = re.compile(r'^\s*\|(.*)\|\s*$')
TABLE_SEP = re.compile(r'^\s*\|[\s:\-|]+\|\s*$')


def parse_table(block_lines):
    """Retourne (headers, rows) ou None si pas un tableau valide."""
    if len(block_lines) < 2:
        return None
    hdr = [c.strip() for c in block_lines[0].strip().strip('|').split('|')]
    # ligne de separation
    if not TABLE_SEP.match(block_lines[1]):
        return None
    rows = []
    for ln in block_lines[2:]:
        if not TABLE_ROW.match(ln):
            break
        rows.append([c.strip() for c in ln.strip().strip('|').split('|')])
    if not rows:
        return None
    return hdr, rows


def is_listing_table(hdr, rows):
    """Decide si ce tableau est un listing a convertir."""
    if not hdr:
        return False
    # en-tete contient un jeton de numero OU de document/fichier
    has_num_hdr = any(NUM_HEADER.search(h) for h in hdr)
    has_doc_hdr = any(re.search(r'document|fichier|dossier|piece|acte|nom', h, re.IGNORECASE) for h in hdr)
    # une colonne contient des liens .md ou noms de fichiers
    has_md_links = False
    for r in rows:
        for cell in r:
            if '.md' in cell:
                has_md_links = True
                break
        if has_md_links:
            break
    # premiere colonne = numeros (01, 02, 1, 2, N°, **01**)
    first_col_numeric = False
    if rows and rows[0]:
        fc = rows[0][0].strip().strip('*`').strip()
        if re.match(r'^(\d+|n°\s*\d+)$', fc, re.IGNORECASE):
            first_col_numeric = True
    return has_md_links and (has_num_hdr or has_doc_hdr or first_col_numeric)


def clean_cell(cell):
    """Retire le gras/backticks autour d'un numero, garde le lien.
    Le LABEL est decode (lisible) ; la CIBLE est re-encodée (url-safe)
    pour rester un lien cliquable sous GitHub (les espaces/emojis dans
    une cible non encodée cassent le rendu du lien)."""
    # extrait le [texte](lien) si present
    m = re.search(r'\[([^\]]+)\]\(([^)]+)\)', cell)
    if m:
        label = m.group(1)
        link = m.group(2)
        try:
            import urllib.parse
            # label lisible (decode pour l'affichage)
            label = urllib.parse.unquote(label)
            # cible : re-encode les espaces/emojis pour que le lien soit cliquable
            if ' ' in link or any(ord(c) > 127 for c in link):
                link = urllib.parse.quote(link)
        except Exception:
            pass
        return label, link
    # sinon texte brut
    return cell.strip('*` '), None


def convert_to_list(hdr, rows):
    """Convertit en liste a puces groupees par la 2e colonne (document)."""
    # trouve l'index de la colonne document/lien et resume
    # heuristique: colonne avec lien .md = document; derniere = resume; 1ere = numero
    doc_idx = None
    for i, h in enumerate(hdr):
        if re.search(r'document|fichier|dossier|piece|acte', h, re.IGNORECASE):
            doc_idx = i
            break
    if doc_idx is None:
        # cherche la colonne contenant le plus de liens
        best = -1
        for i, h in enumerate(hdr):
            cnt = sum(1 for r in rows if '.md)' in r[i])
            if cnt > best:
                best = cnt; doc_idx = i
    # resume = derniere colonne non-vide apres doc
    res_idx = len(hdr) - 1
    items = []
    for r in rows:
        label, link = clean_cell(r[doc_idx] if doc_idx < len(r) else r[-1])
        fond = ""
        # fondement = colonne entre doc et resume
        if doc_idx is not None and res_idx > doc_idx + 1:
            for i in range(doc_idx + 1, res_idx):
                if i < len(r) and r[i] and r[i] != '—':
                    fond = r[i]
                    break
        resume = r[res_idx] if res_idx < len(r) else ""
        resume = resume.replace('—', '').strip()
        if link:
            item = f"- **[{label}]({link})**"
        else:
            item = f"- **{label}**"
        if fond:
            item += f" — *{fond}*"
        if resume:
            item += f" — {resume}"
        items.append(item)
    return "\n".join(items)


def process_file(rel_path, dry_run):
    p = os.path.join(ROOT, rel_path)
    lines = open(p, encoding='utf-8').read().split('\n')
    out = []
    i = 0
    changed = False
    while i < len(lines):
        # detecte un bloc tableau
        if TABLE_ROW.match(lines[i]) and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1]):
            block = [lines[i], lines[i + 1]]
            j = i + 2
            while j < len(lines) and TABLE_ROW.match(lines[j]):
                block.append(lines[j]); j += 1
            parsed = parse_table(block)
            if parsed and is_listing_table(*parsed):
                hdr, rows = parsed
                converted = convert_to_list(hdr, rows)
                if dry_run:
                    out.append(f"<!-- TABLEAU CONVERTI ({len(rows)} lignes) -->")
                    out.append(converted)
                else:
                    out.append(converted)
                changed = True
                i = j
                continue
            else:
                out.extend(block)
                i = j
                continue
        out.append(lines[i])
        i += 1
    if changed and not dry_run:
        open(p, 'w', encoding='utf-8').write('\n'.join(out))
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--path', default=None)
    args = ap.parse_args()
    dry = not args.apply
    targets = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, args.path) if args.path else ROOT):
        parts = os.path.relpath(dp, ROOT).split(os.sep)
        if any(s in SKIP_DIRS for s in parts):
            continue
        for f in fn:
            if f.endswith('.md'):
                targets.append(os.path.relpath(os.path.join(dp, f), ROOT))
    total = 0
    for t in targets:
        if process_file(t, dry):
            total += 1
            if total <= 20:
                print(f"  {'[DRY] ' if dry else ''}{t}")
    print(f"\n{'DRY-RUN' if dry else 'APPLY'} : {total} fichiers avec tableaux de listing convertis.")


if __name__ == '__main__':
    main()
