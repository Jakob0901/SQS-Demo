import os
import sys
import unittest
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from wrapper.quotes_impl.PythonQuoteApi import PythonQuoteApi
from wrapper.QuotesApi import QuotesApi, QuoteServiceError

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
        def fake_get(url, params, verify, timeout):
            return DummyResponse(200, {'quoteText': 'Test', 'quoteAuthor': 'Tester'})
        api = PythonQuoteApi(requests_get=fake_get)
        wrapper = QuotesApi()
        wrapper.client = api

        result = wrapper.get_random_quote()
        self.assertEqual('Test', result["quote"])
        self.assertEqual("Tester", result["source"])

    def test_get_quote_random_non_200(self):
        def fake_get(url, params, verify, timeout):
            return DummyResponse(404)

        api = PythonQuoteApi(requests_get=fake_get)
        wrapper = QuotesApi()
        wrapper.client = api

        with self.assertRaises(QuoteServiceError) as context:
            wrapper.get_random_quote()

        self.assertIn("nicht verfügbar", str(context.exception))

    def test_get_quote_random_timeout(self):
        def fake_get(url, params, verify, timeout):
            raise requests.exceptions.Timeout()

        api = PythonQuoteApi(requests_get=fake_get)
        wrapper = QuotesApi()
        wrapper.client = api

        with self.assertRaises(QuoteServiceError) as context:
            wrapper.get_random_quote()

        self.assertIn("nicht verfügbar", str(context.exception))

    def test_get_quote_random_request_exception(self):
        def fake_get(url, params, verify, timeout):
            raise requests.exceptions.RequestException("Fehler")

        api = PythonQuoteApi(requests_get=fake_get)
        wrapper = QuotesApi()
        wrapper.client = api

        with self.assertRaises(QuoteServiceError) as context:
            wrapper.get_random_quote()

        self.assertIn("nicht verfügbar", str(context.exception))

if __name__ == '__main__':
    unittest.main()