import pytest
from app.add_page_breaks import normalize

def test_normalize_vertical_tabs():
    content = "Hello\u000bWorld\u000b!"
    assert normalize(content) == "Hello\n\nWorld\n\n!"

def test_normalize_consecutive_newlines():
    content = "Line 1\n\n\nLine 2\n\n\n\nLine 3"
    assert normalize(content) == "Line 1\n\nLine 2\n\nLine 3"

def test_normalize_broken_numbered_lists():
    content = "1. Item A\n1. Item B\n1. Item C"
    expected = "1. Item A\n2. Item B\n3. Item C"
    assert normalize(content) == expected

def test_normalize_correct_numbered_lists():
    content = "1. Item A\n2. Item B\n3. Item C"
    expected = "1. Item A\n2. Item B\n3. Item C"
    assert normalize(content) == expected

def test_normalize_nested_numbered_lists():
    content = "1. Item A\n  1. Sub A\n  1. Sub B\n1. Item B"
    expected = "1. Item A\n  1. Sub A\n  2. Sub B\n2. Item B"
    assert normalize(content) == expected

def test_normalize_reset_list_after_text():
    content = "1. Item A\n2. Item B\n\nSome text\n\n1. Item C\n1. Item D"
    expected = "1. Item A\n2. Item B\n\nSome text\n\n1. Item C\n2. Item D"
    assert normalize(content) == expected
