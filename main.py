from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Library Books API",
    description="REST API для библиотеки книг",
    version="1.0.0"
)

class BookInput(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(ge=1, le=2100)

    @field_validator("title", "author")
    @classmethod
    def not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Поле не может быть пустым")
        return value

class Book(BookInput):
    id: int

books: list[Book] = []
next_id = 1

def find_book(book_id: int) -> Book:
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )

@app.get("/books", response_model=list[Book])
def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    return find_book(book_id)

@app.post("/books", response_model=Book, status_code=201)
def create_book(data: BookInput):
    global next_id
    book = Book(id=next_id, **data.model_dump())
    next_id += 1
    books.append(book)
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, data: BookInput):
    old_book = find_book(book_id)
    updated = Book(id=book_id, **data.model_dump())
    books[books.index(old_book)] = updated
    return updated

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    book = find_book(book_id)
    books.remove(book)
    return Response(status_code=204)
