from fastapi import FastAPI
from .api import books
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(books.router)
