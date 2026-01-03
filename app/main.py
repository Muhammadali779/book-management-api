from fastapi import FastAPI

from . import database, models
from .routers import books

app = FastAPI(
    title="Book Management API",
    description="Simple CRUD API for managing books with search and filter",
    version="1.0.0",
)

# Jadval yaratish
models.Base.metadata.create_all(bind=database.engine)

# Routerlarni qo'shish
app.include_router(books.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Book Management API! Visit /docs for interactive documentation."
    }
