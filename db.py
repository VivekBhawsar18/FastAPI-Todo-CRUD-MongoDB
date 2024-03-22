from fastapi.responses import HTMLResponse
import motor.motor_asyncio
import os
from model import Todo


conn_string = os.getenv("MONGODB_CONNECTION_STRING")

client = motor.motor_asyncio.AsyncIOMotorClient(conn_string)
database = client.TodoList
collection = database.todo


async def test_db_conn():
    response = f"<h1>Database Connection Details:</h1>\n"
    response += f"<p><b>Connection String:</b> {conn_string}</p>\n"
    response += f"<p><b>Database Name:</b> {database}</p>\n"
    response += f"<p><b>Collection Name:</b> {collection}</p>"
    return HTMLResponse(content=response, status_code=200)




async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document

async def fetch_one_todo(title):
    document = await collection.find_one({"title" : title})
    return document

async def update_todo(title , desc):
    await collection.update_one({"title" : title} , {"$set" : {"description" :desc}})
    documnet = await collection.find_one({"title" : title})
    return documnet