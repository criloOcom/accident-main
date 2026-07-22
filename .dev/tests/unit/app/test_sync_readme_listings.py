import os
import pytest
import shutil
from unittest.mock import patch
from app.sync_readme_listings import (
    scan_readmes,
    find_listed_files,
    actual_files_in_dir,
    determine_format,
    find_insertion_point,
    generate_entries,
    sync_readme
)

def test_find_listed_files():
    content = """
    - [File A](file_a.md)
    - **[File B](file_b.md)**
    - [file_c.md]
    - **file_d.md**
    - [External](https://example.com)
    - Just some text
    """
    found = find_listed_files(content)
    assert found == {"file_a.md", "file_b.md", "file_c.md", "file_d.md"}

def test_determine_format():
    table_content = "| File | Description |\n|---|---|\n| [a](a.md) | desc |\n| [b](b.md) | desc |"
    assert determine_format(table_content) == "table"

    bold_link_content = "## Files\n- **[a](a.md)**\n- **[b](b.md)**"
    assert determine_format(bold_link_content) == "bold_link"

    link_content = "## Files\n- [a](a.md)\n- [b](b.md)"
    assert determine_format(link_content) == "link"

    bold_name_content = "## Files\n- **a.md** — desc\n- **b.md**"
    assert determine_format(bold_name_content) == "bold_name"

    none_content = "Just some text without any listings"
    assert determine_format(none_content) == "none"

def test_find_insertion_point():
    bold_link_content = "## Files\n- **[a](a.md)**\n- **[b](b.md)**\n\nSome other text"
    # Lines:
    # 0: ## Files
    # 1: - **[a](a.md)**
    # 2: - **[b](b.md)**
    # 3:
    # 4: Some other text
    # Should insert after line 2, so at index 3.
    assert find_insertion_point(bold_link_content, "bold_link") == 3

    none_content = "## Liste\nSome text\n\n## Next section"
    # Lines:
    # 0: ## Liste
    # 1: Some text
    # 2:
    # 3: ## Next section
    # Should insert before "## Next section" so at index 3.
    assert find_insertion_point(none_content, "none") == 3

def test_generate_entries():
    files = ["file_a.md", "file_b.md"]
    assert generate_entries(files, "bold_link") == [
        "- **[file_a](file_a.md)**",
        "- **[file_b](file_b.md)**"
    ]
    assert generate_entries(files, "bold_name") == [
        "- **[file_a](file_a.md)**",
        "- **[file_b](file_b.md)**"
    ]
    assert generate_entries(files, "link") == [
        "- [file_a](file_a.md)",
        "- [file_b](file_b.md)"
    ]

    files_with_space = ["my file.md"]
    assert generate_entries(files_with_space, "link") == [
        "- [my file](my%20file.md)"
    ]

def test_scan_readmes(tmp_path):
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "README.md").touch()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir2" / "README.md").touch()
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "README.md").touch()
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "README.md").touch()

    readmes = scan_readmes(str(tmp_path))
    assert len(readmes) == 2
    assert os.path.join(str(tmp_path), "dir1", "README.md") in readmes
    assert os.path.join(str(tmp_path), "dir2", "README.md") in readmes

def test_actual_files_in_dir(tmp_path):
    (tmp_path / "README.md").touch()
    (tmp_path / "file1.md").touch()
    (tmp_path / "file2.md").touch()
    (tmp_path / "image.png").touch()

    files = actual_files_in_dir(str(tmp_path / "README.md"))
    assert files == {"file1.md", "file2.md"}

def test_sync_readme_no_missing(tmp_path):
    readme_path = tmp_path / "README.md"
    readme_path.write_text("## Liste\n- [file1](file1.md)\n")
    (tmp_path / "file1.md").touch()

    result = sync_readme(str(readme_path), dry_run=False, backup=False)
    assert "à jour" in result

def test_sync_readme_with_missing(tmp_path):
    readme_path = tmp_path / "README.md"
    readme_path.write_text("## Liste\n- [file1](file1.md)\n")
    (tmp_path / "file1.md").touch()
    (tmp_path / "file2.md").touch()

    # Dry run
    result = sync_readme(str(readme_path), dry_run=True, backup=False)
    assert "à ajouter" in result
    assert "file2" not in readme_path.read_text()

    # Apply
    result = sync_readme(str(readme_path), dry_run=False, backup=False)
    assert "ajouté" in result
    assert "- [file2](file2.md)" in readme_path.read_text()

def test_sync_readme_table_format(tmp_path):
    readme_path = tmp_path / "README.md"
    readme_path.write_text("| File | Desc |\n|---|---|\n| [file1](file1.md) | desc |\n| [f](f.md) | d |")
    (tmp_path / "file1.md").touch()
    (tmp_path / "f.md").touch()
    (tmp_path / "file2.md").touch() # missing

    result = sync_readme(str(readme_path), dry_run=False, backup=False)
    assert "format tableau ignoré" in result
    assert "file2" not in readme_path.read_text()
