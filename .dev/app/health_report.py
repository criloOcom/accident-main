#!/usr/bin/env python3
"""Rapport de santé hebdomadaire — audit complet du dépôt.

Usage :
    python3 .dev/app/health_report.py                          # rapport complet
    python3 .dev/app/health_report.py --quick                  # seulement checks rapides
    python3 .dev/app/health_report.py --path dossier/          # ciblé
    python3 .dev/app/health_report.py --json                   # sortie JSON
    python3 .dev/app/health_report.py --no-write               # pas de fichier rapport

Génère : 📊 Rapports/HEALTH_REPORT_YYYY-MM-DD.md
"""

import argparse
import json
import os
import re
import sys
import subprocess
from datetime import date
from pathlib import Path

from yaml_utils import (
    REPO_ROOT,
    read_frontmatter,
    in_perimeter,
    is_excluded,
    validate_date_format,
)

REPORTS_DIR = os.path.join(REPO_ROOT, "📊 Rapports")
CALENDAR_MAP = os.path.join(REPO_ROOT, "🧠 Memory", "CALENDAR_MAP.md")


def run_script(script_name: str, *args: str) -> tuple[int, str]:
    """Exécute un script .dev/app/ et retourne (exit_code, stdout)."""
    script = os.path.join(REPO_ROOT, ".dev", "app", script_name)
    if not os.path.exists(script):
        return (-1, f"Script introuvable : {script}")
    cmd = [sys.executable, script] + list(args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, timeout=120)
        return (r.returncode, r.stdout + r.stderr)
    except subprocess.TimeoutExpired:
        return (-1, "TIMEOUT")
    except Exception as e:
        return (-1, str(e))


# ── Checks individuels ──

def check_yaml_violations(path: str | None = None) -> list[str]:
    """Check 1 : validation YAML frontmatter."""
    from yaml_validator import walk_md_files, validate_file
    files = walk_md_files(path)
    all_v: list[str] = []
    for fp in files:
        all_v.extend(validate_file(fp))
    return all_v


EVENT_REQUIRED_TYPES = {"courrier", "assignation", "plainte", "attestation", "preuve"}

def check_calendar_ids(path: str | None = None) -> list[str]:
    """Check 2 : fichiers avec date (non-FIXME) et sans calendar_event_id."""
    issues: list[str] = []
    from yaml_validator import walk_md_files, read_frontmatter
    files = walk_md_files(path) if path else walk_md_files()
    for fp in files:
        fm = read_frontmatter(fp)
        if not fm:
            continue
        date_val = fm.get("date")
        cal_id = fm.get("calendar_event_id")
        dtype = fm.get("type", "")
        rel = os.path.relpath(fp, REPO_ROOT)
        if date_val and date_val != "FIXME" and not cal_id and dtype in EVENT_REQUIRED_TYPES:
            issues.append(f"{rel}: date={date_val} type={dtype} mais calendar_event_id manquant")
    return issues


def check_reel_paths(path: str | None = None) -> list[str]:
    """Check 3 : reel_path pointant vers fichier inexistant."""
    issues: list[str] = []
    from yaml_validator import walk_md_files, read_frontmatter
    files = walk_md_files(path) if path else walk_md_files("⚖️ Actes/🔑 Token")
    for fp in files:
        fm = read_frontmatter(fp)
        if not fm:
            continue
        rp = fm.get("reel_path")
        if not rp:
            continue
        resolved = os.path.normpath(os.path.join(os.path.dirname(fp), str(rp)))
        if not os.path.exists(resolved):
            rel = os.path.relpath(fp, REPO_ROOT)
            issues.append(f"{rel}: reel_path -> {rp} -> introuvable")
    return issues


def check_internal_links() -> tuple[int, str]:
    """Check 4 : liens internes (full scan, pas diff-driven)."""
    return run_script("audit_internal_links.py", "--json")


def check_citation_links() -> tuple[int, str]:
    """Check 5 : citations non liées."""
    return run_script("audit_citation_links.py")


def check_factual_deviation() -> tuple[int, str]:
    """Check 6 : écarts factuels vs STRICT VARIABLES."""
    return run_script("audit_faits_canoniques.py")


def check_reel_orphans() -> tuple[int, str]:
    """Check 7 : fichier Reel sans Token frère."""
    return run_script("check_reel_orphans.py")


def check_legifrance_urls() -> tuple[int, str]:
    """Check 8 : validation URLs Légifrance."""
    return run_script("validate_legifrance_urls.py")


def check_calendar_map_consistency() -> list[str]:
    """Check 9 : CALENDAR_MAP.md vs YAML files."""
    issues: list[str] = []
    if not os.path.exists(CALENDAR_MAP):
        issues.append("CALENDAR_MAP.md introuvable")
        return issues

    # Parse event IDs from CALENDAR_MAP.md
    map_ids: set[str] = set()
    with open(CALENDAR_MAP, "r", encoding="utf-8") as f:
        for line in f:
            m = re.findall(r'`([a-z0-9]{10,})`', line)
            map_ids.update(m)

    # Collect calendar_event_id from YAML
    yaml_ids: set[str] = set()
    from yaml_validator import walk_md_files
    for fp in walk_md_files():
        fm = read_frontmatter(fp)
        if fm and fm.get("calendar_event_id"):
            cid = str(fm["calendar_event_id"])
            if cid not in map_ids:
                rel = os.path.relpath(fp, REPO_ROOT)
                issues.append(f"{rel}: calendar_event_id '{cid}' absent de CALENDAR_MAP.md")
                yaml_ids.add(cid)
            else:
                yaml_ids.add(cid)

    return issues


def format_violations(violations: list[str], prefix: str = "  ") -> str:
    return "\n".join(f"{prefix}• {v}" for v in violations) if violations else "  Aucune."


def main():
    parser = argparse.ArgumentParser(description="Rapport de santé du dépôt")
    parser.add_argument("--quick", action="store_true", help="Seulement checks rapides")
    parser.add_argument("--path", help="Cibler un dossier spécifique")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    parser.add_argument("--no-write", action="store_true", help="Ne pas écrire le fichier rapport")
    args = parser.parse_args()

    today = date.today().isoformat()
    report_date = today

    results: dict[str, dict] = {}

    # ── Exécution des checks ──

    # Check 1 : YAML
    yaml_violations = check_yaml_violations(args.path if args.path else None)
    results["yaml_validation"] = {
        "label": "YAML frontmatter",
        "passed": len(yaml_violations) == 0,
        "critical": len(yaml_violations) > 0,
        "count": len(yaml_violations),
        "details": yaml_violations[:50],
    }

    # Check 2 : Calendar IDs
    if not args.quick:
        cal_issues = check_calendar_ids(args.path if args.path else None)
        results["calendar_ids"] = {
            "label": "calendar_event_id manquants",
            "passed": len(cal_issues) == 0,
            "critical": False,
            "count": len(cal_issues),
            "details": cal_issues[:50],
        }
    else:
        results["calendar_ids"] = {"label": "calendar_event_id", "passed": True, "critical": False, "count": 0, "details": [], "skipped": True}

    # Check 3 : reel_path
    if not args.quick:
        reel_issues = check_reel_paths(args.path if args.path else None)
        results["reel_paths"] = {
            "label": "reel_path invalides",
            "passed": len(reel_issues) == 0,
            "critical": True,
            "count": len(reel_issues),
            "details": reel_issues[:50],
        }
    else:
        results["reel_paths"] = {"label": "reel_path", "passed": True, "critical": False, "count": 0, "details": [], "skipped": True}

    # Check 4 : Internal links
    if not args.quick:
        rc4, out4 = check_internal_links()
        try:
            data4 = json.loads(out4)
        except json.JSONDecodeError:
            data4 = {"total_broken": -1}
        results["internal_links"] = {
            "label": "Liens internes",
            "passed": data4.get("total_broken", 1) == 0,
            "critical": True,
            "count": data4.get("total_broken", -1),
            "details": [f"{b['source']}: {b['decoded']}" for b in data4.get("results", [])[:50]] if "results" in data4 else [out4[:500]],
        }
    else:
        results["internal_links"] = {"label": "Liens internes", "passed": True, "critical": False, "count": 0, "details": [], "skipped": True}

    # Check 5 : Citation links
    if not args.quick:
        rc5, out5 = check_citation_links()
        cit_lines = [l for l in out5.split("\n") if l.strip() and "Aucune" not in l and "✅" not in l and "⚠️" not in l]
        results["citation_links"] = {
            "label": "Citations non liées",
            "passed": rc5 == 0,
            "critical": False,
            "count": len(cit_lines),
            "details": cit_lines[:50],
        }
    else:
        results["citation_links"] = {"label": "Citations non liées", "passed": True, "critical": False, "count": 0, "details": [], "skipped": True}

    # Check 6 : Factual deviation
    if not args.quick:
        rc6, out6 = check_factual_deviation()
        fact_lines = [l for l in out6.split("\n") if l.strip() and "✅" not in l and "Aucune" not in l]
        results["factual_deviation"] = {
            "label": "Écarts factuels",
            "passed": rc6 == 0,
            "critical": True,
            "count": len(fact_lines),
            "details": fact_lines[:50],
        }
    else:
        results["factual_deviation"] = {"label": "Écarts factuels", "passed": True, "critical": False, "count": 0, "details": [], "skipped": True}

    # Check 7 : Reel orphans
    if not args.quick:
        rc7, out7 = check_reel_orphans()
        orphan_lines = [l for l in out7.split("\n") if l.strip() and "✅" not in l and "Aucun" not in l]
        results["reel_orphans"] = {
            "label": "Reel orphelins",
            "passed": rc7 == 0,
            "critical": True,
            "count": len(orphan_lines),
            "details": orphan_lines[:50],
        }
    else:
        results["reel_orphans"] = {"label": "Reel orphelins", "passed": True, "critical": False, "count": 0, "details": [], "skipped": True}

    # Check 8 : Calendar map consistency
    if not args.quick:
        cmap_issues = check_calendar_map_consistency()
        results["calendar_map"] = {
            "label": "CALENDAR_MAP.md vs YAML",
            "passed": len(cmap_issues) == 0,
            "critical": False,
            "count": len(cmap_issues),
            "details": cmap_issues[:50],
        }
    else:
        results["calendar_map"] = {"label": "CALENDAR_MAP.md", "passed": True, "critical": False, "count": 0, "details": [], "skipped": True}

    # ── Synthèse ──
    total = len(results)
    skipped = sum(1 for r in results.values() if r.get("skipped"))
    passed = sum(1 for r in results.values() if not r.get("skipped") and r.get("passed"))
    critical_fail = sum(1 for r in results.values() if not r.get("skipped") and not r.get("passed") and r.get("critical"))
    warnings = sum(1 for r in results.values() if not r.get("skipped") and not r.get("passed") and not r.get("critical"))

    # ── Sortie ──
    if args.json:
        output = {
            "date": report_date,
            "summary": {
                "total": total,
                "passed": passed,
                "critical_fail": critical_fail,
                "warnings": warnings,
                "skipped": sum(1 for r in results.values() if r.get("skipped")),
            },
            "checks": results,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return critical_fail

    # ── Génération du rapport markdown ──
    lines = []
    lines.append("---")
    lines.append(f'title: "Rapport de Santé — {report_date}"')
    lines.append(f'description: "Audit complet du dépôt au {report_date}"')
    lines.append("type: rapport")
    lines.append(f"date: {report_date}")
    lines.append("---")
    lines.append("")
    lines.append(f"# Rapport de Santé — {report_date}")
    lines.append("")
    lines.append("## Résumé")
    lines.append("")
    lines.append(f"| Métrique | Valeur |")
    lines.append(f"|----------|--------|")
    lines.append(f"| Checks exécutés | {total} |")
    lines.append(f"| ✅ Passés | {passed} |")
    if critical_fail:
        lines.append(f"| 🔴 Échecs critiques | {critical_fail} |")
    if warnings:
        lines.append(f"| ⚠️ Avertissements | {warnings} |")
    if skipped:
        lines.append(f"| ⏭️ Ignorés (--quick) | {skipped} |")
    lines.append("")
    lines.append("<hr><hr>")
    lines.append("")

    for key, r in results.items():
        if r.get("skipped"):
            lines.append(f"## ⏭️ {r['label']} (ignoré)")
            lines.append("")
            lines.append("Check non exécuté (mode --quick).")
            lines.append("")
            continue

        icon = "✅" if r["passed"] else ("🔴" if r.get("critical") else "⚠️")
        lines.append(f"## {icon} {r['label']}")
        lines.append("")
        lines.append(f"**Statut :** {'Passé' if r['passed'] else 'Échec'} | **{r['count']}** occurrence(s)")
        lines.append("")
        if r["details"]:
            lines.append("Détail :")
            lines.append("")
            for d in r["details"][:50]:
                lines.append(f"  • {d}")
            lines.append("")
        else:
            lines.append("Aucune anomalie.")
            lines.append("")
        lines.append("<hr>")
        lines.append("")

    lines.append(f"*Rapport généré le {report_date} par health_report.py*")
    lines.append("")

    report_content = "\n".join(lines)

    if not args.no_write:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        report_path = os.path.join(REPORTS_DIR, f"HEALTH_REPORT_{report_date}.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"📄 Rapport écrit : {os.path.relpath(report_path, REPO_ROOT)}")
    else:
        print(report_content)

    return critical_fail


if __name__ == "__main__":
    sys.exit(main())
