#!/usr/bin/env python3
"""Link all `**[Finance Xxx]**` tokens to their token-finance-*.md files."""

import os
import re
from pathlib import Path

BASE = Path("/home/crilocom/accident-main")

# Mapping: token text -> relative filename in 🗂️ Tokens/
TOKEN_MAP = {
    "Finance Provision Référé": "token-finance-provision-refere.md",
    "Finance Article 700": "token-finance-article-700.md",
    "Finance Article 700 Référé 145": "token-finance-article-700-refere-145.md",
    "Finance Astreinte 145": "token-finance-astreinte-145.md",
    "Finance Evaluation Initiale": "token-finance-evaluation-initiale.md",
    "Finance Facture Chirurgie": "token-finance-facture-chirurgie.md",
    "Finance PGPA": "token-finance-pgpa.md",
    "Finance Incidence Professionnelle": "token-finance-incidence-professionnelle.md",
    "Finance DFP": "token-finance-dfp.md",
    "Finance Souffrances Endurées": "token-finance-souffrances-endurees.md",
    "Finance Préjudice Agrément": "token-finance-prejudice-agrement.md",
    "Finance Prestation Salon": "token-finance-prestation-salon.md",
    "Finance Préjudice Esthétique": "token-finance-prejudice-esthetique.md",
    "Finance Dévalorisation Pro": "token-finance-devalorisation-pro.md",
    "Finance Frais Divers": "token-finance-frais-divers.md",
    "Finance Prejudice Esthetique": "token-finance-prejudice-esthetique.md",
}

TOKENS_DIR = "🧠 Memory/🗂️ Tokens"

# URL-encode the tokens dir the way existing links are done
def url_encode_path(s: str) -> str:
    """Encode Unicode characters in a path segment (same style as existing links)."""
    result = []
    for ch in s:
        if ord(ch) > 127:
            for b in ch.encode("utf-8"):
                result.append(f"%{b:02X}")
        elif ch == " ":
            result.append("%20")
        else:
            result.append(ch)
    return "".join(result)

def get_relative_path(file_path: Path, token_filename: str) -> str:
    """Compute the relative path from file to the token file."""
    # Get the directory of the file
    file_dir = file_path.parent
    # Relative path from file_dir to BASE / TOKENS_DIR / token_filename
    rel_dir = os.path.relpath(BASE / TOKENS_DIR, file_dir)
    rel_path = Path(rel_dir) / token_filename
    # URL-encode the path
    parts = []
    for part in rel_path.parts:
        parts.append(url_encode_path(part))
    return "/".join(parts)

def find_affected_files() -> list[Path]:
    """Find all .md files under ⚖️ Actes/🔑 Token/ that contain Finance tokens."""
    actes_dir = BASE / "⚖️ Actes" / "🔑 Token"
    affected = []
    for root, _dirs, files in os.walk(actes_dir):
        for f in files:
            if not f.endswith(".md"):
                continue
            fp = Path(root) / f
            try:
                content = fp.read_text("utf-8")
            except Exception:
                continue
            for token_text in TOKEN_MAP:
                if f"**[{token_text}]**" in content:
                    affected.append(fp)
                    break
    return sorted(set(affected))

def main():
    files = find_affected_files()
    print(f"Found {len(files)} files with Finance tokens to link.")
    
    total_replacements = 0
    
    for fp in files:
        content = fp.read_text("utf-8")
        original = content
        
        for token_text, token_file in TOKEN_MAP.items():
            old = f"**[{token_text}]**"
            if old not in content:
                continue
            rel_path = get_relative_path(fp, token_file)
            new = f"[{old}]({rel_path})"
            content = content.replace(old, new)
            count = content.count(new) - original.count(new) + original.count(old) - content.count(old)
            # More precise: count replacements
            count_old = original.count(old)
            count_new = content.count(old)  # should be 0 if all replaced
            actual = count_old
            total_replacements += actual
        
        if content != original:
            fp.write_text(content, "utf-8")
            print(f"  ✅ {fp.relative_to(BASE)}")
    
    print(f"\nDone. Total replacements: {total_replacements}")

if __name__ == "__main__":
    main()
