from unittest.mock import patch, MagicMock
import pytest

from app.tools import search_law_code
from app.tools import get_law_article
from app.tools import search_jurisprudence


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


def test_search_jurisprudence_success():
    with patch("app.tools.ServerJudilibreClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.search.return_value = {
            "total": 1,
            "results": [
                {
                    "id": "123",
                    "title": "Arrêt Cour Cassation",
                    "decisionDate": "2024-01-01",
                    "chamber": "Sociale",
                    "solution": "Cassation",
                    "highlights": {"text": ["Extrait 1", "Extrait 2"]}
                }
            ]
        }

        result = search_jurisprudence("accident de travail")

        assert "Résultats de recherche jurisprudence pour 'accident de travail'" in result
        assert "(1 résultats au total)" in result
        assert "Arrêt Cour Cassation" in result
        assert "Date : 2024-01-01" in result
        assert "Chambre : Sociale" in result
        assert "Solution : Cassation" in result
        assert "Extrait : Extrait 1 / Extrait 2" in result


def test_search_jurisprudence_no_results():
    with patch("app.tools.ServerJudilibreClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.search.return_value = {
            "total": 0,
            "results": []
        }

        result = search_jurisprudence("recherche sans resultat")

        assert result == "Aucune jurisprudence trouvée pour la recherche : 'recherche sans resultat'"


def test_search_jurisprudence_client_unavailable():
    with patch("app.tools.ServerJudilibreClient", None):
        result = search_jurisprudence("test unavail")
        assert result == "Erreur : Client Judilibre non disponible."


def test_search_jurisprudence_exception():
    with patch("app.tools.ServerJudilibreClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.search.side_effect = Exception("Erreur de connexion")

        result = search_jurisprudence("test exception")

        assert result == "Erreur lors de la recherche de jurisprudence : Erreur de connexion"
