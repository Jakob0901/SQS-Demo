import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.FavoriteQuote import Base, FavoriteQuote
from database.Storage import Storage

class TestStorage(unittest.TestCase):
    def setUp(self):
        # Verwende eine In-Memory-SQLite-Datenbank für Tests
        self.db_url = 'sqlite:///:memory:'
        self.username = 'testuser'
        self.password = 'testpassword'
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        # Use the optimized constructor with db_type
        self.storage = Storage(self.db_url, self.username, self.password, db_type='sqlite', session=self.Session)

    def test_store_and_get_quote(self):
        quote_text = "The only way to do great work is to love what you do."
        quote_source = "Steve Jobs"

        # Speichere das Zitat
        self.storage.store_quote(quote_text, quote_source)

        # Hole alle Zitate ab
        quotes = self.storage.get_all_quotes()

        # Überprüfe, ob das Zitat korrekt gespeichert und abgerufen wurde
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0].quote, quote_text)
        self.assertEqual(quotes[0].source, quote_source)

    def test_get_all_quotes_empty(self):
        # Hole alle Zitate ab, wenn keine vorhanden sind
        quotes = self.storage.get_all_quotes()

        # Überprüfe, ob die Liste leer ist
        self.assertEqual(len(quotes), 0)

if __name__ == '__main__':
    unittest.main()