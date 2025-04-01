# database_wrapper.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.FavoriteQuote import Base, FavoriteQuote
import uuid

class DatabaseWrapper:
    def __init__(self, db_url, username, password):
        self.engine = create_engine(f'postgresql://{username}:{password}@{db_url}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def store_quote(self, quote, movie=None):
        session = self.Session()
        new_quote = FavoriteQuote(id=str(uuid.uuid4()), quote=quote, movie=movie)
        session.add(new_quote)
        session.commit()
        session.close()

    def get_all_quotes(self):
        session = self.Session()
        quotes = session.query(FavoriteQuote).all()
        session.close()
        return quotes