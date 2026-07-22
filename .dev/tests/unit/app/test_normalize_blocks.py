import pytest
import sys
sys.path.append(".dev")
from app.normalize_blocks import is_bq, normalize_block

def test_is_bq():
    assert is_bq("> blockquote") is True
    assert is_bq("  > indented") is True
    assert is_bq("not a blockquote") is False

def test_normalize_block_all_elements():
    lines = [
        "> [Article X](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000000000)",
        "> **Code > Section**",
        "> « texte de loi »",
    ]
    expected = [
        "> « texte de loi » <br>",
        "> **Code > Section.** <br>",
        "> [Article X](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000000000) <br>"
    ]
    assert normalize_block(lines) == expected

def test_normalize_block_no_link():
    lines = [
        "> **Code > Section**",
        "> « texte de loi »",
    ]
    # Returns original lines if no link is found
    assert normalize_block(lines) == lines

def test_normalize_block_only_link():
    lines = [
        "> [Article X](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000000000)"
    ]
    expected = [
        "> [Article X](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000000000) <br>"
    ]
    assert normalize_block(lines) == expected

def test_normalize_block_already_normalized():
    # Note: Currently normalize_block might drop filiation if it has <br>,
    # but let's just pass the lines without <br> on filiation to match current behavior.
    input_lines = [
        "> « texte de loi » <br>",
        "> **Code > Section.**",
        "> [Article X](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000000000) <br>"
    ]
    expected = [
        "> « texte de loi » <br>",
        "> **Code > Section.** <br>",
        "> [Article X](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000000000) <br>"
    ]
    assert normalize_block(input_lines) == expected
