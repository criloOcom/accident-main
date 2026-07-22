#!/usr/bin/env python3
"""Tests unitaires pour validate_organization.py."""

import os
import sys
import importlib.util
from unittest.mock import patch, mock_open, MagicMock

# Charger validate_organization.py de manière robuste
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
APP = os.path.join(ROOT, '.dev', 'app', 'validate_organization.py')
spec = importlib.util.spec_from_file_location('validate_organization', APP)
mod = importlib.util.module_from_spec(spec)
sys.modules['validate_organization'] = mod
spec.loader.exec_module(mod)

validate_breadcrumbs = mod.validate_breadcrumbs
validate_yaml_urls = mod.validate_yaml_urls
validate_readme_files = mod.validate_readme_files
main = mod.main

@patch('validate_organization.Path')
def test_validate_breadcrumbs_ok(mock_path):
    mock_lois_dir = MagicMock()
    mock_path.return_value = mock_lois_dir

    mock_md_file = MagicMock()
    mock_md_file.__str__.return_value = "Article1.md"
    mock_lois_dir.rglob.return_value = [mock_md_file]

    with patch('builtins.open', mock_open(read_data="🏠 Breadcrumb\nContent")):
        ok, errors = validate_breadcrumbs()

    assert ok is True
    assert len(errors) == 0

@patch('validate_organization.Path')
def test_validate_breadcrumbs_error(mock_path):
    mock_lois_dir = MagicMock()
    mock_path.return_value = mock_lois_dir

    mock_md_file = MagicMock()
    mock_md_file.__str__.return_value = "Article1.md"
    mock_lois_dir.rglob.return_value = [mock_md_file]

    with patch('builtins.open', mock_open(read_data="No Breadcrumb\nContent")):
        ok, errors = validate_breadcrumbs()

    assert ok is False
    assert len(errors) == 1
    assert "Pas de breadcrumb en première ligne" in errors[0]

@patch('validate_organization.Path')
def test_validate_yaml_urls_ok(mock_path):
    mock_lois_dir = MagicMock()
    mock_path.return_value = mock_lois_dir

    mock_md_file = MagicMock()
    mock_md_file.__str__.return_value = "Article1.md"
    mock_lois_dir.rglob.return_value = [mock_md_file]

    with patch('builtins.open', mock_open(read_data="url: https://legifrance.gouv.fr\n")):
        ok, missing = validate_yaml_urls()

    assert ok is True
    assert len(missing) == 0

@patch('validate_organization.Path')
def test_validate_yaml_urls_error(mock_path):
    mock_lois_dir = MagicMock()
    mock_path.return_value = mock_lois_dir

    mock_md_file = MagicMock()
    mock_md_file.__str__.return_value = "Article1.md"
    mock_lois_dir.rglob.return_value = [mock_md_file]

    with patch('builtins.open', mock_open(read_data="no link here\n")):
        ok, missing = validate_yaml_urls()

    assert ok is False
    assert len(missing) == 1

@patch('validate_organization.Path')
def test_validate_readme_files_ok(mock_path):
    mock_readme = MagicMock()
    mock_readme.exists.return_value = True
    mock_path.return_value = mock_readme

    ok, missing = validate_readme_files()

    assert ok is True
    assert len(missing) == 0

@patch('validate_organization.Path')
def test_validate_readme_files_error(mock_path):
    mock_readme = MagicMock()
    mock_readme.exists.return_value = False
    mock_path.return_value = mock_readme

    ok, missing = validate_readme_files()

    assert ok is False
    assert len(missing) == 4

@patch('validate_organization.validate_breadcrumbs')
@patch('validate_organization.validate_yaml_urls')
@patch('validate_organization.validate_readme_files')
def test_main_all_ok(mock_readmes, mock_urls, mock_breadcrumbs):
    mock_breadcrumbs.return_value = (True, [])
    mock_urls.return_value = (True, [])
    mock_readmes.return_value = (True, [])

    assert main() is True

@patch('validate_organization.validate_breadcrumbs')
@patch('validate_organization.validate_yaml_urls')
@patch('validate_organization.validate_readme_files')
def test_main_error(mock_readmes, mock_urls, mock_breadcrumbs):
    mock_breadcrumbs.return_value = (False, ["error"])
    mock_urls.return_value = (True, [])
    mock_readmes.return_value = (True, [])

    assert main() is False
