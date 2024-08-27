#!/usr/bin/env python3
""" A Function that lists all documents in a collection."""
from pymongo import MongoClient


def list_all(mongo_collection):
    """ Returns an empty list if no document in the collection."""
    if mongo_collection is None:
        return []
    docs = list(mongo_collection.find())
    return docs
