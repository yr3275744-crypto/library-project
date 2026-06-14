#TODO : check if i shoode creat difult value is_active in databas or in pydantic.
from fastapi import APIRouter
from database.member_db import MemberDB, MemberType
from database.db_connection import get_connection
member_db = MemberDB()

router = APIRouter()

@router.post("/members")
def create_member(body:MemberType):
    """docstring"""
    connection = get_connection()
    id = member_db.create_member(body, connection)
    connection.close()
    return {"mesaage": f"member {id} is created succesffully"}