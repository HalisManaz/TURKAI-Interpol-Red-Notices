import os
from typing import Optional

from dotenv import load_dotenv
from pymongo import MongoClient

# Load variables from .env file
load_dotenv()


class MongoDB:
    def __init__(self):
        username = os.getenv("MONGODB_USERNAME")
        password = os.getenv("MONGODB_PASSWORD")
        cluster = os.getenv("MONGODB_CLUSTER")
        database_name = os.getenv("MONGODB_DATABASE")
        collection_name = os.getenv("MONGODB_COLLECTION")
        conn_str = f"mongodb+srv://{username}:{password}@{cluster}.mongodb.net/test"
        self.client = MongoClient(conn_str)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def find_one(self, query: dict):
        cursor = self.collection.find_one(query)
        return cursor
