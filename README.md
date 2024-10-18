# Library Management System API

## Project Description
This project is a RESTful API for a Library Management System built using Python and FastAPI. The API handles essential library operations, such as managing books, authors, borrowers, genres, and publishers, with validation for inputs to ensure data integrity.

The system supports the following features:
- Book management (with validations for ISBN, publish date, and author existence). 
- Borrow and return operations (with validations for book availability and borrower limits). 
- Genre and publisher management (with unique constraints and validation on established year). 
- User registration/authentication feature.


## Installation
Clone the repository:

```shell
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
```
Create `.env` file with variables: 
```shell
POSTGRES_DB=DB_NAME
POSTGRES_PASSWORD=DB_PASSWORD
POSTGRES_USER=DB_USER
POSTGRES_HOST=DB_HOST
POSTGRES_PORT=DB_PORT

JWT_SECRET=JWT_SECRET_KEY
JWT_ALGORITHM=JWT_ALGORITHM
ACCESS_TOKEN_LIFETIME=3600
REFRESH_TOKEN_LIFETIME=10080

AUTH_COOKIE_HTTPONLY=true
AUTH_COOKIE_SECURE=true
AUTH_COOKIE_SAME_SITE=Lax

```

Run docker:

```shell
docker compse up -d
```
The server will be running at http://localhost:8000.

## Usage
**Swagger Documentation**: Visit http://localhost:8000/docs to view and interact with the API documentation.

**ReDoc Documentation**: Visit http://localhost:8000/redoc for an alternative API documentation format.


## Database Models
**Book**: Stores information about each book (title, ISBN, author, publish date, etc.).  
**Author**: Stores author information (name, birthdate).  
**BorrowHistory**: Stores borrowing history (borrower details, book details, borrow/return dates).  
**Genre**: Represents a book genre.  
**Publisher**: Represents a publisher with validation on the established year.  
**User**: Represents a user of the library with needed data.