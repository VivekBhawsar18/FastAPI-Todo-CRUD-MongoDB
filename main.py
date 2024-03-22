from fastapi import FastAPI , HTTPException
from dotenv import load_dotenv
from pathlib import Path
from model import Todo
# import os

from db import (
    test_db_conn ,
    create_todo ,
    fetch_one_todo, 
    update_todo
) 


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)




app = FastAPI()

@app.get("/")
async def print_db_details():
    responce = await test_db_conn()
    return responce

@app.post('/api/todo/' , response_model=Todo)
async def post_todo(todo:Todo):
    responce = await create_todo(todo.model_dump())
    if responce:
        return responce
    raise HTTPException(400 , "Something went wrong")


@app.get("/api/todo/{title}" ,response_model=Todo )
async def get_todo_title(title):
    responce = await fetch_one_todo(title)
    if responce:
        return responce
    raise HTTPException(404 , f"There is no todo with the title {title} ")

@app.put("/api/todo/{title}/" , response_model=Todo)
async def put_todo(title :str , desc:str):
    responce = await update_todo(title , desc)
    if responce:
        return responce
    raise HTTPException(404 , f"There is no todo with the title {title} ")

# # Load environment variables from .env file
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)


# print(os.getenv("MONGODB_CONNECTION_STRING"))