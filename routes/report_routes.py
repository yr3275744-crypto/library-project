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
