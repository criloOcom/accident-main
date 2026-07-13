#!/usr/bin/env python3
"""
encode_jeton_links.py — URL-encode les chemins des liens vers 🗂️ Tokens/
qui ont été écrits avec des caractères littéraux (espaces, emojis).

Les liens passent de :
  ../../../🧠 Memory/🗂️ Tokens/token-la-victime.md
à :
  ../../../%F0%9F%A7%A0%20Memory/%F0%9F%97%82%EF%B8%8F%20Tokens/token-la-victime.md

Usage: python3 .dev/app/encode_jeton_links.py [--dry-run]
"""

import os, re, sys
from urllib.parse import quote

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DRY_RUN = "--dry-run" in sys.argv

def encode_url_path(url):
    """URL-encode a path while preserving slashes, parentheses, and hash."""
    return quote(url, safe='/#()')

def main():
    all_files = []
    for root, dirs, filenames in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', '.pytest_cache'}]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            all_files.append(os.path.join(root, fn))
    
    total_fixed = 0
    total_files_changed = 0
    
    # Pattern: ](some-path-with-Tokens-but-already-with-literal-chars)
    # Match links pointing to Tokens that have NOT been URL-encoded
    # (contain literal emoji characters or spaces)
    pattern = re.compile(
        r'(]\([^)]*)'            # ]( and the URL
        r'(\u2b50|\U0001f9e0|\U0001f5c2|\U0001f4c2|\u0020)'  # has literal unicode or space
        r'[^)]*'                  # rest of URL
        r'Tokens[^)]*\.md\)',     # ends with Tokens/...md)
        re.UNICODE
    )
    
    # Simpler approach: find any ](url) where url contains literal 🧠 or 🗂️ or space in the Tokens path
    # and the url is NOT already URL-encoded (no % in the Tokens part)
    
    for fp in all_files:
        with open(fp) as f:
            content = f.read()
        
        if '🗂️ Tokens' not in content and '🧠 Memory/🗂' not in content:
            continue
        
        # Look for patterns like ](../../../🧠 Memory/🗂️ Tokens/token-xxx.md)
        # These have literal emoji and/or spaces in the URL
        fix_pattern = re.compile(
            r'(]\('
            r')([^)]*?)'         # the URL path
            r'(\))',              # closing paren
            re.DOTALL
        )
        
        modified = content
        fixed = 0
        
        for m in fix_pattern.finditer(content):
            url = m.group(2)
            # Only touch links that point to Tokens with literal chars
            if 'Tokens' not in url and '🗂️ Tokens' not in url:
                continue
            # Skip already-encoded links
            if '%' in url:
                continue
            # Check if actually needs encoding (has spaces or emoji)
            needs_encoding = ' ' in url or '🧠' in url or '🗂️' in url
            if not needs_encoding:
                continue
            
            encoded = encode_url_path(url)
            if encoded == url:
                continue
            
            old = m.group(0)
            new = f"] ({encoded})"  # Wait, m.group(0) = ](url)
            # Actually let me reconstruct properly
            
            fixed += 1
        
        # Actually let me use a simpler approach
        modified = content
        fixed = 0
        
        # Find all markdown links
        link_pattern = re.compile(r'\]\(([^)]+)\)')
        
        for m in link_pattern.finditer(content):
            url = m.group(1)
            # Only process Tokens links with literal chars
            if 'Tokens' not in url and '🗂️ Tokens' not in url:
                continue
            if '%' in url:
                continue
            if ' ' not in url and '🧠' not in url and '🗂️' not in url:
                continue
            
            encoded = encode_url_path(url)
            if encoded == url:
                continue
            
            old = f']({url})'
            new = f']({encoded})'
            modified = modified.replace(old, new, 1)
            fixed += 1
        
        if fixed > 0:
            if DRY_RUN:
                rel = os.path.relpath(fp, BASE)
                print(f"  ~ {rel}: {fixed} lien(s)")
            else:
                with open(fp, 'w') as f:
                    f.write(modified)
                rel = os.path.relpath(fp, BASE)
                print(f"  ✅ {rel}: {fixed} lien(s)")
            total_fixed += fixed
            total_files_changed += 1
    
    print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}Total: {total_files_changed} fichiers, {total_fixed} liens encodés")

if __name__ == '__main__':
    main()
