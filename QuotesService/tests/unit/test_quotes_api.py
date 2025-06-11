import os
import sys
import unittest
from unittest.mock import MagicMock

import tenacity

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from wrapper.QuotesApi import QuotesApi, QuoteServiceError
from wrapper.quotes_impl.PythonQuoteApi import QuoteApiError

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

        # Überprüfe, ob die erwartete Exception geworfen wird
        with self.assertRaises(QuoteServiceError) as context:
            self.api.get_random_quote()

        # Überprüfe die Fehlermeldung
        self.assertEqual(str(context.exception), "Zitat nicht verfügbar")

    def test_get_random_quote_no_author(self):
        # Mock die Methode get_quote_random mit Zitat aber ohne Autor
        self.api.client.get_quote_random.return_value = ("This is a test quote.", None)

        # Rufe die Methode auf
        result = self.api.get_random_quote()

        # Überprüfe die Ergebnisse
        self.assertEqual(result['quote'], "This is a test quote.")
        self.assertEqual(result['source'], "Unbekannt")

    def test_get_random_quote_retry_on_error(self):
        # Mock die Methode get_quote_random um erst Fehler zu werfen und dann zu erfolgen
        self.api.client.get_quote_random.side_effect = [
            QuoteApiError("API Fehler"),
            ("This is a test quote.", "Test Author")
        ]

        # Rufe die Methode auf
        result = self.api.get_random_quote()

        # Überprüfe die Ergebnisse
        self.assertEqual(result['quote'], "This is a test quote.")
        self.assertEqual(result['source'], "Test Author")
        self.assertEqual(self.api.client.get_quote_random.call_count, 2)

    def test_get_random_quote_max_retries_exceeded(self):
        # Mock die Methode get_quote_random um mehrmals Fehler zu werfen
        self.api.client.get_quote_random.side_effect = [
            QuoteApiError("API Fehler"),
            QuoteApiError("API Fehler"),
            QuoteApiError("API Fehler"),
            ("This is a test quote.", "Test Author")  # Sollte nicht erreicht werden
        ]

        # Überprüfe, ob die erwartete Exception nach 3 Versuchen geworfen wird
        with self.assertRaises(tenacity.RetryError):
            self.api.get_random_quote()

        # Überprüfe, dass genau 3 Versuche unternommen wurden
        self.assertEqual(self.api.client.get_quote_random.call_count, 3)

    def test_get_random_quote_service_error_propagation(self):
        # Mock die Methode get_quote_random um einen QuoteServiceError zu werfen
        error_message = "Service nicht verfügbar"
        self.api.client.get_quote_random.side_effect = QuoteServiceError(error_message)

        # Überprüfe, ob die Exception korrekt weitergegeben wird
        with self.assertRaises(QuoteServiceError) as context:
            self.api.get_random_quote()

        # Überprüfe die Fehlermeldung
        self.assertEqual(str(context.exception), error_message)

if __name__ == '__main__':
    unittest.main()