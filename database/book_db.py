#TODO: add commit every time!
from fastapi import HTTPException
from pydantic import BaseModel

class BookType(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: str | None = None
    is_available: bool | None = None
    borrowed_by_member_id: int | None = None

class BookNotFound(Exception):
    pass

class BookNotAvailable(Exception):
    pass

class BookNotBorrowed(Exception):
    pass

class MemberHasMaximum(Exception):
    pass

class NotBorroedToHim(Exception):
    pass

class BookDB:
    """docstring"""
    VALIDE_GENER = ('Fiction', 'Non-Fiction', 'Science', 'History', 'Other')
    def __init__(self):
        pass

    def create_book(self, body:BookType, connection ) -> int:
        """docstring"""
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
        
        return id
    
    def get_all_books(self, connection) -> list:
        """docstring"""
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()

        cursor.close()
        return rows

    def get_book_by_id(self, id:int, connection) -> dict:
        """docstring"""
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
        row = cursor.fetchone()

        cursor.close()
        if not row:
            raise BookNotFound
        return row 

    def update_book(self, id:int, data:BookType, connection) -> int:
        """docstring"""
        the_book = self.get_book_by_id(id, connection)
        
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
        
        cursor.close()
        return True

    def set_avilable(self, id:int, val:bool, member_id:int, connection) -> bool:
        """docstring"""
        cursor = connection.cursor(dictionary = True)

        values_tuple = (val, member_id, id)
        cursor.execute("UPDATE books SET is_available = %s, borrowed_by_member_id = %s WHERE id = %s", values_tuple)

        connection.commit()
        cursor.close()
        return True

    def count_active_borrows_by_member(self, member_id:int, connection):
        """docstring"""
        cursor = connection.cursor(dictionary = True)

        cursor.execute("""SELECT borrowed_by_member_id, count(*) as borrows_num 
                       FROM books WHERE borrowed_by_member_id = %s 
                       GROUP BY borrowed_by_member_id""", (member_id,))
        
        row = cursor.fetchone()
        cursor.close()

        return row.get("borrows_num") if row else None

    def borrow_book(self, id:int, member_id:int, connection) -> bool:
        """docstring"""
        the_book = self.get_book_by_id(id, connection)

        if not the_book.get("is_available"):
            raise BookNotAvailable

        borrows = self.count_active_borrows_by_member(member_id, connection)
        if borrows:
            if borrows >= 3:
                raise MemberHasMaximum
        
        return self.set_avilable(id, False, member_id, connection)
    
    def is_borrowed_to(self, id:int, member_id:int, connection) -> bool:
        """Checkes if the book borrowed to a spesific member."""
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM books WHERE id = %s and borrowed_by_member_id = %s", (id, member_id))
        row = cursor.fetchone()
        cursor.close()
        
        return True if row else False

    def return_book(self, id:int, member_id:int, connection) -> bool:
        """docstring"""
        the_book = self.get_book_by_id(id, connection)
        
        is_borroed_to_him = self.is_borrowed_to(id, member_id, connection)
        if not is_borroed_to_him:
            raise NotBorroedToHim

        return self.set_avilable(id, True, None, connection)


if __name__ == "__main__":
    import db_connection as db_conn
    books_manager = BookDB()
    connection = db_conn.Connection().get_connection()
    # print(books_manager.set_available(7, 0, 2, connection))
    print(books_manager.count_active_borrows_by_member( 3, connection))
    # print(books_manager.create_book(BookTypes(title="bible", author="gu d", genre= "sgfdgdgd")))
    # print(books_manager.get_all_books())
    # t = BookType(title= "aaa")
    # print(books_manager.update_book(8, t))