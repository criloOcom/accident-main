import pytest
from app.validate_legifrance_urls import validate_url_format, check_yaml_structure

def test_validate_url_format_valid():
    valid_url = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038312693"
    assert validate_url_format(valid_url) == True

def test_validate_url_format_invalid_scheme():
    invalid_url = "http://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038312693"
    assert validate_url_format(invalid_url) == False

def test_validate_url_format_invalid_domain():
    invalid_url = "https://www.example.com/codes/article_lc/LEGIARTI000038312693"
    assert validate_url_format(invalid_url) == False

def test_validate_url_format_invalid_path():
    invalid_url = "https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038312693"
    assert validate_url_format(invalid_url) == False

def test_validate_url_format_not_a_url():
    invalid_url = "not a url"
    assert validate_url_format(invalid_url) == False

def test_check_yaml_structure_valid():
    valid_yaml = """---
title: Article 706-3
code: Code de procédure pénale
article: 706-3
date: 2026-07-11
source: Légifrance
status: En vigueur
url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038312693
---
Contenu de l'article
"""
    is_valid, msg = check_yaml_structure(valid_yaml)
    assert is_valid == True
    assert msg == "YAML valide"

def test_check_yaml_structure_missing_frontmatter():
    invalid_yaml = "Contenu sans frontmatter"
    is_valid, msg = check_yaml_structure(invalid_yaml)
    assert is_valid == False
    assert msg == "Pas de frontmatter YAML"

def test_check_yaml_structure_malformed_frontmatter():
    invalid_yaml = """---
title: Article 706-3
Contenu sans fin de frontmatter
"""
    is_valid, msg = check_yaml_structure(invalid_yaml)
    assert is_valid == False
    assert msg == "Frontmatter YAML mal formé"

def test_check_yaml_structure_missing_field():
    invalid_yaml = """---
title: Article 706-3
code: Code de procédure pénale
article: 706-3
date: 2026-07-11
source: Légifrance
url: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038312693
---
Contenu de l'article
"""
    is_valid, msg = check_yaml_structure(invalid_yaml)
    assert is_valid == False
    assert msg == "Champ status manquant"

def test_check_yaml_structure_invalid_url():
    invalid_yaml = """---
title: Article 706-3
code: Code de procédure pénale
article: 706-3
date: 2026-07-11
source: Légifrance
status: En vigueur
url: https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038312693
---
Contenu de l'article
"""
    is_valid, msg = check_yaml_structure(invalid_yaml)
    assert is_valid == False
    assert msg == "URL invalide: https://www.legifrance.gouv.fr/codes/id/LEGIARTI000038312693"
