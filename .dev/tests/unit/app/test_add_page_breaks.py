import pytest
from app.add_page_breaks import add_page_breaks, normalize, BREAK

def test_add_page_breaks_before_first_heading_after_intro():
    content = "# INTRODUCTION\nSome text\n# First Section\nMore text"
    result = add_page_breaks(content)
    assert f"\n{BREAK}\n\n# First Section" in result

def test_add_page_breaks_before_roman_headings():
    content = "# I. Section One\nSome text\n# II. Section Two\nMore text"
    result = add_page_breaks(content)
    assert f"\n{BREAK}\n\n# I. Section One" in result
    assert f"\n{BREAK}\n\n# II. Section Two" in result

def test_add_page_breaks_before_annex():
    content = "# ANNEXE A\nSome text\n## Annexe C\nMore text"
    result = add_page_breaks(content)
    assert f"\n{BREAK}\n\n# ANNEXE A" in result
    assert f"\n{BREAK}\n\n## Annexe C" in result

def test_no_double_page_breaks():
    content = f"# INTRODUCTION\nSome text\n\n{BREAK}\n\n# First Section"
    result = add_page_breaks(content)
    assert result.count(BREAK) == 1

def test_no_break_before_intro():
    content = "# INTRODUCTION\nSome text"
    result = add_page_breaks(content)
    assert BREAK not in result

def test_normalize_remove_vertical_tabs():
    content = "Hello\u000bWorld"
    result = normalize(content)
    assert result == "Hello\n\nWorld"

def test_normalize_collapse_consecutive_newlines():
    content = "Line1\n\n\nLine2\n\n\n\nLine3"
    result = normalize(content)
    assert result == "Line1\n\nLine2\n\nLine3"

def test_normalize_fix_broken_numbered_lists():
    content = "1. First\n2. Second\n2. Third\n3. Fourth"
    result = normalize(content)
    expected = "1. First\n2. Second\n3. Third\n4. Fourth"
    assert result == expected

def test_add_page_breaks_does_not_break_on_non_targeted_headings():
    content = "# INTRODUCTION\n## Not Roman Nor Annex\nSome text\n### Subheading"
    result = add_page_breaks(content)
    assert f"{BREAK}\n\n## Not Roman Nor Annex" not in result
    assert f"{BREAK}\n\n### Subheading" not in result

def test_add_page_breaks_on_subsequent_h1():
    content = "# INTRODUCTION\n# First Heading\n# Another H1"
    result = add_page_breaks(content)
    assert f"\n{BREAK}\n\n# First Heading" in result
    assert f"\n{BREAK}\n\n# Another H1" not in result
