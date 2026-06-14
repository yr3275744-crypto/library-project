#TODO: add commit every time!

from pydantic import BaseModel
from database.db_connection import get_connection

class BookType(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    is_available: bool | None = None
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
            raise ValueError("Invalid input. You must enter a valid gener")

        field_tuple = (body.title, body.author, body.genre)
        
        if not field_tuple[0] or not field_tuple[1]:
            raise ValueError("Invalid input. You must enter a valid name and email.")

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

    def update_book(self, id:int, data:BookType) -> int:
        """docstring"""
        connection = get_connection()
        cursor = connection.cursor()
        
        values_dict = data.model_dump(exclude_none = True)
        values_list = list(values_dict.values()) + [id]
        query_names_str = ", ".join([key + " = %s" for key in values_dict])
        query = "UPDATE books SET " + query_names_str + " WHERE id = %s"
        if values_dict.get("gener"):
            if values_dict.get("gener") not in self.VALIDE_GENER:
                raise ValueError("Invalid input. You must enter a valid gener")
        
        cursor.execute(query, values_list)
        connection.commit()
        
        cursor.fetchall()
        count = cursor.rowcount
        cursor.close()
        connection.close()
        return count

if __name__ == "__main__":
    books_manager = BookDB()
    # print(books_manager.create_book(BookTypes(title="bible", author="gu d", genre= "sgfdgdgd")))
    print(books_manager.get_all_books())
    t = BookType(title= "aaa")
    print(books_manager.update_book(8, t))