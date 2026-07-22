#!/usr/bin/env python3
"""Hermès Phase 2: URL-encode spaces in markdown inline link URLs.

Replaces raw spaces with %%20 inside [text](url) and ![alt](url) patterns
across all .md files in the repo. Avoids double-encoding existing %%20
and skips file:/// URLs.
"""

import re
import os
import subprocess
import sys

BASE = "/home/crilocom/accident-main"

def url_encode_spaces(url: str) -> str:
    if url.startswith("file:///"):
        return url
    # Preserve existing %%20 to avoid double-encoding
    parts = url.split("%20")
    encoded_parts = [p.replace(" ", "%20") for p in parts]
    return "%20".join(encoded_parts)

def fix_file(filepath: str) -> int:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    def _replace(m):
        before = m.group(1)  # !?[text](
        url    = m.group(2)  # URL portion
        after  = m.group(3)  # ) or )> … etc.

        if url.startswith("file:///"):
            return m.group(0)

        new_url = url_encode_spaces(url)
        if new_url != url:
            return before + new_url + after
        return m.group(0)

    # Match [text](url) and ![alt](url) — URL is everything up to the first )
    content = re.sub(
        r'(!?\[[^\]]*\]\()([^)]+)(\))',
        _replace,
        content,
    )

    if content == original:
        return 0

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return 1

def main():
    # Gather files that still have raw spaces inside markdown link URLs
    result = subprocess.run(
        ["grep", "-rPl", r'\]\([^)]* [^)]*\)', "--include=*.md", BASE],
        capture_output=True, text=True,
    )
    files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]

    if not files:
        print("No files with raw spaces found — nothing to do.")
        return

    print(f"Found {len(files)} files with raw spaces in markdown URLs\n")

    ok = err = 0
    for fp in files:
        try:
            if fix_file(fp):
                print(f"  \u2713 {os.path.relpath(fp, BASE)}")
                ok += 1
            else:
                print(f"  - {os.path.relpath(fp, BASE)} (no change)")
        except Exception as e:
            print(f"  \u2717 {os.path.relpath(fp, BASE)} — {e}")
            err += 1

    print(f"\nDone: {ok} modified, {err} errors")

if __name__ == "__main__":
    main()
