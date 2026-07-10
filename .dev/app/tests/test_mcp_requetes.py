#!/usr/bin/env python3
"""Tests unitaires pour les requêtes MCP Légifrance et Judilibre.

Ces tests vérifient que les requêtes MCP fonctionnent correctement
et produisent les résultats attendus.
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock

# Ajouter le chemin parent pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_bridge.legifrance import LegifranceClient
from mcp_bridge.judilibre import JudilibreClient


class TestLegifranceClient(unittest.TestCase):
    """Tests pour le client Légifrance."""
    
    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour les tests."""
        # S'assurer que les credentials sont disponibles
        if not os.environ.get("PISTE_CREDENTIALS"):
            # Charger depuis le fichier local
            creds_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                ".piste-credentials.json"
            )
            if os.path.exists(creds_path):
                with open(creds_path) as f:
                    os.environ["PISTE_CREDENTIALS"] = json.dumps(json.load(f))
        
        # Forcer l'environnement sandbox pour les tests
        os.environ["PISTE_ENV"] = "sandbox"
    
    def test_initialization(self):
        """Test l'initialisation du client Légifrance."""
        client = LegifranceClient()
        self.assertIsNotNone(client._client)
        # Le client est initialisé avec succès si _client existe
    
    def test_search_code(self):
        """Test la recherche dans les codes."""
        client = LegifranceClient()
        result = client.search("responsabilité civile", "CODE", page_size=5)
        
        # Vérifier la structure de la réponse
        self.assertIn("results", result)
        self.assertIn("totalResultNumber", result)
        self.assertIsInstance(result["results"], list)
    
    def test_search_juri(self):
        """Test la recherche dans la jurisprudence."""
        client = LegifranceClient()
        result = client.search("accident", "JURI", page_size=3)
        
        # Vérifier la structure de la réponse
        self.assertIn("results", result)
        self.assertIn("totalResultNumber", result)
        self.assertIsInstance(result["results"], list)
    
    def test_consulte_article(self):
        """Test la consultation d'un article spécifique."""
        client = LegifranceClient()
        # Utiliser un article connu pour exister
        article = client.consulte_article("LEGIARTI000032041571")  # Art. 1240 C. civ.
        
        # Vérifier la structure de la réponse
        # Note: La clé 'texte' est dans article['article']
        self.assertIn("article", article)
        self.assertIn("texte", article["article"])
        # Vérifier que le texte n'est pas vide
        self.assertGreater(len(article["article"]["texte"]), 0)
        # Vérifier le numéro de l'article
        self.assertEqual(article["article"]["num"], "1240")
    
    def test_invalid_fond(self):
        """Test avec un fond invalide (doit utiliser JURI par défaut)."""
        client = LegifranceClient()
        result = client.search("test", "INVALID_FOND", page_size=2)
        
        # Doit retourner des résultats (fond JURI par défaut)
        self.assertIn("results", result)


class TestJudilibreClient(unittest.TestCase):
    """Tests pour le client Judilibre."""
    
    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour les tests."""
        # S'assurer que les credentials sont disponibles
        if not os.environ.get("PISTE_CREDENTIALS"):
            creds_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                ".piste-credentials.json"
            )
            if os.path.exists(creds_path):
                with open(creds_path) as f:
                    os.environ["PISTE_CREDENTIALS"] = json.dumps(json.load(f))
    
    def test_initialization(self):
        """Test l'initialisation du client Judilibre."""
        client = JudilibreClient()
        self.assertIsNotNone(client._token)
        self.assertIsNotNone(client._session)
    
    def test_search_basic(self):
        """Test la recherche de base."""
        client = JudilibreClient()
        result = client.search("accident du travail", page=1, page_size=5)
        
        # Vérifier la structure de la réponse
        self.assertIn("results", result)
        self.assertIn("total", result)
        self.assertIsInstance(result["results"], list)
    
    def test_search_with_chamber(self):
        """Test la recherche avec filtre par chambre."""
        client = JudilibreClient()
        result = client.search(
            "responsabilité civile",
            chamber="civ1",
            page_size=3
        )
        
        # Vérifier la structure de la réponse
        self.assertIn("results", result)
        self.assertGreaterEqual(result["total"], 0)
    
    def test_search_with_solution(self):
        """Test la recherche avec filtre par solution."""
        client = JudilibreClient()
        result = client.search(
            "accident",
            solution="cassation",
            page_size=3
        )
        
        # Vérifier la structure de la réponse
        self.assertIn("results", result)
        self.assertIsInstance(result["results"], list)
    
    def test_search_with_dates(self):
        """Test la recherche avec filtre par dates."""
        client = JudilibreClient()
        result = client.search(
            "travail",
            date_from="2020-01-01",
            date_to="2026-12-31",
            page_size=5
        )
        
        # Vérifier la structure de la réponse
        self.assertIn("results", result)
        self.assertIsInstance(result["results"], list)
    
    def test_search_by_ecli(self):
        """Test la recherche par ECLI."""
        client = JudilibreClient()
        # Utiliser un ECLI connu - la méthode s'appelle search, pas rechercher_par_ecli
        result = client.search("ECLI:FR:CCASS:2018:C100865", page_size=1)
        
        # Vérifier la structure de la réponse
        self.assertIn("results", result)


class TestRequetesSpecifiques(unittest.TestCase):
    """Tests pour les requêtes spécifiques au projet accident-main."""
    
    def test_recherche_responsabilite_erp(self):
        """Test recherche sur la responsabilité des ERP."""
        client = LegifranceClient()
        result = client.search("responsabilité ERP accident", "JURI")
        self.assertIn("results", result)
    
    def test_recherche_vasque_coiffure(self):
        """Test recherche sur les vasques de salon de coiffure."""
        client = LegifranceClient()
        result = client.search("vasque salon coiffure", "JURI")
        self.assertIn("results", result)
    
    @unittest.skip("Test instable - dépend de la disponibilité de l'API Judilibre")
    def test_recherche_dirigeant_assurance(self):
        """Test recherche sur la responsabilité des dirigeants."""
        client = JudilibreClient()
        result = client.search(
            "dirigeant responsabilité",  # Simplifier la requête
            chamber="com",
            page_size=5
        )
        self.assertIn("results", result)
    
    def test_recherche_accident_travail_coiffure(self):
        """Test recherche sur les accidents du travail dans les salons."""
        client = JudilibreClient()
        result = client.search(
            "accident travail salon coiffure",
            chamber="soc"
        )
        self.assertIn("results", result)
    
    def test_recherche_indemnisation_dintilhac(self):
        """Test recherche sur l'indemnisation Dintilhac."""
        client = JudilibreClient()
        result = client.search("indemnisation préjudice", page_size=5)
        self.assertIn("results", result)


if __name__ == "__main__":
    # Configuration pour les tests
    print("Configuration des tests MCP...")
    print(f"PISTE_ENV: {os.environ.get('PISTE_ENV', 'non configuré')}")
    print(f"PISTE_CREDENTIALS: {'configuré' if os.environ.get('PISTE_CREDENTIALS') else 'non configuré'}")
    
    # Exécuter les tests
    print("\nExécution des tests...")
    unittest.main(verbosity=2)