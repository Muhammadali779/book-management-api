from typing import Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year: int = Field(..., ge=1000, le=2100)
    rating: float = Field(..., ge=0.0, le=5.0)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = Field(None, ge=1000, le=2100)
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
