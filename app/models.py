from sqlalchemy import Column, Integer, String, Boolean, Date
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String(6), unique=True, index=True, nullable=False)
    title = Column(String, index=True)
    author = Column(String, index=True)
    is_borrowed = Column(Boolean, default=False)
    borrowed_by = Column(String(6), index=True, nullable=True)  
    borrowed_date = Column(Date, nullable=True)
