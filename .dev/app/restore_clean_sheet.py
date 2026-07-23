#!/usr/bin/env python3
"""
Restore clean Google Sheet @ while reconciling A-C (Token files) and preserving existing structure.
"""
import os
import re
import urllib.parse
from typing import Dict, List, Any
from tools import _get_gdrive_token

SHEET_ID = "1cwb8L5fc7HqsAHP6IH32gSFwKRIdSztcYk1XmfbaYIg"
SHEET_NAME = "@"
BACKUP_SHEET_NAME = "@ Backup AvantInterventionAgent IA"
TOKEN_DIR = "Actes/Token"
GITHUB_BASE_URL = "https://github.com/criloOcom/accident-main/blob/main/Actes/Token/"

def get_token_files_map() -> Dict[str, Dict[str, str]]:
    token_map = {}
    for root, _, files in os.walk(TOKEN_DIR):
        for f in files:
            if f.endswith('.md') and f != 'README.md':
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                m = re.search(r"---\s*\n(.*?)\n---", content, re.DOTALL)
                if m:
                    yaml = m.group(1)
                    uid_m = re.search(r"^uid\s*:\s*(\S+)", yaml, re.MULTILINE)
                    drive_m = re.search(r"^drive_id\s*:\s*(\S+)", yaml, re.MULTILINE)
                    if uid_m:
                        uid = uid_m.group(1)
                        drive_id = drive_m.group(1) if drive_m else ""
                        if drive_id == "À":
                            drive_id = ""
                        rel_path = os.path.relpath(path, TOKEN_DIR).replace(os.sep, "/")
                        token_map[uid] = {
                            "rel_path": rel_path,
                            "drive_id": drive_id
                        }
    return token_map

def read_sheet_range(range_name: str) -> List[List[Any]]:
    import json, urllib.request
    token = _get_gdrive_token()
    encoded_range = urllib.parse.quote(range_name, safe='')
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{encoded_range}?majorDimension=ROWS"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    return data.get("values", [])

def update_sheet_range(range_name: str, values: List[List[Any]]) -> None:
    import json, urllib.request
    token = _get_gdrive_token()
    encoded_range = urllib.parse.quote(range_name, safe='')
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{encoded_range}?valueInputOption=RAW"
    body = json.dumps({"values": values}).encode('utf-8')
    req = urllib.request.Request(url, data=body, method="PUT", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        _ = json.load(resp)
    return

def clear_sheet_range(range_name: str) -> None:
    import urllib.request
    token = _get_gdrive_token()
    encoded_range = urllib.parse.quote(range_name, safe='')
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{encoded_range}:clear"
    req = urllib.request.Request(url, data=b'{}', method="POST", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        pass

def main():
    print("1. Reading backup sheet whole data...")
    backup_rows = read_sheet_range(f"'{BACKUP_SHEET_NAME}'!A1:AZ200")
    print(f"Read {len(backup_rows)} rows from Backup.")

    print("2. Scanning local Actes/Token markdown files...")
    token_map = get_token_files_map()
    print(f"Found {len(token_map)} valid markdown files.")

    # We will build clean rows for sheet @
    # Make sure we have at least header rows 1 and 2
    max_cols = 0
    for r in backup_rows:
        if len(r) > max_cols:
            max_cols = len(r)
    if max_cols < 26:
        max_cols = 26

    # Normalize backup rows size
    grid = []
    for r in backup_rows:
        row_copy = list(r) + [""] * (max_cols - len(r))
        grid.append(row_copy)

    # Ensure header rows 1 & 2 are exact from backup
    # If backup has empty A-C header row 1 & 2:
    if len(grid) > 1:
        grid[1][0] = "uid"
        grid[1][1] = "uid Url .md"
        grid[1][2] = "📄Fichier 🔑ID Drive"

    # Now populate A, B, C for all 136 local token files starting at row 3 (index 2)
    sorted_uids = sorted(token_map.keys())
    
    # We want to fill A-C from row 3 (index 2) onwards
    for i, uid in enumerate(sorted_uids):
        row_idx = 2 + i
        while len(grid) <= row_idx:
            grid.append([""] * max_cols)
        
        info = token_map[uid]
        encoded_path = urllib.parse.quote(info["rel_path"])
        url = GITHUB_BASE_URL + encoded_path
        drive_id = info["drive_id"]

        grid[row_idx][0] = uid
        grid[row_idx][1] = url
        grid[row_idx][2] = drive_id

    # If grid is longer than 2 + len(sorted_uids), clear A-C for remaining rows
    for r_idx in range(2 + len(sorted_uids), len(grid)):
        grid[r_idx][0] = ""
        grid[r_idx][1] = ""
        grid[r_idx][2] = ""

    print("3. Clearing existing sheet @ range...")
    clear_sheet_range(f"'{SHEET_NAME}'!A1:AZ300")

    print("4. Writing reconstructed grid to sheet @...")
    update_sheet_range(f"'{SHEET_NAME}'!A1", grid)
    print("Done! Sheet @ restored and reconciled successfully.")

if __name__ == "__main__":
    main()
