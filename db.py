import os
from typing import Optional

import pymongo
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

    def find_one(self, filter: dict):
        cursor = self.collection.find_one(filter)
        return cursor

    def find(self, filter: Optional[dict] = None):
        cursor = self.collection.find(
            filter,
        ).sort([("record_year", pymongo.DESCENDING), ("record_id", pymongo.DESCENDING)])
        return list(cursor)

    def bulk_insert(self, data: list):
        self.collection.insert_many(data)
