#!/usr/bin/env python3
"""Graphe de dépendances entre fichiers .md du projet.

Analyse tous les liens internes pour construire un graphe orienté :
  A → B  si le fichier A contient un lien vers B.

Usage :
    python3 .dev/app/dependency_graph.py                     # graphe complet → DEPENDENCIES.md
    python3 .dev/app/dependency_graph.py --json              # sortie JSON
    python3 .dev/app/dependency_graph.py --target dossier/   # ciblé
    python3 .dev/app/dependency_graph.py --cycles-only       # seulement les cycles

Génère : Memory/DEPENDENCIES.md
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from urllib.parse import unquote

from yaml_utils import REPO_ROOT

ROOT = REPO_ROOT
SKIP_DIRS = {'.git', '.venv', '__pycache__', 'node_modules', '.pytest_cache', '.opencode', '.dev/jules_'}
ROOT_DIRS = ('Actes', 'Lois', 'Memory', 'Rapports', 'Annexes', '.dev')
MD_LINK_RE = re.compile(r'\]\(([^)]+)\)')
HTML_LINK_RE = re.compile(r'<a\s+(?:[^>]*?\s+)?href="([^"]+)"')

OUTPUT_FILE = os.path.join(ROOT, "Memory", "DEPENDENCIES.md")


def is_internal(link: str) -> bool:
    if unquote(link).startswith(('http://', 'https://', 'file://', '#')):
        return False
    return True


def resolve_path(link: str, source_dir: str) -> str | None:
    clean = unquote(link.split('#')[0])
    if not clean:
        return None
    if not clean.endswith('.md'):
        return None
    seg = clean.split('/')[0]
    if seg in ROOT_DIRS:
        candidate = os.path.normpath(os.path.join(ROOT, clean))
    else:
        candidate = os.path.normpath(os.path.join(source_dir, clean))
    return candidate


def walk_md_files() -> list[str]:
    files = []
    for dp, dirs, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT).split(os.sep)
        if any(s in SKIP_DIRS for s in rel):
            dirs[:] = []
            continue
        for f in fn:
            if f.endswith('.md'):
                files.append(os.path.join(dp, f))
    return sorted(files)


def build_graph(files: list[str]) -> dict[str, dict]:
    """Construit le graphe orienté.

    Retourne:
        { relpath: {
            "title": str,
            "outgoing": [relpath, ...],   # fichiers cités
            "incoming": [relpath, ...],    # fichiers qui citent
        }}
    """
    # Index basename -> relpaths
    basename_index: dict[str, list[str]] = defaultdict(list)
    path_to_rel: dict[str, str] = {}
    for fp in files:
        rel = os.path.relpath(fp, ROOT).replace("\\", "/")
        path_to_rel[fp] = rel
        basename_index[os.path.basename(fp)].append(rel)

    # Extraire les liens
    outgoing: dict[str, set[str]] = defaultdict(set)

    for fp in files:
        rel = path_to_rel[fp]
        try:
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            continue

        source_dir = os.path.dirname(fp)

        for m in MD_LINK_RE.finditer(content):
            link = m.group(1).strip()
            if not is_internal(link):
                continue
            resolved = resolve_path(link, source_dir)
            if not resolved or not os.path.exists(resolved):
                continue
            target_rel = path_to_rel.get(resolved)
            if target_rel and target_rel != rel:
                outgoing[rel].add(target_rel)

        for m in HTML_LINK_RE.finditer(content):
            link = m.group(1).strip()
            if not is_internal(link):
                continue
            resolved = resolve_path(link, source_dir)
            if not resolved or not os.path.exists(resolved):
                continue
            target_rel = path_to_rel.get(resolved)
            if target_rel and target_rel != rel:
                outgoing[rel].add(target_rel)

    # Construire incoming
    incoming: dict[str, set[str]] = defaultdict(set)
    all_nodes: set[str] = set()
    for src, targets in outgoing.items():
        all_nodes.add(src)
        for tgt in targets:
            all_nodes.add(tgt)
            incoming[tgt].add(src)

    # Titres
    titles: dict[str, str] = {}
    for fp in files:
        rel = path_to_rel[fp]
        try:
            with open(fp, "r", encoding="utf-8") as f:
                first_line = f.readline()
                f.seek(0)
                content = f.read(1024)
            m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if m:
                titles[rel] = m.group(1).strip().rstrip(". ")
            else:
                titles[rel] = os.path.basename(rel)
        except (OSError, UnicodeDecodeError):
            titles[rel] = os.path.basename(rel)

    node_list = set()
    for rel in all_nodes:
        node_list.add(rel)
    for rel in path_to_rel.values():
        if rel in outgoing or rel in incoming:
            node_list.add(rel)

    result: dict[str, dict] = {}
    for rel in sorted(node_list):
        result[rel] = {
            "title": titles.get(rel, rel),
            "outgoing": sorted(outgoing.get(rel, set())),
            "incoming": sorted(incoming.get(rel, set())),
        }
    return result


def split_token_cycles(cycles: list[list[str]]) -> tuple[list[list[str]], list[list[str]]]:
    """Sépare les cycles impliquant token-*.md du reste."""
    tokens = []
    others = []
    for c in cycles:
        if any("token-" in n or "/Tokens/" in n for n in c):
            tokens.append(c)
        else:
            others.append(c)
    return others, tokens


def detect_cycles(graph: dict[str, dict]) -> tuple[list[list[str]], list[list[str]], list[list[str]], list[list[str]]]:
    """Détection de cycles par DFS (Tarjan simplifié).

    Retourne (content_cycles, nav_cycles) où nav_cycles sont ceux
    impliquant au moins un README.md.
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {n: WHITE for n in graph}
    cycles: list[list[str]] = []

    def dfs(node: str, path: list[str]):
        color[node] = GRAY
        path.append(node)
        for neighbor in graph[node]["outgoing"]:
            if neighbor not in color:
                continue
            if color[neighbor] == GRAY:
                cycle = path[path.index(neighbor):] + [neighbor]
                cycles.append(cycle)
            elif color[neighbor] == WHITE:
                dfs(neighbor, path)
        path.pop()
        color[node] = BLACK

    for node in sorted(graph):
        if color[node] == WHITE:
            dfs(node, [])

    content_cycles = [c for c in cycles if not any("README" in n for n in c)]
    nav_cycles = [c for c in cycles if any("README" in n for n in c)]
    # Filtrer les cycles token (token-*.md ↔ acte ↔ token — normal)
    nav_cycles, token_cycles_in_nav = split_token_cycles(nav_cycles)
    content_cycles, token_cycles = split_token_cycles(content_cycles)
    return content_cycles, nav_cycles, token_cycles, token_cycles_in_nav


def main():
    parser = argparse.ArgumentParser(description="Graphe de dépendances")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    parser.add_argument("--cycles-only", action="store_true", help="Afficher seulement les cycles")
    parser.add_argument("--target", help="Cibler un fichier/dossier")
    args = parser.parse_args()

    files = walk_md_files()
    graph = build_graph(files)
    content_cycles, nav_cycles, token_cycles, token_nav_cycles = detect_cycles(graph)

    total_nodes = len(graph)
    total_edges = sum(len(v["outgoing"]) for v in graph.values())
    roots = sorted([r for r, v in graph.items() if not v["incoming"] and v["outgoing"]])
    leaves = sorted([r for r, v in graph.items() if v["incoming"] and not v["outgoing"]])

    if args.target:
        target = args.target.replace("\\", "/")
        filtered = {k: v for k, v in graph.items() if target in k}
        if not filtered:
            print(f"Aucun fichier contenant '{target}' dans le graphe.")
            return 1
        graph = filtered
        content_cycles, nav_cycles, token_cycles, token_nav_cycles = detect_cycles(graph)

    if args.cycles_only:
        all_real = content_cycles + nav_cycles
        all_tokens = token_cycles + token_nav_cycles
        if all_real or all_tokens:
            print(f"📊 {len(all_real) + len(all_tokens)} cycle(s) total")
            print(f"   {len(nav_cycles)} navigation (README)")
            print(f"   {len(token_nav_cycles)} navigation + token")
            print(f"   {len(content_cycles)} contenu pur")
            print(f"   {len(token_cycles)} token (attendu — cross-refs normales)")
            print()
            if content_cycles:
                for i, cycle in enumerate(content_cycles[:20], 1):
                    print(f"  Cycle contenu {i} ({len(cycle)-1} fichiers) :")
                    for c in cycle:
                        print(f"    → {c}")
                if len(content_cycles) > 20:
                    print(f"  ... et {len(content_cycles)-20} autres cycles contenu")
        if not content_cycles and not nav_cycles and not token_cycles:
            print("✅ Aucun cycle problématique détecté")
        return int(len(content_cycles) > 0)

    if args.json:
        output = {
            "stats": {
                "total_files": len(files),
                "nodes": total_nodes,
                "edges": total_edges,
                "roots": len(roots),
                "leaves": len(leaves),
                "cycles": {
                    "total": len(content_cycles) + len(nav_cycles) + len(token_cycles) + len(token_nav_cycles),
                    "navigation": len(nav_cycles),
                    "navigation_token": len(token_nav_cycles),
                    "content": len(content_cycles),
                    "token": len(token_cycles),
                },
            },
            "content_cycles": content_cycles,
            "nav_cycles": nav_cycles,
            "token_cycles": token_cycles,
            "graph": graph,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return 0

    # ── Génération du rapport markdown ──
    lines = []
    lines.append("---")
    lines.append('title: "Graphe de Dépendances"')
    lines.append('description: "Graphe orienté des liens internes entre fichiers .md"')
    lines.append("type: memory")
    lines.append("---")
    lines.append("")
    lines.append("# Graphe de Dépendances")
    lines.append("")
    lines.append("Graphe orienté : **A → B** signifie que le fichier A contient un lien vers B.")
    lines.append("")
    lines.append("## Statistiques")
    lines.append("")
    lines.append(f"| Métrique | Valeur |")
    lines.append(f"|----------|--------|")
    lines.append(f"| Fichiers .md scannés | {len(files)} |")
    lines.append(f"| Nœuds dans le graphe | {total_nodes} |")
    lines.append(f"| Arêtes (liens internes) | {total_edges} |")
    lines.append(f"| Fichiers racines (cités, ne citent pas) | {len(leaves)} |")
    lines.append(f"| Fichiers sources (citent, ne sont pas cités) | {len(roots)} |")
    total_cycles = len(content_cycles) + len(nav_cycles) + len(token_cycles) + len(token_nav_cycles)
    lines.append(f"| Cycles (via README) | {len(nav_cycles)} |")
    lines.append(f"| Cycles (via README + token) | {len(token_nav_cycles)} |")
    lines.append(f"| Cycles (contenu pur) | {len(content_cycles)} |")
    lines.append(f"| Cycles (token — attendus) | {len(token_cycles)} |")
    lines.append("")
    lines.append("*Les cycles via README et token-*.md sont normaux dans un projet de documentation.*")
    lines.append("")

    if content_cycles:
        lines.append("## 🔴 Cycles de contenu pur")
        lines.append("")
        lines.append("Ces cycles n'impliquent **ni** README **ni** fichier token — ils peuvent indiquer des dépendances circulaires :")
        lines.append("")
        for i, cycle in enumerate(content_cycles[:50], 1):
            lines.append(f"### Cycle contenu {i}")
            lines.append("")
            for c in cycle:
                lines.append(f"  → `{c}`")
            lines.append("")
        if len(content_cycles) > 50:
            lines.append(f"*... et {len(content_cycles)-50} autres cycles de contenu (affichage limité à 50)*")
            lines.append("")

    lines.append("## Détail par fichier")
    lines.append("")

    # Trier : les fichiers les plus cités en premier
    sorted_nodes = sorted(graph.items(), key=lambda x: (-len(x[1]["incoming"]), x[0]))

    for rel, data in sorted_nodes:
        title = data["title"]
        inc = data["incoming"]
        out = data["outgoing"]
        lines.append(f"### `{rel}`")
        lines.append("")
        lines.append(f"**{title}**")
        lines.append("")
        if inc:
            lines.append("**Cité par :**")
            lines.append("")
            for i in inc:
                lines.append(f"  • `{i}`")
            lines.append("")
        if out:
            lines.append("**Cite :**")
            lines.append("")
            for o in out:
                lines.append(f"  • `{o}`")
            lines.append("")
        if not inc and not out:
            lines.append("*Aucune dépendance.*")
            lines.append("")
        lines.append("<hr>")
        lines.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    rel_out = os.path.relpath(OUTPUT_FILE, ROOT)
    print(f"📄 Graphe écrit : {rel_out}")
    print(f"   {total_nodes} nœuds, {total_edges} arêtes, {total_cycles} cycles")
    print(f"   {len(nav_cycles)} nav · {len(token_nav_cycles)} nav+token · {len(content_cycles)} contenu · {len(token_cycles)} token")
    return 0


if __name__ == "__main__":
    sys.exit(main())
