from app.enhance_markdown import bold_tokens
from app.enhance_markdown import get_heading_level


def test_bold_tokens_single_token():
    text = "Hello [La Victime] how are you"
    expected = "Hello **[La Victime]** how are you"
    assert bold_tokens(text) == expected


def test_bold_tokens_multiple_tokens():
    text = "[Token1] and [Token2]"
    expected = "**[Token1]** and **[Token2]**"
    assert bold_tokens(text) == expected


def test_bold_tokens_no_tokens():
    text = "Just some normal text."
    expected = "Just some normal text."
    assert bold_tokens(text) == expected


def test_bold_tokens_empty_string():
    text = ""
    expected = ""
    assert bold_tokens(text) == expected


def test_bold_tokens_adjacent_tokens():
    text = "[Token1][Token2]"
    expected = "**[Token1]****[Token2]**"
    assert bold_tokens(text) == expected


def test_bold_tokens_multiline():
    text = "Line 1 with [token]\nLine 2 with [another token]"
    expected = "Line 1 with **[token]**\nLine 2 with **[another token]**"
    assert bold_tokens(text) == expected


def test_bold_tokens_with_special_characters():
    text = "This is a [token-with_special:characters!]"
    expected = "This is a **[token-with_special:characters!]**"
    assert bold_tokens(text) == expected


def test_get_heading_level_h1():
    assert get_heading_level("PAR CES MOTIFS") == 1
    assert get_heading_level("  PAR CES MOTIFS  ") == 1
    assert get_heading_level("I. Introduction") == 1
    assert get_heading_level("IV. Conclusion") == 1


def test_get_heading_level_h2():
    assert get_heading_level("DEMANDES") == 2
    assert get_heading_level("CONCLUSIONS") == 2
    assert get_heading_level("A. First part") == 2
    assert get_heading_level("Sur le fond") == 2
    assert get_heading_level("ANNEXE 1") == 2


def test_get_heading_level_default():
    assert get_heading_level("Some random text") == 2
    assert get_heading_level("1. Not a roman numeral") == 2
    assert get_heading_level("E. Letter not in A-D") == 2
    assert get_heading_level("Not a heading string") == 2
