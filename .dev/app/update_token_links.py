#!/usr/bin/env python3
"""
update_token_links.py — Remplace les liens TOKEN MAP.md#section par
des liens vers les fiches individuelles dans Memory/Tokens/.

Seules les liaisons de type [**[Token]**](...TOKEN MAP...) sont remplacées.
Les non-tokens (N°..., Adresse..., Téléphone...) restent vers la section.

Usage: python3 .dev/app/update_token_links.py [--dry-run]
"""

import os, re, sys, unicodedata
from urllib.parse import quote

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
JETONS_DIR = os.path.join(BASE, "Memory", "Tokens")
DRY_RUN = "--dry-run" in sys.argv

# ─── build token mapping ───────────────────────────────────

def normalize(s):
    """Lowercase + remove accents + standardize spaces."""
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().replace("'", " ").replace("-", " ").replace("  ", " ").strip()
    return s

TOKEN_MAP_RAW = {
    'La Victime': 'token-victime-nom-complet',
    'Le Président de l\'Exploitation': 'token-exploitation-president-nom',
    'La Directrice Générale de l\'Exploitation': 'token-exploitation-dg-nom',
    'Le Préposé de l\'Exploitation': 'token-exploitation-prepose-nom',
    'Le Propriétaire des Murs': 'token-exploitation-bailleur-nom',
    'Le Chirurgien SOS Main': 'token-hopital-sosmain-chirurgien',
    'Le Médecin en Urgence': 'token-hopital-urgence-medecin',
    'Le Médecin Généraliste': 'token-victime-medecin-generaliste',
    'La Gestionnaire CPAM': 'token-cpam-gestionnaire-nom',
    'Nom de l\'Avocat de la Victime': 'token-victime-avocat-nom',
    'L\'Adjoint au Maire de la Commune': 'token-mairie-adjoint-nom',
    'L\'Exploitant du Commerce (La SAS)': 'token-exploitation-raison-sociale',
    'L\'Établissement SOS Main': 'token-hopital-sosmain-nom',
    'L\'Adresse de la Victime': 'token-victime-adresse',
    'L\'Adresse de l\'Exploitation': 'token-exploitation-adresse',
    'L\'Adresse du Président': 'token-exploitation-president-adresse',
    'La Ville de l\'Accident': 'token-accident-ville',
    'La Ville de Résidence de la Victime': 'token-victime-ville-residence',
    'La Métropole Régionale': 'token-accident-metropole',
    'La Ville de l\'Établissement SOS Main': 'token-hopital-sosmain-ville',
    'Le Téléphone de la Victime': 'token-victime-telephone',
    'Code Postal de l\'Accident': 'token-accident-code-postal',
    'Date de naissance de la victime': 'token-victime-date-naissance',
    'L\'Email de la Victime': 'token-victime-email',
    'L\'Identifiant Professionnel de la Victime': 'token-victime-id-professionnel',
    'L\'Identifiant de l\'Exploitation': 'token-exploitation-id',
    'SIREN de l\'Exploitation': 'token-exploitation-siren',
    'Prénom de la Victime': 'token-victime-prenom',
    'Âge de la Victime': 'token-victime-age',
    'Capital Social de l\'Exploitation': 'token-exploitation-capital-social',
    'L\'Email de l\'Adjoint au Maire': 'token-mairie-adjoint-email',
    'L\'Email du Secrétariat de la Mairie': 'token-mairie-secretariat-email',
    'DATE RELANCE V2': 'token-accident-date-relance-v2',
    'DATE REOUVERTURE BOUTIQUE': 'token-exploitation-date-reouverture',
    'J+0 Accident': 'token-j-0-accident',
    'J+1 Chirurgie': 'token-j-1-chirurgie',
    'J+2 Sortie': 'token-j-2-sortie',
    'J+3 Premiers arrêts': 'token-j-3-premiers-arrets',
    'J+4 Dépôt de plainte': 'token-j-4-depot-de-plainte',
    'J+5 Ouverture CPAM': 'token-j-5-ouverture-cpam',
    'J+12 Facture': 'token-j-12-facture',
    'J+18 Incohérence CPAM': 'token-j-18-incoherence-cpam',
    'J+21 Contrôle chirurgical': 'token-j-21-controle-chirurgical',
    'J+25 Première kiné': 'token-j-25-premiere-kine',
    'J+27 Confirmation kiné': 'token-j-27-confirmation-kine',
    'J+31 Mises en demeure': 'token-j-31-mises-en-demeure',
    'J+32 Assignation référé': 'token-j-32-assignation-refere',
    'J+33 Plainte complémentaire': 'token-j-33-plainte-complementaire',
    'J+35 AR propriétaire': 'token-j-35-ar-proprietaire',
    'J+36 Lettre consolidation': 'token-j-36-lettre-consolidation',
    'J+37 Assignation 145': 'token-j-37-assignation-145',
    'J+37 Requête 145': 'token-j-37-assignation-145',
    'J+38 Constitution PC': 'token-j-38-constitution-pc',
    'J+38 Mise à jour': 'token-j-38-mise-a-jour',
    'J+40 Consultation suivi': 'token-j-40-consultation-suivi',
    'J+41 Courrier SIE URSSAF': 'token-j-41-courrier-sie-urssaf',
    'J+41 Requête Constat 145': 'token-j-41-requete-constat-145',
    'J+46 Échéance amiable': 'token-j-46-echeance-amiable',
    'J+55 Fin d\'ITT': 'token-j-55-fin-d-itt',
    'J+167 Expertise UMJ': 'token-j-167-expertise-umj',
}

# Build normalized index for fuzzy matching
NORM_MAP = {normalize(k): v for k, v in TOKEN_MAP_RAW.items()}

# Non-token names that should stay pointing to section
NON_TOKENS = {
    'N° PV Police',
    'N° Transaction Wero',
    'N° LRAR Exploitant',
    'N° LRAR Président',
    'N° LRAR Directrice',
    'N° LRAR Propriétaire',
    'N° LRAR Parquet',
    'Adresse Tribunal Judiciaire',
    'Adresse de la Mairie',
    'Adresse du Commissariat',
    'Téléphone Commissariat',
    'Téléphone Huissier',
    'Téléphone Ordre Avocats',
    'Téléphone Tribunal Judiciaire',
    # Already have token files:
}

def resolve_token(name):
    if name in NON_TOKENS:
        return None
    if name in TOKEN_MAP_RAW:
        return TOKEN_MAP_RAW[name]
    norm = normalize(name)
    if norm in NORM_MAP:
        return NORM_MAP[norm]
    return None

def jeton_relative_path(from_file):
    from_dir = os.path.dirname(from_file)
    return os.path.relpath(JETONS_DIR, from_dir)

def find_tokens_in_content(content):
    pattern = re.compile(
        r'(\*\*\[([^\]]+)\]\*\*)'
        r'\]\('
        r'[^)]*'
        r'TOKEN[^)]*MAP\.md[^)]*\)',
        re.DOTALL
    )
    results = []
    for m in pattern.finditer(content):
        full_display = m.group(1)
        token_name = m.group(2).strip()
        anchor = resolve_token(token_name)
        if anchor is None:
            continue  # non-token reference or unknown
        results.append({
            'start': m.start(),
            'end': m.end(),
            'display': full_display,
            'token_name': token_name,
            'anchor': anchor,
            'full_match': m.group(0),
        })
    return results

def replace_links(content, from_file):
    tokens = find_tokens_in_content(content)
    if not tokens:
        return content, 0
    rel_path = jeton_relative_path(from_file)
    tokens.sort(key=lambda t: t['start'], reverse=True)
    modified = content
    count = 0
    for t in tokens:
        old = t['full_match']
        new_url = os.path.join(rel_path, f"{t['anchor']}.md")
        new_url = quote(new_url, safe='/')
        new = f"{t['display']}]({new_url})"
        if old in modified:
            modified = modified.replace(old, new, 1)
            count += 1
    return modified, count

def link_plain_tokens_in_tokenmap():
    """
    Traite TOKEN MAP.md : transforme les `**[...]**` en texte brut
    en liens cliquables vers Tokens/*.md.
    """
    tokenmap_path = os.path.join(BASE, "Memory", "TOKEN MAP.md")
    if not os.path.isfile(tokenmap_path):
        print("  ❌ TOKEN MAP.md introuvable")
        return 0, 0

    rel_tokens_dir = os.path.relpath(JETONS_DIR, os.path.dirname(tokenmap_path))

    with open(tokenmap_path) as f:
        content = f.read()

    new_content = content
    # Match `` `**[Token Name]**` `` OR `**[Token Name]**` (with or without backticks)
    pattern = re.compile(r'`?\*\*\[([^\]]+)\]\*\*`?')
    replaced = 0

    # Find all matches; iterate in reverse order to preserve positions
    matches = []
    for m in pattern.finditer(content):
        token_name = m.group(1).strip()
        anchor = resolve_token(token_name)
        if anchor is None:
            continue
        # Check not already inside a Markdown link
        start = m.start()
        # Look backwards to see if there's a `](...)` or similar link context
        # A simple heuristic: if there's a `[` immediately before without `!`, it might be linked
        before = content[max(0, start - 6):start]
        if before.rstrip().endswith('[') and not before.rstrip().endswith('!['):
            # Could be part of an existing link — check if followed by `](...)`
            after = content[m.end():m.end() + 100]
            # Skip if this is already inside a Markdown link (...) 
            if after.lstrip().startswith(']('):
                continue
        matches.append(m)

    # Process in reverse to maintain offsets
    for m in reversed(matches):
        token_name = m.group(1).strip()
        anchor = resolve_token(token_name)
        if anchor is None:
            continue
        # Build the link
        token_file = f"{anchor}.md"
        rel_url = os.path.join(rel_tokens_dir, token_file)
        rel_url = quote(rel_url, safe='/')
        new_link = f"[**[{token_name}]**]({rel_url})"
        new_content = new_content[:m.start()] + new_link + new_content[m.end():]
        replaced += 1

    if replaced > 0:
        if DRY_RUN:
            print(f"  ~ Memory/TOKEN MAP.md: {replaced} lien(s) (dry-run)")
        else:
            with open(tokenmap_path, 'w') as f:
                f.write(new_content)
            print(f"  ✅ Memory/TOKEN MAP.md: {replaced} lien(s)")
    else:
        print("  ℹ️  Memory/TOKEN MAP.md: aucun changement")
    return 1 if replaced > 0 else 0, replaced


def main():
    # ── Step 1: process TOKEN MAP.md itself ──
    tmap_files, tmap_links = link_plain_tokens_in_tokenmap()

    # ── Step 2: process all other .md files that reference TOKEN MAP.md ──
    all_files = []
    for root, dirs, filenames in os.walk(BASE):
        skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'Tokens'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            all_files.append(os.path.join(root, fn))
    total_replaced = tmap_links
    total_files_changed = tmap_files
    for fp in all_files:
        with open(fp) as f:
            content = f.read()
        if 'TOKEN' not in content and 'TOKEN%20MAP' not in content:
            continue
        new_content, replaced = replace_links(content, fp)
        if replaced > 0:
            if DRY_RUN:
                rel = os.path.relpath(fp, BASE)
                print(f"  ~ {rel}: {replaced} lien(s)")
            else:
                with open(fp, 'w') as f:
                    f.write(new_content)
                rel = os.path.relpath(fp, BASE)
                print(f"  ✅ {rel}: {replaced} lien(s)")
            total_replaced += replaced
            total_files_changed += 1
    print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}Total: {total_files_changed} fichiers, {total_replaced} liens remplacés")

if __name__ == '__main__':
    main()
