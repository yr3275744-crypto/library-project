# TODO : (create the files.)
# (create simple router and server.) 
# create the conection to the database and tables.
# daclarate the db classes.
# daclarate the routs handle the methods in the db classes.
# add logger and loggs.
import uvicorn
from fastapi import FastAPI
from routes import book_routes, member_routes, report_routes

app = FastAPI()

app.include_router(book_routes.router)

if __name__ == "__main__":
    uvicorn.run(app)