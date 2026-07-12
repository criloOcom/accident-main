#!/usr/bin/env python3
"""
update_token_links.py — Remplace les liens TOKEN MAP.md#section par
des liens vers les fiches individuelles dans 🧠 Memory/🗂️ Jetons/.

Seules les liaisons de type [**[Token]**](...TOKEN MAP...) sont remplacées.
Les non-tokens (N°..., Adresse..., Téléphone...) restent vers la section.

Usage: python3 .dev/app/update_token_links.py [--dry-run]
"""

import os, re, sys, unicodedata

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
JETONS_DIR = os.path.join(BASE, "🧠 Memory", "🗂️ Jetons")
DRY_RUN = "--dry-run" in sys.argv

# ─── build token mapping ───────────────────────────────────

def normalize(s):
    """Lowercase + remove accents + standardize spaces."""
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().replace("'", " ").replace("-", " ").replace("  ", " ").strip()
    return s

TOKEN_MAP_RAW = {
    'La Victime': 'token-la-victime',
    'Le Président de l\'Exploitation': 'token-le-president-de-l-exploitation',
    'La Directrice Générale de l\'Exploitation': 'token-la-directrice-generale-de-l-exploitation',
    'Le Préposé de l\'Exploitation': 'token-le-prepose-de-l-exploitation',
    'Le Propriétaire des Murs': 'token-le-proprietaire-des-murs',
    'Le Chirurgien SOS Main': 'token-le-chirurgien-sos-main',
    'Le Médecin en Urgence': 'token-le-medecin-en-urgence',
    'Le Médecin Généraliste': 'token-le-medecin-generaliste',
    'La Gestionnaire CPAM': 'token-la-gestionnaire-cpam',
    'Nom de l\'Avocat de la Victime': 'token-nom-de-l-avocat-de-la-victime',
    'L\'Adjoint au Maire de la Commune': 'token-l-adjoint-au-maire-de-la-commune',
    'L\'Exploitant du Commerce (La SAS)': 'token-l-exploitant-du-commerce-la-sas',
    'L\'Établissement SOS Main': 'token-l-etablissement-sos-main',
    'L\'Adresse de la Victime': 'token-l-adresse-de-la-victime',
    'L\'Adresse de l\'Exploitation': 'token-l-adresse-de-l-exploitation',
    'L\'Adresse du Président': 'token-l-adresse-du-president',
    'La Ville de l\'Accident': 'token-la-ville-de-l-accident',
    'La Ville de Résidence de la Victime': 'token-la-ville-de-residence-de-la-victime',
    'La Métropole Régionale': 'token-la-metropole-regionale',
    'La Ville de l\'Établissement SOS Main': 'token-la-ville-de-l-etablissement-sos-main',
    'L\'Email de la Victime': 'token-l-email-de-la-victime',
    'L\'Identifiant Professionnel de la Victime': 'token-l-identifiant-professionnel-de-la-victime',
    'L\'Identifiant de l\'Exploitation': 'token-l-identifiant-de-l-exploitation',
    'SIREN de l\'Exploitation': 'token-siren-de-l-exploitation',
    'L\'Email de l\'Adjoint au Maire': 'token-l-email-de-l-adjoint-au-maire',
    'L\'Email du Secrétariat de la Mairie': 'token-l-email-du-secretariat-de-la-mairie',
    'DATE RELANCE V2': 'token-date-relance-v2',
    'DATE REOUVERTURE BOUTIQUE': 'token-date-reouverture-boutique',
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
    'Le Téléphone de la Victime',
    'Code Postal de l\'Accident',
    'Date de naissance de la victime',
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
        new = f"{t['display']}]({new_url})"
        if old in modified:
            modified = modified.replace(old, new, 1)
            count += 1
    return modified, count

def main():
    all_files = []
    for root, dirs, filenames in os.walk(BASE):
        skip_dirs = {'.git', '__pycache__', '.pytest_cache', '🗂️ Jetons'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            all_files.append(os.path.join(root, fn))
    total_replaced = 0
    total_files_changed = 0
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
