import pytest
import re
from unittest.mock import patch, mock_open
from app.inject_citations import norm, resolve_code, ART_RE, process_file, load_gloss, main

def test_norm():
    """Test normalization of article numbers."""
    # norm removes all non alphanumeric EXCEPT dash!
    # Let's check `norm` implementation:
    # return re.sub(r"[^0-9A-Za-z\-]", "", s.replace(" ", "").replace(".", "")).upper()
    assert norm("123-4") == "123-4"
    assert norm(" L. 123 - 4 ") == "L123-4"
    assert norm("R.123.4") == "R1234"
    assert norm("123") == "123"
    assert norm("L. 211-4-1") == "L211-4-1"

def test_resolve_code():
    """Test resolution of code names from fragments."""
    assert resolve_code("procédure civile") == "Code de procédure civile"
    assert resolve_code("civil") == "Code civil"
    assert resolve_code("du travail") == "Code du travail"
    assert resolve_code("inconnu") is None
    assert resolve_code("PROCÉDURE PÉNALE") == "Code de procédure pénale"
    assert resolve_code("pénal") == "Code pénal"
    assert resolve_code("de la route") == "Code de la route"

def test_art_re():
    """Test the regular expression for finding article citations."""
    text1 = "Article L. 123-4 du code de la route."
    matches1 = list(ART_RE.finditer(text1))
    assert len(matches1) == 1
    assert matches1[0].group(1) == "L. 123-4"
    assert matches1[0].group(2).strip() == "de la route"

    text2 = "article 123 du code pénal"
    matches2 = list(ART_RE.finditer(text2))
    assert len(matches2) == 1
    assert matches2[0].group(1) == "123"
    assert matches2[0].group(2).strip() == "pénal"

    text3 = "L'article D. 123-4-5 du Code de la sécurité sociale prévoit que..."
    matches3 = list(ART_RE.finditer(text3))
    assert len(matches3) == 1
    assert matches3[0].group(1) == "D. 123-4-5"
    assert "sécurité sociale" in matches3[0].group(2)

def test_process_file_no_inject(tmp_path):
    """Test that citations are NOT injected if legifrance link is present."""
    idx = {
        ("L123-4", "Code de la route"): {"block": "> **Article L123-4 du Code de la route**\n> Texte"}
    }

    file_content = """Voici l'article L. 123-4 du Code de la route.
> **Article L123-4 du Code de la route**
> [legifrance](https://legifrance...)
"""
    test_file = tmp_path / "test.md"
    test_file.write_text(file_content, encoding="utf-8")

    inserts = process_file(str(test_file), idx, apply=True)
    assert inserts == 0

def test_process_file_inject(tmp_path):
    """Test that citations ARE injected if no legifrance link is present."""
    idx = {
        ("L123-4", "Code de la route"): {"block": "> **Article L123-4 du Code de la route**\n> Texte"}
    }

    file_content = """Voici l'article L. 123-4 du Code de la route.

Quelque chose d'autre ici.
"""
    test_file = tmp_path / "test.md"
    test_file.write_text(file_content, encoding="utf-8")

    inserts = process_file(str(test_file), idx, apply=True)
    assert inserts == 1

    content = test_file.read_text(encoding="utf-8")
    assert "> **Article L123-4 du Code de la route**" in content

def test_process_file_abroge_diff(tmp_path):
    """Test that 'abrogation différée' is correctly added."""
    idx = {
        ("123", "Code pénal"): {"block": "> **Article 123 du Code pénal.** <br>\n> Texte pénal", "etat": "ABROGE_DIFF"}
    }

    file_content = """Voici l'article 123 du Code pénal.
"""
    test_file = tmp_path / "test.md"
    test_file.write_text(file_content, encoding="utf-8")

    inserts = process_file(str(test_file), idx, apply=True)
    assert inserts == 1

    content = test_file.read_text(encoding="utf-8")
    assert "abrogation différée" in content

def test_load_gloss():
    """Test loading the glossary JSON."""
    json_data = '{"L. 123-4||Code de la route": {"block": "...", "etat": "VIGUEUR"}}'
    with patch("builtins.open", mock_open(read_data=json_data)):
        idx = load_gloss()
        assert ("L123-4", "Code de la route") in idx

def test_process_file_no_insert_in_yaml_or_headers(tmp_path):
    """Test that citations are ignored if inside yaml or headers."""
    idx = {
        ("L123-4", "Code de la route"): {"block": "> **Article L123-4 du Code de la route**\n> Texte"}
    }

    file_content = """---
yaml: true
description: L'article L. 123-4 du Code de la route.
---
# L'article L. 123-4 du Code de la route

> Article L. 123-4 du Code de la route (déjà cité en blockquote)
"""
    test_file = tmp_path / "test.md"
    test_file.write_text(file_content, encoding="utf-8")

    inserts = process_file(str(test_file), idx, apply=True)
    assert inserts == 0

@patch('app.inject_citations.sys')
@patch('app.inject_citations.os.walk')
@patch('app.inject_citations.load_gloss')
@patch('app.inject_citations.process_file')
def test_main(mock_process_file, mock_load_gloss, mock_walk, mock_sys):
    """Test the main function argument parsing and directory walking."""
    mock_sys.argv = ['inject_citations.py']
    mock_load_gloss.return_value = {}
    mock_walk.return_value = [
        ('/fake/TOKEN', [], ['file1.md', 'file2.txt']),
        ('/fake/TOKEN/sub', [], ['file3.md'])
    ]
    mock_process_file.return_value = 1

    main()

    assert mock_process_file.call_count == 2
    mock_process_file.assert_any_call('/fake/TOKEN/file1.md', {}, apply=False)
    mock_process_file.assert_any_call('/fake/TOKEN/sub/file3.md', {}, apply=False)
