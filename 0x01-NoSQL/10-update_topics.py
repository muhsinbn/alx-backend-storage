#!/usr/bin/env python3
""" A Function that changes all topics of a school doc based on the name."""
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """ name(string) will be the school name to update, topics(list of strings)
    will be the list of topics approached in the school.
    """
    if mongo_collection is None:
        return []
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
