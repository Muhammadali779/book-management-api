from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from .. import database, models, schemas

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[schemas.BookResponse])
def get_all_books(db: Session = Depends(database.get_db)):
    return db.query(models.Book).all()


@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(database.get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post(
    "/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED
)
def create_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(database.get_db),
):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return None


@router.get("/search/", response_model=List[schemas.BookResponse])
def search_books(
    search: str = Query(..., min_length=1), db: Session = Depends(database.get_db)
):
    search_term = f"%{search.lower()}%"
    books = (
        db.query(models.Book)
        .filter(
            (models.Book.title.ilike(search_term))
            | (models.Book.author.ilike(search_term))
        )
        .all()
    )
    return books


@router.get("/filter/", response_model=List[schemas.BookResponse])
def filter_books(
    min: Optional[int] = Query(None, alias="min"),
    max: Optional[int] = Query(None, alias="max"),
    db: Session = Depends(database.get_db),
):
    query = db.query(models.Book)

    if min is not None:
        query = query.filter(models.Book.year >= min)
    if max is not None:
        query = query.filter(models.Book.year <= max)

    return query.all()
