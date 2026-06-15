#TODO : check if i shoode create difult value is_active in databas or in pydantic.
import mysql
from fastapi import APIRouter, HTTPException
from database.member_db import MemberDB, MemberType, MemberNotFound
from database.db_connection import Connection


member_db = MemberDB()

router = APIRouter()

@router.post("/members", status_code = 201)
def create_member(body:MemberType):
    """docstring"""
    connection = None
    try:
        connection = Connection().get_connection()
        id = member_db.create_member(body, connection)
        return {"mesaage": f"member {id} is created successfully"}
    
    except ValueError:
        raise HTTPException(status_code = 400, detail = "Invlid input. You must anter name and email.")
    
    except mysql.connector.errors.IntegrityError:
        raise HTTPException(status_code = 409, detail = "The email addres is already exists")
    
    except Exception:
        raise HTTPException(status_code=500, detail= "Somthing get wrong")
    
    finally:
        if connection:
            connection.close()
    
    

@router.get("/members")
def get_all_members():
    """docstring"""
    connection = None
    try:
        connection = Connection().get_connection()
        
        rows = member_db.get_all_members(connection)
        
        connection.close()
        return rows
    except Exception:
        raise HTTPException(status_code = 500, detail = "Somthing get wrong")
    
    finally:
        if connection:
            connection.close()

@router.get("/members/{id}")
def get_member_by_id(id:int):
    """docstring"""
    connection = None
    try:
        connection = Connection().get_connection()
        row = member_db.get_member_by_id(id, connection)
        if row:
            return row

    except MemberNotFound:
        raise HTTPException(status_code= 404, detail = "The member does not found")
    
    except Exception:
        raise HTTPException(status_code = 500, detail= "Somthing get wrong")
    
    finally:
        if connection:
            connection.close()

@router.put("/members/{id}")
def update_member(id:int, body:MemberType):
    """docstring"""
    connection = None
    try:
        connection = Connection().get_connection()
        is_updated = member_db.update_member(id, body, connection)
        if is_updated:
            return {"message": f"The member {id} is updated successfully"}
    
    except MemberNotFound:
        raise HTTPException(status_code= 404, detail = "The member does not found")
    
    except Exception:
        raise HTTPException(status_code=500, detail= "Somthing get wrong")

    finally:
        if connection:
            connection.close()

@router.put("/members/{id}/deactivate")
def deactivate_member(id:int) -> dict:
    """docsting"""
    connection = None
    try:
        connection = Connection().get_connection()
        is_deactive = member_db.deactivate_mumber(id, connection)
        return {"message": f"The member {id} is deactivated successfully"}

    except MemberNotFound:
        raise HTTPException(status_code= 404, detail = "The member does not found")
    
    except Exception:
        raise HTTPException(status_code=500, detail= "Somthing get wrong")

    finally:
        if connection:
            connection.close()

@router.put("/members/{id}/activate")
def activate_member(id:int) -> dict:
    """docsting"""
    connection = None
    try:
        connection = Connection().get_connection()
        is_deactive = member_db.activate_member(id, connection)
        return {"message": f"The member {id} is deactivated successfully"}

    except MemberNotFound:
        raise HTTPException(status_code= 404, detail = "The member does not found")
    
    except Exception:
        raise HTTPException(status_code=500, detail= "Somthing get wrong")

    finally:
        if connection:
            connection.close()