import logging
import requests
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class QuoteApiError(Exception):
    """Fehler bei API-Anfragen"""
    pass

class PythonQuoteApi:
    def __init__(self, requests_get=None):
        self.url = "https://api.forismatic.com/api/1.0/"
        self.requests_get = requests_get or requests.get
        logger.debug(f"API initialisiert mit URL: {self.url}")

    def get_quote_random(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Ruft ein zufälliges Zitat von der API ab.
        """
        params = {
            "method": "getQuote",
            "format": "json",
            "lang": "en"
        }

        try:
            response = self.requests_get(self.url, params=params, verify=True, timeout=5)

            if response.status_code == 200:
                data = response.json()
                quote = data.get('quoteText')
                author = data.get('quoteAuthor')

                if quote:
                    logger.info("Zitat erfolgreich abgerufen")
                    return quote.strip(), author.strip() if author else None

                logger.warning("Leeres Zitat von API erhalten")
                return None, None

            logger.error(f"API-Fehler: Status Code {response.status_code}")
            return None, None

        except requests.exceptions.Timeout:
            logger.error("API-Timeout nach 5 Sekunden")
            return None, None
        except requests.exceptions.RequestException as e:
            logger.error(f"API-Anfragefehler: {e}")
            return None, None