#!/usr/bin/env python3
import os
import re
import urllib.parse

BASE_DIR = "/home/crilocom/accident-main"

def encode_relative_url(url):
    # Si c'est une URL absolue (http, mailto, etc.), on n'y touche pas
    if url.startswith(("http://", "https://", "mailto:", "tel:")):
        return url
    
    # On décode d'abord pour éviter les doubles encodages
    decoded = urllib.parse.unquote(url)
    
    # On encode proprement chaque segment en gardant les / intacts
    # safe='/' permet de ne pas encoder les séparateurs de dossiers
    # safe='/#' permet de garder aussi les ancres de paragraphes intactes
    encoded = urllib.parse.quote(decoded, safe='/#')
    return encoded

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Regex pour capturer les liens markdown standard : [texte](url)
    # On doit être attentif à ne pas capturer les sauts de ligne ou d'autres parenthèses
    pattern = r"(\]\()([^)\n]+)(\))"
    
    modified = False
    new_lines = []
    
    for line in content.split("\n"):
        def replace_match(match):
            prefix = match.group(1)
            url = match.group(2).strip()
            suffix = match.group(3)
            
            encoded_url = encode_relative_url(url)
            if encoded_url != url:
                nonlocal modified
                modified = True
                return f"{prefix}{encoded_url}{suffix}"
            return match.group(0)
            
        new_line = re.sub(pattern, replace_match, line)
        new_lines.append(new_line)
        
    if modified:
        new_content = "\n".join(new_lines)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Modifié : {os.path.relpath(file_path, BASE_DIR)}")

def main():
    print("=== Début de l'audit et encodage des liens dans tous les README.md ===")
    for root, dirs, files in os.walk(BASE_DIR):
        # Exclure les répertoires techniques de développement
        if any(p in root for p in (".git", "node_modules", "__pycache__", ".venv", ".pytest_cache")):
            continue
            
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                process_file(file_path)
    print("=== Fin de l'encodage ===")

if __name__ == "__main__":
    main()
