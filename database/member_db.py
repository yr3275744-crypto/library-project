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

    def check_is_exists(self, id:int, connection):
        """docstring"""
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows

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
        the_member = self.check_is_exists()
        if not the_member:
            raise ValueError("The member does not found")
        
        body = data.model_dump(exclude_none= True)
        values_list = list(body.values()) + [id]
        query_values_str = ", ".join([key + " = %s" for key in body])
        query = "UPDATE members SET " + query_values_str + " WHERE id = %s"
        print(query, values_list)
        cursor.execute(query, values_list)
        connection.commit()
    
        cursor.close()
        return True
    
    def deactivate_mumber(self, id:int, connection:connector.PooledMySQLConnection | connector.MySQLConnectionAbstract) -> bool:
        """docstring"""
        the_member = self.check_is_exists(id, connection)
        if not the_member:
            raise ValueError("The member does not found")

        cursor = connection.cursor()

        cursor.execute("UPDATE members SET is_active = False WHERE id = %s", (id,))

        connection.commit()
        cursor.close()

        return True

    def activate_member(self, id:int, connection:connector.PooledMySQLConnection | connector.MySQLConnectionAbstract) -> bool:
        """docstring"""
        the_member = self.check_is_exists(id, connection)
        if not the_member:
            raise ValueError("The member does not found")

        cursor = connection.cursor()

        cursor.execute("UPDATE members SET is_active = True WHERE id = %s", (id,))

        connection.commit()
        cursor.close()

        return True

if __name__ == "__main__":
    import database.db_connection as db_connection
    m = MemberDB()
    connection = db_connection.Connection().get_connection()
    print(m.get_member_by_id(2, connection))
    # t = MemberType(name = "jjjj")

    # id = m.update_member(15, t, connection)
    # print(id)
    # print(m.activate_member(1, connection))
    # connection.close()
