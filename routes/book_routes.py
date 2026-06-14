import mysql
from fastapi import APIRouter, HTTPException
from database.book_db import BookDB, BookType

books_managr = BookDB()

router = APIRouter()

@router.post("/books", status_code = 201)
def create_book(body:BookType):
    """docstring"""
    try:
        return books_managr.create_book(body)
    
    except ValueError as e:
        raise HTTPException(400, detail = "Invalid input")
    
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
        return {"message":"The book is updated successfully"}
    except ValueError as e:
        raise HTTPException(400, detail = "Invalid input")