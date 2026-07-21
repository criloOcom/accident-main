import pytest
from app.generate_real_versions import (
    replace_header_block,
    update_yaml_frontmatter,
    deduplicate_lrar_numbers,
    preprocess_nested_bracket_tokens,
)

def test_replace_header_block():
    original = "Hello\n\n**[L'Adresse de la Victime]**\n\nCourriel : **[L'Email de la Victime]**\n\nGoodbye"
    expected = "Hello\n\nSébastien GRAZIDE\n10 Avenue de Purpan, 31700 Blagnac\nCourriel : sebastien.grazide@gmail.com\n\nGoodbye"
    assert replace_header_block(original) == expected

def test_replace_header_block_no_match():
    original = "Some other text without the specific pattern."
    assert replace_header_block(original) == original

def test_update_yaml_frontmatter_adds_version():
    original = "---\ntitre: Mon Document\n---\nContent here."
    expected = "---\ntitre: Mon Document - Version réelle\n---\nContent here."
    assert update_yaml_frontmatter(original) == expected

def test_update_yaml_frontmatter_already_present():
    original = "---\ntitre: Mon Document - Version réelle\n---\nContent here."
    assert update_yaml_frontmatter(original) == original

def test_update_yaml_frontmatter_no_title():
    original = "---\nauthor: Someone\n---\nContent here."
    assert update_yaml_frontmatter(original) == original

def test_deduplicate_lrar_numbers_pattern_a():
    original = "Some text LRAR n° [1234567890123](http://link) — `1234567890123` more text"
    expected = "Some text LRAR n° [1234567890123](http://link) more text"
    assert deduplicate_lrar_numbers(original) == expected

def test_deduplicate_lrar_numbers_pattern_b():
    original = "Some text (LRAR n° 1234567890123 — 1234567890123) more text"
    expected = "Some text (LRAR n° 1234567890123) more text"
    assert deduplicate_lrar_numbers(original) == expected

def test_deduplicate_lrar_numbers_pattern_c():
    original = "Some text LRAR n° 1234567890123 — 1234567890123 more text"
    expected = "Some text LRAR n° 1234567890123 more text"
    assert deduplicate_lrar_numbers(original) == expected

def test_deduplicate_lrar_numbers_pattern_d():
    original = "Some text LRAR n° <1234567890123> — 1234567890123 more text"
    expected = "Some text LRAR n° <1234567890123> more text"
    assert deduplicate_lrar_numbers(original) == expected

def test_preprocess_nested_bracket_tokens():
    original_cpam_link = "[**[N° [Dossier CPAM](http://link)]**](http://link2)"
    assert "31727387" in preprocess_nested_bracket_tokens(original_cpam_link)

    original_cpam_bold = "**[N° [Dossier CPAM](http://link)]**"
    assert "31727387" in preprocess_nested_bracket_tokens(original_cpam_bold)

    original_cpam_errone_link = "[**[N° [Dossier CPAM erroné](http://link)]**](http://link2)"
    assert "2631103960" in preprocess_nested_bracket_tokens(original_cpam_errone_link)

    original_cpam_errone_bold = "**[N° [Dossier CPAM erroné](http://link)]**"
    assert "2631103960" in preprocess_nested_bracket_tokens(original_cpam_errone_bold)
