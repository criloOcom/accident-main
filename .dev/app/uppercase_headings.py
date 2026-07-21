import os
import re

EXCLUDED = {'README.md', 'INDEX.md'}

def process_heading(line):
    match = re.match(r'^(#{1,6}\s*)(.*)$', line)
    if not match:
        return line
    prefix = match.group(1)
    rest = match.group(2)
    if not rest.strip():
        return line
    return prefix + rest.upper()

def process_toc_line(line):
    def replace_link(m):
        return m.group(1) + m.group(2) + m.group(3).upper() + m.group(4)
    return re.sub(r'(^|\s)(\[)([^\]]+)(\]\(#[^)]+\))', replace_link, line)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    modified = False
    new_lines = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('#'):
            processed = process_heading(line)
        else:
            processed = process_toc_line(line)
        if processed != line:
            modified = True
        new_lines.append(processed)
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def main():
    total_modified = 0
    total_files = 0
    for root, dirs, files in os.walk('Actes/Token'):
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            if fname in EXCLUDED:
                continue
            filepath = os.path.join(root, fname)
            if process_file(filepath):
                total_modified += 1
                print(f'  MODIFIED: {filepath}')
            total_files += 1
    print(f'\n--- {total_modified}/{total_files} fichiers modifies ---')

if __name__ == '__main__':
    main()
