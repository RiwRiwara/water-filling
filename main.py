from fastapi import FastAPI, HTTPException
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from fastapi import Query

app = FastAPI()

name = "iot"
password = "YnISAZpALeXfbVE3"

uri = f"mongodb+srv://{name}:{password}@newcluster.fxldupt.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["iot"]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test-db-connection")
def test_db_connection():
    try:
        client.admin.command('ping')
        return {"message": "Successfully connected to MongoDB!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")



@app.get("/users")
def get_users(tag_id: str = Query(None, description="Filter users by tag_id")):
    try:
        query = {}  
        if tag_id:
            query["tag_id"] = tag_id  

        users = db.users.find_one(query)
        return{
            "volume":  users['volume'],
            'name': users['name'],
            "status": 200
        }

    except Exception as e:
        print(e)
        # api resonse 404
        return {"message": "User not found", "status": 404}
