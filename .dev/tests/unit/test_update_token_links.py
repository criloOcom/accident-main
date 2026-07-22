import os
from unittest.mock import patch
from app.update_token_links import (
    normalize,
    resolve_token,
    jeton_relative_path,
    find_tokens_in_content,
    replace_links
)

def test_normalize():
    assert normalize(' La Victime ') == 'la victime'
    assert normalize('Éléphant') == 'elephant'
    assert normalize('L\'Exploitation') == 'l exploitation'
    assert normalize('Prénom de la Victime') == 'prenom de la victime'
    assert normalize('  La  Victime  ') == 'la victime'

def test_resolve_token_known_token():
    assert resolve_token('La Victime') == 'token-victime-nom-complet'
    assert resolve_token('la victime') == 'token-victime-nom-complet'
    assert resolve_token('L\'Adresse de la Victime') == 'token-victime-adresse'

def test_resolve_token_unknown_token():
    assert resolve_token('Token Inconnu') is None

def test_resolve_token_non_token():
    assert resolve_token('N° PV Police') is None
    assert resolve_token('Adresse Tribunal Judiciaire') is None

@patch('app.update_token_links.JETONS_DIR', '/base/🧠 Memory/🗂️ Tokens')
def test_jeton_relative_path():
    from_file = '/base/⚖️ Actes/file.md'
    rel_path = jeton_relative_path(from_file)
    assert rel_path == '../🧠 Memory/🗂️ Tokens'

@patch('app.update_token_links.resolve_token')
def test_find_tokens_in_content(mock_resolve_token):
    mock_resolve_token.side_effect = lambda x: 'token-test' if x == 'La Victime' else None
    content = "Here is [**[La Victime]**](../../🧠 Memory/TOKEN MAP.md#la-victime) and an unknown [**[Unknown]**](../../🧠 Memory/TOKEN MAP.md#unknown)"
    tokens = find_tokens_in_content(content)
    assert len(tokens) == 1
    assert tokens[0]['token_name'] == 'La Victime'
    assert tokens[0]['anchor'] == 'token-test'
    assert tokens[0]['display'] == '**[La Victime]**'
    assert 'TOKEN MAP.md' in tokens[0]['full_match']

@patch('app.update_token_links.jeton_relative_path')
@patch('app.update_token_links.find_tokens_in_content')
def test_replace_links(mock_find_tokens, mock_jeton_rel_path):
    content = "Contact [**[La Victime]**](../../🧠 Memory/TOKEN MAP.md#la-victime) for details."
    mock_find_tokens.return_value = [{
        'start': 8,
        'end': 69,
        'display': '**[La Victime]**',
        'token_name': 'La Victime',
        'anchor': 'token-victime-nom-complet',
        'full_match': '[**[La Victime]**](../../🧠 Memory/TOKEN MAP.md#la-victime)'
    }]
    mock_jeton_rel_path.return_value = '../🧠 Memory/🗂️ Tokens'

    new_content, count = replace_links(content, '/some/path/file.md')

    assert count == 1
    assert 'token-victime-nom-complet.md' in new_content
    assert new_content != content
