from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
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

# Route to test database connection
@app.get("/test-db")
async def test_database_connection():
    return await test_db_conn()

# Get todo by title
@app.get("/api/todo/{title}", response_model=Todo)
async def get_todo_by_title(title: str):
    todo = await fetch_one_todo(title)
    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail=f"No todo found with title: {title}")

# Get all todos
@app.get("/api/todos", response_model=list[Todo])
async def get_all_todos():
    return await fetch_all_todos()

# Create a new todo
@app.post('/api/todo', response_model=Todo)
async def create_new_todo(todo: Todo):
    return await create_todo(todo.model_dump())

# Update todo by title
@app.put("/api/todo/{title}/update", response_model=Todo)
async def update_todo_by_title(title: str, new_description: str):
    return await update_todo(title, new_description)

# Delete todo by title
@app.delete("/api/todo/{title}/delete")
async def delete_todo_by_title(title: str):
    deleted = await delete_todo(title)
    if deleted:
        return {"message": f"Todo with title '{title}' deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"No todo found with title: {title}")
