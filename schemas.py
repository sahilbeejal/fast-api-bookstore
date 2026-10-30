"""Define Pydantic schemas for validating and returning book data."""

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    """Share the common book fields used by create and response schemas."""

    title: str
    description: str
    author: str
    year: int


class BookCreate(BookBase):
    """Validate the book details expected when creating a book."""

    pass


class Book(BookBase):
    """Represent a returned book, including its database-generated ID."""

    id: int

    model_config = ConfigDict(from_attributes=True)  # Read response fields from ORM objects.
