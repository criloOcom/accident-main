import re

def deduplicate_lrar_numbers(content):
    content = re.sub(r'(LRAR n° \[[0-9a-zA-Z]+\]\([^)]+\))\s*—\s*`[0-9a-zA-Z]+`', r'\1', content)
    content = re.sub(r'\(LRAR n° ([0-9a-zA-Z]+)\s*—\s*[0-9a-zA-Z]+\)', r'(LRAR n° \1)', content)
    content = re.sub(r'LRAR n° ([0-9a-zA-Z]+)\s*—\s*[0-9a-zA-Z]+', r'LRAR n° \1', content)
    content = re.sub(r'LRAR n° <([0-9a-zA-Z]+)>\s*—\s*[0-9a-zA-Z]+', r'LRAR n° <\1>', content)
    return content

def preprocess_nested_bracket_tokens(content):
    content = re.sub(r'\[\*\*\[N° \[Dossier CPAM\]\([^)]+\)\]\*\*\]\([^)]+\)', '31727387', content)
    content = re.sub(r'\*\*\[N° \[Dossier CPAM\]\([^)]+\)\]\*\*', '31727387', content)
    content = re.sub(r'\[\*\*\[N° \[Dossier CPAM erroné\]\([^)]+\)\]\*\*\]\([^)]+\)', '2631103960', content)
    content = re.sub(r'\*\*\[N° \[Dossier CPAM erroné\]\([^)]+\)\]\*\*', '2631103960', content)
    return content
