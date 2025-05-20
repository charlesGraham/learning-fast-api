from fastapi import FastAPI, APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ... import models, database
from pydantic import BaseModel

app = FastAPI()
api_router = APIRouter(prefix="/api")

class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    category: str

    class Config:
      orm_mode = True

class BookCreate(BaseModel):
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

@api_router.get("/books", response_model=list[BookSchema])
async def get_books(db: Session = Depends(database.get_db)):
    return db.query(models.Book).all()


@api_router.get("/books/{id}", response_model=BookSchema)
async def get_book(id: int, db: Session = Depends(database.get_db)):
  book = db.query(models.Book).filter(models.Book.id == id).first()
  
  if book is None:
    raise HTTPException(status_code=404, detail="Book not found")
  return book


@api_router.post("/books", response_model=BookSchema)
async def add_book(new_book: BookCreate, db: Session = Depends(database.get_db)):
  book = models.Book(**new_book.model_dump())
  db.add(book)
  db.commit()
  db.refresh(book)
  return book


@api_router.put("/books/{id}", response_model=BookSchema)
async def update_book(id: int, update_book: BookCreate, db: Session = Depends(database.get_db)):
  book = get_book(id, db)
  if book is None:
    raise HTTPException(status_code=404, detail="Book not found")

  for key, value in book.dict().items():
    setattr(book, key, value)
    
  db.commit()
  db.refresh(book)
  return book

  
@api_router.delete("/books/{id}")
async def delete_book(id: int, db: Session = Depends(database.get_db)):
  book = get_book(id, db)
  if book is None:
    raise HTTPException(status_code=404, detail="Book not found")

  db.delete(book)
  db.commit()

  return {
    "message": "Book deleted successfully",
    "book": book
    }


app.include_router(api_router)