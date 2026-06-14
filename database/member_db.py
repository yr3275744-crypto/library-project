from typing import Optional
from pydantic import BaseModel
from mysql import connector

class MemberType(BaseModel):
    """docstring"""
    name: str | None = None
    email: str | None = None
    is_active: Optional[bool] = None
    total_borrows: Optional[int] = None


class MemberDB:
    """docstring"""
    def __init__(self):
        pass

    def create_member(self, data:MemberType, connection:connector.PooledMySQLConnection | connector.MySQLConnectionAbstract) -> int:
        """docstring"""
        cursor = connection.cursor()
        values_tuple = (data.name, data.email)
        if not values_tuple[0] or not values_tuple[1]:
            raise ValueError("Invlid input. You must anter name and email.")

        cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)", values_tuple)
        connection.commit()

        id = cursor.lastrowid
        cursor.close()
        return id
    
    def get_all_members(self, connection:connector.PooledMySQLConnection | connector.MySQLConnectionAbstract) -> list:
        """docstring"""
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()

        cursor.close()
        return rows
    
    def get_member_by_id(self, id:int, connection:connector.PooledMySQLConnection | connector.MySQLConnectionAbstract) -> dict:
        """docstring"""
        cursor = connection.cursor(dictionary = True)

        cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
        row = cursor.fetchone()

        cursor.close()
        return row

    def update_member(self, id:int, data:MemberType, connection:connector.PooledMySQLConnection | connector.MySQLConnectionAbstract) -> int:
        """docstring"""
        cursor = connection.cursor(dictionary = True)
        
        body = data.model_dump(exclude_none= True)
        values_list = list(body.values()) + [id]
        query_values_str = ", ".join([key + " = %s" for key in body])
        query = "UPDATE members SET " + query_values_str + " WHERE id = %s"
        print(query, values_list)
        cursor.execute(query, values_list)
        connection.commit()
        
        cursor.fetchall()
        count = cursor.rowcount

        if not count:
            raise ValueError
        cursor.close()
        return count
    

if __name__ == "__main__":
    import db_connection
    m = MemberDB()
    t = MemberType(name = "jjjj")
    connection = db_connection.get_connection()
    id = m.update_member(15, t, connection)
    print(id)
    connection.close()
