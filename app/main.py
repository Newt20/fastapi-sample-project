import os
from fastapi import FastAPI
from app.tasks import create_task
from pymongo import MongoClient

mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
client = MongoClient(mongo_uri)
db = client["celery_db"]
collection = db["task_results"]

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI with Celery and Docker Compose"}

@app.post("/tasks/{data}")
def run_task(data: str):
    task = create_task.delay(data)
    return {"task_id": task.id, "status": "Processing"}

@app.get("/tasks/")
def get_all_tasks():
    tasks = list(collection.find({}, {"_id": 0}))
    return {"tasks": tasks}

