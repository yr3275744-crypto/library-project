import mysql
from fastapi import APIRouter, HTTPException
from database.book_db import BookDB, BookType

books_managr = BookDB()

router = APIRouter()

@router.post("/books", status_code = 201)
def create_book(body:BookType):
    """docstring"""
    try:
        id = books_managr.create_book(body)
        return {"message": f"The book {id} is created succesffully"}

    except ValueError as e:
        raise HTTPException(400, detail = "Invalid input. You must enter a valid name, email and gener.")
    
@router.get("/books")
def get_all_books():
    """docstring"""
    return books_managr.get_all_books()

@router.get("/books/{id}")
def get_by_id(id:int):
    """docstring"""
    row = books_managr.get_book_by_id(id)
    
    if not row:
        raise HTTPException(status_code = 404, detail = "The book is not found")
    
    return row

@router.put("/books/{id}")
def update_book(id:int, body:BookType):
    """docstribg"""
    try:
        is_updated = books_managr.update_book(id, body)
        if is_updated:
            return {"message":"The book is updated successfully"}
        else:
            raise HTTPException(status_code= 404, detail= "The book is not found or have no change.")
    
    except ValueError as e:
        raise HTTPException(400, detail = "Invalid input. You must enter a valid name, email and gener.")