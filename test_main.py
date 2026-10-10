import pytest
import main
from fastapi.testclient import TestClient

client = TestClient(main.app)

@pytest.fixture(autouse=True)
def reset_library():
    main.books.clear()
    main.next_id = 1

def sample_book():
    return {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949
    }

def test_get_empty_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

def test_post_book():
    response = client.post("/books", json=sample_book())
    assert response.status_code == 201
    assert response.json()["id"] == 1

def test_get_all_books():
    client.post("/books", json=sample_book())
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_book_by_id():
    client.post("/books", json=sample_book())
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["title"] == "1984"

def test_update_book():
    client.post("/books", json=sample_book())
    response = client.put("/books/1", json={
        "title": "Animal Farm",
        "author": "George Orwell",
        "year": 1945
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Animal Farm"

def test_delete_book():
    client.post("/books", json=sample_book())
    response = client.delete("/books/1")
    assert response.status_code == 204
    assert client.get("/books/1").status_code == 404

def test_book_not_found():
    assert client.get("/books/999").status_code == 404

def test_update_missing_book():
    response = client.put("/books/999", json=sample_book())
    assert response.status_code == 404

def test_delete_missing_book():
    response = client.delete("/books/999")
    assert response.status_code == 404

def test_invalid_year():
    data = sample_book()
    data["year"] = -5
    response = client.post("/books", json=data)
    assert response.status_code == 422

def test_empty_title():
    data = sample_book()
    data["title"] = "   "
    response = client.post("/books", json=data)
    assert response.status_code == 422

def test_missing_author():
    data = sample_book()
    del data["author"]
    response = client.post("/books", json=data)
    assert response.status_code == 422

def test_unique_ids_after_delete():
    client.post("/books", json=sample_book())
    client.delete("/books/1")
    response = client.post("/books", json=sample_book())
    assert response.json()["id"] == 2

def test_swagger_docs():
    response = client.get("/docs")
    assert response.status_code == 200
