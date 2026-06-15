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
        raise HTTPException(status_code=500, detail= "Something get wrong")
    
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
        
        return row
    
    except book_db.BookNotFound:
        raise HTTPException(status_code= 404, detail= "The book does not found")
    
    except Exception:
        raise HTTPException(status_code=500, detail= "Something get wrong")
    
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
        raise HTTPException(status_code=500, detail= "Something get wrong")
    
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
        
        member_is_active = member_db_instance.is_active(member)
        
        borrow = books_managr.borrow_book(id, member_id, connection)
        count = member_db_instance.increment_borrows(member_id, connection)
        return {"message": f"The book {id} borrowed to the member {member_id}"}
    
    except book_db.BookNotFound:
        raise HTTPException(status_code= 404, detail= "The book does not found")
    
    except book_db.BookNotAvailable:
        raise HTTPException(status_code = 400, detail = "The book is not available")
    
    except book_db.MemberHasMaximum:
        raise HTTPException(status_code = 400, detail = "The member has exceeded the maximum number of available books.")
    
    except member_db.MemberNotFound:
        raise HTTPException(status_code= 404, detail = "The member does not found")
    
    except member_db.MemberDoesNotActive:
        raise HTTPException(status_code = 400, detail = "Member is not active")
    
    except Exception:
        raise HTTPException(status_code=500, detail= "Something get wrong")
    
    finally:
        if connection:
            connection.close()

@router.put("/books/{id}/return/{member_id}")
def return_book(id:int, member_id:int):
    """docstring"""
    connection = None
    try:
        connection = Connection().get_connection()
        member_db_instance = member_db.MemberDB()
        member = member_db_instance.get_member_by_id(member_id, connection)

        is_returnd = books_managr.return_book(id, member_id, connection)
        if is_returnd:
            return {"message":f"The book {id} is returnd successfully"}

    except book_db.BookNotFound:
        raise HTTPException(status_code= 404, detail= "The book does not found")

    except member_db.MemberNotFound:
        raise HTTPException(status_code= 404, detail = "The member does not found")

    except book_db.BookNotBorrowed:
        raise HTTPException(status_code = 400, detail = "The book is not borrowed")

    except book_db.NotBorroedToHim:
        raise HTTPException(status_code = 400, detail = "The book is not borrowed to this member.")

    except Exception:
        raise HTTPException(status_code=500, detail= "Something get wrong")
    
    finally:
        if connection:
            connection.close()