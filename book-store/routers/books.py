from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models
from database import SessionLocal
import schemas
import crud

router = APIRouter(prefix="/books", tags=["Books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_new_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Create a new book"""
    return crud.create_book(db=db, book=book)

@router.get("/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search in book titles"),
    db: Session = Depends(get_db)
):
    """Get all books with pagination and search"""
    return crud.get_books(db=db, skip=skip, limit=limit, search=search)

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    return crud.get_book(db=db, book_id=book_id)

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Update a book"""
    return crud.update_book(db=db, book_id=book_id, data=book)

@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book"""
    return crud.delete_book(db=db, book_id=book_id)

@router.get("/search/")
def search_books(title: str, db: Session = Depends(get_db)):
    return crud.search_books(db, title)

@router.get("/by_author/{author_id}")
def books_by_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_author(db, author_id)

@router.get("/by_category/{category_id}")
def books_by_category(category_id: int, db: Session = Depends(get_db)):
    return crud.get_books_by_category(db, category_id)


@router.get("/sorted/")
def get_sorted_books(sort_by: str = "title", order: str = "asc", db: Session = Depends(get_db)):
    return crud.get_books_sorted(db, sort_by=sort_by, order=order)



@router.get("/stats/")
def book_stats(db: Session = Depends(get_db)):
    total_books = db.query(models.Book).count()
    total_authors = db.query(models.Author).count()
    total_categories = db.query(models.Category).count()
    return {
        "total_books": total_books,
        "total_authors": total_authors,
        "total_categories": total_categories,
    }
