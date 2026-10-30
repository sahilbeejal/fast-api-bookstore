"""Load database configuration used by the bookstore's SQLAlchemy setup."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker



load_dotenv()  # Read local development settings before checking for the database URL.

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError(
        "SQLALCHEMY_DATABASE_URL is missing; configure it in the environment or .env file."
    )

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # Share one connection pool across sessions.

SessionLocal = sessionmaker(  # Give each request its own session and explicit flush control.
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()  # Register model tables in one shared metadata collection.


def get_db():
    """Yield a database session and close it after the caller is done.

    Inputs: None.
    Outputs: Yields a SQLAlchemy session.
    Why: Ensures each API request gets a session that is always closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create database tables declared by the bookstore's ORM models.

    Inputs: None.
    Outputs: None.
    Why: Register models before creating their tables in the shared metadata.
    """
    import models  # Register model classes without introducing an import cycle.

    Base.metadata.create_all(bind=engine)
    
    
