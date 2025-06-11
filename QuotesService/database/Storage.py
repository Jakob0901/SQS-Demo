# database_wrapper.py
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.FavoriteQuote import Base, FavoriteQuote
import uuid

class Storage:
    def __init__(self, db_url, username, password, db_type='postgresql', session=None):
        if session is not None:
            self.Session = session
            self.engine = None
            return

        try:
            self.engine = create_engine(f'{db_type}://{username}:{password}@{db_url}')
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except ValueError as e:
            logging.error(f"Error creating database engine: {e}")
            raise e

    def store_quote(self, quote, source=None):
        session = self.Session()
        new_quote = FavoriteQuote(id=str(uuid.uuid4()), quote=quote, source=source)
        session.add(new_quote)
        session.commit()
        session.close()

    def get_all_quotes(self):
        session = self.Session()
        quotes = session.query(FavoriteQuote).all()
        session.close()
        return quotes