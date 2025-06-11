import os
import sys
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from models.FavoriteQuote import Base, FavoriteQuote
from database.Storage import Storage, DatabaseError

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.db_url = 'sqlite:///:memory:'
        self.username = 'testuser'
        self.password = 'testpassword'
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.storage = Storage(self.db_url, self.username, self.password,
                             db_type='sqlite', session=self.Session)

    def tearDown(self):
        if self.storage.engine:
            Base.metadata.drop_all(self.storage.engine)

    def test_store_and_get_quote(self):
        quote_text = "The only way to do great work is to love what you do."
        quote_source = "Steve Jobs"
        self.storage.store_quote(quote_text, quote_source)
        quotes = self.storage.get_all_quotes()
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]["quote"], quote_text)
        self.assertEqual(quotes[0]["source"], quote_source)

    def test_get_all_quotes_empty(self):
        quotes = self.storage.get_all_quotes()
        self.assertEqual(len(quotes), 0)

    def test_store_quote_without_source(self):
        quote_text = "Test quote without source"
        self.storage.store_quote(quote_text)
        quotes = self.storage.get_all_quotes()
        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]["quote"], quote_text)
        self.assertIsNone(quotes[0]["source"])

    def test_store_empty_quote(self):
        with self.assertRaises(ValueError):
            self.storage.store_quote("")

    def test_store_none_quote(self):
        with self.assertRaises(ValueError):
            self.storage.store_quote(None)

    def test_multiple_quotes(self):
        quotes_data = [
            ("Quote 1", "Source 1"),
            ("Quote 2", "Source 2"),
            ("Quote 3", None)
        ]
        for quote, source in quotes_data:
            self.storage.store_quote(quote, source)

        stored_quotes = self.storage.get_all_quotes()
        self.assertEqual(len(stored_quotes), 3)
        for i, (quote, source) in enumerate(quotes_data):
            self.assertEqual(stored_quotes[i]["quote"], quote)
            self.assertEqual(stored_quotes[i]["source"], source)

    def test_session_rollback_on_error(self):
        session_mock = MagicMock()
        session_mock.commit.side_effect = SQLAlchemyError("Commit error")
        session_mock.query.side_effect = SQLAlchemyError("Query error")

        storage = Storage(self.db_url, self.username, self.password,
                         db_type='sqlite', session=lambda: session_mock)

        with self.assertRaises(DatabaseError):
            storage.store_quote("Test quote")

        session_mock.rollback.assert_called_once()
        session_mock.close.assert_called_once()

    def test_get_quotes_database_error(self):
        session_mock = MagicMock()
        session_mock.query.side_effect = SQLAlchemyError("Query error")

        storage = Storage(self.db_url, self.username, self.password,
                         db_type='sqlite', session=lambda: session_mock)

        with self.assertRaises(DatabaseError):
            storage.get_all_quotes()

    def test_existing_session_usage(self):
        session = self.Session()
        storage = Storage(self.db_url, self.username, self.password,
                         db_type='sqlite', session=lambda: session)
        self.assertIsNone(storage.engine)

    def test_context_manager(self):
        with self.storage.session_scope() as session:
            quote = FavoriteQuote(id='test-id', quote='Test quote')
            session.add(quote)

        stored_quotes = self.storage.get_all_quotes()
        self.assertEqual(len(stored_quotes), 1)
        self.assertEqual(stored_quotes[0]["quote"], 'Test quote')


if __name__ == '__main__':
    unittest.main()