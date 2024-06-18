from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BookBase(BaseModel):
    serial_number: int = Field(..., gt=99999, lt=1000000, description="Six-digit serial number")
    title: str
    author: str
    is_borrowed: Optional[bool] = False
    borrowed_by: Optional[int] = None  
    borrowed_date: Optional[date] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    class Config:
        orm_mode = True
