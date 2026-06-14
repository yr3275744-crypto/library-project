from pydantic import BaseModel
from mysql import connector

class MemberType(BaseModel):
    """docstring"""
    id: int
    name: str
    email: str
    is_active: bool = True
    total_borrows: int = 0


class MemberDB:
    """docstring"""
    def __init__(self):
        pass

    def create_member(self, data:MemberType, connection:connector.PooledMySQLConnection | connector.MySQLConnectionAbstract) -> int:
        """docstring"""
        cursor = connection.cursor()
        values_tuple = (data.name, data.email, data.is_active, data.total_borrows)

        cursor.execute("INSERT INTO members (name, email, is_active, total_borrows) VALUES (%s, %s, %s, %s)", values_tuple)
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
        # try:
        cursor = connection.cursor(dictionary = True)

        cursor.execute("SELECT * FROM members WHERE id = %s", (id,))
        row = cursor.fetchone()

        cursor.close()
        return row
        # except connector.Error:
        #     raise connector.Error