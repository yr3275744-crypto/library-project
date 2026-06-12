import mysql
from fastapi import APIRouter, HTTPException
from database.book_db import BookDB, BookTypes

books_managr = BookDB()

router = APIRouter()

@router.post("/books", status_code = 201)
def create_book(body:BookTypes):
    """docstring"""
    try:
        return books_managr.create_book(body)
    
    except mysql.connector.errors.DatabaseError:
        raise HTTPException(400, detail = "Invalid gener.")
    
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