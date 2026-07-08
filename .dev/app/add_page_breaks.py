import re
import os

NORMALIZED_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'markdown_normalized')
RAW_DIR = '/tmp/opencode/markdown_originals'

FILES = [
    '01_Assignation_REFERE_PROVISION_FINAL.md',
    '02_ActionDirecte_AssureurRC.md',
    '03_Plainte_Complet_Defaut_Assurance.md',
    '04_Assignation_Refere_Provision_V1.md',
    '05_Constitution_Partie_Civile.md',
    '06_Dossier_Presentation.md',
    '07_ETUDE_Indemnisation_MAX.md',
    '08_Index_EtatFinal_Dossier.md',
    '09_PlanAction_Chronologie.md',
    '10_Synthese_FAQ.md',
    '11_ANALYSE_correction_juridique.md',
    '12_ANALYSE_Jurisprudence.md',
    '13_ANALYSE_Plaidoirie_Dirigeants.md',
    '14_ANALYSE_Responsabilites_Legales.md',
]

BREAK = '=== PAGE BREAK ==='

# Normalization rules originally from normalize_markdown.py
def normalize(content):
    # Remove \u000b (vertical tab) artifacts
    content = content.replace('\u000b', '\n\n')
    # Collapse 3+ consecutive newlines into 2
    content = re.sub(r'\n{3,}', '\n\n', content)
    # Fix broken numbered lists: "1. 1. 1." -> "1. 2. 3."
    lines = content.split('\n')
    result = []
    list_counter = {}
    for line in lines:
        m = re.match(r'^(\s*)(\d+)\.\s+(.*)', line)
        if m:
            indent = m.group(1)
            num = int(m.group(2))
            text = m.group(3)
            key = indent
            if key not in list_counter:
                list_counter[key] = 1
            expected = list_counter[key]
            if num != expected:
                line = f'{indent}{expected}. {text}'
            list_counter[key] += 1
        else:
            list_counter = {}
        result.append(line)
    return '\n'.join(result)


def add_page_breaks(content):
    lines = content.split('\n')

    # Find first heading after # INTRODUCTION
    first_content_heading_idx = -1
    found_intro = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '# INTRODUCTION':
            found_intro = True
        elif found_intro and first_content_heading_idx < 0 and re.match(r'^#\s+\S', stripped):
            first_content_heading_idx = i
            break

    result = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        is_heading = re.match(r'^#{1,2}\s+\S', stripped)
        should_break = False

        if is_heading and stripped not in ('# INTRODUCTION',):
            is_roman = bool(re.match(r'^# (I{1,3}|IV|V|VI|VII|VIII|IX|X)\.\s', stripped))
            is_annex = bool(re.match(r'^# ANNEXE [ABC]', stripped))
            is_annex_c = bool(re.match(r'^## Annexe C', stripped))
            is_content_start = (i == first_content_heading_idx)
            if is_content_start or is_roman or is_annex or is_annex_c:
                should_break = True

        if should_break:
            recent = result[-3:] if len(result) >= 3 else result
            already = any(l.strip() == BREAK for l in recent)
            if not already:
                result.append('')
                result.append(BREAK)
                result.append('')

        result.append(line)

    return '\n'.join(result)


def main():
    for fname in FILES:
        src = os.path.join(RAW_DIR, fname)
        dst = os.path.join(NORMALIZED_DIR, fname)

        if not os.path.exists(src):
            print(f"  ⚠ Raw file not found: {fname}")
            continue

        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()

        content = normalize(content)
        content = add_page_breaks(content)

        with open(dst, 'w', encoding='utf-8') as f:
            f.write(content)

        count = content.count(BREAK)
        print(f"  ✅ {fname} → {count} breaks")


if __name__ == '__main__':
    main()
