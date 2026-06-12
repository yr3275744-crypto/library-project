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