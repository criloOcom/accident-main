#!/usr/bin/env python3
"""
Enhance anonymized text to markdown with:
- Bold tokens **[token]**
- Line breaks after periods (one sentence per paragraph)
- Proper heading detection
"""
import re, sys

HEADING_PATTERNS = [
    r'^PAR CES MOTIFS',
    r'^DEMANDES',
    r'^CONCLUSIONS',
    r'^[IVX]+\.\s+.+',     # "I. ", "II. ", "III. ", "IV. ", "V. "
    r'^[A-D]\.\s+.+',       # "A. ", "B. ", "C. ", "D. "
    r'^Sur\s+[a-zé]',       # "Sur le ", "Sur la "
    r'^ANNEXE\s',            # "ANNEXE "
]

H1_PATTERNS = [
    r'^PAR CES MOTIFS',
    r'^[IVX]+\.\s+.+',     # I., II., III., IV., V.
]

H2_PATTERNS = [
    r'^DEMANDES',
    r'^CONCLUSIONS',
    r'^[A-D]\.\s+.+',       # A., B., C., D.
    r'^Sur\s+[a-zé]',       # Sur le, Sur la
    r'^ANNEXE\s',
]

HEADING_PATTERNS_COMPILED = [re.compile(pat, re.IGNORECASE) for pat in HEADING_PATTERNS]
H1_PATTERNS_COMPILED = [re.compile(pat, re.IGNORECASE) for pat in H1_PATTERNS]
H2_PATTERNS_COMPILED = [re.compile(pat, re.IGNORECASE) for pat in H2_PATTERNS]

PROTECTED_PATTERNS = [
    (re.compile(r'\bM\.'), 'M§DOT§'),
    (re.compile(r'\bMe\b'), 'Me'),
    (re.compile(r'\bDr\b'), 'Dr'),
    (re.compile(r'\bMme\b'), 'Mme'),
    (re.compile(r'\bn°\b'), 'n°'),
    (re.compile(r'\bArt\.'), 'Art§DOT§'),
    (re.compile(r'\bL\.(?=\s+\d)'), 'L§DOT§'),
]


def is_heading(line):
    stripped = line.strip()
    if not stripped:
        return False
    for pat in HEADING_PATTERNS_COMPILED:
        if pat.match(stripped):
            return True
    return False


def get_heading_level(line):
    stripped = line.strip()
    for pat in H1_PATTERNS_COMPILED:
        if pat.match(stripped):
            return 1
    for pat in H2_PATTERNS_COMPILED:
        if pat.match(stripped):
            return 2
    return 2


def split_sentences(text):
    """Split text into sentences with paragraph breaks."""
    for pattern, replacement in PROTECTED_PATTERNS:
        text = pattern.sub(replacement, text)

    # Split into lines first
    lines = text.split('\n')
    result_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            result_lines.append('')
            continue

        # Check if it's a heading (single line)
        if is_heading(stripped):
            level = get_heading_level(stripped)
            result_lines.append(f'{"#" * level} {stripped}')
            continue

        # Check if it starts with a section marker like "A." but text follows
        # These should NOT be split
        marker_match = re.match(r'^([A-D]\.|1°?\.|2°?\.|3°?\.)\s+(.+)', stripped)
        if marker_match:
            result_lines.append(stripped)
            continue

        # For normal text, split by sentence endings
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z«\[\(\d])', stripped)

        for i, sent in enumerate(sentences):
            sent = sent.strip()
            if sent:
                result_lines.append(sent)

        result_lines.append('')

    text = '\n'.join(result_lines)

    text = text.replace('§DOT§', '.')

    text = re.sub(r'\n{4,}', '\n\n', text)
    text = re.sub(r'\n{3}', '\n\n', text)

    return text


def bold_tokens(text):
    text = re.sub(r'(\[[^\]]+\])', r'**\1**', text)
    return text


def enhance(text):
    text = split_sentences(text)
    text = bold_tokens(text)
    return text


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: enhance_markdown.py <input_file> [output_file]")
        sys.exit(1)

    input_path = sys.argv[1]
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    result = enhance(text)

    if len(sys.argv) >= 3:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Enhanced markdown written to {sys.argv[2]}")
    else:
        print(result)
