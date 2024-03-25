# Building Notes App with Python FastAPI, Sqlmodel, Poetry and neon postgresql

![FastAPI, SQLModel, Postgres](https://github.com/MohsinRaz3/fastapi-notesapp/blob/main/notesapp.png)


This project aims to create a Notes App using Python FastAPI, Sqlmodel, Poetry, and neon PostgreSQL. FastAPI is a modern Python web framework known for its high-performance capabilities, making it ideal for building web applications efficiently. Here's a brief overview of the project:

- **FastAPI**: A modern Python web framework known for its high-performance capabilities.
- **Sqlmodel**: A library for SQL databases in Python, which integrates seamlessly with FastAPI for database operations.
- **Poetry**: A dependency management and packaging tool for Python projects, used here to manage project dependencies.
- **Neon PostgreSQL**: A PostgreSQL database for storing notes data.

## Endpoints

The backend of this app consists of five endpoints:

- One POST request for the create operation
- Two GET requests for the read operation
- One PATCH request for the update operation
- One DELETE request for the delete operation

## Getting Started

To set up FastAPI for a basic project, you need to install two things from pip: FastAPI and Uvicorn. Here's how you can create the project and set it up:

### Create Project

```bash
poetry new fastapi-notesapp

cd fastapi-notesapp

poetry add fastapi "uvicorn[standard]"

poetry run uvicorn fastapi-notesapp.main:app --host 0.0.0.0 --port 8000

