from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel

app = FastAPI()
api_router = APIRouter(prefix="/api")

class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str


BOOKS = [
    {"id": 1, "title": "Title One", "author": "Author One", "category": "Science"},
    {"id": 2, "title": "Title Two", "author": "Author Two", "category": "Science"},
    {"id": 3, "title": "Title Three", "author": "Author Three", "category": "History"},
    {"id": 4, "title": "Title Four", "author": "Author Four", "category": "Math"},
    {"id": 5, "title": "Title Five", "author": "Author Five", "category": "Math"},
    {"id": 6, "title": "Title Six", "author": "Author Two", "category": "Math"}
]

@api_router.get("/books")
async def get_books():
    return BOOKS


@api_router.get("/books/{id}")
async def get_book(id: int):
    for book in BOOKS:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@api_router.post("/books")
async def add_book(new_book: Book):
    BOOKS.append(new_book.model_dump())
    return new_book


@api_router.put("/books/{id}")
async def update_book(id: int, update_book: Book):
  for book in BOOKS:
    if book["id"] == id:
      book["title"] = update_book.title
      book["author"] = update_book.author
      book["category"] = update_book.category
      return book
  raise HTTPException(status_code=404, detail="Book not found")

  
@api_router.delete("/books/{id}")
async def delete_book(id: int):
  for book in BOOKS:
    if book["id"] == id:
      BOOKS.remove(book)
      return {
        "message": "Book deleted successfully",
        "book": book
        }
  raise HTTPException(status_code=404, detail="Book not found")


app.include_router(api_router)