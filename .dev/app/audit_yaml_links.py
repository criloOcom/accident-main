"""
Audit YAML front matter for markdown links `[text](url)`.

Returns exit codes:
  0 = no violations
  1 = violations found
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
EXCLUDE_DIRS = {"/👤 Reel/", ".git", ".dev/jules_"}

YAML_BLOCK_RE = re.compile(r'^---\s*\n(.*?)\n---', re.DOTALL)
YAML_LINK_RE = re.compile(r'\[(.+?)\]\([^)]+\)')


def audit_file(path: Path) -> list[dict]:
    content = path.read_text(encoding="utf-8")
    yaml_m = YAML_BLOCK_RE.search(content)
    if not yaml_m:
        return []
    yaml_block = yaml_m.group(1)
    violations = []
    for m in YAML_LINK_RE.finditer(yaml_block):
        violations.append({
            "match": m.group(0),
            "start": m.start(),
        })
    return violations


def main():
    violations_total = 0
    for f in sorted(REPO.rglob("*.md")):
        rel = str(f.relative_to(REPO))
        if any(excl in rel for excl in EXCLUDE_DIRS):
            continue
        violations = audit_file(f)
        if violations:
            violations_total += len(violations)
            for v in violations:
                print(f"  📄 {rel} → {v['match']}")

    if violations_total:
        print(f"\n❌ {violations_total} violation(s) — liens Markdown dans le YAML interdits (Règle #25)")
        return 1
    else:
        print("✅ Aucun lien Markdown dans le YAML.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
