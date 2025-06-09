import logging

import requests


class PythonQuoteApi:
    def __init__(self, requests_get=None):
        self.url = "https://api.quotable.io/random"
        self.requests_get = requests_get or requests.get

    def get_quote_random(self):
        try:
            response = requests.get(self.url, verify=False, timeout=5)

            if response.status_code == 200:
                data = response.json()
                return data['content'], data['author']

        except requests.exceptions.Timeout:
            logging.warning('The request timed out')
        except requests.exceptions.RequestException as e:
            logging.warning(f'An error occurred: {e}')

        return None, None
