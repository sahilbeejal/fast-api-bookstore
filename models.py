"""Define SQLAlchemy models for bookstore records."""

from db import Base
from sqlalchemy import Column, Integer, String


class Book(Base):
    """Describe the book record and its intended database columns."""

    __tablename__ = "Books"  # Match the table name used by the bookstore schema.

    id = Column(Integer, primary_key=True, index=True)  # Identify each book row.
    title = Column(String, index=True)
    description = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer)
    