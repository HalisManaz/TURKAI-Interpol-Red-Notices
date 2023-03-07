from os import getenv

import pytest
from dotenv import load_dotenv
from pymongo import MongoClient

from db import MongoDB

load_dotenv()

# Load MongoDB connection info from .env file
MONGODB_USERNAME = getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = getenv("MONGODB_PASSWORD")
MONGODB_CLUSTER = getenv("MONGODB_CLUSTER")
MONGODB_DATABASE = getenv("MONGODB_DATABASE")
MONGODB_COLLECTION = getenv("MONGODB_COLLECTION")

# MongoDB tests
def test_mongo_db():
    """Check connection to MongoDB"""
    conn_str = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER}.mongodb.net/test?retryWrites=true&w=majority"
    client = MongoClient(conn_str)
    db = client[MONGODB_DATABASE]
    assert db.name == MONGODB_DATABASE
    assert db[MONGODB_COLLECTION].name == MONGODB_COLLECTION
    client.close()


# Test functions
def test_insert_one():
    """Test inserting one document"""
    mongo_db = MongoDB()
    data = {"name": "John", "age": 25}
    mongo_db.collection.insert_one(data)
    assert mongo_db.find_one(data) == data
    mongo_db.collection.delete_one(data)


# Test for many insertions
def test_many_insert():
    """Test inserting many document"""
    mongo_db = MongoDB()
    data = [{"name": "John", "age": 25}, {"name": "Arthur", "age": 25}]
    mongo_db.bulk_insert(data)
    for i in data:
        assert mongo_db.find_one(i) == i
    mongo_db.collection.delete_one(data[0])
    mongo_db.collection.delete_one(data[1])


# Test for update
def test_update():
    """Test update one document"""
    mongo_db = MongoDB()
    data = {"name": "John", "age": 25}
    mongo_db.collection.insert_one(data)
    mongo_db.collection.update_one({"name": "John"}, {"$set": {"age": 26}})
    assert mongo_db.find_one({"name": "John"})["age"] == 26
    mongo_db.collection.delete_one(data)
