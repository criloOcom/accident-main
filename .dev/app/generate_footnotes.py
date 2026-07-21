#!/usr/bin/env python3
"""
Scanne tous les fichiers .md dans Actes/Token/ et ajoute
des marqueurs de footnote [^N] sur la ligne **chemin** (blockquote),
puis crée/remplace la section ## Sources Législation en bas de document.

Usage:
    python3 .dev/app/generate_footnotes.py

Idempotent : peut être relancé sans risque.
Migration automatique : les [^N] placés après les URLs sont déplacés
vers la ligne **chemin**.
"""

import re
from pathlib import Path

TOKEN_DIR = Path("Actes/Token")
LEGIFRANCE_PATTERN = re.compile(r'\[([^\]]+)\]\((https?://[^)]*legifrance\.gouv\.fr[^)]*)\)')
YAML_DELIM = "---"
FOOTNOTE_DEF = re.compile(r'^\[\^\d+\]:')
SECTION_OLD = "## Notes de bas de page"
SECTION_NEW = "## Sources Législation"

# Pattern: ](legifrance_url)\s*[^N] — used to strip old-position markers
STRIP_OLD_FN = re.compile(
    r'\]\((https?://[^)]*legifrance\.gouv\.fr[^)]*)\)\s*\[\^\d+\]'
)


def is_yaml_line(idx, lines):
    yaml_starts = [i for i, l in enumerate(lines) if l.strip() == YAML_DELIM]
    if len(yaml_starts) < 2:
        return False
    start, end = yaml_starts[0], yaml_starts[1]
    return start <= idx <= end


def is_footnote_def(line):
    return bool(FOOTNOTE_DEF.match(line.strip()))


def find_bold_chemin_line(lines, line_idx):
    """Find the > **...** line adjacent to line_idx within the same blockquote."""
    for offset in (-2, -1, 1, 2):
        check = line_idx + offset
        if 0 <= check < len(lines):
            ln = lines[check]
            if ln.strip().startswith('>') and '**' in ln:
                return check
    return None


def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    url_map = {}
    positions = []
    fn_counter = 0

    # Pass 0: strip [^N] from after legifrance URLs (migration + clean slate)
    for i, line in enumerate(lines):
        if is_yaml_line(i, lines):
            continue
        lines[i] = STRIP_OLD_FN.sub(r'](\1)', line)

    # Pass 1: collect all legifrance URLs that need footnotes
    for i, line in enumerate(lines):
        if is_yaml_line(i, lines) or is_footnote_def(line):
            continue
        for m in LEGIFRANCE_PATTERN.finditer(line):
            text = m.group(1)
            url = m.group(2)
            end = m.end()
            if url not in url_map:
                fn_counter += 1
                url_map[url] = [text, fn_counter]
            positions.append((i, end, url))

    # Ensure ↩ on existing footnote defs
    any_arrow = False
    for i, line in enumerate(lines):
        if is_footnote_def(line) and not line.rstrip("\n").endswith("↩"):
            lines[i] = line.rstrip("\n") + " ↩\n"
            any_arrow = True

    if not positions and not any_arrow:
        return False

    if not positions:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
        rel = filepath.relative_to(TOKEN_DIR.parent.parent)
        print(f"  ↩ only  {rel}")
        return True

    # Pass 2: insert [^N] on bold chemin line (or fallback after URL)
    for line_idx, end, url in positions:
        fn_num = url_map[url][1]
        marker = f"[^{fn_num}]"

        bold_idx = find_bold_chemin_line(lines, line_idx)
        if bold_idx is not None:
            bold_line = lines[bold_idx]
            last_ast = bold_line.rfind('**')
            if last_ast >= 0:
                lines[bold_idx] = bold_line[:last_ast] + marker + bold_line[last_ast:]
            else:
                old = lines[line_idx]
                lines[line_idx] = old[:end] + marker + old[end:]
        else:
            old = lines[line_idx]
            lines[line_idx] = old[:end] + marker + old[end:]

    # Build sources section
    entries = []
    for url, (text, fn_num) in sorted(url_map.items(), key=lambda x: x[1][1]):
        short = url.replace("https://", "").replace("http://", "")
        link_text = f"{text} — {short}"
        entries.append(f"[^{fn_num}]: [{link_text}]({url}) ↩")

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
