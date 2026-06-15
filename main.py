# TODO : (create the files.)
# (create simple router and server.) 
# (create the conection to the database and tables.)
# (daclarate the db classes.)
# (add pydantic class to book and member in their files.)
# (daclarate the routs handle the methods in the db classes.)
# (add check if the emaile is already exists!)
# (add mysqlo generic exception to all routs!)
# add logger and loggs.
import uvicorn
from fastapi import FastAPI
from routes import book_routes, member_routes, report_routes
from database import db_connection
import logging

logger = logging.getLogger(__name__)

def app_server():
    """Play manage_library server. get calles, connect to database and return the result.
    save logs in logs/app.log
    """
    FORMAT = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(filename = "logs/app.log", level= logging.DEBUG, format= FORMAT)
    logger.info("Play app")
    connection = db_connection.Connection()
    the_initalizer = db_connection.Initalizer(connection)
    the_initalizer.create_books_table()
    the_initalizer.create_members_table()

    app = FastAPI()
    app.include_router(book_routes.router)
    app.include_router(member_routes.router)
    app.include_router(report_routes.router)

    return app



if __name__ == "__main__":
    app = app_server()
    uvicorn.run(app)