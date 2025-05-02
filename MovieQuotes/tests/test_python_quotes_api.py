import unittest
from unittest.mock import patch
from MovieQuotes.wrapper.quotes_impl.PythonQuoteApi import PythonQuoteApi

class TestPythonQuoteApi(unittest.TestCase):
    @patch('MovieQuotes.wrapper.quotes_impl.PythonQuoteApi.requests.get')
    def test_get_quote_random_success(self, mock_get):
        # Mock die Antwort von requests.get
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'content': 'This is a test quote.',
            'author': 'Test Author'
        }

        # Instanziiere die API und rufe die Methode auf
        api = PythonQuoteApi()
        quote, author = api.get_quote_random()

        # Überprüfe die Ergebnisse
        self.assertEqual(quote, 'This is a test quote.')
        self.assertEqual(author, 'Test Author')
        mock_get.assert_called_once_with(api.url, verify=False)

    @patch('MovieQuotes.wrapper.quotes_impl.PythonQuoteApi.requests.get')
    def test_get_quote_random_failure(self, mock_get):
        # Mock die Antwort von requests.get mit einem Fehlerstatus
        mock_response = mock_get.return_value
        mock_response.status_code = 500

        # Instanziiere die API und rufe die Methode auf
        api = PythonQuoteApi()
        quote, author = api.get_quote_random()

        # Überprüfe die Ergebnisse
        self.assertIsNone(quote)
        self.assertIsNone(author)
        mock_get.assert_called_once_with(api.url, verify=False)

if __name__ == '__main__':
    unittest.main()