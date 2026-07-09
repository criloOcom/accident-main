#!/usr/bin/env python3
"""
Script d'injection .md → Google Docs avec sauts de page.

Usage (via un agent ayant les MCP Google Docs) :
    from injection import inject_document

    inject_document(
        filepath='markdown_normalized/01_Assignation_REFERE_PROVISION_FINAL.md',
        doc_id='1ZIfWjszjl5VoxBxourQiDeRATbkckkWPzbU9tYmg5yg'
    )

Prérequis :
    - Les fichiers .md dans markdown_normalized/ avec marqueurs <hr><hr>
    - Mapping fichier ↔ doc_id dans 🧠_Memory/PIECES_MAP.md
    - MCP Google Docs disponible (outils : replaceDocumentWithMarkdown,
      appendMarkdown, insertPageBreak, readDocument)
"""

import os

MARKDOWN_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'markdown_normalized')
BREAK = '<hr><hr>'

# Mapping fichier → Google Doc ID
# Source : 🧠_Memory/PIECES_MAP.md
DOC_MAP = {
    '01_Assignation_REFERE_PROVISION_FINAL.md': '1ZIfWjszjl5VoxBxourQiDeRATbkckkWPzbU9tYmg5yg',
    '02_ActionDirecte_AssureurRC.md': '1_tNTGHf1VGnx1zD0PvyrdvqHLAyYDBU_7wRibBwWlJY',
    '03_Plainte_Complet_Defaut_Assurance.md': '1TVN7SyAWgTLQtOvUzpWqqlfF7fyzT8H8yLziKLQhelc',
    '04_Assignation_Refere_Provision_V1.md': '1L3lJuFQ3CmswKlBg8P5YF6whQQ1AV7QTCLQ_arWo39A',
    '05_Constitution_Partie_Civile.md': '1tdFbDxNceGVjaABoYiHkUR1jxd8y0OaezWUOoV3ZDGc',
    '06_Dossier_Presentation.md': '1DdpbOypghzt9XE09oxtzx46ngPdU4pnc4gayLQEZ_TU',
    '07_ETUDE_Indemnisation_MAX.md': '1PiBFn1oA1DtkT61N-zvdPmsCYsmR0au9V4BA9IZzrH4',
    '08_Index_EtatFinal_Dossier.md': '1Zp-JK9kz0V0DTqNbA7QDDfHliWAqv7Ebyw4Yu3Li6lU',
    '09_PlanAction_Chronologie.md': '153cOANMpw-OoxZqq3jgo34NsWHPY_-cRXZntM_Ydf9s',
    '10_Synthese_FAQ.md': '1eoOJ-bcHBNnLsKYo7_mVz7K1w0gFfhZE_NHdUj3CBoM',
    '11_ANALYSE_correction_juridique.md': '1Ikk9wlfyLuFlTofsyLiz6836bHM5g4_ejQhGuRdUkes',
    '12_ANALYSE_Jurisprudence.md': '1AO7GLNpbNGa9ChiUVa5rbbhLtmppzMTgOcg9qCIJBRU',
    '13_ANALYSE_Plaidoirie_Dirigeants.md': '1uHOesWZrUf16NVs7kC_dr15JtthOfaJnUNo6e3Z7W90',
    '14_ANALYSE_Responsabilites_Legales.md': '1lUKoGE8kozmE3KA4zErv9GYmJZ0yctOk9tn92O8KT34',
}


def read_markdown(filepath: str) -> str:
    """Lit un fichier .md et retourne son contenu."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def get_segments(content: str) -> list[str]:
    """
    Découpe le contenu sur le marqueur <hr><hr>.
    Retourne une liste de segments (sans les marqueurs, stripés).
    """
    segments = [s.strip() for s in content.split(BREAK)]
    return [s for s in segments if s]


def inject_document(filepath: str, doc_id: str, dry_run: bool = False) -> list[dict]:
    """
    Injecte un fichier .md dans un Google Doc.

    Algorithme :
        1. Segment 0 → replaceDocumentWithMarkdown (remplace tout le doc)
        2. Segments 1..N → appendMarkdown + insertPageBreak

    Args:
        filepath: Chemin vers le fichier .md
        doc_id: ID du Google Doc de destination
        dry_run: Si True, affiche les actions sans les exécuter

    Returns:
        Liste des actions effectuées
    """
    content = read_markdown(filepath)
    segments = get_segments(content)
    actions = []

    if not segments:
        print(f"⚠  Aucun segment trouvé dans {filepath}")
        return actions

    for i, seg in enumerate(segments):
        if i == 0:
            # Premier segment : remplace tout le document
            action = {
                'type': 'replaceDocumentWithMarkdown',
                'params': {
                    'documentId': doc_id,
                    'markdown': seg,
                    'firstHeadingAsTitle': True,
                }
            }
            if dry_run:
                print(f"  [{i}] replaceDocumentWithMarkdown (firstHeadingAsTitle=True) — {len(seg)} chars")
            else:
                print(f"  [{i}] Injecting segment 0...")
                # Appel MCP : replaceDocumentWithMarkdown(**action['params'])
            actions.append(action)

        else:
            # Segments suivants : append + page break
            action_append = {
                'type': 'appendMarkdown',
                'params': {
                    'documentId': doc_id,
                    'markdown': seg,
                }
            }
            action_break = {
                'type': 'insertPageBreak',
                'params': {
                    'documentId': doc_id,
                    'index': None,  # À déterminer après append (fin du doc)
                }
            }
            if dry_run:
                print(f"  [{i}] appendMarkdown ({len(seg)} chars) + insertPageBreak")
            else:
                print(f"  [{i}] Appending segment {i}...")
                # Appel MCP : appendMarkdown(**action_append['params'])
                # Puis : insertPageBreak à la fin du doc
            actions.append(action_append)
            actions.append(action_break)

    return actions


def inject_all(dry_run: bool = True) -> None:
    """Injecte tous les fichiers markdown_normalized/ dans leurs Google Docs."""
    for fname, doc_id in DOC_MAP.items():
        fpath = os.path.join(MARKDOWN_DIR, fname)
        if not os.path.exists(fpath):
            print(f"⚠  {fname} introuvable")
            continue
        print(f"\n📄 {fname} → {doc_id}")
        inject_document(fpath, doc_id, dry_run=dry_run)


if __name__ == '__main__':
    inject_all(dry_run=True)
