import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Setzen der Umgebungsvariable für den Testkontext
os.environ['FLASK_ENV'] = 'testing'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        app.config['WTF_CSRF_ENABLED'] = False  # CSRF-Schutz für Tests deaktivieren

        # Setze den API_KEY für die Tests
        app.API_KEY = 'test_api_key'

        # Mock-Datenbank initialisieren
        app.db = MagicMock()

    @patch('app.quotes_api_wrapper.get_random_quote')
    def test_get_quote(self, mock_get_random_quote):
        mock_get_random_quote.return_value = "Test Quote"
        response = self.client.get('/quote')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Test Quote")

    @patch('app.db', autospec=True)
    def test_get_stored_quotes(self, mock_db):

        # Mock-Datenbankantwort
        mock_db.get_all_quotes.return_value = [{"quote": "Test Quote"}]

        # Führe die Anfrage aus
        response = self.client.get('/stored_quotes', headers={'x-api-key': 'test_api_key'})

        # Überprüfe die Antwort
        self.assertEqual(200, response.status_code)
        self.assertIn(b'"quote": "Test Quote"', response.data)

    @patch('app.db', autospec=True)
    def test_save_quote(self, mock_db):

        # Führe die Anfrage aus
        response = self.client.post('/save', data={'quote': 'Test Quote'}, headers={'x-api-key': 'test_api_key'})

        # Überprüfe die Antwort
        self.assertEqual(200, response.status_code)
        self.assertIn(b'Quote saved!', response.data)

        # Überprüfe, ob die Methode store_quote mit den richtigen Argumenten aufgerufen wurde
        mock_db.store_quote.assert_called_with('Test Quote')

    def test_save_quote_no_data(self):

        # Führe die Anfrage ohne Daten aus
        response = self.client.post('/save', data={}, headers={'x-api-key': 'test_api_key'})

        # Überprüfe die Antwort
        self.assertEqual(400, response.status_code)
        self.assertIn(b'No quote provided', response.data)


if __name__ == '__main__':
    unittest.main()