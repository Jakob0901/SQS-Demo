import logging
from contextlib import contextmanager
from typing import Optional, List, Dict

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from models.FavoriteQuote import Base, FavoriteQuote
import uuid

logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Basis-Ausnahmeklasse für Datenbankfehler"""
    pass


class Storage:
    def __init__(self, db_url: str, username: str, password: str, db_type: str = 'postgresql',
                 session: Optional[Session] = None):
        self.db_url = f'{db_type}://{username}:{password}@{db_url}'

        if session is not None:
            logger.debug("Verwendung einer vorhandenen Datenbanksession")
            self.Session = session
            self.engine = None
            return

        try:
            logger.info(f"Verbindung zur Datenbank wird hergestellt: {db_type}://{username}:***@{db_url}")
            self.engine = create_engine(self.db_url)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            logger.info("Datenbankverbindung erfolgreich hergestellt")
        except SQLAlchemyError as e:
            error_msg = f"Fehler beim Erstellen der Datenbankverbindung: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(error_msg) from e

    @contextmanager
    def session_scope(self):
        """Kontext-Manager für Datenbank-Sessions"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Datenbankfehler in der Session: {str(e)}")
            session.rollback()
            raise DatabaseError(f"Datenbankoperationsfehler: {str(e)}") from e
        finally:
            session.close()

    def store_quote(self, quote: str, source: Optional[str] = None) -> None:
        """Speichert ein neues Zitat in der Datenbank"""
        if not quote:
            logger.error("Versuch, ein leeres Zitat zu speichern")
            raise ValueError("Das Zitat darf nicht leer sein")

        quote_id = str(uuid.uuid4())
        logger.debug(f"Speichere neues Zitat mit ID {quote_id}")

        try:
            with self.session_scope() as session:
                new_quote = FavoriteQuote(id=quote_id, quote=quote, source=source)
                session.add(new_quote)
                logger.info(f"Zitat erfolgreich gespeichert (ID: {quote_id})")
        except DatabaseError:
            logger.error(f"Fehler beim Speichern des Zitats: {quote[:50]}...")
            raise

    def get_all_quotes(self) -> List[Dict[str, str]]:
        """Ruft alle gespeicherten Zitate ab"""
        logger.debug("Rufe alle gespeicherten Zitate ab")

        try:
            with self.session_scope() as session:
                quotes = session.query(FavoriteQuote).all()
                quote_list = [{'source': q.source, 'quote': q.quote} for q in quotes]
                logger.info(f"{len(quote_list)} Zitate erfolgreich abgerufen")
                return quote_list
        except DatabaseError:
            logger.error("Fehler beim Abrufen der Zitate")
            raise