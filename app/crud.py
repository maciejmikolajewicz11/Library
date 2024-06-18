# pylint: disable=missing-module-docstring, import-error, pointless-string-statement

from datetime import date

from sqlalchemy.orm import Session

from .models import Book

"""
CRUD operations for the Book model.
"""


def get_book_by_serial_number(db_session: Session, serial_number: str):
    """
    Retrieve a book by its serial number.

    Args:
        db_session (Session): The database session.
        serial_number (str): The serial number of the book.

    Returns:
        Book: The book object if found, otherwise None.
    """
    return db_session.query(Book).filter(Book.serial_number == serial_number).first()


def create_book(db_session: Session, book_data: dict):
    """
    Create a new book in the database.

    Args:
        db_session (Session): The database session.
        book_data (dict): A dictionary containing the book data.

    Returns:
        Book: The newly created book object.
    """
    db_book = Book(**book_data)
    db_session.add(db_book)
    db_session.commit()
    db_session.refresh(db_book)
    return db_book


def delete_book(db_session: Session, serial_number: str):
    """
    Delete a book by its serial number.

    Args:
        db_session (Session): The database session.
        serial_number (str): The serial number of the book.

    Returns:
        Book: The deleted book object if it was found and deleted, otherwise None.
    """
    book = db_session.query(Book).filter(Book.serial_number == serial_number).first()
    if book:
        db_session.delete(book)
        db_session.commit()
        return book
    return None


def get_all_books(db_session: Session):
    """
    Retrieve all books from the database.

    Args:
        db_session (Session): The database session.

    Returns:
        list: A list of all book objects.
    """
    return db_session.query(Book).all()


def update_book_status(
    db_session: Session, serial_number: str, is_borrowed: bool, borrowed_by: str = None
):
    """
    Update the status of a book.

    Args:
        db_session (Session): The database session.
        serial_number (str): The serial number of the book.
        is_borrowed (bool): The borrowed status of the book.
        borrowed_by (str, optional): The ID of the person who borrowed the book. Defaults to None.

    Returns:
        Book: The updated book object if it was found and updated, otherwise None.
    """
    book = db_session.query(Book).filter(Book.serial_number == serial_number).first()
    if book:
        book.is_borrowed = is_borrowed
        book.borrowed_by = borrowed_by
        if is_borrowed:
            book.borrowed_date = date.today()
        else:
            book.borrowed_date = None
        db_session.commit()
        db_session.refresh(book)
        return book
    return None
