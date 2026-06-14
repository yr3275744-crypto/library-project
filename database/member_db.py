from pydantic import BaseModel
import mysql

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

    def create_member(self, data:MemberType, connection:PooledMySQLConnection | MySQLConnectionAbstract):
        """docstring"""
        cursor = connection.cursor()
        values_tuple = (data.name, data.email, data.is_active, data.total_borrows)

        cursor.execute("INSERT INTO members (name, email, is_active, total_borrows) VALUES (%s, %s, %s, %s)", values_tuple)
        connection.commit()

        id = cursor.lastrowid
        cursor.close()
        return id