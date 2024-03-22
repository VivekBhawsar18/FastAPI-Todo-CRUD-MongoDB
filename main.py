from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI , HTTPException
from dotenv import load_dotenv
from pathlib import Path
from model import Todo
# import os

from db import (
    test_db_conn ,
    fetch_all_todos,
    fetch_one_todo, 
    create_todo ,
    update_todo ,
    delete_todo
) 


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


app = FastAPI()

# CORS (Cross-Origin Resource Sharing) Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/")
async def print_db_details():
    responce = await test_db_conn()
    return responce

@app.get("/api/todo/{title}" ,response_model=Todo )
async def get_todo_title(title):
    responce = await fetch_one_todo(title)
    if responce:
        return responce
    raise HTTPException(404 , f"There is no todo with the title {title} ")


@app.get("/api/todo", response_model=list[Todo])
async def get_all_todos():
    try:
        response = await fetch_all_todos()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/api/todo' , response_model=Todo)
async def post_todo(todo:Todo):
    responce = await create_todo(todo.model_dump())
    if responce:
        return responce
    raise HTTPException(400 , "Something went wrong")



@app.put("/api/todo/update/{title}" , response_model=Todo)
async def put_todo(title :str , desc:str):
    responce = await update_todo(title , desc)
    if responce:
        return responce
    raise HTTPException(404 , f"There is no todo with the title {title} ")


@app.delete("/api/todo/{title}")
async def delete_todo_by_title(title: str):
    try:
        response = await delete_todo(title)
        if response:
            return {"message": f"Todo with title '{title}' deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"There is no todo with the title {title}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))