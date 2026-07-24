#!/usr/bin/env python3
import os, glob, re

# Mapping officiel des références juridiques fréquentes vers Légifrance / Judilibre
LEGAL_DB = [
    (r"\barticle\s+L\.?\s*227-8\b(?!\s*\[)", "Article L227-8 du Code de commerce", "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006423238"),
    (r"\barticle\s+L\.?\s*124-3\b(?!\s*\[)", "Article L124-3 du Code des assurances", "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006411993"),
    (r"\barticle\s+1240\b(?!\s*\[)", "Article 1240 du Code civil", "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041571"),
    (r"\barticle\s+1241\b(?!\s*\[)", "Article 1241 du Code civil", "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041567"),
    (r"\barticle\s+1242\b(?!\s*\[)", "Article 1242 du Code civil", "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041565"),
    (r"\barticle\s+145\s+(?:du\s+Code\s+de\s+procédure\s+civile|CPC)\b(?!\s*\[)", "Article 145 du Code de procédure civile", "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006410264"),
    (r"\barticle\s+434-4\b(?!\s*\[)", "Article 434-4 du Code pénal", "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006418608"),
    (r"\bCass\.\s*Com\.?,?\s*20\s+mai\s+2003.*?(?:SATI|99-17\.092)\b(?!\s*\[)", "Cass. Com., 20 mai 2003, n° 99-17.092 (Arrêt SATI)", "https://www.legifrance.gouv.fr/juri/id/JURITEXT000007466847"),
    (r"\bCass\.\s*Com\.?,?\s*15\s+janvier\s+2020.*?(?:18-12\.256)\b(?!\s*\[)", "Cass. Com., 15 janvier 2020, n° 18-12.256", "https://www.legifrance.gouv.fr/juri/id/JURITEXT000041492576"),
    (r"\bCass\.\s*Civ\.?\s*2e,?\s*13\s+septembre\s+2018\b(?!\s*\[)", "Cass. Civ. 2e, 13 septembre 2018, n° 17-22.396", "https://www.legifrance.gouv.fr/juri/id/JURITEXT000037434551"),
]

def enrich_file(file_path):
    content = open(file_path, encoding="utf-8").read()
    new_content = content
    modified = False
    
    existing_fns = [int(n) for n in re.findall(r"\[\^(\d+)\]", content)]
    next_fn_idx = max(existing_fns) + 1 if existing_fns else 1
    
    new_footnotes = []
    
    for pattern, title, url in LEGAL_DB:
        def repl(m):
            nonlocal next_fn_idx, modified
            matched_text = m.group(0)
            fn_key = f"fn_legal_{next_fn_idx}"
            new_footnotes.append(f"[^{fn_key}]: {title} — {url}")
            res = f"{matched_text}[^{fn_key}]"
            next_fn_idx += 1
            modified = True
            return res
            
        new_content = re.sub(pattern, repl, new_content, flags=re.IGNORECASE)
        
    if modified and new_footnotes:
        new_content += "\n\n" + "\n".join(new_footnotes) + "\n"
        open(file_path, "w", encoding="utf-8").write(new_content)
        return True
    return False

def main():
    token_files = glob.glob("Actes/Token/**/*.md", recursive=True)
    count = 0
    for f in token_files:
        if "README.md" in f:
            continue
        if enrich_file(f):
            count += 1
    print(f"✅ Ingestion juridique terminée : {count} fichiers matrices Token enrichis de footnotes Légifrance/Judilibre !")

if __name__ == "__main__":
    main()
