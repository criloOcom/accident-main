#!/usr/bin/env python3
"""
generate_token_files.py — Génère les fiches individuelles pour chaque token
dans Memory/Tokens/ avec contenu enrichi (identité, chronologie, documents liés).

Usage: python3 .dev/app/generate_token_files.py [--dry-run]
"""

import os, re, unicodedata, sys

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
JETONS_DIR = os.path.join(BASE, "Memory", "Tokens")
TOKENMAP = os.path.join(BASE, "Memory", "TOKEN MAP.md")
STRICT = os.path.join(BASE, "Memory", "STRICT VARIABLES.md")

DRY_RUN = "--dry-run" in sys.argv

# ─── helpers ───────────────────────────────────────────────

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:50].strip('-')

def jplus_from_name(name):
    m = re.search(r'J\+(\d+)', name)
    return int(m.group(1)) if m else None

def read_strict():
    with open(STRICT) as f:
        return f.read()

def strict_var(content, key):
    m = re.search(r'^-\s+' + re.escape(key) + r'\s*:\s*(.+)$', content, re.MULTILINE)
    return m.group(1) if m else None

# ─── build token registry ──────────────────────────────────

def parse_tokens(tokenmap_content, strict_content):
    entries = []
    current_section = None
    lines = tokenmap_content.split('\n')

    # First pass: build anchor -> token_name mapping from <a id> tags
    pending_anchor = None
    for line in lines:
        sm = re.match(r'^## (.+?) \{#(.+?)\}$', line)
        if sm:
            current_section = sm.group(1)
            continue

        am = re.match(r'<a id="(token-[^"]+)"></a>', line)
        if am:
            pending_anchor = am.group(1)
            continue

        if pending_anchor:
            tm = re.search(r'`\*\*\[([^\]]+)\]\*\*`', line)
            if tm:
                token_name = tm.group(1)
                parts = line.split('`**[')
                real_values = []
                if len(parts) > 0:
                    before = parts[0].strip('| ')
                    cells = [c.strip() for c in before.split('|') if c.strip()]
                    if cells:
                        real_values = cells

                note = ""
                am2 = re.search(r'\]\*\*`\s*\|(.+)$', line)
                if am2:
                    note = am2.group(1).strip()

                entries.append({
                    'token_name': token_name,
                    'section': current_section or '',
                    'anchor': pending_anchor,
                    'real_values': real_values,
                    'note': note,
                })
            pending_anchor = None

    return entries

def add_enrichment(entries, strict_content):
    """Add context, role, professions from STRICT VARIABLES."""
    
    roles = {
        'La Victime': 'Victime de l\'accident corporel du 29 mai 2026',
        'Le Président de l\'Exploitation': 'Président de la SAS LES MAUVAIS GARÇONS',
        'La Directrice Générale de l\'Exploitation': 'Directrice Générale de la SAS LES MAUVAIS GARÇONS',
        'Le Préposé de l\'Exploitation': 'Coiffeur employé par la SAS (préposé)',
        'Le Propriétaire des Murs': 'Propriétaire-bailleur des locaux commerciaux',
        'Le Chirurgien SOS Main': 'Chirurgien de la main — SOS Main, Clinique de l\'Union',
        'Le Médecin en Urgence': 'Médecin urgentiste',
        'Le Médecin Généraliste': 'Médecin traitant',
        'La Gestionnaire CPAM': 'Gestionnaire de dossier à la CPAM',
        'Nom de l\'Avocat de la Victime': 'Avocat de la victime (nom réel à définir/confirmer)',
        'L\'Adjoint au Maire de la Commune': 'Adjoint au Maire de Foix (urbanisme, ERP)',
        'L\'Exploitant du Commerce (La SAS)': 'Personne morale exploitant le salon de coiffure au 22 Rue Lafaurie, 09000 Foix',
        'L\'Établissement SOS Main': 'Clinique spécialisée en chirurgie de la main',
    }
    
    professions = {
        'La Victime': 'Informaticien indépendant',
        'Le Président de l\'Exploitation': 'Chef d\'entreprise',
        'La Directrice Générale de l\'Exploitation': 'Chef d\'entreprise',
        'Le Préposé de l\'Exploitation': 'Coiffeur',
        'Le Chirurgien SOS Main': 'Chirurgien orthopédiste spécialiste de la main',
        'Le Médecin en Urgence': 'Médecin urgentiste',
        'Le Médecin Généraliste': 'Médecin généraliste',
        'La Gestionnaire CPAM': 'Agent CPAM',
        'L\'Adjoint au Maire de la Commune': 'Élu local',
    }

    notes = {
        'La Victime': f'A pris en charge la préparation du dossier juridique. Profession : {professions.get("La Victime", "")}. SIREN : {strict_var(strict_content, "IDENTIFIANT_PROFESSIONNEL") or strict_var(strict_content, "IDENTIFIANT Professionnel de la Victime") or "500 474 457"}.',
        'Le Président de l\'Exploitation': 'Dirigeant de droit de la SAS. Assigné personnellement in solidum avec la SAS (art. L.227-8 C.com. + art. 1240 C.civ.).',
        'La Directrice Générale de l\'Exploitation': 'Dirigeante de droit de la SAS. Assignée personnellement in solidum avec la SAS (art. L.227-8 C.com. + art. 1240 C.civ.).',
        'Le Préposé de l\'Exploitation': 'C\'est lui qui a provoqué l\'accident en montant sur la vasque en céramique du bac à shampoing. La SAS est civilement responsable en tant que commettant (art. 1242 al. 5 C.civ.).',
        'Le Propriétaire des Murs': 'Propriétaire des locaux commerciaux. Mis en demeure en qualité de bailleur, responsable de l\'état des lieux et des équipements.',
        'Le Chirurgien SOS Main': 'A réalisé la microchirurgie d\'urgence le 30 mai 2026 (J+1). Consultation de contrôle J+21 le 19 juin 2026.',
        'Le Médecin Généraliste': 'A initialement prescrit 1 jour d\'ITT par erreur matérielle (1er juin 2026). Rectifiée à 56 jours après dépôt de plainte.',
        'Nom de l\'Avocat de la Victime': 'À confirmer et renseigner dès que le mandat est signé.',
        'L\'Exploitant du Commerce (La SAS)': f'Capital social : 200 €. SIREN : 938 033 222. Créée le 01/06/2024. Statut : Active (vérifié le 06/07/2026). Siège social : 22 Rue Lafaurie, 09000 Foix.',
        'L\'Établissement SOS Main': 'Situé à Saint-Jean (31). A pris en charge la victime en urgence le 30 mai 2026.',
        'L\'Adjoint au Maire de la Commune': 'Contact privilégié pour les démarches administratives, le signalement ERP, et les échanges avec la police municipale.',
    }

    for e in entries:
        e['role'] = roles.get(e['token_name'], '')
        e['profession'] = professions.get(e['token_name'], '')
        e['detailed_note'] = notes.get(e['token_name'], e['note'])

    return entries

def scan_jplus_docs():
    docs = {}
    base = os.path.join(BASE, "Actes", "Token")
    for root, dirs, filenames in os.walk(base):
        for fn in filenames:
            if fn.endswith(".md") and fn != "README.md":
                m = re.match(r'J\+(\d+)', fn)
                if m:
                    jnum = int(m.group(1))
                    rel = os.path.relpath(os.path.join(root, fn), BASE)
                    docs.setdefault(jnum, []).append(rel)
    return docs

# ─── generate token file content ───────────────────────────

def generate_personne_physique(e, strict_content, jplus_docs):
    lines = []
    t = e['token_name']
    lines.append(f'# 👤 {t}')
    lines.append('')
    lines.append(f'**Token :** `**[{t}]**`')
    lines.append('')

    lines.append('## Identité')
    lines.append('')
    lines.append('| Champ | Valeur |')
    lines.append('|---|---|')
    if e['real_values']:
        lines.append(f'| **Nom réel** | {e["real_values"][0]} |')
    if e['role']:
        lines.append(f'| **Rôle** | {e["role"]} |')
    if e['profession']:
        lines.append(f'| **Profession** | {e["profession"]} |')
    if t == 'La Victime':
        naiss = strict_var(strict_content, 'DATE_NAISSANCE')
        if naiss:
            lines.append(f'| **Date naissance** | {naiss} |')
        email = strict_var(strict_content, 'EMAIL')
        if email:
            lines.append(f'| **Email** | sebastien.grazide@gmail.com |')
        addr = '10 Avenue de Purpan, 31700 Blagnac'
        lines.append(f'| **Adresse** | {addr} |')
        sir = strict_var(strict_content, 'SIREN') or '500 474 457'
        lines.append(f'| **SIREN** | {sir} |')
    lines.append('')

    lines.append('## Contexte')
    lines.append('')
    if t == 'La Victime':
        lines.append(f'Victime directe de l\'accident corporel survenu le **29 mai 2026** dans les locaux de **[L\'Exploitant du Commerce (La SAS)]** à **[La Ville de l\'Accident]** (22 Rue Lafaurie, 09000 Foix).')
        lines.append('')
        lines.append('Blessure : plaie de la main droite avec section du tendon fléchisseur, du paquet collatéral et neurolyse du nerf palmaire de l\'index droit. Microchirurgie d\'urgence pratiquée le 30 mai 2026.')
        lines.append('')
        lines.append(f'Profession : informaticien indépendant (CA mensuel moyen 750 €). ITT : 56 jours.')
    elif e.get('detailed_note'):
        lines.append(e['detailed_note'])
    lines.append('')

    lines.append('## Source')
    lines.append('')
    section = e.get('section', '')
    if section:
        lines.append(f'[TOKEN MAP → {section}](../TOKEN%20MAP.md#{e["anchor"]})')
    else:
        lines.append(f'[TOKEN MAP](../TOKEN%20MAP.md)')
    lines.append('')
    return '\n'.join(lines)

def generate_personne_morale(e, strict_content, jplus_docs):
    lines = []
    t = e['token_name']
    lines.append(f'# 🏢 {t}')
    lines.append('')
    lines.append(f'**Token :** `**[{t}]**`')
    lines.append('')

    lines.append('## Identité')
    lines.append('')
    lines.append('| Champ | Valeur |')
    lines.append('|---|---|')
    if e['real_values']:
        lines.append(f'| **Nom réel** | {e["real_values"][0]} |')
    if e['role']:
        lines.append(f'| **Rôle** | {e["role"]} |')
    if t == "L'Exploitant du Commerce (La SAS)":
        lines.append('| **Forme juridique** | SAS |')
        lines.append('| **Capital social** | 200 € (2 000 actions de 0,10 €) |')
        lines.append('| **SIREN** | 938 033 222 |')
        lines.append('| **RCS** | Foix |')
        lines.append('| **Création** | 01/06/2024 |')
        lines.append('| **Statut** | Active (vérifié le 06/07/2026) |')
        lines.append('| **Siège social** | 22 Rue Lafaurie, 09000 Foix |')
    elif t == "L'Établissement SOS Main":
        lines.append('| **Établissement** | Clinique de l\'Union |')
        lines.append('| **Ville** | Saint-Jean (31) |')
    lines.append('')

    lines.append('## Contexte')
    lines.append('')
    if e.get('detailed_note'):
        lines.append(e['detailed_note'])
    lines.append('')

    lines.append('## Source')
    lines.append('')
    section = e.get('section', '')
    if section:
        lines.append(f'[TOKEN MAP → {section}](../TOKEN%20MAP.md#{e["anchor"]})')
    else:
        lines.append(f'[TOKEN MAP](../TOKEN%20MAP.md)')
    lines.append('')
    return '\n'.join(lines)

def generate_donnee_localisante(e, strict_content, jplus_docs):
    lines = []
    t = e['token_name']
    lines.append(f'# 📍 {t}')
    lines.append('')
    lines.append(f'**Token :** `**[{t}]**`')
    lines.append('')

    lines.append('## Valeur')
    lines.append('')
    lines.append('| Champ | Valeur |')
    lines.append('|---|---|')
    if e['real_values']:
        lines.append(f'| **Donnée réelle** | {e["real_values"][0]} |')
    lines.append(f'| **Type** | {e.get("section", "Donnée localisante")} |')

    context_map = {
        'L\'Adresse de la Victime': 'Domicile de la victime Sébastien GRAZIDE.',
        'L\'Adresse de l\'Exploitation': 'Adresse du lieu de l\'accident (salon de coiffure exploité par la SAS).',
        'L\'Adresse du Président': 'Domicile du dirigeant Sabir MOUNTASSER.',
        'La Ville de l\'Accident': 'Foix (09) — ville où s\'est produit l\'accident et où se trouve le tribunal compétent.',
        'La Ville de Résidence de la Victime': 'Blagnac (31) — domicile de la victime.',
        'La Métropole Régionale': 'Toulouse — métropole de référence pour les expertises et soins spécialisés.',
        'La Ville de l\'Établissement SOS Main': 'Saint-Jean (31) — ville où se trouve la clinique SOS Main.',
        'L\'Email de la Victime': 'sebastien.grazide@gmail.com — principal moyen de contact.',
        'L\'Identifiant Professionnel de la Victime': 'SIREN personnel de la victime (auto-entrepreneur).',
        'L\'Identifiant de l\'Exploitation': '938 033 222 00010 — SIRET de la SAS.',
        'SIREN de l\'Exploitation': '938 033 222 — SIREN de la SAS LES MAUVAIS GARÇONS.',
    }
    ctx = context_map.get(t, '')
    if ctx:
        lines.append(f'| **Contexte** | {ctx} |')
    lines.append('')

    lines.append('## Source')
    lines.append('')
    section = e.get('section', '')
    if section:
        lines.append(f'[TOKEN MAP → {section}](../TOKEN%20MAP.md#{e["anchor"]})')
    else:
        lines.append(f'[TOKEN MAP](../TOKEN%20MAP.md)')
    lines.append('')
    return '\n'.join(lines)

def generate_token_temporel(e, strict_content, jplus_docs):
    lines = []
    t = e['token_name']
    lines.append(f'# ⏱ {t}')
    lines.append('')
    lines.append(f'**Token :** `**[{t}]**`')
    lines.append('')

    real_val = e['real_values'][0] if e['real_values'] else ''
    lines.append('## Valeur')
    lines.append('')
    lines.append(f'| Champ | Valeur |')
    lines.append(f'|---|---|')
    lines.append(f'| **Token** | `**[{t}]**` |')
    if real_val:
        lines.append(f'| **Valeur réelle** | {real_val} |')
    lines.append('')

    lines.append('## Source')
    lines.append('')
    section = e.get('section', '')
    if section:
        lines.append(f'[TOKEN MAP → {section}](../TOKEN%20MAP.md#{e["anchor"]})')
    else:
        lines.append(f'[TOKEN MAP](../TOKEN%20MAP.md)')
    lines.append('')
    return '\n'.join(lines)

def generate_evenementiel(e, strict_content, jplus_docs):
    lines = []
    t = e['token_name']
    lines.append(f'# 📅 {t}')
    lines.append('')
    lines.append(f'**Token :** `**[{t}]**`')
    lines.append('')

    jnum = jplus_from_name(t)
    real_first = e['real_values'][0] if e['real_values'] else ''

    lines.append('## Événement')
    lines.append('')
    lines.append(f'| Champ | Valeur |')
    lines.append(f'|---|---|')
    if real_first:
        lines.append(f'| **J+X** | J+{jnum} — {real_first} |' if jnum is not None else f'| **Description** | {real_first} |')
    if jnum is not None:
        lines.append(f'| **Date** | (calculée : 29 mai 2026 + {jnum} jours) |')
    lines.append('')

    # Related documents
    if jnum is not None and jnum in jplus_docs:
        doc_paths = jplus_docs[jnum]
        if doc_paths:
            lines.append('## Documents liés')
            lines.append('')
            for dp in doc_paths:
                # Convert to relative path from Tokens directory
                from_jeton = os.path.relpath(os.path.join(BASE, dp), JETONS_DIR)
                display = os.path.basename(dp).replace('.md', '')
                lines.append(f'- [{display}]({from_jeton})')
            lines.append('')

    lines.append('## Source')
    lines.append('')
    section = e.get('section', '')
    if section:
        lines.append(f'[TOKEN MAP → {section}](../TOKEN%20MAP.md#{e["anchor"]})')
    else:
        lines.append(f'[TOKEN MAP](../TOKEN%20MAP.md)')
    lines.append('')
    return '\n'.join(lines)

# ─── main ──────────────────────────────────────────────────

def main():
    with open(TOKENMAP) as f:
        tokenmap_content = f.read()
    strict_content = read_strict()

    entries = parse_tokens(tokenmap_content, strict_content)
    entries = add_enrichment(entries, strict_content)
    jplus_docs = scan_jplus_docs()

    # Deduplicate by anchor
    seen = set()
    unique = []
    for e in entries:
        if e['anchor'] not in seen:
            seen.add(e['anchor'])
            unique.append(e)

    print(f"Génération de {len(unique)} fiches tokens dans {JETONS_DIR}")

    # Categories
    personne_physique_sections = {'Personnes physiques'}
    personne_morale_sections = {'Personnes morales', 'Personnes morales (suite)'}
    donnee_sections = {'Données localisantes / identifiantes'}
    temporel_sections = {'Tokens temporaires / date tokens (generate_real_versions.py)'}
    evenementiel_sections = {'Tokens événementiels (J+)'}

    generators = {
        'pp': generate_personne_physique,
        'pm': generate_personne_morale,
        'dl': generate_donnee_localisante,
        'tt': generate_token_temporel,
        'ev': generate_evenementiel,
    }

    created = 0
    for e in unique:
        section = e.get('section', '')
        if section in personne_physique_sections:
            content = generators['pp'](e, strict_content, jplus_docs)
        elif section in personne_morale_sections:
            content = generators['pm'](e, strict_content, jplus_docs)
        elif section in donnee_sections:
            content = generators['dl'](e, strict_content, jplus_docs)
        elif section in temporel_sections:
            content = generators['tt'](e, strict_content, jplus_docs)
        elif section in evenementiel_sections:
            content = generators['ev'](e, strict_content, jplus_docs)
        else:
            print(f"  ? Section inconnue: {section} — fallback générique")
            content = generate_personne_physique(e, strict_content, jplus_docs)

        filename = f"{e['anchor']}.md"
        filepath = os.path.join(JETONS_DIR, filename)

        if DRY_RUN:
            print(f"  ~ {filename} ({len(content)} chars)")
        else:
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"  ✅ {filename}")

        created += 1

    print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}Crée {created} fichiers tokens.")

if __name__ == '__main__':
    main()
