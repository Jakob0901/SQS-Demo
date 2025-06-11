import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models.FavoriteQuote import Base, FavoriteQuote
from database.Storage import Storage

# Load environment variables for database connection
DB_URL = os.getenv('DATABASE_URL', 'localhost:5432/testdb')
DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

class TestStorageIntegration(unittest.TestCase):
    def setUp(self):
        # Use a real PostgreSQL database for integration tests
        self.storage = Storage(DB_URL, DB_USERNAME, DB_PASSWORD, db_type='postgresql')

    def tearDown(self):
        # Drop all tables after the tests
        Base.metadata.drop_all(self.storage.engine)

    def test_store_and_get_quote(self):
        quote_text = "The only way to do great work is to love what you do."
        quote_source = "Steve Jobs"

        # Store the quote
        self.storage.store_quote(quote_text, quote_source)

        # Retrieve all quotes
        quotes = self.storage.get_all_quotes()

        # Check if the quote is correctly stored and retrieved
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]["quote"], quote_text)
        self.assertEqual(quotes[0]["source"], quote_source)

    def test_get_all_quotes_empty(self):
        # Retrieve all quotes when none are present
        quotes = self.storage.get_all_quotes()

        # Check if the list is empty
        self.assertEqual(len(quotes), 0)

if __name__ == '__main__':
    unittest.main()