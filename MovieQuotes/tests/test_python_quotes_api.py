import os
import sys
import unittest
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wrapper.quotes_impl.PythonQuoteApi import PythonQuoteApi

class DummyResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def json(self):
        return self._json_data

class DummyTimeout(Exception):
    pass

class DummyRequestException(Exception):
    pass

class TestPythonQuoteApi(unittest.TestCase):
    def test_get_quote_random_success(self):
        def fake_get(url, verify, timeout):
            return DummyResponse(200, {'content': 'Test', 'author': 'Tester'})
        api = PythonQuoteApi(requests_get=fake_get)
        quote, author = api.get_quote_random()
        self.assertEqual(quote, 'Test')
        self.assertEqual(author, 'Tester')

    def test_get_quote_random_non_200(self):
        def fake_get(url, verify, timeout):
            return DummyResponse(404)
        api = PythonQuoteApi(requests_get=fake_get)
        quote, author = api.get_quote_random()
        self.assertIsNone(quote)
        self.assertIsNone(author)

    def test_get_quote_random_timeout(self):
        def fake_get(url, verify, timeout):
            raise requests.exceptions.Timeout()
        api = PythonQuoteApi(requests_get=fake_get)
        quote, author = api.get_quote_random()
        self.assertIsNone(quote)
        self.assertIsNone(author)

    def test_get_quote_random_request_exception(self):
        def fake_get(url, verify, timeout):
            raise requests.exceptions.RequestException("Fehler")
        api = PythonQuoteApi(requests_get=fake_get)
        quote, author = api.get_quote_random()
        self.assertIsNone(quote)
        self.assertIsNone(author)

if __name__ == '__main__':
    unittest.main()
