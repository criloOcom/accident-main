import pytest
from unittest.mock import patch, MagicMock
from app.tools import search_jurisprudence

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
