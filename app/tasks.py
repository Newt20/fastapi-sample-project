import os
from celery import Celery
import time
import pymongo

redis_uri = os.getenv("REDIS_URI", "redis://redis:6379/0")
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")


celery_app = Celery(
    "worker",
    broker=redis_uri,
    backend=f"{mongo_uri}tasks"
)

# MongoDB client
client = pymongo.MongoClient(mongo_uri)
db = client["celery_db"]
collection = db["task_results"]

@celery_app.task
def create_task(data):
    time.sleep(5)  # Simulate a long-running task
    result = {"data": data, "status": "completed"}
    collection.insert_one(result)
    return result
