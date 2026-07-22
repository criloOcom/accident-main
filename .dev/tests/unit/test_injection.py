import pytest
from app.injection import get_segments, BREAK
from app.injection import read_markdown

def test_get_segments_empty_string():
    assert get_segments("") == []
    assert get_segments("   ") == []

def test_get_segments_no_marker():
    assert get_segments("Hello world") == ["Hello world"]
    assert get_segments("  Hello world  ") == ["Hello world"]

def test_get_segments_one_marker():
    content = f"Part 1 {BREAK} Part 2"
    assert get_segments(content) == ["Part 1", "Part 2"]

def test_get_segments_multiple_markers():
    content = f"Part 1 {BREAK} Part 2 {BREAK} Part 3"
    assert get_segments(content) == ["Part 1", "Part 2", "Part 3"]

def test_get_segments_whitespace_around_markers():
    content = f"  Part 1  \n\n{BREAK}\n  Part 2  "
    assert get_segments(content) == ["Part 1", "Part 2"]

def test_get_segments_consecutive_markers():
    content = f"Part 1 {BREAK}{BREAK} Part 2"
    assert get_segments(content) == ["Part 1", "Part 2"]

    content2 = f"Part 1 {BREAK} {BREAK} Part 2"
    assert get_segments(content2) == ["Part 1", "Part 2"]

def test_get_segments_marker_at_edges():
    content_start = f"{BREAK} Part 1"
    assert get_segments(content_start) == ["Part 1"]

    content_end = f"Part 1 {BREAK}"
    assert get_segments(content_end) == ["Part 1"]

    content_both = f"{BREAK} Part 1 {BREAK}"
    assert get_segments(content_both) == ["Part 1"]


def test_read_markdown_valid_file(tmp_path):
    test_file = tmp_path / "test.md"
    test_file.write_text("Hello, world!", encoding="utf-8")
    assert read_markdown(str(test_file)) == "Hello, world!"

def test_read_markdown_empty_file(tmp_path):
    test_file = tmp_path / "empty.md"
    test_file.write_text("", encoding="utf-8")
    assert read_markdown(str(test_file)) == ""

def test_read_markdown_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_markdown("non_existent_file.md")
