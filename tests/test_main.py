import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app, get_db
from app import crud
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("SQLALCHEMY_DATABASE_URL_TESTS", ""))

engine = create_engine("sqlite:///./test.db")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    yield client
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")

# Test data
test_book = {
    "serial_number": 123456,
    "title": "Test Book",
    "author": "Test Author",
}

@pytest.fixture
def book_data():
    return {
        "serial_number": 123456,
        "title": "Test Book",
        "author": "Test Author",
    }

def test_create_book(test_client, book_data):
    response = test_client.post("/books/", json=book_data)
    print(response)
    assert response.status_code == 200
    created_book = response.json()
    assert created_book["serial_number"] == book_data["serial_number"]
    assert created_book["title"] == book_data["title"]
    assert created_book["author"] == book_data["author"]

    response = test_client.post("/books/", json=book_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Book with this serial number already exists"

def test_list_books(test_client):
    response = test_client.get("/books/")
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert all("serial_number" in book for book in books)
    assert all("title" in book for book in books)
    assert all("author" in book for book in books)

def test_update_book_status(test_client, book_data):
    response = test_client.post("/books/", json=book_data)
    update_data = {
        "is_borrowed": True,
        "borrowed_by": 987654,  
    }
    print(f"/books/{book_data['serial_number']}")
    response = test_client.put(f"/books/{book_data['serial_number']}", params=update_data)
    assert response.status_code == 200
    updated_book = response.json()
    assert updated_book["is_borrowed"] == update_data["is_borrowed"]
    assert updated_book["borrowed_by"] == update_data["borrowed_by"]

def test_remove_book(test_client, book_data):
    response = test_client.post("/books/", params=book_data)

    response = test_client.delete(f"/books/{book_data['serial_number']}")
    assert response.status_code == 200
    deleted_book = response.json()
    assert deleted_book["serial_number"] == book_data["serial_number"]

    response = test_client.delete(f"/books/{book_data['serial_number']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_create_book_with_serial_number_limit(test_client):
    response = test_client.post("/books/", json={"serial_number": 1234567, "title": "Test Book", "author": "Test Author"})
    assert response.status_code == 422  

def test_create_book_with_card_number_limit(test_client):
    response = test_client.put("/books/123456", json={"is_borrowed": True, "borrowed_by": 6543217})
    assert response.status_code == 422  
