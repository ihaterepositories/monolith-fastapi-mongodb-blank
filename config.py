from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
REDIS_URI = os.getenv("REDIS_URI")

client = MongoClient(MONGO_URI)
db = client.item_db
items_collection = db["items_collection"]