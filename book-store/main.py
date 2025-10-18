from fastapi import FastAPI
import models, crud
from database import engine
from routers import books, authors, categories

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Store API")

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(categories.router)

@app.get("/")
def root():
    return {"message": "Welcome to Bookstore API"}
