#!/usr/bin/env python3
"""
Normalize blank lines between paragraph-level elements in Token .md files.

Pattern A: Insert blank line before ##/### heading when preceded by a paragraph
            (non-blank, non-heading, non-<hr>, non-YAML content line).

Pattern B: Insert blank line between a ### heading or a bold numbered point
            (e.g. "1. **Title**") and the following - bullet item.

Pattern C: Insert blank line after ##/### heading when followed directly by a
            paragraph (non-blank, non-heading content line).

Pattern D: Insert blank line between consecutive numbered list items
            (N. **... immediately followed by N+1. **...).

Pattern E: Insert blank line between consecutive bullet list items
            (- ... immediately followed by another - ...).
"""

import argparse
import re
import sys
from pathlib import Path

TOKEN_DIR = Path.home() / "accident-main" / "Actes" / "Token"


def is_yaml_section(lines, idx):
    """Check if line idx is within the YAML front matter (between --- markers)."""
    if len(lines) < 2:
        return False
    if lines[0].strip() != "---":
        return False
    for i in range(1, min(idx + 1, len(lines))):
        if lines[i].strip() == "---":
            return i >= idx
    return False


def fix_pattern_a(lines):
    """Insert blank line before ##/### when preceded by paragraph content."""
    modified = False
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        prev_line = new_lines[-1] if new_lines else ""

        # Check if current line starts a ## or ### heading
        is_heading = re.match(r"^#{2,3}\s", line)

        # Previous line is non-blank content (paragraph, blockquote, etc.)
        prev_is_content = bool(
            prev_line.strip()
            and not prev_line.startswith("#")
            and not prev_line.startswith("<hr")
            and not prev_line.startswith("---")
        )

        # But skip if previous line is a blockquote continuation (>) — already fine
        # Actually no, even blockquote content should have blank line before heading

        if is_heading and prev_is_content and prev_line.strip():
            new_lines.append("")
            modified = True

        new_lines.append(line)
        i += 1

    return new_lines, modified


def fix_pattern_b(lines):
    """Insert blank line between heading/bold-number and following - bullet."""
    modified = False
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        prev_line = new_lines[-1] if new_lines else ""

        # Check if current line starts with a - bullet
        is_bullet = re.match(r"^\s*[-*]\s", line)

        # Previous line is a ### heading
        prev_is_heading = bool(re.match(r"^#{3}\s", prev_line))

        # Previous line is a numbered bold point: "N. **Title**" or "N. **Titre**"
        prev_is_bold_point = bool(
            re.match(r"^\s*\d+\.\s+\*\*[^*]+\*\*:?\s*$", prev_line.strip())
        )

        if is_bullet and (prev_is_heading or prev_is_bold_point) and prev_line.strip():
            new_lines.append("")
            modified = True

        new_lines.append(line)
        i += 1

    return new_lines, modified


def fix_pattern_c(lines):
    """Insert blank line after ##/### heading when followed by paragraph content."""
    modified = False
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        prev_line = new_lines[-1] if new_lines else ""

        # Check if previous line was a ##/### heading
        prev_is_heading = bool(re.match(r"^#{2,3}\s", prev_line))

        # Current line is non-blank, non-heading, non-hr content
        # Everything (paragraph, bullet, blockquote, numbered point) gets
        # a blank line after a heading, except another heading or <hr>
        curr_is_content = bool(
            line.strip()
            and not line.startswith("#")
            and not line.startswith("<hr")
        )

        if prev_is_heading and curr_is_content:
            new_lines.append("")
            modified = True

        new_lines.append(line)
        i += 1

    return new_lines, modified


def fix_pattern_d(lines):
    """Insert blank line between consecutive numbered list items (N. **...)."""
    modified = False
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        prev_line = new_lines[-1] if new_lines else ""

        is_numbered = bool(re.match(r"^\d+\.\s+\*\*", line))
        prev_is_numbered = bool(re.match(r"^\d+\.\s+\*\*", prev_line))

        if is_numbered and prev_is_numbered and prev_line.strip():
            new_lines.append("")
            modified = True

        new_lines.append(line)
        i += 1

    return new_lines, modified


def fix_pattern_e(lines):
    """Insert blank line between consecutive bullet list items (- ...)."""
    modified = False
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        prev_line = new_lines[-1] if new_lines else ""

        is_bullet = bool(re.match(r"^\s*[-*]\s+", line))
        prev_is_bullet = bool(re.match(r"^\s*[-*]\s+", prev_line))

        if is_bullet and prev_is_bullet and prev_line.strip():
            new_lines.append("")
            modified = True

        new_lines.append(line)
        i += 1

    return new_lines, modified


def process_file(filepath, args):
    """Process a single .md file, applying patterns A and/or B."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}", file=sys.stderr)
        return False

    lines = content.split("\n")
    original = lines.copy()

    # Preserve YAML front matter boundaries
    # Find YAML end
    yaml_end = 0
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                yaml_end = j + 1
                break

    # Only apply to non-YAML portion
    body_lines = lines[yaml_end:]
    body_modified = False

    if args.pattern_a:
        fixed_body, mod_a = fix_pattern_a(body_lines)
        body_lines = fixed_body
        body_modified = body_modified or mod_a

    if args.pattern_b:
        fixed_body, mod_b = fix_pattern_b(body_lines)
        body_lines = fixed_body
        body_modified = body_modified or mod_b

    if args.pattern_c:
        fixed_body, mod_c = fix_pattern_c(body_lines)
        body_lines = fixed_body
        body_modified = body_modified or mod_c

    if args.pattern_d:
        fixed_body, mod_d = fix_pattern_d(body_lines)
        body_lines = fixed_body
        body_modified = body_modified or mod_d

    if args.pattern_e:
        fixed_body, mod_e = fix_pattern_e(body_lines)
        body_lines = fixed_body
        body_modified = body_modified or mod_e

    if not body_modified:
        return False

    new_lines = lines[:yaml_end] + body_lines
    new_content = "\n".join(new_lines)

    if args.dry_run:
        print(f"  WOULD FIX: {filepath.relative_to(TOKEN_DIR.parent)}")
        return True

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  FIXED: {filepath.relative_to(TOKEN_DIR.parent)}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Normalize blank lines between paragraph elements in Token .md files."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files",
    )
    parser.add_argument(
        "--pattern-a",
        action="store_true",
        default=True,
        help="Fix Pattern A: blank line before ##/### after paragraph (default)",
    )
    parser.add_argument(
        "--pattern-b",
        action="store_true",
        default=True,
        help="Fix Pattern B: blank line between ###/bold point and - bullet (default)",
    )
    parser.add_argument(
        "--no-pattern-a",
        action="store_true",
        help="Disable Pattern A",
    )
    parser.add_argument(
        "--no-pattern-b",
        action="store_true",
        help="Disable Pattern B",
    )
    parser.add_argument(
        "--pattern-c",
        action="store_true",
        default=True,
        help="Fix Pattern C: blank line after ##/### heading before paragraph (default)",
    )
    parser.add_argument(
        "--no-pattern-c",
        action="store_true",
        help="Disable Pattern C",
    )
    parser.add_argument(
        "--pattern-d",
        action="store_true",
        default=True,
        help="Fix Pattern D: blank line between numbered list items (default)",
    )
    parser.add_argument(
        "--no-pattern-d",
        action="store_true",
        help="Disable Pattern D",
    )
    parser.add_argument(
        "--pattern-e",
        action="store_true",
        default=True,
        help="Fix Pattern E: blank line between bullet list items (default)",
    )
    parser.add_argument(
        "--no-pattern-e",
        action="store_true",
        help="Disable Pattern E",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Specific files to process (default: all .md in Token directory)",
    )

    args = parser.parse_args()

    # Handle the --no-* flags
    if args.no_pattern_a:
        args.pattern_a = False
    if args.no_pattern_b:
        args.pattern_b = False
    if args.no_pattern_c:
        args.pattern_c = False
    if args.no_pattern_d:
        args.pattern_d = False
    if args.no_pattern_e:
        args.pattern_e = False

    if args.files:
        md_files = [Path(f) for f in args.files]
    else:
        md_files = list(TOKEN_DIR.rglob("*.md"))

    # Filter out README.md files
    md_files = [f for f in md_files if f.name != "README.md"]

    count = 0
    error_count = 0

    for filepath in sorted(md_files):
        try:
            if process_file(filepath, args):
                count += 1
        except Exception as e:
            print(f"  ERROR: {filepath} — {e}", file=sys.stderr)
            error_count += 1

    mode = "DRY RUN" if args.dry_run else "MODIFIED"
    print(f"\n{mode}: {count} files")

    if error_count:
        print(f"Errors: {error_count}", file=sys.stderr)

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
