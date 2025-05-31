import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wrapper.QuotesApi import QuotesApi

class TestQuotesApi(unittest.TestCase):
    def setUp(self):
        self.api = QuotesApi()
        self.api.client = MagicMock()

    def test_get_random_quote_success(self):
        # Mock die Methode get_quote_random
        self.api.client.get_quote_random.return_value = ("This is a test quote.", "Test Author")

        # rufe die Methode auf
        result = self.api.get_random_quote()

        # Überprüfe die Ergebnisse
        self.assertEqual(result['quote'], "This is a test quote.")
        self.assertEqual(result['source'], "Test Author")

    def test_get_random_quote_failure(self):
        # Mock die Methode get_quote_random, um None zurückzugeben
        self.api.client.get_quote_random.return_value = (None, None)

        # rufe die Methode auf
        result = self.api.get_random_quote()

        # Überprüfe die Ergebnisse
        self.assertIsNone(result['quote'])
        self.assertIsNone(result['source'])

if __name__ == '__main__':
    unittest.main()