from unittest.mock import patch, MagicMock
from app.tools import search_law_code

def test_search_law_code_client_unavailable():
    with patch("app.tools.ServerLegifranceClient", None):
        result = search_law_code("query")
        assert "Erreur : Client Légifrance non disponible." in result

@patch("app.tools.ServerLegifranceClient")
def test_search_law_code_exception(mock_client_class):
    mock_client_class.side_effect = Exception("Test error")
    result = search_law_code("query")
    assert "Erreur lors de la recherche Légifrance : Test error" in result

@patch("app.tools.ServerLegifranceClient")
def test_search_law_code_no_articles(mock_client_class):
    mock_instance = MagicMock()
    mock_instance.search.return_value = {"results": []}
    mock_client_class.return_value = mock_instance

    result = search_law_code("query")
    assert "Aucun article de loi trouvé pour la recherche : 'query'" in result

@patch("app.tools.ServerLegifranceClient")
def test_search_law_code_success(mock_client_class):
    mock_instance = MagicMock()
    mock_instance.search.return_value = {
        "totalResultNumber": 1,
        "results": [
            {
                "article": {
                    "num": "123",
                    "id": "ID_123"
                },
                "texteTitle": "Code de Test"
            }
        ]
    }
    mock_client_class.return_value = mock_instance

    result = search_law_code("query")
    assert "Résultats Légifrance pour 'query'" in result
    assert "1 articles trouvés" in result
    assert "Article 123 du Code de Test" in result
    assert "ID article : ID_123" in result
