"""Service-layer helpers for managing bookstore records in the database."""

from sqlalchemy.orm import Session
from models import Book
from schemas import BookCreate


def create_book(db: Session, data: BookCreate):
    """Create a new book record in the database and return the saved object."""
    # Convert the validated Pydantic payload into a database model instance.
    book_instance = Book(**data.model_dump())

    # Add the new row to the current SQLAlchemy session.
    db.add(book_instance)

    # Persist the record and refresh it so the database-generated fields are available.
    db.commit()
    db.refresh(book_instance)

    return book_instance


def get_books(db: Session):
    """Return every book stored in the database."""
    return db.query(Book).all()


def get_book(db: Session, book_id: int):
    """Fetch a single book by its database ID, or return None if it does not exist."""
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db: Session, book: BookCreate, book_id: int):
    """Update an existing book with new values from a validated input payload."""
    # Find the target book before applying any changes.
    book_queryset: Book | None = db.query(Book).filter(Book.id == book_id).first()

    if book_queryset:
        # Copy each field from the incoming schema to the ORM object.
        for key, value in book.model_dump().items():
            setattr(book_queryset, key, value)

        # Save the updates and reload the model state from the database.
        db.commit()
        db.refresh(book_queryset)
        return book_queryset


def delete_book(db: Session, book_id: int):
    """Delete a book entry by ID and return the removed record if it was found."""
    # Retrieve the target row before attempting the deletion.
    book_queryset = db.query(Book).filter(Book.id == book_id).first()

    if book_queryset:
        db.delete(book_queryset)
        db.commit()
        return book_queryset