from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import schemas
import crud


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
router = APIRouter(prefix="/authors", tags=["Authors"])

@router.post("/", response_model=schemas.Author, status_code=status.HTTP_201_CREATED)
def create_new_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author"""
    return crud.create_author(db=db, author=author)

@router.get("/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all authors with pagination"""
    return crud.get_authors(db=db, skip=skip, limit=limit)

@router.get("/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """Get a specific author by ID"""
    return crud.get_author(db=db, author_id=author_id)

@router.put("/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    """Update an author"""
    return crud.update_author(db=db, author_id=author_id, data=author)

@router.delete("/{author_id}", status_code=status.HTTP_200_OK)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete an author"""
    return crud.delete_author(db=db, author_id=author_id)