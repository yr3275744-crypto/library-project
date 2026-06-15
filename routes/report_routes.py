from fastapi import APIRouter, HTTPException
import database.book_db as book_db
import database.member_db as member_db
from database.db_connection import Connection
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

books_manager = book_db.BookDB()
members_manager = member_db.MemberDB()

@router.get("/reports/books-by-genre")
def get_count_by_genre() -> list:
    """Return list of genre and how many books have in this type."""
    connection = None
    logger.info("GET /reports/books-by-genre is called")
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
def get_summary() -> dict:
    """Return dict of basic summery."""
    connection = None
    logger.info("GET /reports/summary is called")
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

@router.get("/reports/top-member")
def get_top_member() -> dict:
    """Return the top member,
    that he have the largest total borrows."""
    connection = None
    logger.info("GET /reports/top-member is called")
    try:
        connection = Connection().get_connection()

        return members_manager.get_top_number(connection)
    
    except Exception:
        raise HTTPException(status_code = 500, detail = "Something get wrong")
    
    finally:
        if connection:
            connection.close()