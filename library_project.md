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

- titel : book title. up to 50 characters

- autor : autor's name. up to 50 characters

- genre : a genre Fiction | Non-Fiction | Science | History | Other

- is_available : is available. True or False.

- borrowed_by_member_id : the id of the member holding the book. null if the book is available.

### members table

- id : primary key. integer, auto-increment, unique

- name : the member's name. up to 50 characters

- email : the email addres. uniqe.

- is_active : if themember is activ = True, he can borrow a book. else False

- total_borrows : the total of borrows. integer, auto-increment.

## Running

git clone https://github.com/yr3275744-crypto/library-project.git

pip install requirements

docker run --name library -e MYSQL_ROOT_PASSWORD=library_manager -e MYSQL_DATABASE=library_db -p 3306:3306 -d mysql:8

py main.py