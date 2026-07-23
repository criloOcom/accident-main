#!/usr/bin/env python3
"""Rebuild the PJ sheet rows 146-279 with normalized paths + titles in I/L."""

import os
import re
import yaml
import unicodedata

SHEET_ID = "1cwb8L5fc7HqsAHP6IH32gSFwKRIdSztcYk1XmfbaYIg"
BASE = "/home/crilocom/accident-main"
TOKEN_DIR = "Actes/Token"
REEL_DIR = "Actes/Reel"
GITHUB_BASE = "https://github.com/criloOcom/accident-main/blob/main/"


def normalize_path(path: str) -> str:
    """Normalize a path component to remove accents/special chars."""
    parts = path.split("/")
    normalized = []
    for p in parts:
        nfkd = unicodedata.normalize("NFKD", p)
        ascii_ = nfkd.encode("ascii", "ignore").decode("ascii")
        ascii_ = ascii_.replace("&", "et")
        ascii_ = ascii_.replace("'", "")
        ascii_ = ascii_.replace("\u2014", "-")
        ascii_ = re.sub(r'[\s\(\)]+', '_', ascii_)
        ascii_ = re.sub(r'_+', '_', ascii_)
        ascii_ = ascii_.strip('_')
        normalized.append(ascii_)
    return "/".join(normalized)


def read_yaml_fields(filepath: str):
    """Read uid, title and date from YAML front matter (resilient parser)."""
    uid = None
    title = None
    date = None
    try:
        with open(filepath) as f:
            content = f.read()
        # Extract YAML between --- markers
        match = re.match(r'^---\s*\n(.*?)\n(?:---|\.\.\.)', content, re.DOTALL)
        if match:
            raw = match.group(1)
            # Try safe YAML first
            try:
                data = yaml.safe_load(raw)
                if data:
                    uid = data.get("uid")
                    title = data.get("title")
                    date = data.get("date")
            except Exception:
                pass
            # Fallback: regex extraction if YAML failed
            if not uid:
                m = re.search(r'^uid:\s*(\S+)', raw, re.MULTILINE)
                if m:
                    uid = m.group(1)
            if not title:
                m = re.search(r'^title:\s*(.+?)$', raw, re.MULTILINE)
                if m:
                    title = m.group(1).strip().strip("'\"")
            if not date:
                m = re.search(r'^date:\s*(.+?)$', raw, re.MULTILINE)
                if m:
                    date = m.group(1).strip().strip("'\"")
    except Exception as e:
        print(f"  WARN: can't read {filepath}: {e}")
    return uid, title, date


def collect_files():
    """Collect all Token and Reel files, extract uid+title, build URLs."""
    rows = []
    token_files = {}
    reel_files = {}
    
    # Walk Token
    for dirpath, _, filenames in os.walk(os.path.join(BASE, TOKEN_DIR)):
        for fname in filenames:
            if not fname.endswith(".md") or fname == "README.md":
                continue
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, os.path.join(BASE, TOKEN_DIR))
            uid, title, date = read_yaml_fields(full)
            if uid:
                token_files[uid] = (rel, title, date, full)
            else:
                print(f"  WARN: no uid in {full}")
    
    # Walk Reel
    for dirpath, _, filenames in os.walk(os.path.join(BASE, REEL_DIR)):
        for fname in filenames:
            if not fname.endswith(".md") or fname == "README.md":
                continue
            full = os.path.join(dirpath, fname)
            rel = os.path.relpath(full, os.path.join(BASE, REEL_DIR))
            uid, title, date = read_yaml_fields(full)
            if uid:
                reel_files[uid] = (rel, title, date, full)
    
    # Build rows: match by uid
    all_uids = set(token_files.keys()) | set(reel_files.keys())
    
    for uid in sorted(all_uids):
        t_rel, t_title, t_date, _ = token_files.get(uid, (None, None, None, None))
        r_rel, r_title, r_date, _ = reel_files.get(uid, (None, None, None, None))
        
        if t_rel:
            t_url = GITHUB_BASE + TOKEN_DIR + "/" + normalize_path(t_rel)
        else:
            t_url = ""
        
        if r_rel:
            r_url = GITHUB_BASE + REEL_DIR + "/" + normalize_path(r_rel)
        else:
            r_url = ""
        
        # Use Token date, fallback to Reel date
        date = t_date or r_date or ""
        if hasattr(date, 'strftime'):
            date = date.strftime("%Y-%m-%d")
        date = str(date)
        
        # Column order: G=uidToken, H=urlToken, I=titleToken, J=uidReel, K=urlReel, L=titleReel
        row = [uid, t_url, t_title or "", uid, r_url, r_title or ""]
        rows.append(row)
        # Store date separately for column Q
        rows[-1].append(date)
    
    return rows


def main():
    import json
    import sys
    
    rows = collect_files()
    print(f"Collected {len(rows)} uid entries")
    
    # Output as JSON for the calling script
    output = {
        "sheet_id": SHEET_ID,
        "range": "@!G146",  # Starting from row 146
        "rows": rows
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
