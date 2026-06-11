# TODO : (create the files.)
# (create simple router and server.) 
# (create the conection to the database and tables.)
# daclarate the db classes.
# add pydantic class to book and member in their files.
# daclarate the routs handle the methods in the db classes.
# add logger and loggs.
import uvicorn
from fastapi import FastAPI
from routes import book_routes, member_routes, report_routes
from database import db_connection, book_db, member_db

def main():
    app = FastAPI()
    app.include_router(book_routes.router)

    db_connection.create_books_table()
    db_connection.create_members_table()

    return app



if __name__ == "__main__":
    app = FastAPI()

    app.include_router(book_routes.router)
    uvicorn.run(app)