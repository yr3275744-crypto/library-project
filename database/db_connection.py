from mysql import connector

class Connection:
    def __init__(self):
        self.user = "root"
        self.password = "library_manager"
        self.database = "library_db"
        self.port = 3306

    def get_connection(self):
        """docstring"""
        return connector.connect(user = self.user,
                                password = self.password,
                                database = self.database,
                                port = self.port
                                )

class Initalizer:
    def __init__(self, connection:Connection):
        self.connection = connection
    
    def create_books_table(self):
        """docstring"""
        connection = self.connection.get_connection()
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

    def create_members_table(self):
        """docstring"""
        connection = self.connection.get_connection()
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS members(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(50) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    is_active BOOL NOT NULL DEFAULT TRUE,
                    total_borrows INT NOT NULL DEFAULT 0
                    )""")

        connection.commit()
        cursor.close()
        connection.close()
        return None

if __name__ == "__main__":
    connection = Connection()
    a_init = Initalizer(connection)
    a_init.create_books_table()
    a_init.create_members_table()
    # conn = get_connection()
    # cursor = conn.cursor()
    # cursor.execute("DESCRIBE books")
    # rows = cursor.fetchall()
    # cursor.close()
    # conn.close()
    # print(rows)