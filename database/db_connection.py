from mysql import connector

def get_connection(user_name:str = "root", password:str = "library_manager", database:str = "library_db", port:int = 3306):
    """docstring"""
    return connector.connect(user = user_name,
                             password = password,
                             database = database,
                             port = port
                             )

def create_books_table():
    """docstring"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS books(
                   id INT PRIMARY KEY AUTO_INCREMENT,
                   title VARCHAR(50) NOT NULL,
                   author VARCHAR(50) NOT NULL,
                   genre ENUM('Fiction', 'Non-Fiction', 'Science', 'History', 'Other') NOT NULL,
                   is_available BOOL NOT NULL DEFAULT TRUE,
                   borrowed_by_member_id INT
                   );""")

    connection.commit()
    cursor.close()
    connection.close()
    return None

def create_members_table():
    """docstring"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS members(
                   id INT PRIMARY KEY AUTO_INCREMENT,
                   name VARCHAR(50) NOT NULL,
                   email VARCHAR(255) UNIQUE NOT NULL,
                   is_active BOOL NOT NULL,
                   total_borrows INT NOT NULL
                   )""")

    connection.commit()
    cursor.close()
    connection.close()
    return None

if __name__ == "__main__":
    create_books_table()
    create_members_table()
    # conn = get_connection()
    # cursor = conn.cursor()
    # cursor.execute("DESCRIBE books")
    # rows = cursor.fetchall()
    # cursor.close()
    # conn.close()
    # print(rows)