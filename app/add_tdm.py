import os
import re
import sys

ACTES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'actes')
EXCLUDE = {'annexes', 'pieces'}

def heading_to_anchor(text):
    anchor = text.lower()
    anchor = re.sub(r'[^a-z0-9\s-]', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor.strip())
    return anchor

def generate_tdm(headings):
    lines = ['**Table des matières**\n']
    for level, text in headings:
        indent = '  ' * (level - 2)
        anchor = heading_to_anchor(text)
        lines.append(f'{indent}- [{text}](#{anchor})')
    lines.append('')
    return '\n'.join(lines)

def process_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has a Table des matières
    if '**Table des matières**' in content:
        return False

    # Extract headings after YAML frontmatter
    body = content
    if body.startswith('---\n'):
        end = body.index('\n---\n', 4)
        body = body[end + 5:]

    headings = []
    for line in body.split('\n'):
        m = re.match(r'^(#{2,4})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            headings.append((level, text))

    if not headings:
        return False

    tdm = generate_tdm(headings)

    # Insert TdM after YAML frontmatter
    if content.startswith('---\n'):
        end = content.index('\n---\n', 4) + 5
        new_content = content[:end] + '\n' + tdm + '\n' + content[end:]
    else:
        new_content = tdm + '\n\n' + content

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    modified = 0
    for root, dirs, files in os.walk(ACTES_DIR):
        rel = os.path.relpath(root, ACTES_DIR)
        if rel == '.':
            dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for fname in files:
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            if process_file(fpath):
                print(f'  ✅ {os.path.relpath(fpath, ACTES_DIR)}')
                modified += 1
    print(f'\nTdM added to {modified} files.')

if __name__ == '__main__':
    main()
