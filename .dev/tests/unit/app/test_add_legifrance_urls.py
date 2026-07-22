import pytest
from app.add_legifrance_urls import extract_article_number, find_legiarti_id, update_yaml_with_url

def test_extract_article_number():
    assert extract_article_number("Article_1240.md") == "1240.md"
    assert extract_article_number("Article-1240.md") == "1240.md"
    assert extract_article_number("Article:1240.md") == "1240.md"
    assert extract_article_number("Article_L124-3.md") == "L124.3.md"
    assert extract_article_number("Article1240.md") == "1240"
    assert extract_article_number("Article124-3.md") == "124.3"
    assert extract_article_number("L124-3_Code_Civil.md") == "L124.3"
    assert extract_article_number("R143-2.md") == "R143.2"
    assert extract_article_number("Unknown.md") is None

def test_find_legiarti_id():
    assert find_legiarti_id("1240") == "LEGIARTI000032041571"
    assert find_legiarti_id("L124.3") == "LEGIARTI000006439100"
    assert find_legiarti_id("Unknown") is None

def test_update_yaml_with_url(tmp_path):
    # Test file with YAML frontmatter
    file1 = tmp_path / "test1.md"
    file1.write_text("---\ntitle: Test\n---\nContent", encoding="utf-8")

    # URL not present, should add it
    assert update_yaml_with_url(str(file1), "LEGIARTI000032041571") == True
    content = file1.read_text(encoding="utf-8")
    assert "url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032041571" in content

    # URL already present, should not add it
    assert update_yaml_with_url(str(file1), "LEGIARTI000032041571") == False

    # Test file without YAML frontmatter
    file2 = tmp_path / "test2.md"
    file2.write_text("Content without yaml", encoding="utf-8")
    assert update_yaml_with_url(str(file2), "LEGIARTI000032041571") == False
