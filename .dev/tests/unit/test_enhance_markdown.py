from app.enhance_markdown import bold_tokens


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
