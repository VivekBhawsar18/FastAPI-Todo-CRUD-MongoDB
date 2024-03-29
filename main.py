from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from typing import Dict
from pathlib import Path
from model import Todo
from db import (
    test_db_conn,
    fetch_all_todos,
    fetch_one_todo,
    create_todo,
    update_todo,
    delete_todo
)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Root route for documentation
@app.get("/", response_class=HTMLResponse)
async def root():
    # HTML content with route descriptions
    content = """
    <html>
        <head>
            <title>API Documentation</title>
        </head>
        <body>
            <h1>Welcome to the API Documentation</h1>
            <p>This is the documentation for your FastAPI application.</p>
            <h2>Available Routes:</h2>
            <p><strong>/test-db</strong>: Test the database connection.</p>
            <p><strong>/api/todo/{title}</strong>: Get a todo by its title.</p>
            <p><strong>/api/todos</strong>: Get all todos.</p>
            <p><strong>/api/todo</strong>: Create a new todo.</p>
            <p><strong>/api/todo/update/{title}</strong>: Update a todo by its title.</p>
            <p><strong>/api/todo/delete/{title}</strong>: Delete a todo by its title.</p>
        </body>
    </html>
    """
    return content



# Route to test database connection
@app.get("/test-db")
async def test_database_connection():
    try:
        response = await test_db_conn()
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get todo by title
@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_title(title: str):
    try:
        todo = await fetch_one_todo(title)
        if todo:
            return todo
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"No todo found with title: {title} . {e}")


# Get all todos
@app.get("/api/todos", response_model=list[Todo])
async def get_all_todos():
    try:
        response = await fetch_all_todos()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new todo
@app.post('/api/todo', response_model=Todo)
async def create_new_todo(todo: Todo):
    try:
        responce = await create_todo(todo.model_dump())
        return responce
    except Exception as e:
        raise HTTPException(status_code=500 , detail=str(e))

# Update todo by title
@app.put("/api/todo/update/{title}", response_model=Todo)
async def update_todo_by_title(todo:Todo):
    try:
        response = await update_todo(todo.title , todo.description)
        if response:
            return response
    except Exception as e:
        raise HTTPException(404 , f"There is no todo with the title {todo.title} . {e}")

# Delete todo by title
@app.delete("/api/todo/delete/{title}")
async def delete_todo_by_title(title: str):
    try:
        deleted = await delete_todo(title)
        if deleted:
            return {"message": f"Todo with title '{title}' deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"No todo found with title: {title}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting todo: {str(e)}")
