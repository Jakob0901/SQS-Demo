import logging
from typing import Dict, Optional

from tenacity import retry, stop_after_attempt, retry_if_exception_type
from wrapper.quotes_impl.PythonQuoteApi import PythonQuoteApi, QuoteApiError

logger = logging.getLogger(__name__)

class QuoteServiceError(Exception):
    """Fehler im Quote-Service"""
    pass

class QuotesApi:
    def __init__(self):
        self.client = PythonQuoteApi()
        logger.debug("QuotesApi initialisiert")

    @retry(
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(QuoteApiError)
    )
    def get_random_quote(self) -> Dict[str, Optional[str]]:
        """
        Ruft ein zufälliges Zitat ab.
        """
        try:
            content, source = self.client.get_quote_random()

            if content is None:
                logger.error("Kein Zitat verfügbar")
                raise QuoteServiceError("Zitat nicht verfügbar")

            result = {
                "quote": content,
                "source": source or "Unbekannt"
            }

            logger.info("Zitat erfolgreich abgerufen")
            return result

        except Exception as e:
            logger.error(f"Fehler beim Abrufen des Zitats: {e}")
            raise QuoteServiceError(str(e)) from e