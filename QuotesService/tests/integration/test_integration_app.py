import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import FlaskApp
from database.Storage import Storage, DatabaseError
from wrapper.QuotesApi import QuoteServiceError


class TestAppIntegration(unittest.TestCase):
    def setUp(self):
        # Setze Testumgebungsvariablen
        os.environ['FLASK_ENV'] = 'testing'
        os.environ['API_KEY'] = 'test_api_key'
        os.environ['DB_USERNAME'] = 'postgres'
        os.environ['DB_PASSWORD'] = 'postgres'
        os.environ['DATABASE_URL'] = 'localhost:5432/testdb'

        # CSRF für Tests deaktivieren
        self.app = FlaskApp()
        self.app.app.config['WTF_CSRF_ENABLED'] = False

        # Test Client erstellen
        self.client = self.app.app.test_client()
        self.client.testing = True

        # Test-Datenbank erstellen
        try:
            self.app.db = Storage(
                'localhost:5432/testdb',
                'postgres',
                'postgres',
                db_type='postgresql'
            )
        except DatabaseError:
            self.app.db = None

    def tearDown(self):
        if self.app.db and self.app.db.engine:
            from models.FavoriteQuote import Base
            Base.metadata.drop_all(self.app.db.engine)

    def test_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_quote_success(self):
        response = self.client.get('/quote')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('quote', data)
        self.assertIn('source', data)

    def test_get_quote_error(self):
        # Mock der QuotesApi um einen Fehler zu simulieren
        def raise_error(*args, **kwargs):
            raise QuoteServiceError("Test-Fehler")

        original_get_quote = self.app.quotes_api_wrapper.get_random_quote
        self.app.quotes_api_wrapper.get_random_quote = raise_error

        try:
            response = self.client.get('/quote')
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.get_json(), {"error": "Interner Serverfehler"})
        finally:
            self.app.quotes_api_wrapper.get_random_quote = original_get_quote

    def test_save_quote_with_api_key(self):
        headers = {'x-api-key': 'test_api_key'}
        data = {'quote': 'Test Quote'}
        response = self.client.post('/save', data=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Quote saved!"})

    def test_save_quote_without_api_key(self):
        data = {'quote': 'Test Quote'}
        response = self.client.post('/save', data=data)
        self.assertEqual(403, response.status_code)
        self.assertEqual({"message": "Forbidden"}, response.get_json())

    def test_save_quote_database_error(self):
        if not self.app.db:
            return  # Skip wenn keine DB verfügbar

        headers = {'x-api-key': 'test_api_key'}
        data = {'quote': 'Test Quote'}

        # Mock der store_quote Methode um einen Fehler zu simulieren
        def raise_error(*args, **kwargs):
            raise DatabaseError("Test-Datenbankfehler")

        original_store = self.app.db.store_quote
        self.app.db.store_quote = raise_error

        try:
            response = self.client.post('/save', data=data, headers=headers)
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.get_json(), {"error": "Datenbankfehler"})
        finally:
            self.app.db.store_quote = original_store

    def test_get_stored_quotes_with_api_key(self):
        if not self.app.db:
            return  # Skip wenn keine DB verfügbar

        headers = {'x-api-key': 'test_api_key'}
        data = {'quote': 'Test Quote'}
        self.client.post('/save', data=data, headers=headers)

        response = self.client.get('/stored_quotes', headers=headers)
        quotes = response.get_json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(isinstance(quotes, list))
        self.assertEqual(len(quotes), 1)
        self.assertEqual('Test Quote', quotes[0]['quote'])

    def test_get_stored_quotes_without_api_key(self):
        response = self.client.get('/stored_quotes')
        self.assertEqual(403, response.status_code)
        self.assertEqual({"message": "Forbidden"}, response.get_json())

    def test_save_quote_no_data(self):
        headers = {'x-api-key': 'test_api_key'}
        response = self.client.post('/save', data={}, headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertEqual({"message": "No quote provided"}, response.get_json())

    def test_save_quote_value_error(self):
        if not self.app.db:
            return  # Skip wenn keine DB verfügbar

        headers = {'x-api-key': 'test_api_key'}
        data = {'quote': ''}  # Leeres Zitat
        response = self.client.post('/save', data=data, headers=headers)
        self.assertEqual(400, response.status_code)
        self.assertIn("No quote provided", response.get_json()["message"])


if __name__ == '__main__':
    unittest.main()