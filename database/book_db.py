from db_connection import get_connection

class BookDB:
    """docstring"""
    VALIDE_GENER = ('Fiction', 'Non-Fiction', 'Science', 'History', 'Other')
    def __init__(self):
        pass

    def create_book(self,titel:str, author:str, genre:str):
        """docstring"""
        connection = get_connection()
        cursor = connection.cursor()
        
        field_tuple = (titel, author, genre)
        cursor.execute("INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)", field_tuple)

        id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return id
    


if __name__ == "__main__":
    books_manager = BookDB()
    print(books_manager.create_book("avada", "bob", "Fiction"))