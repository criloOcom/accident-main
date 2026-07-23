#!/usr/bin/env python3
"""Scan all Token .md files, extract uid, build mapping, then fix sheet URLs."""

import os
import re
import json
import sys

TOKEN_DIR = "Actes/Token"
SHEET_ID = "1cwb8L5fc7HqsAHP6IH32gSFwKRIdSztcYk1XmfbaYIg"

def extract_uid_from_file(filepath):
    """Extract uid from YAML front matter of a .md file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Match YAML front matter between --- markers
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if m:
        yaml_block = m.group(1)
        uid_m = re.search(r'^uid:\s*(\S+)', yaml_block, re.MULTILINE)
        if uid_m:
            return uid_m.group(1)
    return None

def extract_drive_id_from_file(filepath):
    """Extract drive_id from YAML front matter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if m:
        yaml_block = m.group(1)
        did_m = re.search(r'^drive_id:\s*(\S+)', yaml_block, re.MULTILINE)
        if did_m:
            val = did_m.group(1)
            if val and val != '"À compléter"' and val != 'À compléter' and val != '""' and val != "''":
                return val.strip('"').strip("'")
    return ""

def build_uid_map():
    """Build mapping uid -> (real_path, drive_id) for all Token .md files."""
    uid_map = {}
    base = os.path.abspath(TOKEN_DIR)
    for root, dirs, files in os.walk(TOKEN_DIR):
        for fname in files:
            if not fname.endswith('.md') or fname == 'README.md':
                continue
            fpath = os.path.join(root, fname)
            uid = extract_uid_from_file(fpath)
            if uid:
                rel_path = os.path.relpath(fpath, base)
                drive_id = extract_drive_id_from_file(fpath)
                uid_map[uid] = (rel_path, drive_id)
    return uid_map

def main():
    print("=== Building uid map from Token .md files ===")
    uid_map = build_uid_map()
    print(f"Found {len(uid_map)} uids in Token files.")

    # Output as JSON for verification
    result = {}
    for uid, (path, did) in sorted(uid_map.items()):
        result[uid] = {"path": path, "drive_id": did}
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
