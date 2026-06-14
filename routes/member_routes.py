#TODO : check if i shoode create difult value is_active in databas or in pydantic.
import mysql
from fastapi import APIRouter, HTTPException
from database.member_db import MemberDB, MemberType
from database.db_connection import get_connection
member_db = MemberDB()

router = APIRouter()

@router.post("/members", status_code = 201)
def create_member(body:MemberType):
    """docstring"""
    
    try:
        connection = get_connection()
        id = member_db.create_member(body, connection)
        return {"mesaage": f"member {id} is created succesffully"}
    
    except mysql.connector.errors.IntegrityError:
        raise HTTPException(status_code = 409, detail = "The email addres is already exists")
    
    finally:
        connection.close()
    
    

@router.get("/members")
def get_all_members():
    """docstring"""
    connection = get_connection()
    
    rows = member_db.get_all_members(connection)
    
    connection.close()
    return rows

@router.get("/members/{id}")
def get_member_by_id(id:int):
    """docstring"""
    try:
        connection = get_connection()
        row = member_db.get_member_by_id(id, connection)
        if row:
            return row
        else:
            raise HTTPException(status_code = 404, detail = "The member is not found")
    
    except Exception:
        raise HTTPException(status_code = 500, detail= "Somthing get wrong")
    
    finally:
        connection.close()

