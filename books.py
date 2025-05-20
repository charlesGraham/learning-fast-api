from fastapi import FastAPI, APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
import database

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
  book = await get_book(id, db)

  if book is None:
    raise HTTPException(status_code=404, detail="Book not found")

  for key, value in update_book.model_dump().items():
    setattr(book, key, value)
    
  db.commit()
  db.refresh(book)
  return book

  
@api_router.delete("/books/{id}")
async def delete_book(id: int, db: Session = Depends(database.get_db)):
  book = await get_book(id, db)
  if book is None:
    raise HTTPException(status_code=404, detail="Book not found")

  db.delete(book)
  db.commit()

  return {
    "message": "Book deleted successfully",
    "book": book
    }


app.include_router(api_router)