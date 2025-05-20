from fastapi import FastAPI

app = FastAPI()


BOOKS = [
    {"title": "Title One", "author": "Author One"},
    {"title": "Title Two", "author": "Author Two"},
    {"title": "Title Three", "author": "Author Three"},
    {"title": "Title Four", "author": "Author Four"},
    {"title": "Title Five", "author": "Author Five"},
]

@app.get("/api/books")
async def get_books():
    return BOOKS