import pytest
import os
import tempfile
import urllib.parse
from app.link_tokens import build_synonyms, get_relative_path, _split_yaml, scan_file, TOKENS_DIR, TARGET_DIR

def test_build_synonyms():
    mapping = {
        "Délégué": ("**[Délégué]**", "token-delegue.md"),
        "Hôpital": ("**[Hôpital]**", "token-hopital.md"),
        "Garçon": ("**[Garçon]**", "token-garcon.md"),
        "Normal": ("**[Normal]**", "token-normal.md"),
    }
    synonyms = build_synonyms(mapping)
    assert "Delegue" in synonyms
    assert synonyms["Delegue"] == ("**[Délégué]**", "token-delegue.md")
    assert "Hopital" in synonyms
    assert "Garcon" in synonyms
    assert "Normal" not in synonyms

def test_split_yaml():
    content = "---\ntitle: Test\n---\nBody text"
    yaml, body = _split_yaml(content)
    assert yaml == "---\ntitle: Test\n---\n"
    assert body == "Body text"

    content_no_yaml = "Just body text\nand more"
    yaml, body = _split_yaml(content_no_yaml)
    assert yaml == ""
    assert body == content_no_yaml

def test_get_relative_path(monkeypatch):
    import app.link_tokens as lt

    # Mock TARGET_DIR and TOKENS_DIR
    monkeypatch.setattr(lt, "TARGET_DIR", "/repo/Actes/Token")
    monkeypatch.setattr(lt, "TOKENS_DIR", "/repo/Memory/Tokens")

    # A file in /repo/Actes/Token/sub/file.md
    file_path = "/repo/Actes/Token/sub/file.md"
    rel = lt.get_relative_path(file_path)

    # expected relative path
    expected = "../../../Memory/Tokens"
    assert rel == expected

def test_scan_file(tmp_path):
    # Setup test file
    content = "---\ntitle: Test\n---\nHere is a **[Délégué]** and a **[Garçon]**. Already linked: [**[Normal]**](path/to/token.md). Link inside: **[Hôpital](url)**. Nested: [N° [Dossier]](path). Placeholder: **[À compléter]**."
    fpath = tmp_path / "sub" / "test.md"
    os.makedirs(fpath.parent, exist_ok=True)
    fpath.write_text(content)

    import app.link_tokens as lt
    original_target = lt.TARGET_DIR
    original_tokens = lt.TOKENS_DIR
    lt.TARGET_DIR = str(tmp_path)
    lt.TOKENS_DIR = str(tmp_path / "Memory" / "Tokens")

    mapping = {
        "Délégué": ("**[Délégué]**", "token-delegue.md"),
        "Hôpital": ("**[Hôpital]**", "token-hopital.md"),
        "Normal": ("**[Normal]**", "token-normal.md")
    }
    synonyms = {
        "Garcon": ("**[Garçon]**", "token-garcon.md")
    }
    all_displays = ["Délégué", "Hôpital", "Normal", "Garcon"]

    # We're calling scan_file but wait, the content contains **[Garçon]** which is not in mapping or synonyms keys
    # Wait, Garçon should be in mapping, and Garcon in synonyms.
    mapping["Garçon"] = ("**[Garçon]**", "token-garcon.md")
    all_displays.append("Garçon")

    changes = scan_file(str(fpath), all_displays, mapping, synonyms, apply=True, dry_run=False)

    # Expected changes:
    # **[Délégué]** -> **[Délégué](../../Memory/Tokens/token-delegue.md)**
    # **[Garçon]** -> **[Garçon](../../Memory/Tokens/token-garcon.md)**
    # **[Normal]** is already linked, no change.
    # **[Hôpital](url)** is already linked, no change.

    assert changes == 2

    result = fpath.read_text()
    assert "**[Délégué](../Memory/Tokens/token-delegue.md)**" in result
    assert "**[Garçon](../Memory/Tokens/token-garcon.md)**" in result
    assert "[**[Normal]**](path/to/token.md)" in result
    assert "**[Hôpital](url)**" in result
    assert "**[À compléter]**" in result

    lt.TARGET_DIR = original_target
    lt.TOKENS_DIR = original_tokens


def test_scan_file_no_changes(tmp_path):
    # Setup test file where all tokens are already linked or no tokens exist
    content = "---\ntitle: Test\n---\nNo unlinked tokens here. Just [**[Délégué]**](path/to/token.md) which is already linked."
    fpath = tmp_path / "test2.md"
    fpath.write_text(content)

    import app.link_tokens as lt
    original_target = lt.TARGET_DIR
    original_tokens = lt.TOKENS_DIR
    lt.TARGET_DIR = str(tmp_path)
    lt.TOKENS_DIR = str(tmp_path / "Memory" / "Tokens")

    mapping = {
        "Délégué": ("**[Délégué]**", "token-delegue.md"),
    }
    synonyms = {}
    all_displays = ["Délégué"]

    changes = scan_file(str(fpath), all_displays, mapping, synonyms, apply=True, dry_run=False)

    assert changes == 0
    result = fpath.read_text()
    assert result == content

    lt.TARGET_DIR = original_target
    lt.TOKENS_DIR = original_tokens

def test_extract_map(tmp_path, monkeypatch):
    import app.link_tokens as lt

    # Create fake TOKEN MAP.md
    token_map_content = """# Token Map

Here is a list of tokens:
- [**[Token A]**](path/token-a.md)
- [**[Token B]**](path/to/token-b.md)
"""
    token_map_file = tmp_path / "TOKEN_MAP.md"
    token_map_file.write_text(token_map_content)

    # Mock TOKEN_MAP_FILE
    monkeypatch.setattr(lt, "TOKEN_MAP_FILE", str(token_map_file))

    mapping = lt.extract_map()

    assert len(mapping) == 2
    assert "Token A" in mapping
    assert mapping["Token A"] == ("**[Token A]**", "token-a.md")
    assert "Token B" in mapping
    assert mapping["Token B"] == ("**[Token B]**", "token-b.md")


def test_extract_from_token_files(tmp_path, monkeypatch):
    import app.link_tokens as lt

    tokens_dir = tmp_path / "Tokens"
    tokens_dir.mkdir()

    (tokens_dir / "README.md").write_text("Should be ignored")
    (tokens_dir / "not_md.txt").write_text("Should be ignored")

    token1 = tokens_dir / "token1.md"
    token1.write_text("---\ntitle: \"Token One\"\n---\n# Some Heading\nContent")

    token2 = tokens_dir / "token2.md"
    token2.write_text("# Just a heading\nSome content without yaml title")

    monkeypatch.setattr(lt, "TOKENS_DIR", str(tokens_dir))

    mapping = lt.extract_from_token_files()

    assert len(mapping) == 1
    assert "token1.md" in mapping
    assert mapping["token1.md"] == "Token One"

def test_token_pattern_from_map():
    import app.link_tokens as lt

    mapping = {
        "Short": ("**[Short]**", "token-short.md"),
        "Very Long Display Name": ("**[Very Long Display Name]**", "token-long.md")
    }
    synonyms = {
        "A Synonym": ("**[A Synonym]**", "token-synonym.md")
    }

    all_displays, ret_mapping, ret_synonyms = lt.token_pattern_from_map(mapping, synonyms)

    assert ret_mapping == mapping
    assert ret_synonyms == synonyms
    # Lengths should be sorted descending
    assert all_displays == ["Very Long Display Name", "A Synonym", "Short"]
