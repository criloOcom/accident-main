#!/usr/bin/env python3
"""
assign_yaml_uids.py — Attribue un identifiant unique 'uid' (9 caractères, alphabet
sans ambiguite) a chaque fichier .md du depot qui possede un YAML frontmatter.

- Idempotent : si 'uid:' est deja present et valide, on ne le change pas.
- L'uid est insere en 2e ligne du bloc YAML (juste apres '---').
- Genere un export CSV Memory/UID_EXPORT.csv :
    * ligne 1 : RESERVEE a l'utilisateur (vide)
    * ligne 2 : libelles (uid | chemin_relatif | titre | type)
    * ligne 3+ : donnees
- Peut optionnellement pousser le tableau vers un Google Sheet (--sheet).
- Aucune saisie manuelle : tout est automatique, souverain via 'souverain'.

Usage :
    python3 .dev/app/assign_yaml_uids.py [--apply] [--sheet] [--sheet-id ID]
"""

import os
import re
import sys
import csv
import random

PROJECT_ROOT = "/home/crilocom/accident-main"
UID_CSV = os.path.join(PROJECT_ROOT, "Memory", "UID_EXPORT.csv")

# Alphabet sans caracteres ambigus : pas de 0/O, 1/l/I
ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz"
UID_LEN = 9

DRY_RUN = "--apply" not in sys.argv
PUSH_SHEET = "--sheet" in sys.argv
SHEET_ID_ARG = None
if "--sheet-id" in sys.argv:
    idx = sys.argv.index("--sheet-id")
    SHEET_ID_ARG = sys.argv[idx + 1]


def log(msg):
    print(f"[UID] {msg}")


def gen_uid(existing):
    """Genere un uid de 9 chars unique (hors 'existing' set)."""
    while True:
        u = "".join(random.choice(ALPHABET) for _ in range(UID_LEN))
        if u not in existing:
            return u


def has_yaml(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            first = f.read(4)
    except Exception:
        return False
    return first.startswith("---")


def extract_title_type(text):
    title = ""
    typ = ""
    m = re.search(r'^title:\s*"?([^"\n]+)"?', text, re.M)
    if m:
        title = m.group(1).strip()
    m = re.search(r'^type:\s*"?([^"\n]+)"?', text, re.M)
    if m:
        typ = m.group(1).strip()
    return title, typ


def add_uid_to_file(path, uid):
    """Insere 'uid: XXXXX' en 2e ligne (apres '---')."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines or not lines[0].strip() == "---":
        return False
    # chercher si uid deja present dans le bloc YAML
    for i in range(1, len(lines)):
        if lines[i].strip().startswith("---"):
            break
        if re.match(r'^uid\s*:', lines[i]):
            return False  # deja la
    # inserer a la ligne 1 (index 1), juste apres '---'
    lines.insert(1, f"uid: {uid}\n")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return True


def main():
    log("Attribution d'uid a tous les .md avec YAML...")
    # 1) collecter tous les .md avec YAML
    targets = []
    for root, _, files in os.walk(PROJECT_ROOT):
        if ".git" in root or "__pycache__" in root:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            if has_yaml(p):
                targets.append(p)
    log(f"{len(targets)} fichiers .md avec YAML detectes.")

    # 2) lire les uid deja existants (pour unicite)
    existing = set()
    for p in targets:
        try:
            t = open(p, encoding="utf-8").read()
        except Exception:
            continue
        m = re.search(r'^uid:\s*([0-9A-Za-z]{9})\s*$', t, re.M)
        if m:
            existing.add(m.group(1))
    log(f"{len(existing)} uid deja presents (conserver l'unicite).")

    # 3) attribuer
    rows = []  # (uid, rel_path, title, type)
    changed = 0
    for p in targets:
        rel = os.path.relpath(p, PROJECT_ROOT)
        text = open(p, encoding="utf-8").read()
        m = re.search(r'^uid:\s*([0-9A-Za-z]{9})\s*$', text, re.M)
        if m:
            uid = m.group(1)
        else:
            uid = gen_uid(existing)
            existing.add(uid)
            if not DRY_RUN:
                if add_uid_to_file(p, uid):
                    changed += 1
            else:
                changed += 1  # comptera comme "a faire"
        title, typ = extract_title_type(text)
        rows.append((uid, rel, title, typ))

    log(f"{'DRY-RUN' if DRY_RUN else 'APPLY'} : {changed} fichiers a (re)marquer.")

    # 4) CSV : ligne 1 vide (utilisateur), ligne 2 libelles, ligne 3+ donnees
    if not DRY_RUN:
        with open(UID_CSV, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow([])  # ligne 1 : reservee a l'utilisateur
            w.writerow(["uid", "chemin_relatif", "titre", "type"])  # ligne 2 : libelles
            for r in rows:
                w.writerow(r)
        log(f"CSV ecrit : {UID_CSV}")

    # 5) Google Sheet (optionnel)
    if PUSH_SHEET and not DRY_RUN:
        push_to_sheet(rows, SHEET_ID_ARG)

    return 0


def push_to_sheet(rows, sheet_id=None):
    """Cree ou met a jour un Google Sheet avec les uid. Ligne 1 reservee,
    ligne 2 libelles, ligne 3+ donnees."""
    sys.path.insert(0, os.path.expanduser("~/.opencode"))
    from souverain import get_credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    creds = get_credentials()
    if not creds.valid:
        creds.refresh(Request())
    svc = build("sheets", "v4", credentials=creds)
    data = [[]] + [["uid", "chemin_relatif", "titre", "type"]] + [list(r) for r in rows]
    if sheet_id:
        # mettre a jour le sheet existant
        svc.spreadsheets().values().clear(spreadsheetId=sheet_id, range="A1:Z").execute()
        svc.spreadsheets().values().update(
            spreadsheetId=sheet_id, range="A1",
            valueInputOption="RAW", body={"values": data}).execute()
        log(f"Sheet mis a jour : {sheet_id}")
    else:
        # creer un nouveau sheet
        sp = svc.spreadsheets().create(body={"properties": {"title": "Accident-Main — UID des fichiers .md"}}).execute()
        new_id = sp["spreadsheetId"]
        svc.spreadsheets().values().update(
            spreadsheetId=new_id, range="A1",
            valueInputOption="RAW", body={"values": data}).execute()
        log(f"NOUVEAU Sheet cree : {new_id}")
        log(f"URL: https://docs.google.com/spreadsheets/d/{new_id}/edit")


if __name__ == "__main__":
    sys.exit(main())
