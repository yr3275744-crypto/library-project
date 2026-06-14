#TODO : check if i shoode create difult value is_active in databas or in pydantic.
import mysql
from fastapi import APIRouter, HTTPException
from database.member_db import MemberDB, MemberType
from database.db_connection import get_connection
member_db = MemberDB()

router = APIRouter()

@router.post("/members")
def create_member(body:MemberType):
    """docstring"""
    connection = get_connection()
    try:
        id = member_db.create_member(body, connection)
    
    except mysql.connector.errors.IntegrityError:
        raise HTTPException(status_code = 409, detail = "The email addres is already exists")
    
    finally:
        connection.close()
    
    return {"mesaage": f"member {id} is created succesffully"}

@router.get("/members")
def get_all_members():
    """docstring"""
    connection = get_connection()
    
    rows = member_db.get_all_members(connection)
    
    connection.close()
    return rows