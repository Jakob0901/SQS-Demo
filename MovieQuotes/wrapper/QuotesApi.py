from tenacity import retry, stop_after_attempt

from wrapper.quotes_impl.PythonQuoteApi import PythonQuoteApi


class QuotesApi:
    def __init__(self):
        self.client = PythonQuoteApi()

    @retry(stop=stop_after_attempt(3))
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
