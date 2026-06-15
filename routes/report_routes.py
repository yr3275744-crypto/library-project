from fastapi import APIRouter, HTTPException
import database.book_db as book_db
import database.member_db as member_db
from database.db_connection import Connection

router = APIRouter()

books_manager = book_db.BookDB()
members_manager = member_db.MemberDB()

@router.get("/reports/books-by-genre")
def get_count_by_genre():
    """play the method from BooksDB"""
    connection = None
    try:
        connection = Connection().get_connection()
        count_by_genre_list = []
        for genre in books_manager.VALID_GENRE:
            count_by_genre_dict = {"genre":genre}
            count = books_manager.count_by_genre(genre, connection)
            count_by_genre_dict["COUNT"] = count
            count_by_genre_list.append(count_by_genre_dict)

        return count_by_genre_list
    
    except Exception:
        raise HTTPException(status_code = 500, detail = "Something get wrong")
    
    finally:
        if connection:
            connection.close()

@router.get("/reports/summary")
def get_summary():
    """docstring"""
    connection = None
    try:
        connection = Connection().get_connection()
        
        summary_dict = {}
        summary_dict["total_books"] = books_manager.count_total_books(connection)
        summary_dict["available_books"] = books_manager.count_available_books(connection)
        summary_dict["currently_borrowed"] = books_manager.count_borrowed_books(connection)
        summary_dict["active_members"] = members_manager.count_active_members(connection)

        return summary_dict
    
    except Exception:
        raise HTTPException(status_code = 500, detail = "Something get wrong")
    
    finally:
        if connection:
            connection.close()