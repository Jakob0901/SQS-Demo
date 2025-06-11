import unittest
from unittest.mock import MagicMock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import FlaskApp

class TestApp(unittest.TestCase):
    def setUp(self):
        # Setze Testumgebungsvariablen
        os.environ['FLASK_ENV'] = 'testing'
        os.environ['API_KEY'] = 'test_api_key'

        self.flask_app = FlaskApp()
        self.flask_app.app.config['WTF_CSRF_ENABLED'] = False

        # Mock-Datenbank und API-Wrapper initialisieren
        self.flask_app.db = MagicMock()
        self.flask_app.quotes_api_wrapper = MagicMock()

        self.client = self.flask_app.app.test_client()
        self.client.testing = True

    def test_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_quote(self):
        self.flask_app.quotes_api_wrapper.get_random_quote.return_value = "Test Quote"
        headers = {'x-api-key': 'test_api_key'}
        response = self.client.get('/quote', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Test Quote")

    def test_get_stored_quotes(self):
        self.flask_app.db.get_all_quotes.return_value = [{"quote": "Test Quote"}]
        headers = {'x-api-key': 'test_api_key'}
        response = self.client.get('/stored_quotes', headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertIn(b'[{"quote":"Test Quote"}]', response.data)

    def test_save_quote(self):
        headers = {'x-api-key': 'test_api_key'}
        data = {'quote': 'Test Quote'}
        response = self.client.post('/save', data=data, headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual({"message": "Quote saved!"}, response.get_json())
        self.flask_app.db.store_quote.assert_called_once_with('Test Quote')

    def test_save_quote_no_data(self):
        headers = {'x-api-key': 'test_api_key'}
        response = self.client.post('/save', data={}, headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual({"message": "No quote provided"}, response.get_json())

    def test_api_key_required(self):
        test_cases = [
            ('GET', '/stored_quotes'),
            ('POST', '/save'),
        ]

        for method, endpoint in test_cases:
            with self.subTest(method=method, endpoint=endpoint):
                if method == 'GET':
                    response = self.client.get(endpoint)
                else:
                    response = self.client.post(endpoint)

                self.assertEqual(403, response.status_code)
                self.assertEqual({"message": "Forbidden"}, response.get_json())

if __name__ == '__main__':
    unittest.main()