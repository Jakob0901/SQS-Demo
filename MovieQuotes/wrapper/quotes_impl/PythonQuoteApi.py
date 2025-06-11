python
import logging
import requests

class PythonQuoteApi:
    def __init__(self, requests_get=None):
        self.url = "https://api.forismatic.com/api/1.0/"
        self.requests_get = requests_get or requests.get

    def get_quote_random(self):
        params = {
            "method": "getQuote",
            "format": "json",
            "lang": "en"
        }
        try:
            response = self.requests_get(self.url, params=params, verify=False, timeout=5)

            if response.status_code == 200:
                data = response.json()
                return data.get('quoteText'), data.get('quoteAuthor')

        except requests.exceptions.Timeout:
            logging.warning('The request timed out')
        except requests.exceptions.RequestException as e:
            logging.warning(f'An error occurred: {e}')

        return None, None