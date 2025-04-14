from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Load variables from .env
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_uri)

try:
    dbs = client.list_database_names()
    print("Connected successfully! Databases:")
    for db in dbs:
        print(f" - {db}")
except Exception as e:
    print("Connection failed:", e)
