#TODO: add commit every time!

from pydantic import BaseModel
from database.db_connection import get_connection

class BookTypes(BaseModel):
    title: str
    author: str
    genre: str
    is_available: bool = True
    borrowed_by_member_id: int | None = None


class BookDB:
    """docstring"""
    VALIDE_GENER = ('Fiction', 'Non-Fiction', 'Science', 'History', 'Other')
    def __init__(self):
        pass

    def create_book(self,body:BookTypes):
        """docstring"""
        connection = get_connection()
        cursor = connection.cursor()
        
        field_tuple = (body.title, body.author, body.genre)
        cursor.execute("INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)", field_tuple)
        connection.commit()

        id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return id
    
    def get_all_books(self):
        """docstring"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()

        cursor.close()
        connection.close()
        return rows

    def get_book_by_id(self, id:int):
        """docstring"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(f"SELECT * FROM books WHERE id = {id}")
        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row

if __name__ == "__main__":
    books_manager = BookDB()
    # print(books_manager.create_book(BookTypes(title="bible", author="gu d", genre= "sgfdgdgd")))
    print(books_manager.get_all_books())