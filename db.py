from fastapi.responses import HTMLResponse
import motor.motor_asyncio
import os
from model import Todo


conn_string = os.getenv("MONGODB_CONNECTION_STRING")

client = motor.motor_asyncio.AsyncIOMotorClient(conn_string)
database = client.TodoList
collection = database.todo


async def test_db_conn():
    try:
        await client.server_info()  # Try to get server info, which verifies the connection
        return "Database connection successful!"
    except Exception as e:
        error_message = str(e)
        if "bad auth" in error_message:
            return "Database authentication failed. Please check your username and password."
        elif "No suitable servers" in error_message:
            return "Unable to connect to the database server. Please check your network connection or database URI."
        elif "timed out" in error_message:
            return "Connection to the database server timed out. Please ensure that the server is reachable and try again."
        elif "SSL handshake failed" in error_message:
            return "The API server's IP address is not authorized to access the database. Please check the MongoDB Atlas IP whitelist settings."
        else:
            return f"Database connection failed: {error_message}"


async def fetch_all_todos():
    todos = []
    async for todo in collection.find():
        todos.append(Todo(**todo))
    return todos


async def fetch_one_todo(title):
    document = await collection.find_one({"title" : title})
    return document

async def create_todo(todo):
    document = todo
    result = await collection.insert_one(document)
    return document


async def update_todo(title , desc):
    await collection.update_one({"title" : title} , {"$set" : {"description" :desc}})
    documnet = await collection.find_one({"title" : title})
    return documnet


async def delete_todo(title):
    result = await collection.delete_one({"title": title})
    if result.deleted_count == 1:
        return True
    else:
        return False