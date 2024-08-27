
#!/usr/bin/env python3
""" A function that inserts a new document in a collection based on kwargs"""
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """ Inserts the new document and returns the new _id."""
    if mongo_collection is None:
        return []
    newDoc = mongo_collection.insert_one(kwargs)
    return newDoc.inserted_id
