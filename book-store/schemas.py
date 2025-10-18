from pydantic import BaseModel

# ---- Author ----
class AuthorBase(BaseModel):
    name: str
    bio: str | None = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: str | None = None
    bio: str | None = None

class Author(AuthorBase):
    id: int
    class Config:
        orm_mode = True


# ---- Category ----
class CategoryBase(BaseModel):
    name: str
    description: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True


# ---- Book ----
class BookBase(BaseModel):
    title: str
    description: str | None = None
    author_id: int
    category_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    author_id: int | None = None
    category_id: int | None = None

class Book(BookBase):
    id: int
    author: Author
    category: Category
    class Config:
        orm_mode = True
