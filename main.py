from dotenv import load_dotenv
import os
from pymongo import MongoClient
import msvcrt

# Load Mongo URI from .env
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

def wait_for_any_key():
    print("\nPress any key to return...")
    msvcrt.getch()

def list_databases():
    dbs = client.list_database_names()
    if not dbs:
        print("No Database")
        return None
    print("\nDatabases")
    for db in dbs:
        print(f" - {db}")
    return dbs

def list_collections(db_name):
    db = client[db_name]
    collections = db.list_collection_names()
    if not collections:
        print("No Collections")
        return None
    print(f"\n{db_name}\nCollections")
    for col in collections:
        print(f" - {col}")
    return collections

def list_documents(db_name, col_name):
    collection = client[db_name][col_name]
    docs = list(collection.find({}, {"_id": 1}))
    if not docs:
        print("No Documents")
        return None
    print(f"\n{db_name}.{col_name}\nDocuments")
    for doc in docs:
        print(f" - {str(doc['_id'])}")
    return docs

def show_document(db_name, col_name, doc_id):
    from bson import ObjectId
    try:
        doc = client[db_name][col_name].find_one({"_id": ObjectId(doc_id)})
        if not doc:
            print("Document not found")
        else:
            print(f"\n{db_name}.{col_name}.{doc_id}")
            for key, value in doc.items():
                print(f"{key}: {value}")
    except Exception:
        print("Invalid ID format")
    wait_for_any_key()

# ----- Main App Flow -----
while True:
    dbs = list_databases()
    if not dbs:
        wait_for_any_key()
        continue

    db_input = input("\nSelect Database: ")
    if db_input not in dbs:
        print("Invalid database. Try again.")
        continue

    collections = list_collections(db_input)
    if not collections:
        wait_for_any_key()
        continue

    col_input = input("\nSelect Collection: ")
    if col_input not in collections:
        print("Invalid collection. Try again.")
        continue

    docs = list_documents(db_input, col_input)
    if not docs:
        wait_for_any_key()
        continue

    doc_input = input("\nSelect Document ID: ")
    show_document(db_input, col_input, doc_input)