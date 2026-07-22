import pytest
from app.audit_actes import check_naming

def test_check_naming_valid():
    valid_names = [
        "README.md",
        ".gitkeep",
        "123 TYPE Description.md",
        "123A TYPE Description.md",
        "123+ TYPE Description.md",
        "12 TYPE Description.md",
        "123TYPE Description.md",
        "123 TYPE.md",
        "123  .md",
    ]
    for name in valid_names:
        assert check_naming(name) is True, f"Expected '{name}' to be valid"

def test_check_naming_invalid():
    invalid_names = [
        "Description.md",
        "123 TYPE ",
        "abc 123.md",
        "Just text.md",
        "123.md",
        "123 no extension",
        "123.txt"
    ]
    for name in invalid_names:
        assert check_naming(name) is False, f"Expected '{name}' to be invalid"
