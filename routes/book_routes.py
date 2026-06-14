import mysql
from fastapi import APIRouter, HTTPException
from database.book_db import BookDB, BookType
from database.db_connection import Connection
import database.member_db as member_db

import database.book_db as book_db

books_managr = BookDB()

router = APIRouter()

@router.post("/books", status_code = 201)
def create_book(body:BookType):
    """docstring"""
    connection = None
    try:
        connection = Connection().get_connection()
        id = books_managr.create_book(body, connection)
        return {"message": f"The book {id} is created succesffully"}

    except ValueError as e:
        raise HTTPException(400, detail = "Invalid input. You must enter a valid name, email and gener.")
    
@router.get("/books")
def get_all_books():
    """docstring"""
    connection = None
    try:
        connection = Connection().get_connection()
        return books_managr.get_all_books(connection)

    except Exception:
        raise HTTPException(status_code=500, detail= "Somthing get wrong")
    
    finally:
        if connection:
            connection.close()

@router.put("/books/{id}/borrow/{member_id}", status_code = 200)
def borrow_to_member(id:int, member_id:int):
    """docstring"""
    connection = None
    try:
        connection = Connection().get_connection()
        member_db_instance = member_db.MemberDB()
        member = member_db_instance.get_member_by_id(member_id, connection)
        if not member:
            raise HTTPException(status_code = 404, detail = "The member does not found")
        
        if not member.get("is_active"):
            raise HTTPException(status_code = 409, detail = "The member is not active.")
        
        borrow = books_managr.set_available(id, False, member_id, connection)
        return {"message": f"The book {id} borroew to the member {member_id}"}
    
    except book_db.BookNotFound:
        raise HTTPException(status_code= 404, detail= "The book does not found")
    
    except book_db.BookNotAvailable:
        raise HTTPException(status_code = 409, detail = "The book is not available")
    
    except book_db.MemberHasMaximum:
        raise HTTPException(status_code = 409, detail = "The member has exceeded the maximum number of available books.")
    
    # except Exception:
    #     raise HTTPException(status_code=500, detail= "Somthing get wrong")
    
    finally:
        if connection:
            connection.close()

@router.get("/books/{id}")
def get_by_id(id:int):
    """docstring"""
    connection = None
    try:
        connection = Connection().get_connection()
        row = books_managr.get_book_by_id(id, connection)
        
        if not row:
            raise HTTPException(status_code = 404, detail = "The book is not found")
        
        return row
    
    except Exception:
        raise HTTPException(status_code=500, detail= "Somthing get wrong")
    
    finally:
        if connection:
            connection.close()

@router.put("/books/{id}")
def update_book(id:int, body:BookType):
    """docstribg"""
    connection = None
    try:
        connection = Connection().get_connection()
        is_updated = books_managr.update_book(id, body, connection)
        return {"message": f"The book {id} is updated successfully"}
    
    except book_db.BookNotFound:
        raise HTTPException(status_code= 404, detail= "The book does not found")

    except ValueError as e:
        raise HTTPException(400, detail = "Invalid input. You must enter a valid name, email and gener.")
    
    except Exception:
        raise HTTPException(status_code=500, detail= "Somthing get wrong")
    
    finally:
        if connection:
            connection.close()

