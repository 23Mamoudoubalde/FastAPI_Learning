from fastapi import FastAPI, Body, HTTPException
from typing import Dict, List, Optional

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Four', 'author': 'Author One', 'category': 'Data-Science'},
    {'title': 'Title Five', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Six', 'author': 'Author One', 'category': 'Sport'}
]

@app.get("/books")
async def books_read():
    return BOOKS

# dynamic parameters - chronological order matters

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# query parameter (optional)
@app.get("/books/")
async def read_category_by_query(category: Optional[str] = None):
    if not category:
        return BOOKS
    books_to_return: List[Dict] = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create-book")
async def create_book(new_book: Dict = Body(...)):
    BOOKS.append(new_book)
    return new_book

@app.put("/books/update_book")
async def update_book(update_book: Dict = Body(...)):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book
            return update_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            removed = BOOKS.pop(i)
            return {"deleted": removed}
    raise HTTPException(status_code=404, detail="Book not found")

# removed duplicate dynamic route to avoid conflicts

@app.get("/")
async def first_api():
    return {"message": "Hello Mamoudou"}