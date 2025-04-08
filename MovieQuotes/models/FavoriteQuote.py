from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class FavoriteQuote(Base):
    __tablename__ = 'favorite_quotes'

    id = Column(String, primary_key=True)
    quote = Column(Text, nullable=False)
    source = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)