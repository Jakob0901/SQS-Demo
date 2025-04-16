from tenacity import retry

from wrapper.quotes_impl.PythonQuoteApi import PythonQuoteApi


class QuotesApi:
    def __init__(self):
        self.client = PythonQuoteApi()

    @retry
    def get_random_quote(self):
        """
        Get the random quote
        """
        conten, source =  self.client.get_quote_random()

        result = {
            "quote": conten,
            "source": source
        }

        return  result
