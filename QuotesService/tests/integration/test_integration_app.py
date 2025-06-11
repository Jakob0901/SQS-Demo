import os
import sys
import unittest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import FlaskApp
from database.Storage import Storage


class TestAppIntegration(unittest.TestCase):
    def setUp(self):
        # Setze Testumgebungsvariablen
        os.environ['FLASK_ENV'] = 'testing'
        os.environ['API_KEY'] = 'test_api_key'

        # Initialisiere Flask-App
        self.app = FlaskApp()
        self.client = self.app.app.test_client()

        # Erstelle Test-Datenbank
        self.app.db = Storage(
            'localhost:5432/testdb',
            'postgres',
            'postgres',
            db_type='postgresql'
        )

    def tearDown(self):
        # Lösche alle Testdaten
        if self.app.db and self.app.db.engine:
            from models.FavoriteQuote import Base
            Base.metadata.drop_all(self.app.db.engine)

    def test_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_quote(self):
        response = self.client.get('/quote')
        self.assertEqual(response.status_code, 200)

    def test_save_quote_with_api_key(self):
        headers = {'x-api-key': 'test_api_key'}
        data = {'quote': 'Test Quote'}

        response = self.client.post('/save',
                                    data=data,
                                    headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.data.decode('utf-8')),
            {"message": "Quote saved!"}
        )

    def test_save_quote_without_api_key(self):
        data = {'quote': 'Test Quote'}
        response = self.client.post('/save', data=data)
        self.assertEqual(response.status_code, 403)

    def test_get_stored_quotes_with_api_key(self):
        # Speichere zuerst einen Quote
        headers = {'x-api-key': 'test_api_key'}
        data = {'quote': 'Test Quote'}
        self.client.post('/save', data=data, headers=headers)

        # Hole gespeicherte Quotes
        response = self.client.get('/stored_quotes', headers=headers)
        quotes = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]['quote'], 'Test Quote')

    def test_get_stored_quotes_without_api_key(self):
        response = self.client.get('/stored_quotes')
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()