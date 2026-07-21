"""
Strip markdown links from YAML front matter in .md files.

Markdown links `[text](url)` are invalid in YAML — YAML doesn't
interpret Markdown, and `:` in URLs can break the parser.
Replaces [text](url) with plain text.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
TOKEN_DIRS = [
    "⚖️ Actes/🔑 Token",
]

EXCLUDE_DIRS = {"/👤 Reel/", ".git", ".dev/jules_"}

YAML_LINK_RE = re.compile(r'\[(.*?)\]\([^)]+\)')


def strip_yaml_links(text: str) -> str:
    """Replace markdown links in YAML blocks with plain text."""
    def _replace_yaml(m: re.Match) -> str:
        yaml_block = m.group(1)

        def _replace_link(m2: re.Match) -> str:
            inner = m2.group(1).strip()
            # if inner is empty, just return empty
            return inner

        new_block = YAML_LINK_RE.sub(_replace_link, yaml_block)
        return f"---\n{new_block}\n---"

    new_text = re.sub(
        r'^---\s*\n(.*?)\n---',
        _replace_yaml,
        text,
        count=1,
        flags=re.DOTALL
    )
    return new_text


def process_file(path: Path, apply: bool = False) -> bool:
    original = path.read_text(encoding="utf-8")
    clean = strip_yaml_links(original)
    if original == clean:
        return False
    rel = str(path.relative_to(REPO))
    if apply:
        path.write_text(clean, encoding="utf-8")
        print(f"  FIXED  {rel}")
    else:
        print(f"  DIRTY  {rel}")
    return True


def main():
    apply = "--apply" in sys.argv
    mode = "APPLY" if apply else "DRY-RUN"
    print(f"\n{'='*60}")
    print(f"  STRIP YAML LINKS — {mode}")
    print(f"{'='*60}\n")

    total_dirty = 0
    for td in TOKEN_DIRS:
        root = REPO / td
        if not root.exists():
            continue
        for f in sorted(root.rglob("*.md")):
            rel = str(f.relative_to(REPO))
            if any(excl in rel for excl in EXCLUDE_DIRS):
                continue
            if process_file(f, apply=apply):
                total_dirty += 1

    print(f"\n{'='*60}")
    if apply:
        print(f"  {total_dirty} fichier(s) corrigé(s).")
    else:
        print(f"  {total_dirty} fichier(s) à corriger.")
        print(f"  Relancer avec --apply pour appliquer.")
    print(f"{'='*60}\n")
    return 0 if total_dirty == 0 or apply else 1


if __name__ == "__main__":
    sys.exit(main())
