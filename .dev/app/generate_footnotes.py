#!/usr/bin/env python3
"""
Scanne tous les fichiers .md dans ⚖️ Actes/🔑 Token/ et ajoute
des marqueurs de footnote [^N] après chaque lien legifrance.gouv.fr,
puis crée/remplace la section ## Sources Législation en bas de document.

Usage:
    python3 .dev/app/generate_footnotes.py

Idempotent : peut être relancé sans risque.
"""

import re
from pathlib import Path

TOKEN_DIR = Path("⚖️ Actes/🔑 Token")
LEGIFRANCE_PATTERN = re.compile(r'\[([^\]]+)\]\((https?://[^)]*legifrance\.gouv\.fr[^)]*)\)')
YAML_DELIM = "---"
FOOTNOTE_DEF = re.compile(r'^\[\^\d+\]:')
SECTION_OLD = "## Notes de bas de page"
SECTION_NEW = "## Sources Législation"


def is_yaml_line(idx, lines):
    """Check if line idx is between YAML --- delimiters."""
    yaml_starts = [i for i, l in enumerate(lines) if l.strip() == YAML_DELIM]
    if len(yaml_starts) < 2:
        return False
    start, end = yaml_starts[0], yaml_starts[1]
    return start <= idx <= end


def is_footnote_def(line):
    return bool(FOOTNOTE_DEF.match(line.strip()))


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    url_map = {}       # url -> [link_text, number]
    positions = []     # (line_idx, end_pos_of_url, url)
    fn_counter = 0

    # Pass 1: collect all legifrance URLs that need footnotes
    for i, line in enumerate(lines):
        if is_yaml_line(i, lines) or is_footnote_def(line):
            continue
        for m in LEGIFRANCE_PATTERN.finditer(line):
            text = m.group(1)
            url = m.group(2)
            end = m.end()
            after = line[end:]
            if after.lstrip().startswith('[^'):
                continue
            if url not in url_map:
                fn_counter += 1
                url_map[url] = [text, fn_counter]
            positions.append((i, end, url))

    if not positions:
        return False

    # Pass 2: insert markers (reversed to preserve indices)
    for line_idx, end, url in reversed(positions):
        fn_num = url_map[url][1]
        marker = f"[^{fn_num}]"
        old = lines[line_idx]
        lines[line_idx] = old[:end] + marker + old[end:]

    # Build sources section
    entries = []
    for url, (text, fn_num) in sorted(url_map.items(), key=lambda x: x[1][1]):
        short = url.replace("https://", "").replace("http://", "")
        link_text = f"{text} — {short}"
        entries.append(f"[^{fn_num}]: [{link_text}]({url})")

    new_section = ["\n", f"{SECTION_NEW}\n", "\n"]
    for e in entries:
        new_section.append(f"{e}\n")

    # Pass 3: find and replace existing section, or append
    found = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped in (SECTION_NEW, SECTION_OLD):
            found = True
            end = len(lines)
            for j in range(i + 1, len(lines)):
                ls = lines[j].strip()
                if ls.startswith("## ") and ls not in ("", "##"):
                    end = j
                    break
            lines[i:end] = new_section
            break

    if not found:
        # Trim trailing blank lines, then append
        while lines and lines[-1].strip() == "":
            lines.pop()
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        lines.append("\n")
        lines.extend(new_section)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)

    total_urls = len(url_map)
    total_pos = len(positions)
    rel = filepath.relative_to(TOKEN_DIR.parent.parent)
    print(f"  {total_pos:3d} markers, {total_urls:2d} urls  {rel}")
    return True


def main():
    md_files = sorted(TOKEN_DIR.rglob("*.md"))
    print(f"Scanning {len(md_files)} .md files in {TOKEN_DIR}...")
    count = 0
    for fp in md_files:
        try:
            if process_file(fp):
                count += 1
        except Exception as e:
            print(f"  ERROR {fp}: {e}")
    print(f"\nDone: {count} files modified")


if __name__ == "__main__":
    main()
