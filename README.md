## Project goal

The goal of the project is to establish a server that manages a library system - managing members and books.

## Through project management

The server is a local fastapi server, which communicates with a database that has two tables:

a members table

and a books table.

The connection to the database will take place via a Docker container.

## Folder structure

library-api/  
│  
├── app/  
│   ├── main.py  
│   ├── database/  
│   │   ├── db\_connection.py  
│   │   ├── book\_db.py  
│   │   └── member\_db.py  
│   ├── routes/  
│   │   ├── book\_routes.py  
│   │   ├── member\_routes.py  
│   │   └── report\_routes.py  
│   └── logs/  
│       └── app.log  
│  
├── README.md  
├── requirements.txt  
└── .gitignore

## Table structure

### books table

- id : primary key. integer, auto-increment, unique

- title : book title. up to 50 characters

- author : autor's name. up to 50 characters

- genre : a genre Fiction | Non-Fiction | Science | History | Other

- is_available : is available. True or False.

- borrowed_by_member_id : the id of the member holding the book. null if the book is available.

### members table

- id : primary key. integer, auto-increment, unique

- name : the member's name. up to 50 characters

- email : the email addres. unique.

- is_active : if themember is active = True, he can borrow a book. else False

- total_borrows : the total of borrows. integer, auto-increment.

## System rules

1. Create book : The user sends genre/author/title — the system adds is_available=True, borrowed_by=NULL

2. Genre : Must be  Fiction / Non-Fiction / Science / History / Other - any other value adds an error.

3. Create member : User sends email/name — system adds True=active_is, total_borrows=0

4. Email: Must be uoniqe. else an error returnd.

5. Inactive member : If False=active_is — book cannot be borrowed

6. Unavailable book : You cannot borrow a book that is already borrowed (False=available_is)

7. Books max : A member cannot hold more than 3 books at a time.

8. Returning a book : A book can only be returned if it is lent to the same member who is returning it.

## Endpoints

### Books

- POST /books

- GET /books

- GET /books/{id}

- PUT /books/{id}

- PUT /books/{id}/borrow/{member_id}

- PUT /books/{id}/return/{member_id} 

### Members

- POST /members

- GET /members

- GET /members/{id}

- PUT /members/{id}

- PUT /members/{id}/deactivate 

- PUT /members/{id}/activate

### Reports

- GET /reports/summary 

- GET /reports/books-by-genre

- GET /reports/top-member 

## System flow

The server is started using main.py, and creates the required tables if they do not exist. 

Each client request is directed to the appropriate router, and the server aggregates them all.

The server addresses the appropriate table in the database and performs the required operation. 

Each operation is logged to the app.log file

## Running

### Create docker container 

```docker run --name library -e MYSQL_ROOT_PASSWORD=library_manager -e MYSQL_DATABASE=library_db -p 3306:3306 -d mysql:8```

### Clone the files
```git clone https://github.com/yr3275744-crypto/library-project.git```

### create venv - windose
```py -m venv venv```

```.\venv\Scripts\activate```

### Install the requirements
```py -m pip install requirements.txt```

### Play the server
```py main.py```