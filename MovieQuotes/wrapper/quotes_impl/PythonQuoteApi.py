import requests


class PythonQuoteApi:
    def __init__(self):
        self.url = "https://api.quotable.io/random"

    def get_quote_random(self):
        response = requests.get(self.url, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data['content'], data['author']
        else:
            return None, None
