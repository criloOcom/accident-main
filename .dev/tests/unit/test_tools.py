import pytest
from unittest.mock import patch, MagicMock

from app.tools import get_law_article

def test_get_law_article_client_none():
    with patch("app.tools.ServerLegifranceClient", None):
        result = get_law_article("LEGIARTI000000000000")
        assert result == "Erreur : Client Légifrance non disponible."

def test_get_law_article_not_found():
    mock_client_instance = MagicMock()
    mock_client_instance.consulte_article.return_value = {"article": {}}
    mock_client_class = MagicMock(return_value=mock_client_instance)

    with patch("app.tools.ServerLegifranceClient", mock_client_class):
        result = get_law_article("LEGIARTI000000000000")
        assert result == "Article introuvable pour l'identifiant 'LEGIARTI000000000000'."
        mock_client_instance.consulte_article.assert_called_once_with("LEGIARTI000000000000")

def test_get_law_article_exception():
    mock_client_instance = MagicMock()
    mock_client_instance.consulte_article.side_effect = Exception("API timeout")
    mock_client_class = MagicMock(return_value=mock_client_instance)

    with patch("app.tools.ServerLegifranceClient", mock_client_class):
        result = get_law_article("LEGIARTI000000000000")
        assert result == "Erreur lors de la récupération de l'article LEGIARTI000000000000 : API timeout"
        mock_client_instance.consulte_article.assert_called_once_with("LEGIARTI000000000000")

def test_get_law_article_success():
    mock_client_instance = MagicMock()
    mock_client_instance.consulte_article.return_value = {
        "article": {
            "num": "1382",
            "texte": "Tout fait quelconque de l'homme, qui cause à autrui un dommage..."
        }
    }
    mock_client_class = MagicMock(return_value=mock_client_instance)

    with patch("app.tools.ServerLegifranceClient", mock_client_class):
        result = get_law_article("LEGIARTI000000000000")
        assert "Article 1382" in result
        assert "Tout fait quelconque" in result
