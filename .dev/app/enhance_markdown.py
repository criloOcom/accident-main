import re


def split_sentences(text):
    # Dummy implementation for testing purposes
    return text

def bold_tokens(text):
    """Wrap all [token] patterns with ** for bold."""
    text = re.sub(r'(\[[^\]]+\])', r'**\1**', text)
    return text

def enhance(text):
    text = split_sentences(text)
    text = bold_tokens(text)
    return text
