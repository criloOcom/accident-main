import os
import re
import sys
from pathlib import Path
from googleapiclient import discovery

sys.path.insert(0, os.path.join(os.getcwd(), "app"))
from drive_auth import get_drive_service

REPO = Path(__file__).resolve().parent.parent
ACTES_DIR = REPO / "actes"

def get_citations_from_sheet():
    service = get_drive_service()
    sheets = discovery.build("sheets", "v4", credentials=service._http.credentials)
    spreadsheet_id = "14wbJajn-Vmz_lnNwiJuYSnT70hcozN7AnzvOVyuF1sQ"
    
    result = sheets.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range="A1:O100"
    ).execute()
    
    rows = result.get("values", [])
    
    id_to_citation = {}
    key_to_citation = {}
    
    for idx, row in enumerate(rows):
        if idx == 0 or idx == 1:
            continue
        if len(row) > 0:
            ref_key = row[0].strip()
            citation = row[5].strip() if len(row) > 5 else ""
            legi_id = row[11].strip() if len(row) > 11 else ""
            
            if citation:
                if legi_id:
                    id_to_citation[legi_id] = citation
                if ref_key:
                    key_to_citation[ref_key] = citation
                    
    return id_to_citation, key_to_citation

def inject_in_file(filepath, id_to_citation, key_to_citation, dry_run=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We split by paragraphs (double newlines)
    paragraphs = content.split('\n\n')
    new_paragraphs = []
    
    # Track which citations have been injected in this file to do it only once per file
    injected_keys = set()
    
    # Compile regex for LEGIARTI and JURITEXT
    legi_pattern = re.compile(r'LEGIARTI\d+')
    juri_pattern = re.compile(r'JURITEXT\d+')
    
    modified = False
    
    i = 0
    while i < len(paragraphs):
        para = paragraphs[i]
        new_paragraphs.append(para)
        
        # Check if the paragraph contains any reference key or ID
        found_ids = []
        for m in legi_pattern.finditer(para):
            found_ids.append(m.group())
        for m in juri_pattern.finditer(para):
            found_ids.append(m.group())
            
        # Also check for reference keys (like Art. 1242 or Arrêt Cousin) by text matching if needed
        # But ID matching via URL is much safer and precise. Let's start with ID matching.
        for ref_id in found_ids:
            if ref_id in id_to_citation and ref_id not in injected_keys:
                citation_text = id_to_citation[ref_id]
                
                # Check if the next paragraph is already a blockquote with this citation
                next_is_bq = False
                if i + 1 < len(paragraphs):
                    next_para = paragraphs[i + 1]
                    if next_para.strip().startswith(">"):
                        # Extract first 30 chars of citation to compare
                        clean_cit = re.sub(r'[^a-zA-Z0-9]', '', citation_text)[:20]
                        clean_next = re.sub(r'[^a-zA-Z0-9]', '', next_para)[:20]
                        if clean_cit in clean_next or clean_next in clean_cit:
                            next_is_bq = True
                            
                if not next_is_bq:
                    # Format blockquote
                    # Format as: > « *citation* » or similar
                    bq_lines = []
                    for line in citation_text.split('\n'):
                        bq_lines.append(f"> {line}")
                    blockquote = "\n".join(bq_lines)
                    
                    new_paragraphs.append(blockquote)
                    injected_keys.add(ref_id)
                    modified = True
                    print(f"  [{filepath.name}] Injected citation for ID {ref_id}")
                else:
                    injected_keys.add(ref_id) # Mark as seen to avoid duplicate checks
                    
        i += 1
        
    if modified:
        new_content = '\n\n'.join(new_paragraphs)
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  [{filepath.name}] SAVED.")
        else:
            print(f"  [{filepath.name}] Dry-run: would save modified content.")
            
    return modified

def main():
    dry_run = "--save" not in sys.argv
    print(f"Loading citations from Google Sheet (Dry Run: {dry_run})...")
    id_to_citation, key_to_citation = get_citations_from_sheet()
    print(f"Loaded {len(id_to_citation)} ID-based citations.")
    
    # Recursively find all markdown files in actes/
    md_files = []
    for root, dirs, files in os.walk(ACTES_DIR):
        for f in files:
            if f.endswith(".md"):
                md_files.append(Path(root) / f)
                
    print(f"Found {len(md_files)} markdown files in actes/.")
    
    modified_count = 0
    for filepath in md_files:
        if inject_in_file(filepath, id_to_citation, key_to_citation, dry_run=dry_run):
            modified_count += 1
            
    print(f"\nTotal files modified: {modified_count}")

if __name__ == "__main__":
    main()
