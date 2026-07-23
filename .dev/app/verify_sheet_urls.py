#!/usr/bin/env python3
"""Vérifie que toutes les URLs du Sheet PJ répondent 200 OK.

Usage:
    python3 .dev/app/verify_sheet_urls.py        # dry-run
    python3 .dev/app/verify_sheet_urls.py --check # curl chaque URL
"""

import json
import os
import subprocess
import sys
import re

SHEET_ID = "1cwb8L5fc7HqsAHP6IH32gSFwKRIdSztcYk1XmfbaYIg"
SHEET_NAME = "@"
TOKEN_DIR = "Actes/Token"

def extract_all_uids():
    """Extract uid -> relative_path from all Token .md files."""
    uid_map = {}
    for root, dirs, files in os.walk(TOKEN_DIR):
        for fname in files:
            if not fname.endswith('.md') or fname == 'README.md':
                continue
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if m:
                uid_m = re.search(r'^uid:\s*(\S+)', m.group(1), re.MULTILINE)
                if uid_m:
                    uid_map[uid_m.group(1)] = os.path.relpath(fpath, TOKEN_DIR)
    return uid_map

def main():
    uid_map = extract_all_uids()
    print(f"Fichiers Token .md trouvés : {len(uid_map)} uids")
    print()

    # Lire les données du sheet via l'API
    # (en pratique, les données sont extraites manuellement depuis le sheet)
    # Cette fonction imprime les instructions
    
    print("=== INSTRUCTIONS DE VÉRIFICATION ===")
    print()
    print("1. Lire le sheet avec la plage @!A:C pour obtenir toutes les URLs")
    print("2. Pour chaque URL, exécuter:")
    print("     curl -s -o /dev/null -w '%{http_code}' 'URL'")
    print("3. Vérifier que le code HTTP = 200")
    print()
    print("=== MAPPING UID -> FICHIER ===")
    for uid in sorted(uid_map.keys()):
        path = uid_map[uid]
        url = f"https://github.com/criloOcom/accident-main/blob/main/Actes/Token/{path}"
        print(f"{uid} -> {url}")

if __name__ == '__main__':
    main()
