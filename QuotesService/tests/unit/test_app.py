import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Setzen der Umgebungsvariable für den Testkontext
os.environ['FLASK_ENV'] = 'testing'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import FlaskApp


class TestApp(unittest.TestCase):
    def setUp(self):
        self.flask_app = FlaskApp()
        self.flask_app.app.config['WTF_CSRF_ENABLED'] = False  # CSRF-Schutz für Tests deaktivieren

        # Setze den API_KEY für die Tests
        self.flask_app.API_KEY = 'test_api_key'

        # Mock-Datenbank initialisieren
        self.flask_app.db = MagicMock()
        self.flask_app.quotes_api_wrapper = MagicMock()

        self.client = self.flask_app.app.test_client()
        self.client.testing = True

    def test_get_quote(self):
        self.flask_app.quotes_api_wrapper.get_random_quote.return_value = "Test Quote"
        response = self.client.get('/quote')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Test Quote")

    def test_get_stored_quotes(self):
        # Mock-Datenbankantwort
        self.flask_app.db.get_all_quotes.return_value = [{"quote": "Test Quote"}]

        # Führe die Anfrage aus
        response = self.client.get('/stored_quotes', headers={'x-api-key': 'test_api_key'})

        # Überprüfe die Antwort
        self.assertEqual(200, response.status_code)
        self.assertIn(b'[{"quote":"Test Quote"}]\n', response.data)

    @patch('database.Storage', autospec=True)
    def test_save_quote(self, mock_db_class):
        # Mock-Datenbank
        mock_db = mock_db_class.return_value
        self.flask_app.db = mock_db

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

    def test_require_api_key(self):
        response = self.client.get('/stored_quotes')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json, {"message": "Forbidden"})


if __name__ == '__main__':
    unittest.main()