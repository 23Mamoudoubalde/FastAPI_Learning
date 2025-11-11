from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from starlette import status

app = FastAPI()
BOOKS=[]
class Book: 
    id: int 
    title: str
    author: str
    description: str
    rating: int
    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
class BookRequest(BaseModel):
    #id: Optional[int]=None
    id: Optional[int]= Field(description='ID NOT NEEDED ON CREATE', default = None)
    title: str =Field(min_length=3)
    author: str = Field(min_length = 1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1,lt=6)

    #modelconfig allow us to default value that we want 
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codewithMB",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }



BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5),
    Book(3, 'Master Endpoints', 'codingwithroby', 'An awesome book!', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

'''
@app.post("/create-book")
async def create_book(book_request=Body()):
    BOOKS.append(book_request)
    Before adding data validation this is was the function. Pydantic
''' 
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.dict()) # this line allow to convert bookrequest to a dict format
    #print(type(new_book)) check type in terminal book_request or Book
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(BOOKS)> 0:
        book.id = BOOKS[-1].id +1
    else:
        book.id = 1
    return book

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK )
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")
@app.get("/books",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int =Query(gt=0, lt=6)):
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)
    return book_to_return
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i]=book
            book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail='Item not found')
    

@app.delete("/books/{books_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(books_id: int=Path(gt=0)):
    book_delete = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == books_id:
            BOOKS.pop(i)
            book_delete = True
            break
    if not book_delete:
        raise HTTPException(status_code=404, detail='Item not found')