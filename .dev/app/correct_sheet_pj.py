#!/usr/bin/env python3
"""Correct the PJ Google Sheet (columns A-C) by reconciling it with the markdown files in Actes/Token.

Requirements:
- Scan all .md files under Actes/Token (excluding README.md) and extract `uid:` and optional `drive_id:` from YAML front‑matter.
- Build a mapping {uid: {path, drive_id}}.
- Read the sheet range '@!A:C' (Token section) via the Google‑Docs MCP tools.
- For each existing row, if the UID is not present in the mapping, clear cells A‑C.
- For each UID in the mapping missing from the sheet, append a new row with UID, GitHub URL, and drive_id (if valid).
- After writing, verify each URL with `curl` returning HTTP 200.
- Log any non‑200 responses.
- Scan columns G‑K starting at row 282 for orphan UIDs and write a report to logs/corruption_report.txt.
- Handle special cases as described in the plan.
"""
import os
import re
import subprocess
import urllib.parse
from typing import Dict, List, Any
from tools import _get_gdrive_token

# Constants (adjust if needed)
SHEET_ID = "1cwb8L5fc7HqsAHP6IH32gSFwKRIdSztcYk1XmfbaYIg"
SHEET_NAME = "@"
TOKEN_DIR = "Actes/Token"
GITHUB_BASE_URL = "https://github.com/criloOcom/accident-main/blob/main/Actes/Token/"
LOG_DIR = "logs"
REPORT_PATH = os.path.join(LOG_DIR, "corruption_report.txt")

# ---------------------------------------------------------------------------
# Helper: extract uid and drive_id from a markdown file's YAML front‑matter
# ---------------------------------------------------------------------------
def extract_uid_and_drive(path: str) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # Flexible regex to find YAML front‑matter allowing optional leading whitespace or newlines
    m = re.search(r"---\s*\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return {}
    yaml = m.group(1)
    uid_match = re.search(r"^uid\s*:\s*(\S+)", yaml, re.MULTILINE)
    if not uid_match:
        return {}
    uid = uid_match.group(1)
    drive_match = re.search(r"^drive_id\s*:\s*(\S+)", yaml, re.MULTILINE)
    drive_id = drive_match.group(1) if drive_match else ""
    # Ignore invalid drive_id like "À"
    if drive_id == "À":
        drive_id = ""
    return {"uid": uid, "drive_id": drive_id}
    # Ignore invalid drive_id like "À"
    if drive_id == "À":
        drive_id = ""
    return {"uid": uid, "drive_id": drive_id}

# ---------------------------------------------------------------------------
# Build the UID mapping from the repository
# ---------------------------------------------------------------------------
def build_uid_map() -> Dict[str, Dict[str, str]]:
    uid_map: Dict[str, Dict[str, str]] = {}
    for root, _, files in os.walk(TOKEN_DIR):
        for fname in files:
            if not fname.endswith('.md') or fname == 'README.md':
                continue
            fpath = os.path.join(root, fname)
            data = extract_uid_and_drive(fpath)
            if data:
                rel_path = os.path.relpath(fpath, TOKEN_DIR).replace(os.sep, "/")
                uid_map[data["uid"]] = {"path": rel_path, "drive_id": data.get("drive_id", "")}
    return uid_map

# ---------------------------------------------------------------------------
# Google‑Sheets MCP wrappers
# ---------------------------------------------------------------------------
def read_sheet_range(range_name: str) -> List[List[Any]]:
    import json, urllib.request
    token = _get_gdrive_token()
    # Encode range for URL (slashes need to be preserved for sheet notation)
    encoded_range = urllib.parse.quote(range_name, safe='')
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{encoded_range}?majorDimension=ROWS"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    return data.get("values", [])

def update_sheet_range(range_name: str, values: List[List[Any]]) -> None:
    import json, urllib.request
    token = _get_gdrive_token()
    # Encode range for URL (slashes need to be preserved)
    encoded_range = urllib.parse.quote(range_name, safe='')
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{encoded_range}?valueInputOption=RAW"
    body = json.dumps({"values": values}).encode('utf-8')
    req = urllib.request.Request(url, data=body, method="PUT", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        _ = json.load(resp)
    return

# ---------------------------------------------------------------------------
# Core reconciliation logic
# ---------------------------------------------------------------------------
def reconcile_sheet(uid_map: Dict[str, Dict[str, str]]) -> None:
    existing_rows = read_sheet_range(f"{SHEET_NAME}!A:C")
    header = existing_rows[0] if existing_rows else []
    data_rows = existing_rows[1:] if len(existing_rows) > 1 else []

    sheet_uids = set()
    rows_to_clear: List[int] = []
    for idx, row in enumerate(data_rows):
        uid = str(row[0]).strip() if len(row) > 0 else ""
        if uid:
            sheet_uids.add(uid)
            if uid not in uid_map:
                rows_to_clear.append(idx)
    # Clear orphan rows
    for idx in rows_to_clear:
        data_rows[idx] = ["", "", ""]

    # Append missing UIDs
    missing_uids = set(uid_map.keys()) - sheet_uids
    new_rows: List[List[str]] = []
    for uid in sorted(missing_uids):
        info = uid_map[uid]
        encoded_path = urllib.parse.quote(info["path"])
        url = GITHUB_BASE_URL + encoded_path
        drive_id = info.get("drive_id", "")
        new_rows.append([uid, url, drive_id])

    updated_rows = ([header] if header else []) + data_rows + new_rows
    update_sheet_range(f"{SHEET_NAME}!A:C", updated_rows)

    # Verify URLs and log any failures
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as log:
        for uid, url, _ in new_rows:
            result = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url], capture_output=True, text=True)
            code = result.stdout.strip()
            if code != "200":
                log.write(f"[WARN] UID {uid} URL {url} returned {code}\n")

    # Scan G‑K columns for orphan UIDs (starting at row 282)
    gk_rows = read_sheet_range(f"{SHEET_NAME}!G282:K")
    orphan_uids: List[str] = []
    for row in gk_rows:
        uid = str(row[0]).strip() if row else ""
        if uid and uid not in uid_map:
            orphan_uids.append(uid)
    if orphan_uids:
        with open(REPORT_PATH, "a", encoding="utf-8") as log:
            log.write("\n=== Orphan UIDs in G‑K (Token/Reel) ===\n")
            for uid in orphan_uids:
                log.write(f"{uid}\n")

def main() -> None:
    uid_map = build_uid_map()
    print(f"Found {len(uid_map)} token markdown files.")
    reconcile_sheet(uid_map)
    print(f"Done. Report written to {REPORT_PATH}")

if __name__ == "__main__":
    main()
