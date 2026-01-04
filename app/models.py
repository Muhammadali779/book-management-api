from sqlalchemy import Column, Float, Integer, String

from .database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=256), nullable=False)
    author = Column(String(length=256), nullable=False)
    genre = Column(String(length=128), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
