from mysql import connector

def get_connection(user_name:str = "root", password:str = "library_manager", database:str = "library_db", port:int = 3306):
    """docstring"""
    return connector.connect(user = user_name,
                             password = password,
                             database = database,
                             port = port
                             )

def create_books():
    """docstring"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS books(
                   id PRIMARY_KEY AUTO_INCREMENT,
                   )""")


if __name__ == "__main__":
    conn = get_connection()
    print("sss")
    conn.close()