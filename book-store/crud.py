from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models, schemas

# -------- AUTHORS --------
def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session, skip=0, limit=100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def get_author(db: Session, author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

def update_author(db: Session, author_id: int, data: schemas.AuthorUpdate):
    author = get_author(db, author_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(author, field, value)
    db.commit()
    db.refresh(author)
    return author

def delete_author(db: Session, author_id: int):
    author = get_author(db, author_id)
    db.delete(author)
    db.commit()
    return {"detail": "Author deleted"}


# -------- CATEGORIES --------
def create_category(db: Session, cat: schemas.CategoryCreate):
    db_cat = models.Category(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_categories(db: Session):
    return db.query(models.Category).all()

def get_category(db: Session, category_id: int):
    cat = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

def update_category(db: Session, category_id: int, data: schemas.CategoryUpdate):
    cat = get_category(db, category_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cat, field, value)
    db.commit()
    db.refresh(cat)
    return cat

def delete_category(db: Session, category_id: int):
    cat = get_category(db, category_id)
    db.delete(cat)
    db.commit()
    return {"detail": "Category deleted"}


# -------- BOOKS --------
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip=0, limit=100, search: str | None = None):
    query = db.query(models.Book)
    if search:
        query = query.filter(models.Book.title.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

def update_book(db: Session, book_id: int, data: schemas.BookUpdate):
    book = get_book(db, book_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted"}


def search_books(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title.ilike(f"%{title}%")).all()

def get_books_by_author(db: Session, author_id: int):
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()

def get_books_by_category(db: Session, category_id: int):
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()



def get_books_sorted(db: Session, sort_by: str = "title", order: str = "asc"):
    query = db.query(models.Book)
    if sort_by == "title":
        column = models.Book.title
    elif sort_by == "id":
        column = models.Book.id
    else:
        column = models.Book.title

    if order == "desc":
        return query.order_by(column.desc()).all()
    return query.order_by(column.asc()).all()