from fastapi import FastAPI, APIRouter

app = FastAPI()
api_router = APIRouter(prefix="/api")


BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "Science"},
    {"title": "Title Two", "author": "Author Two", "category": "Science"},
    {"title": "Title Three", "author": "Author Three", "category": "History"},
    {"title": "Title Four", "author": "Author Four", "category": "Math"},
    {"title": "Title Five", "author": "Author Five", "category": "Math"},
    {"title": "Title Six", "author": "Author Two", "category": "Math"}
]

@api_router.get("/books")
async def get_books():
    return BOOKS

    
app.include_router(api_router)