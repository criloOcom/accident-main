import os
import sys
from unittest.mock import patch
import pytest

from app.encode_jeton_links import encode_url_path, main

def test_encode_url_path_basic():
    assert encode_url_path("path/to/file.md") == "path/to/file.md"

def test_encode_url_path_spaces():
    assert encode_url_path("path with spaces/file.md") == "path%20with%20spaces/file.md"

def test_encode_url_path_emojis():
    assert encode_url_path("Memory/🧠 Tokens/token.md") == "Memory/%F0%9F%A7%A0%20Tokens/token.md"
    assert encode_url_path("Memory/🗂️ Tokens/token.md") == "Memory/%F0%9F%97%82%EF%B8%8F%20Tokens/token.md"

def test_encode_url_path_preserves_special_chars():
    assert encode_url_path("/path/with (parentheses)#hash") == "/path/with%20(parentheses)#hash"

def test_encode_url_path_accents():
    assert encode_url_path("dossier/éléphant.md") == "dossier/%C3%A9l%C3%A9phant.md"

def test_main_encodes_links_in_files(tmp_path):
    # Create a dummy markdown file with links that need encoding
    md_file = tmp_path / "test.md"
    content = """
    Here is a link: [Token 1](../../Memory/🧠 Tokens/token1.md)
    And another: [Token 2](../../Memory/🗂️ Tokens/token2.md)
    And with space: [Token 3](../../Memory/ Tokens/token3.md)
    Already encoded: [Token 4](../../Memory/%F0%9F%A7%A0%20Tokens/token4.md)
    Not a token link: [Link](https://example.com/some link)
    """
    md_file.write_text(content, encoding='utf-8')

    # Mock BASE to point to tmp_path
    with patch("app.encode_jeton_links.BASE", str(tmp_path)):
        with patch("app.encode_jeton_links.DRY_RUN", False):
            main()

    # Read modified content
    modified_content = md_file.read_text(encoding='utf-8')

    # Check that links were encoded
    assert "[Token 1](../../Memory/%F0%9F%A7%A0%20Tokens/token1.md)" in modified_content
    assert "[Token 2](../../Memory/%F0%9F%97%82%EF%B8%8F%20Tokens/token2.md)" in modified_content
    assert "[Token 3](../../Memory/%20Tokens/token3.md)" in modified_content
    # Already encoded link should remain unchanged
    assert "[Token 4](../../Memory/%F0%9F%A7%A0%20Tokens/token4.md)" in modified_content
    # Not a token link should remain unchanged
    assert "[Link](https://example.com/some link)" in modified_content

def test_main_dry_run(tmp_path, capsys):
    md_file = tmp_path / "test.md"
    content = """
    Here is a link: [Token 1](../../Memory/🧠 Tokens/token1.md)
    """
    md_file.write_text(content, encoding='utf-8')

    with patch("app.encode_jeton_links.BASE", str(tmp_path)):
        with patch("app.encode_jeton_links.DRY_RUN", True):
            main()

    # Read content, should be unmodified
    assert md_file.read_text(encoding='utf-8') == content

    # Check stdout
    captured = capsys.readouterr()
    assert "[DRY-RUN]" in captured.out
    assert "test.md: 1 lien(s)" in captured.out
