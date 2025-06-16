from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class FavoriteQuote(Base):
    """
    SQLAlchemy-Modell für gespeicherte Zitate in der Datenbank.

    Attributes:
        id (str): Eindeutige UUID als Primärschlüssel
        quote (Text): Der Zitattext (nicht null)
        source (str): Optionale Quelle oder Autor des Zitats (max. 255 Zeichen)
        created_at (datetime): Zeitstempel der Erstellung, automatisch gesetzt
    """

    __tablename__ = 'favorite_quotes'

    id = Column(String, primary_key=True)
    quote = Column(Text, nullable=False)
    source = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)