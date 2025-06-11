import unittest
from unittest.mock import MagicMock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import FlaskApp
from wrapper.QuotesApi import QuoteServiceError
from database.Storage import DatabaseError

class TestApp(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_ENV'] = 'testing'
        os.environ['API_KEY'] = 'test_api_key'
        os.environ['SECRET_KEY'] = 'test_secret_key'

        self.flask_app = FlaskApp()
        self.flask_app.app.config['WTF_CSRF_ENABLED'] = False
        self.flask_app.db = MagicMock()
        self.flask_app.quotes_api_wrapper = MagicMock()
        self.client = self.flask_app.app.test_client()
        self.client.testing = True

    def tearDown(self):
        # Entferne Testumgebungsvariablen
        for key in ['FLASK_ENV', 'API_KEY', 'SECRET_KEY']:
            if key in os.environ:
                del os.environ[key]

    def test_get_quote_error(self):
        self.flask_app.quotes_api_wrapper.get_random_quote.side_effect = QuoteServiceError("API Error")
        headers = {'x-api-key': 'test_api_key'}
        response = self.client.get('/quote', headers=headers)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {"error": "Interner Serverfehler"})

    def test_save_quote_database_error(self):
        headers = {'x-api-key': 'test_api_key'}
        data = {'quote': 'Test Quote'}
        self.flask_app.db.store_quote.side_effect = DatabaseError("DB Error")
        response = self.client.post('/save', data=data, headers=headers)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {"error": "Datenbankfehler"})

    def test_save_quote_value_error(self):
        headers = {'x-api-key': 'test_api_key'}
        data = {'quote': 'Test Quote'}
        self.flask_app.db.store_quote.side_effect = ValueError("Empty quote")
        response = self.client.post('/save', data=data, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Empty quote"})

    def test_get_stored_quotes_no_db(self):
        self.flask_app.db = None
        headers = {'x-api-key': 'test_api_key'}
        response = self.client.get('/stored_quotes', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_save_quote_no_db(self):
        self.flask_app.db = None
        headers = {'x-api-key': 'test_api_key'}
        data = {'quote': 'Test Quote'}
        response = self.client.post('/save', data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Quote saved!"})

    #def test_initialize_database_error(self):
    #    # Simulate a database initialization error - this is pretty slow, but necessary for testing
    #    os.environ['FLASK_ENV'] = 'production'
    #    os.environ['DATABASE_URL'] = 'invalid_url'
    #    os.environ['DB_USERNAME'] = 'test_user'
    #    os.environ['DB_PASSWORD'] = 'test_pass'

    #    app = FlaskApp()
    #    self.assertIsNone(app.db)

    def test_run_without_api_key(self):
        if 'API_KEY' in os.environ:
            del os.environ['API_KEY']
        app = FlaskApp()
        with self.assertRaises(ValueError) as context:
            app.run()
        self.assertEqual(str(context.exception), "No API_KEY environment variable set")

    def test_csrf_enabled(self):
        app = FlaskApp()
        self.assertTrue(app.app.config['WTF_CSRF_ENABLED'])
        self.assertIsNotNone(app.csrf)

    def test_different_api_key(self):
        headers = {'x-api-key': 'wrong_api_key'}
        test_cases = [
            ('GET', '/stored_quotes'),
            ('POST', '/save'),
            ('GET', '/quote')
        ]

        for method, endpoint in test_cases:
            with self.subTest(method=method, endpoint=endpoint):
                if method == 'GET':
                    response = self.client.get(endpoint, headers=headers)
                else:
                    response = self.client.post(endpoint, headers=headers)

                if endpoint == '/quote':
                    self.assertEqual(response.status_code, 200)
                else:
                    self.assertEqual(response.status_code, 403)
                    self.assertEqual(response.get_json(), {"message": "Forbidden"})

if __name__ == '__main__':
    unittest.main()