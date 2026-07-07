import pytest
import sys
import os

# Add the app directory to the path so we can import from it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from app.enhance_markdown import get_heading_level

def test_get_heading_level_h1():
    """Test get_heading_level for H1 patterns."""
    assert get_heading_level("PAR CES MOTIFS") == 1
    assert get_heading_level("  PAR CES MOTIFS  ") == 1
    assert get_heading_level("I. Introduction") == 1
    assert get_heading_level("IV. Conclusion") == 1

def test_get_heading_level_h2():
    """Test get_heading_level for H2 patterns."""
    assert get_heading_level("DEMANDES") == 2
    assert get_heading_level("CONCLUSIONS") == 2
    assert get_heading_level("A. First part") == 2
    assert get_heading_level("Sur le fond") == 2
    assert get_heading_level("ANNEXE 1") == 2

def test_get_heading_level_default():
    """Test get_heading_level for patterns that match neither H1 nor H2, it should return default 2."""
    assert get_heading_level("Some random text") == 2
    assert get_heading_level("1. Not a roman numeral") == 2
    assert get_heading_level("E. Letter not in A-D") == 2
    # "Sur un autre sujet" matches H2 pattern, so we shouldn't use it to test the default fallback
    assert get_heading_level("Not a heading string") == 2
