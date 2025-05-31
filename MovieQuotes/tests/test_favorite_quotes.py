import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MovieQuotes.models.FavoriteQuote import FavoriteQuote

class TestFavoriteQuote(unittest.TestCase):
    def test_favorite_quote_initialization(self):
        # Testdaten
        test_id = "12345"
        test_quote = "This is a test quote."
        test_source = "Test Source"
        test_created_at = datetime.utcnow()

        # Instanziiere ein FavoriteQuote-Objekt
        favorite_quote = FavoriteQuote(
            id=test_id,
            quote=test_quote,
            source=test_source,
            created_at=test_created_at
        )

        # Überprüfe die Attribute
        self.assertEqual(favorite_quote.id, test_id)
        self.assertEqual(favorite_quote.quote, test_quote)
        self.assertEqual(favorite_quote.source, test_source)
        self.assertEqual(favorite_quote.created_at, test_created_at)

if __name__ == '__main__':
    unittest.main()