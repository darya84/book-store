from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import schemas
import crud

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_new_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    return crud.create_category(db=db, cat=category)

@router.get("/", response_model=List[schemas.Category])
def read_categories(db: Session = Depends(get_db)):
    """Get all categories"""
    return crud.get_categories(db=db)

@router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID"""
    return crud.get_category(db=db, category_id=category_id)

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    """Update a category"""
    return crud.update_category(db=db, category_id=category_id, data=category)

@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category"""
    return crud.delete_category(db=db, category_id=category_id)