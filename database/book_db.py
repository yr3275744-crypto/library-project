#TODO: add commit every time!

from pydantic import BaseModel
from database.db_connection import get_connection

class BookType(BaseModel):
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

    def create_book(self,body:BookType) -> int:
        """docstring"""
        connection = get_connection()
        cursor = connection.cursor()
        
        if body.genre not in self.VALIDE_GENER:
            raise ValueError("Invalid input.")
        
        field_tuple = (body.title, body.author, body.genre)
        cursor.execute("INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)", field_tuple)
        connection.commit()

        id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return id
    
    def get_all_books(self) -> list:
        """docstring"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()

        cursor.close()
        connection.close()
        return rows

    def get_book_by_id(self, id:int) -> list | None:
        """docstring"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books")
        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row if row else None

    def update_book(self, id:int, data:BookType) -> bool:
        """docstring"""
        connection = get_connection()
        cursor = connection.cursor()

        if data.genre not in self.VALIDE_GENER:
            raise ValueError("Invalid input.")
        
        query = """UPDATE books 
        SET title = %s , author = %s, genre = %s, is_available = %s, borrowed_by_member_id = %s 
        WHERE id = %s"""
        values_list = [data.title, data.author, data.genre, data.is_available, data.borrowed_by_member_id] + [id]
        
        cursor.execute(query, values_list)
        connection.commit()
        
        cursor.close()
        connection.close()
        return True

if __name__ == "__main__":
    books_manager = BookDB()
    # print(books_manager.create_book(BookTypes(title="bible", author="gu d", genre= "sgfdgdgd")))
    print(books_manager.get_all_books())