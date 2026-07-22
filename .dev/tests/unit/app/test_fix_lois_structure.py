import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import os
from datetime import datetime
import re

from app.fix_lois_structure import (
    fix_breadcrumb_content,
    add_yaml_frontmatter,
    create_readme_for_directory,
    reorganize_articles,
    process_directory,
    update_main_readme
)

def test_fix_breadcrumb_content():
    content1 = "Ligne 1\n🏠 [HUB]\nLigne 3"
    assert fix_breadcrumb_content(content1) == "Ligne 1\n🏠\nLigne 3"

    content2 = "🏠[Accueil]....../README.md"
    assert fix_breadcrumb_content(content2) == "🏠 [Accueil](../README.md)"

    content3 = "Pas de breadcrumb ici"
    assert fix_breadcrumb_content(content3) == "Pas de breadcrumb ici"

def test_add_yaml_frontmatter_new():
    content = "# Article content"
    title = "Test Title"
    code = "Test Code"
    article = "123"

    with patch('app.fix_lois_structure.datetime') as mock_date:
        mock_date.now.return_value.strftime.return_value = '2023-10-27'
        result = add_yaml_frontmatter(content, title, code, article)

    expected_yaml = f"---\ntitle: Test Title\ncode: Test Code\narticle: 123\ndate: 2023-10-27\nsource: Légifrance\nstatus: En vigueur\n---\n\n# Article content"
    assert result == expected_yaml

def test_add_yaml_frontmatter_existing():
    content = "---\ntitle: Existing\n---\n# Article content"
    result = add_yaml_frontmatter(content, "New Title", "New Code", "456")
    assert result == content

def test_reorganize_articles(tmp_path):
    base_dir = tmp_path / "Lois"
    autres_codes = base_dir / "Autres_codes"
    autres_codes.mkdir(parents=True)

    # Create target directories
    (base_dir / "Code penal").mkdir()
    (base_dir / "Code_civil").mkdir()
    (base_dir / "Code procedure civile").mkdir()
    (base_dir / "Code procedure penale").mkdir()
    (base_dir / "Code_assurances").mkdir()
    (base_dir / "Code_commerce").mkdir()

    # Create some dummy files in Autres_codes
    (autres_codes / "Article_121_3.md").write_text("")  # Code pénal requires _ or no -
    (autres_codes / "Article_1240.md").write_text("")   # Code civil
    (autres_codes / "Article_145.md").write_text("")    # CPC
    (autres_codes / "Article_475-1.md").write_text("")  # CPP
    (autres_codes / "Article_L113-2.md").write_text("") # Assurances
    (autres_codes / "Article_L210_6.md").write_text("") # Commerce requires _ or no -
    (autres_codes / "Article_9999.md").write_text("")   # Unknown, should stay

    with patch('app.fix_lois_structure.BASE_DIR', base_dir):
        reorganize_articles()

    assert (base_dir / "Code penal" / "Article_121_3.md").exists()
    assert (base_dir / "Code_civil" / "Article_1240.md").exists()
    assert (base_dir / "Code procedure civile" / "Article_145.md").exists()
    assert (base_dir / "Code procedure penale" / "Article_475-1.md").exists()
    assert (base_dir / "Code_assurances" / "Article_L113-2.md").exists()
    assert (base_dir / "Code_commerce" / "Article_L210_6.md").exists()
    assert (autres_codes / "Article_9999.md").exists()

def test_process_directory(tmp_path):
    base_dir = tmp_path / "Lois"
    dir_path = base_dir / "Code_test"
    dir_path.mkdir(parents=True)

    md_file = dir_path / "Article_1.md"
    md_file.write_text("# Le premier article\n\n🏠 [HUB]", encoding='utf-8')

    with patch('app.fix_lois_structure.BASE_DIR', base_dir), \
         patch('app.fix_lois_structure.datetime') as mock_date:
        mock_date.now.return_value.strftime.return_value = '2023-10-27'
        process_directory(dir_path)

    content = md_file.read_text(encoding='utf-8')
    assert "---\ntitle: Le premier article" in content
    assert "code: Code Test" in content
    assert "article: 1" in content
    assert "🏠" in content
    assert "🏠 [HUB]" not in content

def test_create_readme_for_directory(tmp_path):
    base_dir = tmp_path / "Lois"
    dir_path = base_dir / "Code_test"
    dir_path.mkdir(parents=True)

    (dir_path / "Article_123.md").write_text("")
    (dir_path / "Article_456-1.md").write_text("")

    with patch('app.fix_lois_structure.BASE_DIR', base_dir):
        create_readme_for_directory(dir_path, "../README.md")

    readme_path = dir_path / "README.md"
    assert readme_path.exists()
    content = readme_path.read_text(encoding='utf-8')
    assert "# Code_test" in content
    assert "- [123](Article_123.md)" in content
    assert "- [456](Article_456-1.md)" in content
    assert f"{datetime.now().strftime('%d %B %Y')}" in content

def test_update_main_readme(tmp_path):
    base_dir = tmp_path / "Lois"
    base_dir.mkdir(parents=True)

    # Create the codes dirs and some dummy files
    codes = ["Code penal", "Code_civil", "Code procedure civile", "Code procedure penale", "Code_assurances", "Code_commerce", "Autres_codes"]
    for code in codes:
        code_dir = base_dir / code
        code_dir.mkdir()
        # Add 2 articles to each code for testing
        (code_dir / "Article_1.md").write_text("")
        (code_dir / "Article_2.md").write_text("")

    readme_path = base_dir / "README.md"
    initial_content = """# Title

### Code_pénal (0 articles)
### Code_civil (0 articles)
### Code de procédure civile (0 articles)
### Code de procédure pénale (0 articles)
### Code des assurances (0 articles)
### Code de commerce (0 articles)
### Autres_codes (0 articles)
    """
    readme_path.write_text(initial_content, encoding='utf-8')

    with patch('app.fix_lois_structure.BASE_DIR', base_dir):
        update_main_readme()

    content = readme_path.read_text(encoding='utf-8')
    assert "### Code_pénal (2 articles)" in content
    assert "### Code_civil (2 articles)" in content
    assert "### Code de procédure civile (2 articles)" in content
    assert "### Code de procédure pénale (2 articles)" in content
    assert "### Code des assurances (2 articles)" in content
    assert "### Code de commerce (2 articles)" in content
    assert "### Autres_codes (2 articles)" in content
