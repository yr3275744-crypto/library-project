import mysql
from fastapi import APIRouter, HTTPException
from database.member_db import MemberDB, MemberType, MemberNotFound
from database.db_connection import Connection
import logging

logger = logging.getLogger(__name__)

member_db = MemberDB()

router = APIRouter()

@router.post("/members", status_code = 201)
def create_member(body:MemberType) -> dict:
    """Create a new member, save it in members table in library database.
    return success message json.
    raise error if the name or email is empty, 
    or if the email is not uniqe."""
    connection = None
    logger.info("POST /members is called")
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
def get_all_members() -> list:
    """return all members in members table."""
    connection = None
    logger.info("GET /members is called")
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
def get_member_by_id(id:int) -> dict:
    """Return member by id if exsits,
    else raise error."""
    connection = None
    logger.info("GET /members/{id} is called")
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
def update_member(id:int, body:MemberType) -> dict:
    """Update member,
    return success message json.
    raise error if member not found
    or email not unique"""
    connection = None
    logger.info("PUT /members/{id} is called")
    try:
        connection = Connection().get_connection()
        is_updated = member_db.update_member(id, body, connection)
        if is_updated:
            return {"message": f"The member {id} is updated successfully"}
    
    except MemberNotFound:
        raise HTTPException(status_code= 404, detail = "The member does not found")
    
    except mysql.connector.errors.IntegrityError:
        raise HTTPException(status_code = 409, detail = "The email addres is already exists")

    except Exception:
        raise HTTPException(status_code=500, detail= "Somthing get wrong")

    finally:
        if connection:
            connection.close()

@router.put("/members/{id}/deactivate")
def deactivate_member(id:int) -> dict:
    """Deactiv member,
    raise error if member not found."""
    connection = None
    logger.info("PUT /members/{id}/deactivate is called")
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
    """Activate a member by id.
    raise error if member not found."""
    connection = None
    logger.info("PUT /members/{id}/activate is called")
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