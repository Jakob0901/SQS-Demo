import unittest
from unittest.mock import patch, MagicMock
from MovieQuotes.wrapper.QuotesApi import QuotesApi

class TestQuotesApi(unittest.TestCase):
    @patch('MovieQuotes.wrapper.QuotesApi.PythonQuoteApi')
    def test_get_random_quote_success(self, mock_python_quote_api):
        # Mock die Methode get_quote_random
        mock_client = mock_python_quote_api.return_value
        mock_client.get_quote_random.return_value = ("This is a test quote.", "Test Author")

        # Instanziiere QuotesApi und rufe die Methode auf
        api = QuotesApi()
        result = api.get_random_quote()

        # Überprüfe die Ergebnisse
        self.assertEqual(result['quote'], "This is a test quote.")
        self.assertEqual(result['source'], "Test Author")
        mock_client.get_quote_random.assert_called_once()

    @patch('MovieQuotes.wrapper.QuotesApi.PythonQuoteApi')
    def test_get_random_quote_failure(self, mock_python_quote_api):
        # Mock die Methode get_quote_random, um None zurückzugeben
        mock_client = mock_python_quote_api.return_value
        mock_client.get_quote_random.return_value = (None, None)

        # Instanziiere QuotesApi und rufe die Methode auf
        api = QuotesApi()
        result = api.get_random_quote()

        # Überprüfe die Ergebnisse
        self.assertIsNone(result['quote'])
        self.assertIsNone(result['source'])
        mock_client.get_quote_random.assert_called_once()

if __name__ == '__main__':
    unittest.main()