"""HTTP endpoints for managing bookstore records."""

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import schemas
import services
from db import create_tables, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create missing database tables before the application serves requests."""
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Collection routes list and create books.
@app.get(path="/books/", response_model=list[schemas.Book])
async def get_all_books(db:Session = Depends(get_db)):
    """Return all books."""
    return services.get_books(db)

# Item routes operate on one book identified by its ID.
@app.get("/book/{id}",response_model=schemas.Book)
async def get_book_by_id(id:int,db:Session=Depends(get_db)):
    """Return a book by ID, or raise 404 if it does not exist."""
    book_queryset = services.get_book(db,id)
    if book_queryset:
        return book_queryset
    
    raise HTTPException(status_code=404, detail="Invalid Book ID provided")


@app.post("/books/", response_model=schemas.Book)

async def create_new_book(book: schemas.BookCreate, db:Session = Depends(get_db)):
    """Create a book from the supplied data and return the new record."""
    return services.create_book(db,book)



@app.put("/book/{id}", response_model=schemas.Book)
async def update_book(book:schemas.BookCreate,id:int,db:Session=Depends(get_db)):
    """Update a book by ID, or raise 404 if no matchisng book exists."""
    db_update = services.update_book(db,book,id)
    if not db_update:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return db_update

@app.delete("/book/{id}", response_model=schemas.Book)
async def delete_book(id:int,db:Session=Depends(get_db)):
    """Delete a book by ID and return it, or raise 404 if it is missing."""
    delete_entry = services.delete_book(db,id)
    if delete_entry:
        return delete_entry
    raise HTTPException(status_code=404, detail="Book Not Found")