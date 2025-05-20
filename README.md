# FastAPI Book API

A RESTful API for managing a collection of books, built with FastAPI and PostgreSQL.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Installation Steps](#installation-steps)
- [Database Setup](#database-setup)
- [API Endpoints](#api-endpoints)
- [Running the Application](#running-the-application)
- [Docker Deployment](#docker-deployment)
- [Development](#development)

## Overview

This FastAPI application provides a RESTful API for managing a book collection. It allows for creating, reading, updating, and deleting book records with persistent storage in a PostgreSQL database. The application demonstrates modern Python API development with asynchronous request handling, data validation, and database integration.

## Project Structure

```
fast_api/
├── app/
│   ├── __init__.py
│   ├── models.py         # SQLAlchemy models
│   ├── database.py       # Database connection and session management
│   └── books.py          # FastAPI routes for book operations
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker configuration for the web service
├── .env                  # Environment variables (not in version control)
├── .env.example          # Example environment variables
├── init_db.py            # Database initialization script
├── alembic/              # Database migration files
├── alembic.ini           # Alembic configuration
└── README.md             # This documentation
```

## Technologies

- **FastAPI**: Modern, fast web framework for building APIs with Python
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) for Python
- **Pydantic**: Data validation and settings management using Python type hints
- **PostgreSQL**: Powerful, open-source object-relational database system
- **Uvicorn**: ASGI server for FastAPI
- **Docker**: Containerization platform
- **Alembic**: Database migration tool

## Setup and Installation

### Prerequisites

- Python 3.12 or newer
- PostgreSQL (local installation or Docker)
- Docker and Docker Compose (optional, for containerized deployment)

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=books_db
```

For Docker deployment, add these variables:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=books_db
```

### Installation Steps

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv learnfastapi
   source learnfastapi/bin/activate  # Linux/Mac
   # or
   learnfastapi\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic python-dotenv
   ```

## Database Setup

### Option 1: Manual Setup

1. Create a PostgreSQL database:

   ```sql
   CREATE DATABASE books_db;
   ```

2. Run the initialization script:
   ```bash
   python init_db.py
   ```

### Option 2: Using Alembic Migrations

1. Initialize Alembic:

   ```bash
   alembic init alembic
   ```

2. Edit `alembic/env.py` to import your models and set up the database URL

3. Create and apply migrations:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

### Option 3: Docker Setup

1. Start the PostgreSQL container:

   ```bash
   docker-compose up -d db
   ```

2. Run migrations from the web container:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

## API Endpoints

| Method | Endpoint        | Description                 |
| ------ | --------------- | --------------------------- |
| GET    | /api/books      | Get all books               |
| GET    | /api/books/{id} | Get a specific book by ID   |
| POST   | /api/books      | Create a new book           |
| PUT    | /api/books/{id} | Update a book (full update) |
| DELETE | /api/books/{id} | Delete a book               |

### Book Model

```python
class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
```

### Example Requests

#### Get all books

```bash
curl -X GET http://localhost:8000/api/books
```

#### Get a specific book

```bash
curl -X GET http://localhost:8000/api/books/1
```

#### Create a new book

```bash
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{"id": 7, "title": "New Book", "author": "New Author", "category": "Fiction"}'
```

#### Update a book

```bash
curl -X PUT http://localhost:8000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "title": "Updated Title", "author": "Author One", "category": "Science"}'
```

#### Delete a book

```bash
curl -X DELETE http://localhost:8000/api/books/1
```

## Running the Application

### Local Development

```bash
uvicorn books:app --reload
```

Visit http://localhost:8000/docs for interactive Swagger documentation.

### Docker Deployment

1. Start all services:

   ```bash
   docker-compose up -d
   ```

2. Access the API at http://localhost:8000

3. Stop services:
   ```bash
   docker-compose down
   ```

## Development

### Code Structure

- **books.py**: Contains API routes and application setup
- **models.py**: Defines SQLAlchemy and Pydantic models
- **database.py**: Handles database connection and session management

### Adding New Features

1. Define new models in `models.py`
2. Create migrations using Alembic
3. Add new routes in `books.py` or create separate route files for new entities

### Database Migrations

When changing models, create and apply migrations:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Testing

The application can be tested using tools like pytest with pytest-asyncio for testing asynchronous endpoints.
