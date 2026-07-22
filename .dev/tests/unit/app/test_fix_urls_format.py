import pytest
from pathlib import Path
from app.fix_urls_format import fix_url_format

def test_fix_url_format_with_date(tmp_path):
    # Setup
    test_file = tmp_path / "test_file.md"
    content = 'url: "https://legifrance.gouv.fr/loda/id/JORFTEXT000000000001" "2026-07-11"\n'
    test_file.write_text(content, encoding='utf-8')

    # Execution
    result = fix_url_format(test_file)

    # Verification
    assert result is True
    expected_content = 'url: "https://legifrance.gouv.fr/loda/id/JORFTEXT000000000001"\n'
    assert test_file.read_text(encoding='utf-8') == expected_content

def test_fix_url_format_without_date(tmp_path):
    # Setup
    test_file = tmp_path / "test_file.md"
    content = 'url: "https://legifrance.gouv.fr/loda/id/JORFTEXT000000000001"\n'
    test_file.write_text(content, encoding='utf-8')

    # Execution
    result = fix_url_format(test_file)

    # Verification
    assert result is False
    assert test_file.read_text(encoding='utf-8') == content

def test_fix_url_format_multiple_urls(tmp_path):
    # Setup
    test_file = tmp_path / "test_file.md"
    content = (
        'url: "https://legifrance.gouv.fr/1" "2026-07-11"\n'
        'url: "https://legifrance.gouv.fr/2"\n'
        'url: "https://legifrance.gouv.fr/3" "2026-07-11"\n'
    )
    test_file.write_text(content, encoding='utf-8')

    # Execution
    result = fix_url_format(test_file)

    # Verification
    assert result is True
    expected_content = (
        'url: "https://legifrance.gouv.fr/1"\n'
        'url: "https://legifrance.gouv.fr/2"\n'
        'url: "https://legifrance.gouv.fr/3"\n'
    )
    assert test_file.read_text(encoding='utf-8') == expected_content

def test_fix_url_format_different_date(tmp_path):
    # Setup
    test_file = tmp_path / "test_file.md"
    content = 'url: "https://legifrance.gouv.fr/1" "2023-01-01"\n'
    test_file.write_text(content, encoding='utf-8')

    # Execution
    result = fix_url_format(test_file)

    # Verification
    assert result is False
    assert test_file.read_text(encoding='utf-8') == content

def test_fix_url_format_http(tmp_path):
    # Setup
    test_file = tmp_path / "test_file.md"
    content = 'url: "http://legifrance.gouv.fr/1" "2026-07-11"\n'
    test_file.write_text(content, encoding='utf-8')

    # Execution
    result = fix_url_format(test_file)

    # Verification
    assert result is False
    assert test_file.read_text(encoding='utf-8') == content
