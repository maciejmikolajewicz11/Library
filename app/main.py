from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import Optional
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/books/", response_model=schemas.Book)
def add_book(book: schemas.Book, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_serial_number(db, book.serial_number)
    if db_book:
        raise HTTPException(status_code=400, detail="Book with this serial number already exists")
    return crud.create_book(db, book.dict())

@app.delete("/books/{serial_number}", response_model=schemas.Book)
def remove_book(serial_number: str, db: Session = Depends(get_db)):
    book = crud.delete_book(db, serial_number)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/books/", response_model=list[schemas.Book])
def list_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db)

@app.put("/books/{serial_number}", response_model=schemas.Book)
def update_book_status(serial_number: int, is_borrowed: bool, borrowed_by: Optional[int] = None, db: Session = Depends(get_db)):
    print(serial_number * 10)
    book = crud.get_book_by_serial_number(db, serial_number)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return crud.update_book_status(db, serial_number, is_borrowed, borrowed_by)